import base64
import binascii
import gzip
import hashlib
import hmac
import json
import os
import secrets
import time
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis

from app.errors import SonolusError
from app.localization import Loc
from app.sonolus_core import ReplayConfiguration

SPEED_OPTION = "#SPEED"
UPLOAD_SESSION_PREFIX = "upload:session:"

Validator = Callable[[int | float], bool]


class UploadKeyData(BaseModel):
    """Payload of a signed replay upload key.

    Attributes:
        user_id: Submitting account id.
        expires_at: Epoch seconds after which the key is rejected.
        chart_name: Level name the replay was played on.
        data_hash: SHA-1 of the replay data.
        configuration_hash: SHA-1 of the replay configuration.
        engine_name: Server engine the replay was played on.
        display_name: Name shown on the leaderboard.
        nonce: Random id of this key, naming the stored session of the submitting player.
    """

    user_id: str
    expires_at: int
    chart_name: str
    data_hash: str
    configuration_hash: str
    engine_name: str
    display_name: str
    nonce: str = ""


@dataclass(frozen=True)
class EngineOption:
    """One option of a rankable engine.

    Attributes:
        name: Option name.
        validator: Checks a submitted value.
    """

    name: str
    validator: Validator


def make_validator(option: dict[str, Any], engine_data: dict[str, Any]) -> Validator:
    """Build the check for one engine option.

    Args:
        option: Option from the engine configuration, overrides applied.
        engine_data: The engine's engine.json.

    Returns:
        Validator: The check.
    """
    name = option["name"]
    if (
        name in engine_data.get("unrankable_options", []) or option["standard"]
    ) and name not in engine_data.get("standard_rankable_options", []):
        default = option["def"]
        return lambda value: value == default
    match option["type"]:
        case "slider":
            low, high = option["min"], option["max"]
            return lambda value: low <= value <= high
        case "toggle":
            return lambda value: value in (0, 1)
        case "select":
            last = len(option["values"]) - 1
            return lambda value: 0 <= value <= last
        case other:
            raise ValueError(f"invalid option type: {other}")


def load_engine_rules(root: Path) -> dict[str, list[EngineOption]]:
    """Build the option checks of every rankable engine in ``files/engines``.

    Args:
        root: Repository root containing ``files/``.

    Returns:
        dict[str, list[EngineOption]]: Options in configuration order, keyed by engine name.
    """
    rules: dict[str, list[EngineOption]] = {}
    base = root / "files" / "engines"
    for name in os.listdir(base):
        folder = base / name
        if not folder.is_dir():
            continue
        with (folder / "engine.json").open("r", encoding="utf8") as handle:
            engine_data: dict[str, Any] = json.load(handle)
        if not engine_data.get("can_be_ranked", False):
            continue
        overrides = engine_data.get("config_overrides", {})
        with gzip.open(folder / "EngineConfiguration", "rb") as handle:
            configuration: dict[str, Any] = json.load(handle)
        options: list[EngineOption] = []
        for option in configuration["options"]:
            if option["name"] in overrides:
                option.update(overrides[option["name"]])
            options.append(EngineOption(option["name"], make_validator(option, engine_data)))
        rules[name] = options
    return rules


def _signature(secret: str, encoded: bytes) -> str:
    """Sign an encoded upload key payload.

    Args:
        secret: HMAC key.
        encoded: Base64 payload.

    Returns:
        str: Hex HMAC-SHA256.
    """
    return hmac.new(secret.encode(), encoded, hashlib.sha256).hexdigest()


def generate_upload_key(secret: str, lifetime: int, data: UploadKeyData) -> tuple[str, str]:
    """Sign an upload key with a fresh random id.

    Args:
        secret: HMAC key.
        lifetime: Seconds the key stays valid.
        data: Payload, its expiry and random id replaced.

    Returns:
        tuple[str, str]: The key ``<base64 payload>.<hex signature>`` and its random id.
    """
    nonce = secrets.token_urlsafe(16)
    payload = data.model_copy(update={"expires_at": int(time.time() + lifetime), "nonce": nonce})
    encoded = base64.urlsafe_b64encode(payload.model_dump_json().encode())
    return f"{encoded.decode()}.{_signature(secret, encoded)}", nonce


def verify_upload_key(secret: str, upload_key: str) -> UploadKeyData:
    """Check an upload key's signature and expiry.

    Args:
        secret: HMAC key.
        upload_key: Key from the Sonolus-Upload-Key header.

    Returns:
        UploadKeyData: The payload.
    """
    encoded, separator, signature = upload_key.rpartition(".")
    if not separator or not hmac.compare_digest(
        _signature(secret, encoded.encode()).encode(), signature.encode()
    ):
        raise SonolusError(401, "Invalid upload token.")
    try:
        data = UploadKeyData.model_validate_json(base64.urlsafe_b64decode(encoded.encode()))
    except (binascii.Error, ValueError, ValidationError):
        raise SonolusError(401, "Invalid upload token.") from None
    if data.expires_at < time.time():
        raise SonolusError(401, "Expired upload token.")
    if not data.nonce:
        raise SonolusError(401, "Invalid upload token.")
    return data


async def store_upload_session(redis: Redis, nonce: str, session: str, lifetime: int) -> None:
    """Keep the submitting player's session until their replay is uploaded.

    Args:
        redis: Redis client.
        nonce: Random id of the upload key.
        session: Player session.
        lifetime: Seconds to keep it, the upload key lifetime.
    """
    await redis.set(UPLOAD_SESSION_PREFIX + nonce, session, ex=lifetime)


async def load_upload_session(redis: Redis, nonce: str) -> str | None:
    """Read the session stored for an upload key.

    Args:
        redis: Redis client.
        nonce: Random id of the upload key.

    Returns:
        str | None: The session, or None when absent or expired.
    """
    value = await redis.get(UPLOAD_SESSION_PREFIX + nonce)
    return value.decode() if value else None


async def drop_upload_session(redis: Redis, nonce: str) -> None:
    """Forget the session stored for an upload key.

    Args:
        redis: Redis client.
        nonce: Random id of the upload key.
    """
    await redis.delete(UPLOAD_SESSION_PREFIX + nonce)


def inflate_limited(data: bytes, limit: int) -> bytes | None:
    """Gunzip bytes, refusing output larger than a limit.

    Args:
        data: Gzip stream.
        limit: Largest output accepted.

    Returns:
        bytes | None: The output, or None when it is invalid or too large.
    """
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        output = inflater.decompress(data, limit + 1)
    except zlib.error:
        return None
    if len(output) > limit or inflater.unconsumed_tail or not inflater.eof:
        return None
    return output


def validate_replay_config(
    rules: dict[str, list[EngineOption]],
    compressed: bytes,
    engine_name: str,
    decompressed_limit: int,
    loc: Loc,
) -> float:
    """Check a replay configuration against a rankable engine and read its speed.

    Args:
        rules: Rankable engines' options.
        compressed: Gzipped replay configuration.
        engine_name: Engine the replay was played on.
        decompressed_limit: Largest decompressed configuration accepted.
        loc: Player locale.

    Returns:
        float: Playback speed, 1.0 when the configuration has none.
    """
    options = rules.get(engine_name)
    if not options:
        raise SonolusError(406, loc.leaderboards.BAD_ENGINE(engine_name))
    raw = inflate_limited(compressed, decompressed_limit)
    if raw is None:
        raise SonolusError(400)
    try:
        configuration = ReplayConfiguration.model_validate_json(raw)
    except ValidationError:
        raise SonolusError(400) from None
    names = configuration.optionNames
    values = configuration.options
    if names is not None and len(names) != len(values):
        raise SonolusError(400)
    if len(values) != len(options):
        raise SonolusError(400)
    speed = 1.0
    for index, value in enumerate(values):
        option = options[index]
        name = names[index] if names is not None else option.name
        if name != option.name:
            raise SonolusError(400, f"invalid config option {name} for engine {engine_name}")
        if not option.validator(value):
            raise SonolusError(400, f"invalid value for {name}: {value}")
        if name == SPEED_OPTION:
            speed = float(value)
    return speed
