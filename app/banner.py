import asyncio
import logging
import time

import aiohttp

from app.backend.client import BackendClient, BackendError
from app.sonolus_core import Srl

logger = logging.getLogger("uc.sonoserver.banner")


class Banner:
    """Server banner from the backend, reused for a while per process.

    Attributes:
        _backend: Chart backend client.
        _seconds: Seconds a fetched banner is reused.
        _value: Last banner locator, None without a banner.
        _fetched_at: Monotonic time of the last fetch attempt, 0 before the first.
        _lock: Prevents parallel fetches.
    """

    def __init__(self, backend: BackendClient, seconds: float) -> None:
        """Create the banner source.

        Args:
            backend: Chart backend client.
            seconds: Seconds a fetched banner is reused.
        """
        self._backend = backend
        self._seconds = seconds
        self._value: Srl | None = None
        self._fetched_at = 0.0
        self._lock = asyncio.Lock()

    def _fresh(self) -> bool:
        """Check whether the last fetch is recent enough to reuse.

        Returns:
            bool: True within the reuse window.
        """
        return self._fetched_at > 0 and time.monotonic() - self._fetched_at < self._seconds

    async def get(self) -> Srl | None:
        """Return the server banner, asking the backend when the last answer is too old.

        Returns:
            Srl | None: The banner locator, or None without a banner. When the backend can't be
                reached the last known banner is kept.
        """
        if self._fresh():
            return self._value
        async with self._lock:
            if self._fresh():
                return self._value
            try:
                assets = await self._backend.assets()
            except (BackendError, aiohttp.ClientError, asyncio.TimeoutError) as error:
                logger.warning("couldn't fetch the server banner: %s", error)
            else:
                banner = assets.banner
                self._value = Srl(hash=banner.hash, url=banner.url) if banner else None
            self._fetched_at = time.monotonic()
            return self._value
