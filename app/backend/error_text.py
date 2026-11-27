from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum

from app.backend.client import BackendError
from app.errors import SonolusError, reason_phrase
from app.localization import Loc

BACKEND_DETAILS: dict[str, tuple[int, str]] = {
    "error.auth.required": (401, "Not logged in."),
    "error.auth.invalid_token": (401, "Not logged in."),
    "error.auth.wrong_session_type": (403, "Invalid token type."),
    "error.account.banned": (403, "User banned."),
    "error.account.not_found": (404, "Not Found"),
    "error.chart.invalid_id": (400, "Invalid chart ID."),
    "error.chart.not_found": (404, "Chart not found."),
    "error.chart.not_deleted": (404, "Chart not found or not pending deletion."),
    "error.chart.rating_out_of_range": (400, "Length limits exceeded"),
    "error.chart.rating_precision": (400, "More than 4 decimal places are not allowed"),
    "error.comment.not_found": (404, "Chart or comment not found."),
    "error.record.not_found": (404, "Not Found"),
    "error.notification.not_found": (400, "Failed to get."),
    "error.staff.permission_required": (403, "Forbidden"),
    "error.staff.target_outranks": (403, "You can't moderate an admin."),
    "error.staff.self_target": (400, "You can't moderate yourself."),
    "error.text.too_long": (400, "Length limits exceeded"),
    "error.file.too_large": (413, "Uploaded files exceed file size limit."),
}

UNSURE = "We're not sure what went wrong!"

AUTHENTICATE_TEXTS: dict[str, tuple[int, str]] = {
    "error.sonolus.signature_missing": (400, "Missing Sonolus-Signature header"),
    "error.sonolus.signature_invalid": (400, "Invalid signature"),
    "error.sonolus.wrong_type": (400, "Bad Request"),
    "error.sonolus.wrong_server": (418, "Are you connecting to the right server?"),
    "error.sonolus.time_invalid": (400, "Invalid time. Please click 'Cancel' and try again."),
}

AUTHENTICATE_EXTERNAL_TEXTS: dict[str, tuple[int, str]] = {
    **AUTHENTICATE_TEXTS,
    "error.sonolus.wrong_server": (418, "Are you using the right website?"),
}


class Site(StrEnum):
    """Backend call sites whose errors players see differently.

    Attributes:
        DETAIL: Shows the old backend detail, used where the old server forwarded or crashed.
        BARE: Shows only the status reason phrase.
        LIKE: Liking or unliking a level.
        CHART_DELETE: Deleting a level.
        CHART_RESTORE: Restoring a deleted level.
        VISIBILITY: Changing a level's visibility.
        RERATE: Rerating a level.
        STAFF_PICK: Adding or removing a staff pick.
        COMMENT_POST: Posting a comment.
        COMMENT_DELETE: Deleting a comment.
        NOTIFICATION_OPEN: Opening a notification.
        ACCOUNT_MODERATION: Banning or unbanning an account.
        REPLAY_UPLOAD: Uploading a replay.
        RECORD_DELETE: Deleting a leaderboard record.
    """

    DETAIL = "detail"
    BARE = "bare"
    LIKE = "like"
    CHART_DELETE = "chart_delete"
    CHART_RESTORE = "chart_restore"
    VISIBILITY = "visibility"
    RERATE = "rerate"
    STAFF_PICK = "staff_pick"
    COMMENT_POST = "comment_post"
    COMMENT_DELETE = "comment_delete"
    NOTIFICATION_OPEN = "notification_open"
    ACCOUNT_MODERATION = "account_moderation"
    REPLAY_UPLOAD = "replay_upload"
    RECORD_DELETE = "record_delete"


@dataclass(frozen=True)
class SiteRule:
    """How one call site turns backend errors into player messages.

    Attributes:
        text: Locale text replacing the message, None to keep the backend detail.
        reason_phrase: Show only the status reason phrase.
        statuses: Old statuses per backend code where they differ at this site.
    """

    text: Callable[[Loc], str] | None = None
    reason_phrase: bool = False
    statuses: Mapping[str, int] = field(default_factory=dict)


NOT_OWNED = {"error.staff.permission_required": 404}

RULES: dict[Site, SiteRule] = {
    Site.DETAIL: SiteRule(),
    Site.BARE: SiteRule(reason_phrase=True),
    Site.LIKE: SiteRule(text=lambda loc: loc.unknown_error),
    Site.CHART_DELETE: SiteRule(text=lambda loc: loc.not_admin_or_owner, statuses=NOT_OWNED),
    Site.CHART_RESTORE: SiteRule(text=lambda loc: loc.not_mod),
    Site.VISIBILITY: SiteRule(text=lambda loc: loc.not_mod_or_owner, statuses=NOT_OWNED),
    Site.RERATE: SiteRule(text=lambda loc: loc.not_mod_or_owner),
    Site.STAFF_PICK: SiteRule(text=lambda loc: loc.not_mod),
    Site.COMMENT_POST: SiteRule(text=lambda loc: loc.unknown_error),
    Site.COMMENT_DELETE: SiteRule(text=lambda loc: loc.unknown_error, statuses=NOT_OWNED),
    Site.NOTIFICATION_OPEN: SiteRule(text=lambda loc: loc.not_found),
    Site.ACCOUNT_MODERATION: SiteRule(text=lambda loc: loc.not_admin),
    Site.REPLAY_UPLOAD: SiteRule(text=lambda loc: loc.unknown_error),
    Site.RECORD_DELETE: SiteRule(text=lambda loc: loc.unknown_error),
}


def to_sonolus_error(error: BackendError, site: Site, loc: Loc) -> SonolusError:
    """Translate a backend error into what players saw from the old server at a call site.

    Args:
        error: The backend error.
        site: Where the call was made.
        loc: Player locale.

    Returns:
        SonolusError: The error to raise.
    """
    rule = RULES[site]
    status, detail = BACKEND_DETAILS.get(error.code, (error.status, reason_phrase(error.status)))
    status = rule.statuses.get(error.code, status)
    if rule.reason_phrase:
        return SonolusError(status)
    if rule.text is not None:
        return SonolusError(status, rule.text(loc))
    return SonolusError(status, detail)


def authenticate_error(error: BackendError) -> SonolusError:
    """Translate a failed in-game login.

    Args:
        error: The backend error.

    Returns:
        SonolusError: The error to raise.
    """
    status, text = AUTHENTICATE_TEXTS.get(error.code, (400, UNSURE))
    return SonolusError(status, text)


def authenticate_external_error(error: BackendError) -> SonolusError:
    """Translate a failed website login approval.

    Args:
        error: The backend error.

    Returns:
        SonolusError: The error to raise.
    """
    status, text = AUTHENTICATE_EXTERNAL_TEXTS.get(error.code, (error.status, UNSURE))
    return SonolusError(status, text)


def invalid_chart_id() -> BackendError:
    """Build the error the backend gives for a malformed chart id.

    Returns:
        BackendError: The error, raised locally before any backend call.
    """
    return BackendError(400, "error.chart.invalid_id")
