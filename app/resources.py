import asyncio
import gzip
import json
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, TypeVar

from app.localization import LocaleManager
from app.repository import Repository
from app.sonolus_core import (
    BackgroundItem,
    EffectItem,
    EngineItem,
    ParticleItem,
    PlaylistItem,
    PostItem,
    SkinItem,
    Srl,
)

ValueT = TypeVar("ValueT")


@dataclass(frozen=True)
class StaticPost:
    """An announcement from ``files/posts``.

    Attributes:
        item: The post item.
        description: Post body.
    """

    item: PostItem
    description: str


@dataclass(frozen=True)
class CompiledParticle:
    """A particle from ``files/particles``.

    Attributes:
        item: The particle item.
        engine_specific: Whether it is hidden from the default particle option.
    """

    item: ParticleItem
    engine_specific: bool


@dataclass(frozen=True)
class CompiledSkin:
    """A skin from ``files/skins``.

    Attributes:
        item: The skin item.
        engines: Engine names the skin is meant for, empty for any.
        themes: Theme names offered in the default skin option.
        locale: Locale the skin is meant for.
    """

    item: SkinItem
    engines: list[str]
    themes: list[str]
    locale: str | None


@dataclass(frozen=True)
class CompiledEngine:
    """An engine from ``files/engines``.

    Attributes:
        item: The engine item.
        description: Engine description shown on its details page.
        sort_order: Position in engine lists, lower first.
    """

    item: EngineItem
    description: str | None
    sort_order: float


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file.

    Args:
        path: File to read.

    Returns:
        dict[str, Any]: The parsed object.
    """
    with path.open("r", encoding="utf8") as handle:
        return json.load(handle)


def _read_gzip_json(path: Path) -> dict[str, Any]:
    """Read a gzipped JSON file.

    Args:
        path: File to read.

    Returns:
        dict[str, Any]: The parsed object.
    """
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def gzip_bytes(data: bytes) -> bytes:
    """Gzip bytes with a zero timestamp so the hash only depends on the content.

    Args:
        data: Bytes to compress.

    Returns:
        bytes: The gzip stream.
    """
    buffer = BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as handle:
        handle.write(data)
    return buffer.getvalue()


class Resources:
    """Items compiled from ``files/``, stored in the repository and cached per process.

    Attributes:
        _root: Repository root containing ``files/``.
        _repository: Blob repository.
        _locales: Locale manager.
        _source: Public server URL put in every item's source.
        _cache: Compiled lists keyed by kind and locale.
        _locks: Locks preventing duplicate compiles.
        background_no_scope: Locator of the scope-less default background configuration.
    """

    def __init__(
        self, root: Path, repository: Repository, locales: LocaleManager, source: str
    ) -> None:
        """Create the compiler.

        Args:
            root: Repository root containing ``files/``.
            repository: Blob repository.
            locales: Locale manager.
            source: Public server URL put in every item's source.
        """
        self._root = root
        self._repository = repository
        self._locales = locales
        self._source = source
        self._cache: dict[str, Any] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self.background_no_scope: Srl | None = None

    def _folders(self, kind: str) -> list[str]:
        """List the item folders of a kind in directory order.

        Args:
            kind: Folder under ``files/``.

        Returns:
            list[str]: Folder names.
        """
        base = self._root / "files" / kind
        return [name for name in os.listdir(base) if (base / name).is_dir()]

    async def _json(self, relative: str) -> dict[str, Any]:
        """Read a JSON file under the root off the event loop.

        Args:
            relative: Path relative to the root.

        Returns:
            dict[str, Any]: The parsed object.
        """
        return await asyncio.to_thread(_read_json, self._root / relative)

    async def _srl(self, relative: str, required: bool = True) -> Srl | None:
        """Store a file and return its locator.

        Args:
            relative: Path relative to the root.
            required: Raise when the file is missing.

        Returns:
            Srl | None: The locator.
        """
        return await self._repository.file_srl(relative, error_on_file_nonexistent=required)

    async def _cached(self, key: str, build: Callable[[], Awaitable[ValueT]]) -> ValueT:
        """Return a cached value, compiling it once while it is missing or empty.

        Args:
            key: Cache key.
            build: Compiles the value.

        Returns:
            ValueT: The value.
        """
        value = self._cache.get(key)
        if value:
            return value
        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            value = self._cache.get(key)
            if value:
                return value
            value = await build()
            self._cache[key] = value
            return value

    async def playlists(self, locale: str) -> list[PlaylistItem]:
        """Compile the playlists.

        Args:
            locale: Requested locale code.

        Returns:
            list[PlaylistItem]: The playlists.
        """
        loc, code = self._locales.get_messages(locale)

        def replace(value: str) -> str:
            """Fill the playlist text placeholders.

            Args:
                value: Raw text.

            Returns:
                str: Localized text.
            """
            return (
                value.replace("#YOU", loc.you)
                .replace("#UPLOADEDSUB", loc.playlist.UPLOADEDSUB)
                .replace("#UPLOADED", loc.playlist.UPLOADED)
            )

        async def build() -> list[PlaylistItem]:
            """Read every playlist folder.

            Returns:
                list[PlaylistItem]: The playlists.
            """
            items: list[PlaylistItem] = []
            for name in self._folders("playlists"):
                folder = f"files/playlists/{name}"
                data = await self._json(f"{folder}/playlist.json")
                if not data.get("enabled", True):
                    continue
                items.append(
                    PlaylistItem(
                        name=name,
                        source=self._source,
                        version=data["version"],
                        title=replace(data["title"]),
                        subtitle=replace(data["subtitle"]),
                        author=replace(data["author"]),
                        tags=[],
                        levels=[],
                        thumbnail=await self._srl(f"{folder}/thumbnail.png", required=False),
                    )
                )
            return items

        return await self._cached(f"playlists_{code}", build)

    async def static_posts(self) -> list[StaticPost]:
        """Compile the announcements.

        Returns:
            list[StaticPost]: The posts in directory order.
        """

        async def build() -> list[StaticPost]:
            """Read every post folder.

            Returns:
                list[StaticPost]: The posts.
            """
            posts: list[StaticPost] = []
            for name in self._folders("posts"):
                folder = f"files/posts/{name}"
                data = await self._json(f"{folder}/post.json")
                if not data.get("enabled", True):
                    continue
                item = PostItem(
                    name=name,
                    source=self._source,
                    version=data["version"],
                    title=data["title"],
                    time=data["time"],
                    author=data["author"],
                    tags=[],
                    thumbnail=await self._srl(f"{folder}/thumbnail.png", required=False),
                )
                posts.append(StaticPost(item=item, description=data["description"]))
            return posts

        return await self._cached("static_posts", build)

    async def effects(self) -> list[EffectItem]:
        """Compile the effects.

        Returns:
            list[EffectItem]: The effects.
        """

        async def build() -> list[EffectItem]:
            """Read every effect folder.

            Returns:
                list[EffectItem]: The effects.
            """
            items: list[EffectItem] = []
            for name in self._folders("effects"):
                folder = f"files/effects/{name}"
                data = await self._json(f"{folder}/effect.json")
                if not data.get("enabled", True):
                    continue
                items.append(
                    EffectItem(
                        name=name,
                        source=self._source,
                        version=data["version"],
                        title=data["title"],
                        subtitle=data["subtitle"],
                        author=data["author"],
                        tags=[],
                        thumbnail=await self._srl(f"{folder}/thumbnail.png"),
                        data=await self._srl(f"{folder}/data"),
                        audio=await self._srl(f"{folder}/audio"),
                    )
                )
            return items

        return await self._cached("effects", build)

    async def _no_scope_configuration(self, folder: str) -> Srl | None:
        """Store the default background configuration without its scope.

        Args:
            folder: Background folder.

        Returns:
            Srl | None: The locator.
        """
        data = await asyncio.to_thread(
            _read_gzip_json, self._root / folder / "configuration.json.gz"
        )
        data.pop("scope", None)
        digest = await self._repository.add_bytes(gzip_bytes(json.dumps(data).encode("utf-8")))
        return await self._repository.get_srl(digest)

    async def backgrounds(self, locale: str) -> list[BackgroundItem]:
        """Compile the backgrounds.

        Args:
            locale: Requested locale code.

        Returns:
            list[BackgroundItem]: The backgrounds in directory order.
        """
        loc, code = self._locales.get_messages(locale)

        def replace(value: str) -> str:
            """Fill the background text placeholders.

            Args:
                value: Raw text.

            Returns:
                str: Localized text.
            """
            return value.replace(
                "#BACKGROUNDSELECTSUB", loc.background.BACKGROUNDSELECTSUB
            ).replace("#BACKGROUNDSELECT", loc.background.BACKGROUNDSELECT)

        async def build() -> list[BackgroundItem]:
            """Read every background folder.

            Returns:
                list[BackgroundItem]: The backgrounds.
            """
            items: list[BackgroundItem] = []
            for name in self._folders("backgrounds"):
                folder = f"files/backgrounds/{name}"
                data = await self._json(f"{folder}/background.json")
                if not data.get("enabled", True):
                    continue
                if name == "PLEASE-SELECT" and not self.background_no_scope:
                    self.background_no_scope = await self._no_scope_configuration(folder)
                configuration = (
                    self.background_no_scope
                    if name == "PLEASE-SELECT"
                    else await self._srl(f"{folder}/configuration.json.gz")
                )
                items.append(
                    BackgroundItem(
                        name=name,
                        source=self._source,
                        version=data["version"],
                        title=replace(data["title"]),
                        subtitle=replace(data["subtitle"]),
                        author=replace(data["author"]),
                        tags=[],
                        thumbnail=await self._srl(f"{folder}/thumbnail.png"),
                        data=await self._srl(f"{folder}/data"),
                        image=await self._srl(f"{folder}/image.png"),
                        configuration=configuration,
                    )
                )
            return items

        return await self._cached(f"backgrounds_{code}", build)

    async def particles(self) -> list[CompiledParticle]:
        """Compile the particles.

        Returns:
            list[CompiledParticle]: The particles, engine-specific ones included.
        """

        async def build() -> list[CompiledParticle]:
            """Read every particle folder.

            Returns:
                list[CompiledParticle]: The particles.
            """
            items: list[CompiledParticle] = []
            for name in self._folders("particles"):
                folder = f"files/particles/{name}"
                data = await self._json(f"{folder}/particle.json")
                if not data.get("enabled", True):
                    continue
                item = ParticleItem(
                    name=name,
                    source=self._source,
                    version=data["version"],
                    title=data["title"],
                    subtitle=data["subtitle"],
                    author=data["author"],
                    tags=[],
                    thumbnail=await self._srl(f"{folder}/thumbnail.png"),
                    data=await self._srl(f"{folder}/data"),
                    texture=await self._srl(f"{folder}/texture"),
                )
                items.append(CompiledParticle(item=item, engine_specific=data["engine_specific"]))
            return items

        return await self._cached("particles", build)

    async def skins(self) -> list[CompiledSkin]:
        """Compile the skins.

        Returns:
            list[CompiledSkin]: The skins sorted by title.
        """

        async def build() -> list[CompiledSkin]:
            """Read every skin folder.

            Returns:
                list[CompiledSkin]: The skins.
            """
            items: list[CompiledSkin] = []
            for name in self._folders("skins"):
                folder = f"files/skins/{name}"
                data = await self._json(f"{folder}/skin.json")
                if not data.get("enabled", True):
                    continue
                item = SkinItem(
                    name=name,
                    source=self._source,
                    version=data["version"],
                    title=data["title"],
                    subtitle=data["subtitle"],
                    author=data["author"],
                    tags=[],
                    thumbnail=await self._srl(f"{folder}/thumbnail.png"),
                    data=await self._srl(f"{folder}/data"),
                    texture=await self._srl(f"{folder}/texture"),
                )
                items.append(
                    CompiledSkin(
                        item=item,
                        engines=data.get("engines") or [],
                        themes=data.get("themes") or [],
                        locale=data.get("locale"),
                    )
                )
            return sorted(items, key=lambda skin: skin.item.title)

        return await self._cached("skins", build)

    async def _engine_configuration(self, folder: str, overrides: dict[str, Any]) -> Srl | None:
        """Store an engine configuration with its option overrides applied.

        Args:
            folder: Engine folder.
            overrides: Option fields to replace, keyed by option name.

        Returns:
            Srl | None: The locator.
        """
        path = f"{folder}/EngineConfiguration"
        if not overrides:
            return await self._srl(path)
        data = await asyncio.to_thread(_read_gzip_json, self._root / path)
        for option in data.get("options", []):
            if option.get("name") in overrides:
                option.update(overrides[option["name"]])
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        digest = await self._repository.add_bytes(gzip_bytes(encoded))
        return await self._repository.get_srl(digest)

    async def engines(self, locale: str) -> list[CompiledEngine]:
        """Compile the engines with their resources.

        Args:
            locale: Requested locale code.

        Returns:
            list[CompiledEngine]: The engines in sort order.
        """
        _, code = self._locales.get_messages(locale)

        async def build() -> list[CompiledEngine]:
            """Read every engine folder.

            Returns:
                list[CompiledEngine]: The engines.
            """
            items: list[CompiledEngine] = []
            skins = await self.skins()
            effects = await self.effects()
            particles = await self.particles()
            backgrounds = await self.backgrounds(code)
            for name in self._folders("engines"):
                folder = f"files/engines/{name}"
                data = await self._json(f"{folder}/engine.json")
                if not data.get("enabled", True):
                    continue
                configuration = await self._engine_configuration(
                    folder, data.get("config_overrides", {})
                )
                skin_name = data.get("skin_name_locale", {}).get(code) or data["skin_name"]
                try:
                    skin = next(skin for skin in skins if skin.item.name == skin_name)
                    effect = next(item for item in effects if item.name == data["effect_name"])
                    particle = next(
                        item for item in particles if item.item.name == data["particle_name"]
                    )
                    background = next(
                        item for item in backgrounds if item.name == data["background_name"]
                    )
                except StopIteration:
                    raise KeyError(
                        "StopIteration raised: incorrect key name! Make sure your engine file "
                        "names and resource file names match."
                    ) from None
                item = EngineItem(
                    name=name,
                    source=self._source,
                    version=13,
                    title=data.get("title"),
                    subtitle=data.get("subtitle"),
                    author=data.get("author"),
                    tags=[],
                    skin=skin.item,
                    background=background,
                    effect=effect,
                    particle=particle.item,
                    thumbnail=await self._srl(f"{folder}/thumbnail.png"),
                    playData=await self._srl(f"{folder}/EnginePlayData"),
                    watchData=await self._srl(f"{folder}/EngineWatchData"),
                    previewData=await self._srl(f"{folder}/EnginePreviewData"),
                    tutorialData=await self._srl(f"{folder}/EngineTutorialData"),
                    rom=await self._srl(f"{folder}/EngineRom", required=False),
                    configuration=configuration,
                )
                items.append(
                    CompiledEngine(
                        item=item,
                        description=data.get("description"),
                        sort_order=data.get("engine_sort_order", float("inf")),
                    )
                )
            return sorted(items, key=lambda engine: (engine.sort_order, engine.item.title.lower()))

        return await self._cached(f"engines_{code}", build)
