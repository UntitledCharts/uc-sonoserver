from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class _Section(BaseModel):
    """Base for config and constants sections: every key required, unknown keys rejected.

    Attributes:
        model_config: Pydantic configuration forbidding extra keys.
    """

    model_config = ConfigDict(extra="forbid")


class ServerConfig(_Section):
    """HTTP server settings.

    Attributes:
        host: Interface uvicorn binds to.
        port: Port uvicorn listens on.
        workers: uvicorn worker processes.
        debug: Enables the API docs and access logs only.
        public_url: Public base URL of this Sonolus server, without a trailing slash.
        allowed_hosts: Host headers accepted.
        trusted_proxies: Number of proxies in front of the app adding X-Forwarded-For entries.
    """

    host: str
    port: int
    workers: int = Field(ge=1)
    debug: bool
    public_url: str
    allowed_hosts: list[str]
    trusted_proxies: int = Field(ge=0)


class SonolusConfig(_Section):
    """Sonolus-facing settings.

    Attributes:
        version: Value of the Sonolus-Version header sent on every response.
        title: Server title shown in the Sonolus app.
        description: Server description used when the locale has none.
        chart_prefix: Prefix of chart item names.
    """

    version: str
    title: str
    description: str
    chart_prefix: str


class BackendConfig(_Section):
    """Chart backend connection settings.

    Attributes:
        url: Base URL of the chart backend, without a trailing slash.
        sonoserver_key: Value of the X-SonoServer-Key header for internal backend calls.
        timeout_seconds: Total timeout of one backend request.
    """

    url: str
    sonoserver_key: str
    timeout_seconds: float = Field(gt=0)


class KeysConfig(_Section):
    """Secret keys.

    Attributes:
        upload_key_secret: HMAC key signing replay upload keys.
    """

    upload_key_secret: str


class RedisConfig(_Section):
    """Redis connection settings.

    Attributes:
        host: Redis host.
        port: Redis port.
        db: Redis database number.
        password: Redis password, None for none.
    """

    host: str
    port: int
    db: int = Field(ge=0)
    password: str | None


class Config(_Section):
    """Whole config.yml.

    Attributes:
        server: HTTP server settings.
        sonolus: Sonolus-facing settings.
        backend: Chart backend connection settings.
        keys: Secret keys.
        redis: Redis connection settings.
    """

    server: ServerConfig
    sonolus: SonolusConfig
    backend: BackendConfig
    keys: KeysConfig
    redis: RedisConfig


class AssetConstants(_Section):
    """Shared site image constants.

    Attributes:
        banner_cache_seconds: Seconds the server banner from the backend is reused.
    """

    banner_cache_seconds: float = Field(ge=0)


class RequestConstants(_Section):
    """Request limits.

    Attributes:
        max_body_size: Largest request body accepted outside the replay upload, in bytes.
    """

    max_body_size: int


class ReplayConstants(_Section):
    """Replay submission limits.

    Attributes:
        upload_key_seconds: Lifetime of a signed upload key.
        max_data_size: Largest compressed replay data accepted, in bytes.
        max_config_size: Largest compressed replay configuration accepted, in bytes.
        max_config_decompressed_size: Largest decompressed replay configuration accepted, in bytes.
        max_multipart_overhead: Multipart framing allowed on top of both files, in bytes.
    """

    upload_key_seconds: int
    max_data_size: int
    max_config_size: int
    max_config_decompressed_size: int
    max_multipart_overhead: int


class ListConstants(_Section):
    """Sizes of item lists and home sections.

    Attributes:
        items_per_page: Items per page of the static lists, keyed by list name with a default.
        resource_section_size: Items in the resource, playlist and announcement sections.
        level_section_size: Levels in each home level section.
        backend_page_size: Items in a full backend page, used to detect more random results.
        replay_section_size: Replays in each home replay section.
        replay_page_size: Replays per replay list page.
        leaderboard_top_records: Records in a leaderboard preview.
        leaderboard_page_size: Records per leaderboard page.
        max_page: Highest page number any list accepts.
        backend_max_limit: Most items the backend returns per offset/limit request.
    """

    items_per_page: dict[str, int]
    resource_section_size: int
    level_section_size: int
    backend_page_size: int
    replay_section_size: int
    replay_page_size: int
    leaderboard_top_records: int
    leaderboard_page_size: int
    max_page: int
    backend_max_limit: int

    def per_page(self, name: str) -> int:
        """Items per page of a static list.

        Args:
            name: List name such as ``posts`` or ``engines``.

        Returns:
            int: The page size.
        """
        return self.items_per_page.get(name, self.items_per_page["default"])


class SearchConstants(_Section):
    """Search form limits.

    Attributes:
        keywords_limit: Longest keywords text.
        title_limit: Longest title filter.
        author_limit: Longest author filter.
        description_limit: Longest description filter.
        artists_limit: Longest artists filter.
        tags_limit: Longest tags filter.
        min_rating: Lowest rating slider value.
        max_rating: Highest rating slider value.
        max_count: Highest likes and comments slider value.
        max_playlist_name_length: Longest encoded playlist name or filter body.
    """

    keywords_limit: int
    title_limit: int
    author_limit: int
    description_limit: int
    artists_limit: int
    tags_limit: int
    min_rating: int
    max_rating: int
    max_count: int
    max_playlist_name_length: int


class ModerationConstants(_Section):
    """Moderation and community form limits.

    Attributes:
        comment_limit: Longest comment text.
        rerate_limit: Longest rating text in the rerate form.
        rerate_bound: Ratings must be between minus this and this, inclusive.
        rerate_max_decimals: Most decimal places a new rating may have.
    """

    comment_limit: int
    rerate_limit: int
    rerate_bound: int
    rerate_max_decimals: int


class Constants(_Section):
    """Whole constants.yml.

    Attributes:
        website_url: Website players are sent to for uploads.
        requests: Request limits.
        replays: Replay submission limits.
        lists: List and section sizes.
        search: Search form limits.
        moderation: Moderation and community form limits.
    """

    website_url: str
    assets: AssetConstants
    requests: RequestConstants
    replays: ReplayConstants
    lists: ListConstants
    search: SearchConstants
    moderation: ModerationConstants


def _read_yaml(path: Path) -> dict:
    """Read a YAML mapping from disk.

    Args:
        path: File to read.

    Returns:
        dict: Parsed mapping.
    """
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def load_config(path: Path) -> Config:
    """Load and validate config.yml.

    Args:
        path: Location of config.yml.

    Returns:
        Config: Validated configuration.
    """
    return Config.model_validate(_read_yaml(path))


def load_constants(path: Path) -> Constants:
    """Load and validate constants.yml.

    Args:
        path: Location of constants.yml.

    Returns:
        Constants: Validated constants.
    """
    return Constants.model_validate(_read_yaml(path))
