import hashlib

from fastapi import APIRouter, Header, Request, Response
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartException
from starlette.requests import Request as StarletteRequest
from starlette.types import Message

from app.backend.error_text import Site
from app.errors import SonolusError
from app.names import chart_id
from app.replay import (
    UploadKeyData,
    drop_upload_session,
    generate_upload_key,
    load_upload_session,
    store_upload_session,
    validate_replay_config,
    verify_upload_key,
)
from app.routers.common import backend, require_chart_id, require_session, respond
from app.sonolus_core import (
    ServerForm,
    ServerLevelResultInfo,
    ServerSubmitLevelResultRequest,
    ServerSubmitLevelResultResponse,
    ServerUploadLevelResultResponse,
)
from app.context import AppContext
from app.state import Context, RequestState, State

router = APIRouter()

TOO_LARGE = "Uploaded files exceed file size limit."
OUTDATED_ENGINE = "You are using an outdated engine"
INVALID_UPLOAD_KEY = "Invalid upload token."


@router.get("/sonolus/levels/result/info")
async def result_info() -> Response:
    """Return the result submission options.

    Returns:
        Response: The replay submit form.
    """
    return respond(
        ServerLevelResultInfo(
            submits=[
                ServerForm(
                    type="replay",
                    title="#REPLAY",
                    requireConfirmation=False,
                    options=[],
                )
            ]
        )
    )


@router.post("/sonolus/levels/result/submit")
async def result_submit(
    context: Context, state: State, body: ServerSubmitLevelResultRequest
) -> Response:
    """Issue a signed upload key for a finished level's replay.

    Args:
        context: App context.
        state: Player configuration.
        body: The replay item and form values.

    Returns:
        Response: The upload key and the hashes to upload.
    """
    loc = state.loc
    session = require_session(state)
    me = await backend(context.backend.me(session), Site.DETAIL, loc)
    if me.account.banned:
        raise SonolusError(403, loc.leaderboards.YOU_ARE_BANNED)
    engines = {
        engine.item.name: engine.item
        for engine in await context.resources.engines(state.localization)
    }
    server = engines[state.engine]
    client = body.replay.level.engine
    if (
        client.playData.hash != server.playData.hash
        or client.watchData.hash != server.watchData.hash
        or (client.rom.hash if client.rom else None) != (server.rom.hash if server.rom else None)
    ):
        raise SonolusError(400, OUTDATED_ENGINE)
    level_name = body.replay.level.name
    require_chart_id(level_name, context.config.sonolus.chart_prefix, Site.DETAIL, loc)
    data_hash = body.replay.data.hash
    configuration_hash = body.replay.configuration.hash
    if not data_hash or not configuration_hash:
        raise SonolusError(400)
    lifetime = context.constants.replays.upload_key_seconds
    key, nonce = generate_upload_key(
        context.config.keys.upload_key_secret,
        lifetime,
        UploadKeyData(
            user_id=me.account.id,
            expires_at=0,
            chart_name=level_name,
            data_hash=data_hash,
            configuration_hash=configuration_hash,
            engine_name=state.engine,
            display_name=f"{me.account.username}#{me.account.handle}",
        ),
    )
    await store_upload_session(context.redis, nonce, session, lifetime)
    return respond(ServerSubmitLevelResultResponse(key=key, hashes=[data_hash, configuration_hash]))


async def _read_body(request: Request, limit: int) -> bytes:
    """Read a request body, failing as soon as it grows past a limit.

    Args:
        request: Current request.
        limit: Largest body accepted.

    Returns:
        bytes: The body.
    """
    declared = request.headers.get("content-length")
    if declared is not None and declared.isdigit() and int(declared) > limit:
        raise SonolusError(406, TOO_LARGE)
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > limit:
            raise SonolusError(406, TOO_LARGE)
    return bytes(body)


async def _read_file(upload: UploadFile, limit: int) -> bytes:
    """Read an uploaded file, at most one byte past its limit.

    Args:
        upload: Uploaded file.
        limit: Largest size accepted.

    Returns:
        bytes: The contents.
    """
    data = await upload.read(limit + 1)
    if len(data) > limit:
        raise SonolusError(406, TOO_LARGE)
    return data


async def _save_replay(
    request: Request,
    context: AppContext,
    state: RequestState,
    key: UploadKeyData,
    session: str,
) -> None:
    """Check the uploaded replay files against the signed key and save the record.

    Args:
        request: Current request.
        context: App context.
        state: Player configuration.
        key: Verified upload key.
        session: Session of the submitting player.
    """
    loc = state.loc
    limits = context.constants.replays
    chart = chart_id(key.chart_name, context.config.sonolus.chart_prefix)
    if chart is None:
        raise SonolusError(400)
    body = await _read_body(
        request,
        limits.max_data_size + limits.max_config_size + limits.max_multipart_overhead,
    )

    async def receive() -> Message:
        """Replay the buffered body to the form parser.

        Returns:
            Message: The whole body in one message.
        """
        return {"type": "http.request", "body": body, "more_body": False}

    try:
        form = await StarletteRequest(request.scope, receive).form(max_files=2, max_fields=0)
    except MultiPartException:
        raise SonolusError(400) from None
    files = {
        upload.filename: upload
        for upload in form.getlist("files")
        if isinstance(upload, UploadFile) and upload.filename
    }
    data_file = files.get(key.data_hash)
    config_file = files.get(key.configuration_hash)
    if data_file is None or config_file is None:
        raise SonolusError(400)
    replay_data = await _read_file(data_file, limits.max_data_size)
    replay_config = await _read_file(config_file, limits.max_config_size)
    if (
        hashlib.sha1(replay_data).hexdigest() != key.data_hash
        or hashlib.sha1(replay_config).hexdigest() != key.configuration_hash
    ):
        raise SonolusError(400)
    speed = validate_replay_config(
        context.engine_rules,
        replay_config,
        key.engine_name,
        limits.max_config_decompressed_size,
        loc,
    )
    await backend(
        context.backend.submit_replay(
            session,
            chart,
            key.display_name,
            key.engine_name,
            replay_data,
            replay_config,
            speed,
        ),
        Site.REPLAY_UPLOAD,
        loc,
    )


@router.post("/sonolus/levels/result/upload")
async def result_upload(
    request: Request,
    context: Context,
    state: State,
    upload_key: str = Header(alias="Sonolus-Upload-Key"),
) -> Response:
    """Validate an uploaded replay and save it as the player's record.

    Args:
        request: Current request.
        context: App context.
        state: Player configuration.
        upload_key: Key from the result submit.

    Returns:
        Response: An empty object.
    """
    key = verify_upload_key(context.config.keys.upload_key_secret, upload_key)
    session = state.session or await load_upload_session(context.redis, key.nonce)
    if not session:
        raise SonolusError(401, state.loc.not_logged_in)
    try:
        me = await backend(context.backend.me(session), Site.REPLAY_UPLOAD, state.loc)
    except SonolusError as error:
        if error.status_code < 500:
            await drop_upload_session(context.redis, key.nonce)
        raise
    if me.account.id != key.user_id:
        raise SonolusError(401, INVALID_UPLOAD_KEY)
    try:
        await _save_replay(request, context, state, key, session)
    except SonolusError as error:
        if error.status_code < 500:
            await drop_upload_session(context.redis, key.nonce)
        raise
    await drop_upload_session(context.redis, key.nonce)
    return respond(ServerUploadLevelResultResponse())
