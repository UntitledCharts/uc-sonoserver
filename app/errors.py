import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger("uc.sonoserver")


class SonolusError(Exception):
    """Error returned to the Sonolus client as ``{"message": ...}``.

    Attributes:
        status_code: HTTP status of the response.
        message: Text shown to the player.
    """

    def __init__(self, status_code: int, message: str | None = None) -> None:
        """Create an error.

        Args:
            status_code: HTTP status of the response.
            message: Text shown to the player, the status reason phrase when None.
        """
        resolved = message if message is not None else reason_phrase(status_code)
        super().__init__(resolved)
        self.status_code = status_code
        self.message = resolved


def reason_phrase(status_code: int) -> str:
    """Return the standard reason phrase of a status.

    Args:
        status_code: HTTP status.

    Returns:
        str: The phrase, or an empty string for unknown statuses.
    """
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return ""


def error_response(request: Request, status_code: int, message: str) -> JSONResponse:
    """Build the error body players see.

    Args:
        request: The failed request.
        status_code: HTTP status.
        message: Text shown to the player.

    Returns:
        JSONResponse: ``{"message": ...}`` below 500, ``{}`` otherwise.
    """
    if status_code < 500:
        return JSONResponse({"message": message}, status_code=status_code)
    logger.error("error %s: %s %s", status_code, request.method, request.url)
    return JSONResponse({}, status_code=status_code)


def install_error_handlers(app: FastAPI) -> None:
    """Register the handlers rendering Sonolus errors.

    Args:
        app: Application to register the handlers on.
    """

    async def handle_sonolus_error(request: Request, exc: Exception) -> JSONResponse:
        """Render a SonolusError.

        Args:
            request: The failed request.
            exc: The raised error.

        Returns:
            JSONResponse: The error response.
        """
        if not isinstance(exc, SonolusError):
            raise exc
        return error_response(request, exc.status_code, exc.message)

    async def handle_http_exception(request: Request, exc: Exception) -> JSONResponse:
        """Render an HTTPException raised by application code.

        Args:
            request: The failed request.
            exc: The raised error.

        Returns:
            JSONResponse: The error response.
        """
        if not isinstance(exc, HTTPException):
            raise exc
        return error_response(request, exc.status_code, str(exc.detail))

    app.add_exception_handler(SonolusError, handle_sonolus_error)
    app.add_exception_handler(HTTPException, handle_http_exception)
