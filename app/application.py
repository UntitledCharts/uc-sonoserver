import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import aiohttp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.backend.client import BackendClient
from app.banner import Banner
from app.context import AppContext
from app.errors import install_error_handlers
from app.localization import LocaleManager
from app.middleware import (
    BodyLimitMiddleware,
    SonolusVersionMiddleware,
    UnhandledErrorMiddleware,
)
from app.replay import load_engine_rules
from app.repository import Repository
from app.resources import Resources
from app.routers import (
    auth,
    community,
    info,
    leaderboards,
    levels,
    playlists,
    posts,
    replays,
    repository,
    resources,
    results,
    users,
)
from app.settings import Config, Constants, load_config, load_constants

CONFIG_ENV = "UC_SONOSERVER_CONFIG"
CONSTANTS_ENV = "UC_SONOSERVER_CONSTANTS"
ROOT = Path(__file__).resolve().parent.parent
UPLOAD_PATH = "/sonolus/levels/result/upload"

ROUTERS = (
    auth.router,
    info.router,
    levels.router,
    results.router,
    playlists.router,
    posts.router,
    replays.router,
    repository.router,
    community.item_router,
    levels.item_router,
    leaderboards.item_router,
    playlists.item_router,
    posts.item_router,
    replays.item_router,
    resources.router,
    users.item_router,
    resources.item_router,
)


def create_app(config: Config, constants: Constants) -> FastAPI:
    """Build the FastAPI application.

    Args:
        config: Validated config.yml.
        constants: Validated constants.yml.

    Returns:
        FastAPI: The application.
    """
    locales = LocaleManager(ROOT / "i18n")
    engine_rules = load_engine_rules(ROOT)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Open and close the process-wide clients.

        Args:
            app: The application.

        Returns:
            AsyncGenerator[None, None]: Lifespan context.
        """
        http = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.backend.timeout_seconds)
        )
        redis = Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
        )
        store = Repository(redis, ROOT)
        compiled = Resources(ROOT, store, locales, config.server.public_url)
        backend = BackendClient(http, config.backend.url, config.backend.sonoserver_key)
        app.state.context = AppContext(
            config=config,
            constants=constants,
            http=http,
            backend=backend,
            redis=redis,
            repository=store,
            locales=locales,
            resources=compiled,
            banner=Banner(backend, constants.assets.banner_cache_seconds),
            engine_rules=engine_rules,
        )
        await compiled.engines("en")
        try:
            yield
        finally:
            await http.close()
            await redis.aclose()

    debug = config.server.debug
    app = FastAPI(
        title="UntitledCharts Sonolus server",
        lifespan=lifespan,
        redirect_slashes=False,
        docs_url="/docs" if debug else None,
        redoc_url="/redoc" if debug else None,
        openapi_url="/openapi.json" if debug else None,
    )
    install_error_handlers(app)
    app.add_middleware(
        BodyLimitMiddleware,
        limit=constants.requests.max_body_size,
        exempt_paths=(UPLOAD_PATH,),
    )
    app.add_middleware(UnhandledErrorMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SonolusVersionMiddleware, version=config.sonolus.version)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.server.allowed_hosts)
    for router in ROUTERS:
        app.include_router(router)
    return app


def create_app_from_env() -> FastAPI:
    """Build the application from the config paths main.py exported.

    Returns:
        FastAPI: The application.
    """
    config = load_config(Path(os.environ.get(CONFIG_ENV, "config.yml")))
    constants = load_constants(Path(os.environ.get(CONSTANTS_ENV, "constants.yml")))
    return create_app(config, constants)
