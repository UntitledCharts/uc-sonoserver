from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from typing import Literal, TypeVar, overload, TYPE_CHECKING
from pydantic import BaseModel, Field

from helpers.data_compilers import *
from helpers.datetime_to_str import datetime_to_str
from helpers.models.sonolus.item import LevelItem, UseItem, UserItem
from helpers.models.sonolus.misc import Tag
from helpers.owoify import handle_uwu

if TYPE_CHECKING:
    from core import SonolusRequest


M = TypeVar("M", bound=BaseModel)


class Chart(BaseModel):
    id: str
    rating: int | Decimal
    author: str  # author sonolus id
    title: str
    staff_pick: bool
    artists: str | None = None
    jacket_file_hash: str
    music_file_hash: str
    chart_file_hash: str
    background_v1_file_hash: str
    background_v3_file_hash: str
    tags: list[str] | None = Field(default_factory=list)
    description: str | None = None
    preview_file_hash: str | None = None
    background_file_hash: str | None = None
    status: Literal["UNLISTED", "PRIVATE", "PUBLIC"]
    like_count: int
    comment_count: int
    created_at: datetime
    published_at: datetime | None = None
    updated_at: datetime
    author_full: str | None = None
    author_handle: int
    chart_design: str
    is_first_publish: bool | None = None  # only returned on update_status
    liked: bool | None = None
    deleted_at: datetime | None = None

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_cached_particle(base_url: str, particle_name: str) -> ParticleItem:
        particles = compile_particles_list(base_url)
        particle_data = next(
            particle for particle in particles if particle.name == particle_name
        )
        return particle_data.to_particle_item()

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_cached_skin(
        base_url: str, skin_name: str, engine_name: str, localization: str
    ) -> SkinItem:
        skins = compile_skins_list(base_url)

        candidates = [
            skin
            for skin in skins
            if skin.themes
            and skin.name in skin.themes
            and (not skin.engines or engine_name in skin.engines)
        ]

        if not candidates:
            raise KeyError("no matching theme/engine for skin found")

        #  try to match locale
        for skin in candidates:
            if skin.locale == localization:
                return skin.to_skin_item()

        # fallback: find skin where no locale is set (some global skin)
        for skin in candidates:
            if skin.locale is None:
                return skin.to_skin_item()

        # fallback 2: just return first item
        return candidates[0].to_skin_item()

    @staticmethod
    def _get_cached_background(base_url: str, localization: str):
        return compile_backgrounds_list(base_url, localization)[0].model_copy(deep=True)

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_cached_engine(base_url: str, engine_name: str, locale: str):
        engines = compile_engines_list(base_url, locale)
        engine_data = next(engine for engine in engines if engine.name == engine_name)
        return engine_data.to_engine_item()

    def _make_url(self, asset_base_url: str, file_hash: str) -> str:
        return "/".join([asset_base_url, self.author, self.id, file_hash])

    @overload
    def to_level_item(
        self,
        request: "SonolusRequest",
        asset_base_url: str,
        bgtype: str,
        include_description: Literal[False] = False,
        disable_replace_missing_preview: bool = False,
        context: Literal["list", "level"] = "list",
        use_engine: str | None = None,
    ) -> LevelItem: ...

    @overload
    def to_level_item(
        self,
        request: "SonolusRequest",
        asset_base_url: str,
        bgtype: str,
        include_description: Literal[True],
        disable_replace_missing_preview: bool = False,
        context: Literal["list", "level"] = "list",
        use_engine: str | None = None,
    ) -> tuple[LevelItem, str]: ...

    def to_level_item(
        self,
        request: "SonolusRequest",
        asset_base_url: str,
        bgtype: str,
        include_description: Literal[False] = False,
        disable_replace_missing_preview: bool = False,
        context: Literal["list", "level"] = "list",
        use_engine: str | None = None,
    ):
        loc = request.state.loc

        default = bgtype.startswith("default_or_")

        if default:
            bgtype = bgtype.removeprefix("default_or_")
            background_hash = self.background_file_hash
        else:
            background_hash = None

        if not background_hash:
            default = False
            background_hash: str = getattr(self, f"background_{bgtype}_file_hash")

        bg_item = self._get_cached_background(
            request.app.base_url, request.state.localization
        )
        bg_item.image = SRL(
            hash=background_hash, url=self._make_url(asset_base_url, background_hash)
        )
        bg_item.thumbnail = SRL(
            hash=self.jacket_file_hash,
            url=self._make_url(asset_base_url, self.jacket_file_hash),
        )
        bg_item.name = "configured"

        if not default and bgtype == "v3":
            title = loc.background.V3
        elif not default and bgtype == "v1":
            title = loc.background.V3
        else:
            title = loc.background.UPLOADED
            bg_item.configuration = cached["BACKGROUND_NO_SCOPE_SRL"]

        bg_item.title = handle_uwu(title, request.state.localization, request.state.uwu)

        if request.state.skin == "engine_default":
            skin_option = UseItem(useDefault=True)
        else:
            try:
                skin_option = UseItem(
                    useDefault=False,
                    item=self._get_cached_skin(
                        request.app.base_url,
                        request.state.skin,
                        use_engine if use_engine else request.state.engine,
                        request.state.localization,
                    ),
                )
            except (
                KeyError
            ):  # handles if an engine does not have a correctly-themed skin
                skin_option = UseItem(useDefault=True)

        if request.state.particle == "engine_default":
            particle_option = UseItem(useDefault=True)
        else:
            try:
                particle_option = UseItem(
                    useDefault=False,
                    item=self._get_cached_particle(
                        request.app.base_url, request.state.particle
                    ),
                )
            except KeyError:
                particle_option = UseItem(useDefault=True)

        time_str = datetime_to_str(self.published_at or self.created_at)
        date_str = handle_uwu(
            (
                loc.time_ago(time_str)
                if self.published_at
                else loc.time_ago_not_published(time_str)
            ),
            request.state.localization,
            request.state.uwu,
        )

        if context == "list":
            additional = []
            tags = [
                Tag(
                    title=handle_uwu(tag, request.state.localization, request.state.uwu)
                )
                for tag in self.tags
            ]
        else:
            visibilities = {
                "PUBLIC": Tag(title="#PUBLIC", icon="globe"),
                "PRIVATE": Tag(title="#PRIVATE", icon="lock"),
                "UNLISTED": Tag(title=loc.search.VISIBILITY_UNLISTED, icon="unlock"),
            }

            additional = [visibilities[self.status]]
            tags = [
                Tag(
                    title=handle_uwu(
                        tag, request.state.localization, request.state.uwu
                    ),
                    icon="tag",
                )
                for tag in self.tags
            ]

        metadata = [
            Tag(title=date_str, icon="clock"),
            Tag(
                title=str(self.like_count),
                icon=("heart" if self.liked else "heartHollow"),
            ),
            Tag(title=str(self.comment_count), icon="comment"),
        ]

        level_tags = additional + metadata + tags
        if self.staff_pick:
            level_tags.insert(
                0,
                Tag(
                    title=loc.staff_pick if context == "level" else None, icon="trophy"
                ),
            )

        item = LevelItem(
            name=f"UnCh-{self.id}",
            source=request.app.base_url,
            rating=self.rating,
            title=handle_uwu(self.title, request.state.localization, request.state.uwu),
            artists=handle_uwu(
                self.artists, request.state.localization, request.state.uwu
            ),
            author=self.author_full,
            tags=level_tags,
            engine=self._get_cached_engine(
                request.app.base_url,
                use_engine if use_engine else request.state.engine,
                request.state.localization,
            ),
            useSkin=skin_option,
            useBackground=UseItem(useDefault=False, item=bg_item),
            useEffect=UseItem(useDefault=True),
            useParticle=particle_option,
            cover=SRL(
                hash=self.jacket_file_hash,
                url=self._make_url(asset_base_url, self.jacket_file_hash),
            ),
            bgm=SRL(
                hash=self.music_file_hash,
                url=self._make_url(asset_base_url, self.music_file_hash),
            ),
            preview=(
                SRL(
                    hash=self.preview_file_hash,
                    url=self._make_url(asset_base_url, self.preview_file_hash),
                )
                if self.preview_file_hash
                else (
                    None
                    if disable_replace_missing_preview
                    else SRL(
                        hash=self.music_file_hash,
                        url=self._make_url(asset_base_url, self.music_file_hash),
                    )
                )
            ),
            data=SRL(
                hash=self.chart_file_hash,
                url=self._make_url(asset_base_url, self.chart_file_hash),
            ),
            authorUser=UserItem(
                name=self.author,
                title=self.author_full.rsplit("#", maxsplit=1)[0],
                handle=str(self.author_handle),
                tags=[],
            ),
        )

        if include_description:
            return item, self.description

        return item


class GetChartResponse(BaseModel):
    data: Chart
    asset_base_url: str
    mod: bool | None = None
    admin: bool | None = None  # XXX (backend): Make optional fields non-optional
    owner: bool


class DeleteChartResponse(Chart):
    admin: bool | None = None
    owner: bool | None = None


class PromotionData(BaseModel):
    chart_id: str
    view_code: str


class PromotionServeResponse(BaseModel):
    promotion: PromotionData | None = None
    data: Chart | None = None
    asset_base_url: str | None = None


class VisibilityChangeResponse(Chart):
    mod: bool | None = None
    owner: bool | None = None


class _BaseChartList(BaseModel):
    data: list[Chart]
    asset_base_url: str


class RandomChartList(_BaseChartList): ...


class ChartList(_BaseChartList):
    pageCount: int
