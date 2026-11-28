from datetime import datetime
from decimal import Decimal
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

ItemT = TypeVar("ItemT")

MOD_PERMISSIONS = frozenset(
    {
        "chart.visibility",
        "chart.delete",
        "chart.restore",
        "chart.view_hidden",
        "chart.rerate",
        "chart.staff_pick",
        "comment.delete",
        "leaderboard.delete",
        "notification.send",
    }
)
ADMIN_PERMISSION = "account.ban"


class BackendModel(BaseModel):
    """Base for backend responses, ignoring fields this server doesn't read.

    Attributes:
        model_config: Ignores unknown fields.
    """

    model_config = ConfigDict(extra="ignore")


class FileRef(BackendModel):
    """A stored file.

    Attributes:
        hash: SHA-1 of the file.
        url: Public URL.
    """

    hash: str
    url: str


class SiteAssets(BackendModel):
    """Shared site images served from storage.

    Attributes:
        banner: Server banner.
    """

    banner: FileRef | None = None


class AccountSummary(BackendModel):
    """Short account reference.

    Attributes:
        id: Sonolus account id.
        handle: Sonolus handle.
        username: Sonolus display name.
    """

    id: str
    handle: int
    username: str


class TaggedAccount(AccountSummary):
    """Account reference with the flags shown as tags.

    Attributes:
        banned: Whether the account is banned.
        permissions: Staff permissions the account holds.
    """

    banned: bool
    permissions: list[str]

    @property
    def is_admin(self) -> bool:
        """Whether the account had the old admin role.

        Returns:
            bool: True when it may ban accounts.
        """
        return ADMIN_PERMISSION in self.permissions

    @property
    def is_mod(self) -> bool:
        """Whether the account had the old moderator role.

        Returns:
            bool: True when it holds any moderation permission.
        """
        return self.is_admin or not MOD_PERMISSIONS.isdisjoint(self.permissions)


class PublicAccount(TaggedAccount):
    """Public profile data, read for its identity and tag flags.

    Attributes:
        banned: Whether the account is banned.
        permissions: Staff permissions the account holds.
    """


class ChartFiles(BackendModel):
    """A chart's files.

    Attributes:
        jacket: Jacket image.
        music: Audio.
        chart: Gzipped level data.
        preview: Preview audio.
        background: Uploaded background.
        background_v1: Generated v1 background.
        background_v3: Generated v3 background.
    """

    jacket: FileRef
    music: FileRef
    chart: FileRef
    preview: FileRef | None = None
    background: FileRef | None = None
    background_v1: FileRef
    background_v3: FileRef


class Chart(BackendModel):
    """A chart.

    Attributes:
        id: Chart id.
        title: Title.
        artists: Artists.
        description: Description.
        tags: Tags.
        rating: Difficulty rating.
        status: Visibility.
        staff_pick: Whether staff picked it.
        owner: Owning account.
        charter: Free-text charter name.
        like_count: Likes.
        comment_count: Comments.
        liked: Whether the viewer liked it.
        files: Stored files.
        created_at: Upload time.
        published_at: First publish time.
        deleted_at: Soft-deletion time, shown to staff and the owner.
    """

    id: str
    title: str
    artists: str | None = None
    description: str | None = None
    tags: list[str]
    rating: Decimal
    status: str
    staff_pick: bool
    owner: AccountSummary
    charter: str
    like_count: int
    comment_count: int
    liked: bool | None = None
    files: ChartFiles
    created_at: datetime | None = None
    published_at: datetime | None = None
    deleted_at: datetime | None = None


class ChartViewer(BackendModel):
    """What the viewer may do with a chart.

    Attributes:
        is_owner: Whether the viewer owns the chart.
        chart_permissions: Collaborator permissions on the chart.
        staff_permissions: Staff permissions usable on the chart.
    """

    is_owner: bool
    chart_permissions: list[str]
    staff_permissions: list[str]

    def staff(self, permission: str) -> bool:
        """Check a staff permission.

        Args:
            permission: Permission name.

        Returns:
            bool: Whether the viewer may use it on this chart.
        """
        return permission in self.staff_permissions

    @property
    def manages_visibility(self) -> bool:
        """Whether the viewer changes visibility as the owner rather than as staff.

        Returns:
            bool: True for the owner and collaborators with the visibility permission.
        """
        return self.is_owner or "visibility" in self.chart_permissions


class ChartDetails(Chart):
    """A chart with the viewer's permissions.

    Attributes:
        viewer: The viewer's permissions.
    """

    viewer: ChartViewer


class Page(BackendModel, Generic[ItemT]):
    """One page of a listing.

    Attributes:
        items: Items on the page.
        page: Zero-based page number.
        page_count: Total number of pages.
    """

    items: list[ItemT]
    page: int
    page_count: int


class Comment(BackendModel):
    """A comment.

    Attributes:
        id: Comment id.
        author: Commenting account.
        content: Text, None when deleted and the viewer can't moderate.
        deleted: Whether the comment was deleted.
        is_own: Whether the viewer wrote it.
        created_at: Posting time.
    """

    id: int
    author: TaggedAccount | None = None
    content: str | None = None
    deleted: bool
    is_own: bool
    created_at: datetime


class CommentPage(Page[Comment]):
    """A page of comments.

    Attributes:
        can_moderate: Whether the viewer may delete any comment.
    """

    can_moderate: bool


class ReplayFiles(BackendModel):
    """A record's replay files.

    Attributes:
        data: Gzipped replay data.
        configuration: Gzipped replay configuration.
    """

    data: FileRef
    configuration: FileRef


class LeaderboardRecord(BackendModel):
    """A leaderboard record.

    Attributes:
        id: Record id.
        chart_id: Chart id.
        submitter: Submitting account.
        display_name: Name shown on the leaderboard.
        engine: Engine name.
        grade: Result grade.
        perfect: Perfect judgments.
        great: Great judgments.
        good: Good judgments.
        miss: Misses.
        arcade_score: Arcade score.
        accuracy_score: Accuracy score.
        speed: Playback speed, None for 1.0.
        replay: Replay files.
        is_own: Whether the viewer submitted it.
        created_at: Submission time.
    """

    id: int
    chart_id: str
    submitter: TaggedAccount | None = None
    display_name: str
    engine: str
    grade: str
    perfect: int
    great: int
    good: int
    miss: int
    arcade_score: int
    accuracy_score: int
    speed: float | None = None
    replay: ReplayFiles
    is_own: bool
    created_at: datetime


class LeaderboardPage(Page[LeaderboardRecord]):
    """A page of a chart's leaderboard.

    Attributes:
        can_moderate: Whether the viewer may delete any record.
    """

    can_moderate: bool


class RecordDetails(BackendModel):
    """A record with its chart.

    Attributes:
        record: The record.
        chart: The chart.
        can_delete: Whether the viewer may delete it.
    """

    record: LeaderboardRecord
    chart: Chart
    can_delete: bool


class GlobalRecord(BackendModel):
    """A record in a global listing.

    Attributes:
        record: The record.
        chart: The chart.
    """

    record: LeaderboardRecord
    chart: Chart


class Notification(BackendModel):
    """A notification.

    Attributes:
        id: Notification id.
        title: Title.
        content: Body text, absent in listings.
        is_read: Whether it was read.
        created_at: Sending time.
    """

    id: int
    title: str
    content: str | None = None
    is_read: bool
    created_at: datetime


class NotificationPage(Page[Notification]):
    """A page of notifications.

    Attributes:
        unread_count: Unread notifications in total.
    """

    unread_count: int


class Me(BackendModel):
    """The logged-in account.

    Attributes:
        account: Public profile.
        unread_notifications: Unread notifications.
    """

    account: PublicAccount
    unread_notifications: int


class Profile(BackendModel):
    """A public profile with its most liked charts.

    Attributes:
        account: Public profile.
        charts: Most liked public charts.
    """

    account: PublicAccount
    charts: list[Chart]


class NewSession(BackendModel):
    """A freshly created session.

    Attributes:
        session: Bearer token.
        expires_at: Expiry time.
    """

    session: str
    expires_at: datetime


class ServedPromotion(BackendModel):
    """A promotion picked for the viewer.

    Attributes:
        chart: The promoted chart.
        view_code: Code to send when the viewer opens it.
    """

    chart: Chart
    view_code: str


class PromotionServe(BackendModel):
    """Result of asking for a promotion.

    Attributes:
        promotion: The promotion, or None when none is shown.
    """

    promotion: ServedPromotion | None = None


class ReplaySaved(BackendModel):
    """Outcome of a replay submission.

    Attributes:
        status: ``ok`` or ``unchanged``.
    """

    status: str
