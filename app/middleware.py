import logging
from http import HTTPStatus

from fastapi.exceptions import HTTPException
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("uc.sonoserver")

UNHANDLED_ERROR = b"Unhandled error. Report to discord.gg/UntitledCharts"
TOO_LARGE = HTTPStatus.REQUEST_ENTITY_TOO_LARGE


class SonolusVersionMiddleware:
    """Adds the Sonolus-Version header to every HTTP response.

    Attributes:
        app: Wrapped application.
        version: Header value.
    """

    def __init__(self, app: ASGIApp, version: str) -> None:
        """Wrap an application.

        Args:
            app: Wrapped application.
            version: Header value.
        """
        self.app = app
        self.version = version

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Forward the request, adding the header to the response start.

        Args:
            scope: ASGI scope.
            receive: ASGI receive channel.
            send: ASGI send channel.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_version(message: Message) -> None:
            """Add the header before the response starts.

            Args:
                message: ASGI message.
            """
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message)["Sonolus-Version"] = self.version
            await send(message)

        await self.app(scope, receive, send_with_version)


class UnhandledErrorMiddleware:
    """Turns exceptions escaping the routes into the old plain 500 response.

    Attributes:
        app: Wrapped application.
    """

    def __init__(self, app: ASGIApp) -> None:
        """Wrap an application.

        Args:
            app: Wrapped application.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Forward the request, answering 500 when it raises before responding.

        Args:
            scope: ASGI scope.
            receive: ASGI receive channel.
            send: ASGI send channel.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        started = False

        async def tracking_send(message: Message) -> None:
            """Remember whether the response started.

            Args:
                message: ASGI message.
            """
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, receive, tracking_send)
        except Exception:
            logger.exception("unhandled error on %s %s", scope.get("method"), scope.get("path"))
            if started:
                raise
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [(b"content-length", str(len(UNHANDLED_ERROR)).encode())],
                }
            )
            await send({"type": "http.response.body", "body": UNHANDLED_ERROR})


class BodyLimitMiddleware:
    """Rejects request bodies over a size limit with 413 before they are buffered.

    Attributes:
        app: Wrapped application.
        limit: Largest body accepted, in bytes.
        exempt_paths: Paths that enforce their own limits.
    """

    def __init__(self, app: ASGIApp, limit: int, exempt_paths: tuple[str, ...]) -> None:
        """Wrap an application.

        Args:
            app: Wrapped application.
            limit: Largest body accepted, in bytes.
            exempt_paths: Paths that enforce their own limits.
        """
        self.app = app
        self.limit = limit
        self.exempt_paths = exempt_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Forward the request, cutting it off once its body passes the limit.

        Args:
            scope: ASGI scope.
            receive: ASGI receive channel.
            send: ASGI send channel.
        """
        if scope["type"] != "http" or scope["path"] in self.exempt_paths:
            await self.app(scope, receive, send)
            return
        declared = Headers(scope=scope).get("content-length")
        if declared is not None and declared.isdigit() and int(declared) > self.limit:
            response = JSONResponse({"message": TOO_LARGE.phrase}, status_code=TOO_LARGE.value)
            await response(scope, receive, send)
            return
        received = 0

        async def limited_receive() -> Message:
            """Count body bytes, failing the request once they pass the limit.

            Returns:
                Message: The next ASGI message.
            """
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.limit:
                    raise HTTPException(TOO_LARGE.value, TOO_LARGE.phrase)
            return message

        await self.app(scope, limited_receive, send)
