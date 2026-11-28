from dataclasses import dataclass

import aiohttp
from redis.asyncio import Redis
from starlette.requests import HTTPConnection

from app.backend.client import BackendClient
from app.banner import Banner
from app.localization import LocaleManager
from app.replay import EngineOption
from app.repository import Repository
from app.resources import Resources
from app.settings import Config, Constants


@dataclass
class AppContext:
    """Everything a request handler needs, created once per process.

    Attributes:
        config: Validated config.yml.
        constants: Validated constants.yml.
        http: Shared outgoing HTTP session.
        backend: Chart backend client.
        redis: Redis client.
        repository: Blob repository.
        locales: Locale manager.
        resources: Items compiled from ``files/``.
        banner: Server banner from the backend.
        engine_rules: Option checks of the rankable engines.
    """

    config: Config
    constants: Constants
    http: aiohttp.ClientSession
    backend: BackendClient
    redis: Redis
    repository: Repository
    locales: LocaleManager
    resources: Resources
    banner: Banner
    engine_rules: dict[str, list[EngineOption]]


def get_context(connection: HTTPConnection) -> AppContext:
    """Return the app context of a request.

    Args:
        connection: Current request.

    Returns:
        AppContext: The context.
    """
    return connection.app.state.context
