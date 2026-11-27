import base64
import binascii
from typing import Any
from urllib.parse import parse_qs, urlencode

from app.errors import SonolusError

FIELDS = (
    "sort_by",
    "page",
    "staff_pick",
    "is_default_staff_pick",
    "min_rating",
    "max_rating",
    "tags",
    "min_likes",
    "max_likes",
    "min_comments",
    "max_comments",
    "liked_by",
    "commented_on",
    "title_includes",
    "description_includes",
    "author_includes",
    "artists_includes",
    "sort_order",
    "level_status",
    "keywords",
)
SORT_BY_VALUES = ["created_at", "rating", "likes", "comments", "decaying_likes", "abc", "random"]
SORT_ORDER_VALUES = ["desc", "asc"]
LEVEL_STATUSES = ["ALL", "PUBLIC_MINE", "UNLISTED", "PRIVATE"]
STAFF_PICKS = {"off": None, "default": None, "true": True, "false": False}
TEXT_FIELDS = (
    "title_includes",
    "description_includes",
    "author_includes",
    "artists_includes",
    "keywords",
)

Filter = dict[str, Any]


def _bad_request(detail: str) -> SonolusError:
    """Build a 400 filter error.

    Args:
        detail: Message.

    Returns:
        SonolusError: The error.
    """
    return SonolusError(400, detail)


def _int(value: str) -> int | None:
    """Parse an integer the way ``int`` does, signs and spaces allowed.

    Args:
        value: Text.

    Returns:
        int | None: The integer, or None when it isn't one.
    """
    try:
        return int(value)
    except ValueError:
        return None


def _count(values: dict[str, str], name: str) -> int | None:
    """Parse a non-negative count filter.

    Args:
        values: Raw values.
        name: Field name.

    Returns:
        int | None: The count, or None when absent.
    """
    raw = values.get(name)
    if raw is None:
        return None
    number = _int(raw) if raw.isdigit() else None
    if number is None or number < 0:
        raise _bad_request(f"{name} must be a non-negative integer.")
    return number


def _flag(values: dict[str, str], name: str) -> bool | None:
    """Parse a ``0``/``1`` flag filter.

    Args:
        values: Raw values.
        name: Field name.

    Returns:
        bool | None: The flag, or None when absent.
    """
    raw = values.get(name)
    if raw is None:
        return None
    if not raw.isdigit():
        raise _bad_request(f"{name} must be a boolean.")
    return raw != "0"


def _flatten(encoded: str, plain: bool) -> dict[str, str]:
    """Decode filter values into a flat mapping keeping the first value per key.

    Args:
        encoded: Base64url query string, or a plain query string.
        plain: Whether the values are a plain query string.

    Returns:
        dict[str, str]: The values.
    """
    if plain:
        return {key: items[0] for key, items in parse_qs(encoded).items()}
    try:
        raw = base64.urlsafe_b64decode(encoded.encode())
        return {key.decode(): items[0].decode() for key, items in parse_qs(raw).items()}
    except (binascii.Error, ValueError):
        raise SonolusError(400) from None


def parse_filter(encoded: str, plain: bool = False) -> Filter:
    """Validate the filters of the uploaded charts playlist.

    Args:
        encoded: Base64url query string from the playlist name, or the submitted form values.
        plain: Whether the values are a plain query string.

    Returns:
        Filter: Parsed filters keyed by field, absent ones None.
    """
    values = _flatten(encoded, plain)
    sort_by = values.get("sort_by")
    if sort_by is not None and sort_by not in SORT_BY_VALUES:
        raise _bad_request(
            f"Invalid value for sort_by. Allowed values are: {', '.join(SORT_BY_VALUES)}."
        )
    page: int | None = 1 if sort_by == "random" else None
    raw_page = values.get("page")
    if sort_by != "random" and raw_page is not None:
        page = _int(raw_page) if raw_page.isdigit() else None
        if page is None or page < 1:
            raise _bad_request("page must be a non-negative integer.")
    raw_staff_pick = values.get("staff_pick")
    is_default_staff_pick = raw_staff_pick and raw_staff_pick == "default"
    if raw_staff_pick is not None and raw_staff_pick not in STAFF_PICKS:
        raise _bad_request("Invalid staff_pick.")
    staff_pick = STAFF_PICKS[raw_staff_pick] if raw_staff_pick is not None else None
    ratings: dict[str, int | None] = {}
    for name in ("min_rating", "max_rating"):
        raw = values.get(name)
        number = _int(raw) if raw is not None else None
        if raw is not None and number is None:
            raise _bad_request(f"{name} must be an integer.")
        ratings[name] = number
    min_rating, max_rating = ratings["min_rating"], ratings["max_rating"]
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise _bad_request("min_rating cannot be greater than max_rating.")
    raw_tags = values.get("tags")
    tags = [tag.strip() for tag in raw_tags.split(",")] if raw_tags is not None else None
    min_likes, max_likes = _count(values, "min_likes"), _count(values, "max_likes")
    if min_likes is not None and max_likes is not None and min_likes > max_likes:
        raise _bad_request("min_likes cannot be greater than max_likes.")
    min_comments, max_comments = _count(values, "min_comments"), _count(values, "max_comments")
    if min_comments is not None and max_comments is not None and min_comments > max_comments:
        raise _bad_request("min_comments cannot be greater than max_comments.")
    liked_by = _flag(values, "liked_by")
    commented_on = _flag(values, "commented_on")
    sort_order = values.get("sort_order")
    if sort_order is not None and sort_order not in SORT_ORDER_VALUES:
        raise _bad_request(
            f"Invalid value for sort_order. Allowed values are: {', '.join(SORT_ORDER_VALUES)}."
        )
    level_status = values.get("level_status")
    if level_status is not None and level_status not in LEVEL_STATUSES:
        raise _bad_request("Invalid level_status.")
    parsed: Filter = {
        "sort_by": sort_by,
        "page": page,
        "staff_pick": staff_pick,
        "is_default_staff_pick": is_default_staff_pick,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "tags": tags,
        "min_likes": min_likes,
        "max_likes": max_likes,
        "min_comments": min_comments,
        "max_comments": max_comments,
        "liked_by": liked_by,
        "commented_on": commented_on,
        "sort_order": sort_order,
        "level_status": level_status,
    }
    for name in TEXT_FIELDS:
        parsed[name] = values.get(name)
    return {name: parsed[name] for name in FIELDS}


def dump_filter(values: Filter) -> dict[str, Any]:
    """Serialize filters for re-encoding, dropping absent ones and keeping a chosen default.

    Args:
        values: Filters, possibly holding already serialized values.

    Returns:
        dict[str, Any]: Values in field order.
    """
    values = dict(values)
    if values.get("staff_pick") is None and values.get("is_default_staff_pick") is True:
        values["staff_pick"] = "default"
    data = {name: values[name] for name in FIELDS if values.get(name) is not None}
    if data.get("sort_by") == "random":
        data.pop("page", None)
    if "staff_pick" in data and data["staff_pick"] in (True, False):
        data["staff_pick"] = "true" if data["staff_pick"] else "false"
    if isinstance(data.get("tags"), list):
        data["tags"] = ",".join(data["tags"])
    for name in ("liked_by", "commented_on"):
        if name in data:
            data[name] = str(int(data[name]))
    return data


def merge_filter(previous: str, submitted: str, max_length: int) -> str:
    """Apply submitted filters on top of a playlist's current ones.

    Args:
        previous: Base64url filters from the playlist name.
        submitted: Submitted form values.
        max_length: Longest submitted form values accepted.

    Returns:
        str: Base64url filters for the new playlist name.
    """
    merged = parse_filter(previous)
    if len(submitted) > max_length:
        raise _bad_request("why so long")
    merged.update(dump_filter(parse_filter(submitted, plain=True)))
    encoded = urlencode(dump_filter(merged))
    return base64.urlsafe_b64encode(encoded.encode()).decode()
