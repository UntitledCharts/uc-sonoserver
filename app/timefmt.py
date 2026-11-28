from datetime import datetime, timedelta, timezone


def time_ago(moment: datetime | None) -> str:
    """Describe how long ago a moment was with its largest unit.

    Args:
        moment: An aware time, None counts as now.

    Returns:
        str: Text like ``3d``, ``5h``, ``12m``, ``40s`` or ``0s`` for the future.
    """
    if moment is None:
        return "0s"
    delta = datetime.now(timezone.utc) - moment
    if delta >= timedelta(days=1):
        return f"{delta.days}d"
    if delta >= timedelta(hours=1):
        return f"{delta.seconds // 3600}h"
    if delta >= timedelta(minutes=1):
        return f"{delta.seconds // 60}m"
    if delta >= timedelta(seconds=1):
        return f"{delta.seconds}s"
    return "0s"


def epoch_ms(moment: datetime) -> int:
    """Convert a time to epoch milliseconds.

    Args:
        moment: An aware time.

    Returns:
        int: Milliseconds since the epoch.
    """
    return int(moment.timestamp() * 1000)
