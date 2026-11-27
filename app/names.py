import re
from dataclasses import dataclass

CHART_ID_PATTERN = re.compile(r"[A-Za-z0-9]{32}")
ROW_ID_PATTERN = re.compile(r"[0-9]{1,10}")
MAX_ROW_ID = 2147483647
VIEW_CODE_PATTERN = re.compile(r"[0-9a-z]{4,16}")
ACCOUNT_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,128}")


@dataclass(frozen=True)
class PromotedName:
    """A promoted level name ``<prefix><chart id>-<view code>``.

    Attributes:
        chart_id: Promoted chart id.
        view_code: View code to report the click with.
    """

    chart_id: str
    view_code: str


@dataclass(frozen=True)
class RecordName:
    """A leaderboard record or replay name ``<prefix><chart id>-<record id>``.

    Attributes:
        chart_id: Chart id.
        record_id: Record id.
    """

    chart_id: str
    record_id: int


def row_id(text: str) -> int | None:
    """Parse a database row id, rejecting values the backend's integer columns can't hold.

    Args:
        text: Digits from a name or path.

    Returns:
        int | None: The id, or None when it is malformed or out of range.
    """
    if not ROW_ID_PATTERN.fullmatch(text):
        return None
    value = int(text)
    return value if 0 < value <= MAX_ROW_ID else None


def chart_id(name: str, prefix: str) -> str | None:
    """Extract the chart id from a level name.

    Args:
        name: Item name like ``UnCh-<32 alphanumerics>``.
        prefix: Chart prefix.

    Returns:
        str | None: The chart id, or None when the name is malformed.
    """
    if not name.startswith(prefix):
        return None
    rest = name[len(prefix) :]
    return rest if CHART_ID_PATTERN.fullmatch(rest) else None


def promoted_name(name: str, prefix: str) -> PromotedName | None:
    """Recognize a promoted level name.

    Args:
        name: Item name.
        prefix: Chart prefix.

    Returns:
        PromotedName | None: The parts, or None for any other name.
    """
    if not name.startswith(prefix):
        return None
    rest = name[len(prefix) :]
    if "-" not in rest:
        return None
    chart, code = rest.split("-", 1)
    if CHART_ID_PATTERN.fullmatch(chart) and VIEW_CODE_PATTERN.fullmatch(code):
        return PromotedName(chart, code)
    return None


def record_name(name: str, prefix: str) -> RecordName | None:
    """Parse a record or replay name.

    Args:
        name: Item name like ``UnCh-<chart id>-<record id>``.
        prefix: Chart prefix.

    Returns:
        RecordName | None: The parts, or None when the name is malformed.
    """
    if not name.startswith(prefix):
        return None
    chart, separator, record = name[len(prefix) :].partition("-")
    parsed = row_id(record) if separator else None
    if parsed is not None and CHART_ID_PATTERN.fullmatch(chart):
        return RecordName(chart, parsed)
    return None
