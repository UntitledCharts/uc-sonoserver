import re

import aiohttp
from fastapi import APIRouter, Request, Response
from pydantic import ValidationError

from app.backend.client import BackendError
from app.backend.error_text import (
    UNSURE,
    authenticate_error,
    authenticate_external_error,
)
from app.errors import SonolusError
from app.routers.common import respond
from app.sonolus_core import (
    ServerAuthenticateResponse,
    ServiceAuthenticateExternalResponse,
    ServiceUserProfile,
    SonolusModel,
)
from app.state import Context
from app.timefmt import epoch_ms

router = APIRouter()

LOGIN_REQUEST_ID = re.compile(r"[A-Za-z0-9._~-]{1,512}")
SIGNATURE_HEADER = "Sonolus-Signature"


class AuthenticateBody(SonolusModel):
    """Body Sonolus signs when logging in to the server.

    Attributes:
        type: Should be ``authenticateServer``.
        address: Server address the player is logging in to.
        time: Signing time in epoch milliseconds.
        userProfile: The player's profile.
    """

    type: str
    address: str
    time: int
    userProfile: ServiceUserProfile


class AuthenticateExternalBody(SonolusModel):
    """Body Sonolus signs when approving a website login.

    Attributes:
        type: Should be ``authenticateExternal``.
        url: URL the approval was sent to.
        time: Signing time in epoch milliseconds.
        userProfile: The player's profile.
    """

    type: str
    url: str
    time: int
    userProfile: ServiceUserProfile


@router.post("/sonolus/authenticate")
async def authenticate(request: Request, context: Context, body: AuthenticateBody) -> Response:
    """Exchange a signed Sonolus login for a game session.

    Args:
        request: Current request.
        context: App context.
        body: Signed login payload, validated before it is forwarded.

    Returns:
        Response: The session and its expiry in epoch milliseconds.
    """
    raw = await request.body()
    try:
        session = await context.backend.game_session(raw, request.headers.get(SIGNATURE_HEADER))
    except BackendError as error:
        raise authenticate_error(error) from None
    except (aiohttp.ClientError, TimeoutError, ValidationError):
        raise SonolusError(400, UNSURE) from None
    return respond(
        ServerAuthenticateResponse(session=session.session, expiration=epoch_ms(session.expires_at))
    )


@router.post("/sonolus/authenticate_external")
async def authenticate_external(
    request: Request, context: Context, body: AuthenticateExternalBody
) -> Response:
    """Approve a website login request with a signed Sonolus payload.

    Args:
        request: Current request.
        context: App context.
        body: Signed approval payload, validated before it is forwarded.

    Returns:
        Response: A message telling the player to return to the browser.
    """
    request_id = request.query_params.get("id")
    if not request_id:
        raise SonolusError(400, "Missing id.")
    if not LOGIN_REQUEST_ID.fullmatch(request_id):
        raise authenticate_external_error(BackendError(404, "error.login_request.not_found"))
    raw = await request.body()
    try:
        await context.backend.approve_login(request_id, raw, request.headers.get(SIGNATURE_HEADER))
    except BackendError as error:
        raise authenticate_external_error(error) from None
    return respond(ServiceAuthenticateExternalResponse(message="Success. Return to the browser."))
