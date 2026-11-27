from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, TypeVar

from app.backend.models import (
    Chart,
    Comment,
    FileRef,
    LeaderboardRecord,
    Notification,
    TaggedAccount,
)
from app.context import AppContext
from app.errors import SonolusError
from app.resources import CompiledSkin
from app.sonolus_core import (
    BackgroundItem,
    EngineItem,
    LevelItem,
    ParticleItem,
    PostItem,
    ReplayItem,
    ServerForm,
    ServerItemCommunityComment,
    ServerItemLeaderboardRecord,
    SkinItem,
    SonolusModel,
    Srl,
    Tag,
    UseItemUseDefaultFalse,
    UseItemUseDefaultTrue,
    UserItem,
)
from app.state import ENGINE_DEFAULT, RequestState
from app.timefmt import epoch_ms, time_ago

ItemT = TypeVar("ItemT", bound=SonolusModel)
LevelContext = Literal["list", "level"]

GRADES = {"allPerfect": "AP", "fullCombo": "FC", "pass": "P", "fail": "X"}
NOTIFICATION_AUTHOR = "UntitledCharts"
DELETED_COMMENT = "[DELETED]"
DELETED_COMMENT_MOD_VIEW = "[DELETED]\nMod View:\n----------\n"


def srl(file: FileRef) -> Srl:
    """Turn a backend file into a resource locator.

    Args:
        file: Stored file.

    Returns:
        Srl: The locator.
    """
    return Srl(hash=file.hash, url=file.url)


def rating_number(rating: Decimal) -> int | float:
    """Render a rating as the JSON number the old server sent.

    Args:
        rating: Rating.

    Returns:
        int | float: An int when integral, otherwise a float.
    """
    return int(rating) if rating == rating.to_integral_value() else float(rating)


def rating_text(rating: Decimal) -> str:
    """Render a rating as text.

    Args:
        rating: Rating.

    Returns:
        str: Text like ``31`` or ``12.5``.
    """
    return str(rating_number(rating))


def delete_form() -> ServerForm:
    """Build the confirmation-only delete form.

    Returns:
        ServerForm: The form.
    """
    return ServerForm(
        type="delete", title="#DELETE", icon="delete", requireConfirmation=True, options=[]
    )


def account_tags(account: TaggedAccount) -> list[Tag]:
    """Build the staff and ban tags of an account.

    Args:
        account: Account with its tag flags.

    Returns:
        list[Tag]: The tags.
    """
    tags: list[Tag] = []
    if account.is_admin:
        tags.append(Tag(title="#ADMIN", icon="crown"))
    elif account.is_mod:
        tags.append(Tag(title="#MODERATOR", icon="crown"))
    if account.banned:
        tags.append(Tag(title="#BANNED", icon="lock"))
    return tags


def user_item(account: TaggedAccount) -> UserItem:
    """Build the user item of an account.

    Args:
        account: Account with its tag flags.

    Returns:
        UserItem: The user item.
    """
    return UserItem(
        name=account.id,
        title=account.username,
        handle=str(account.handle),
        tags=account_tags(account),
    )


def uwu_fields(item: ItemT, state: RequestState, fields: Iterable[str]) -> ItemT:
    """Owoify text fields of an item copy, the author without symbols.

    Args:
        item: Item to copy.
        state: Player configuration.
        fields: Field names among title, author and subtitle.

    Returns:
        ItemT: The changed copy.
    """
    update: dict[str, str] = {}
    for field in fields:
        value = getattr(item, field, None)
        if value:
            update[field] = state.owo(value, symbols=field != "author")
    return item.model_copy(update=update) if update else item.model_copy()


def uwu_items(items: list[ItemT], state: RequestState) -> list[ItemT]:
    """Owoify the title, author and subtitle of items.

    Args:
        items: Items to copy.
        state: Player configuration.

    Returns:
        list[ItemT]: The changed copies.
    """
    return [uwu_fields(item, state, ("title", "author", "subtitle")) for item in items]


def uwu_levels(items: list[LevelItem], state: RequestState) -> list[LevelItem]:
    """Owoify level authors; titles were owoified when the levels were built.

    Args:
        items: Levels to copy.
        state: Player configuration.

    Returns:
        list[LevelItem]: The changed copies.
    """
    return [uwu_fields(item, state, ("author",)) for item in items]


def uwu_replays(items: list[ReplayItem], state: RequestState) -> list[ReplayItem]:
    """Owoify replay subtitles and authors; titles come from already owoified levels.

    Args:
        items: Replays to copy.
        state: Player configuration.

    Returns:
        list[ReplayItem]: The changed copies.
    """
    return [uwu_fields(item, state, ("author", "subtitle")) for item in items]


@dataclass(frozen=True)
class LevelKit:
    """Compiled resources needed to turn charts into level items for one request.

    Attributes:
        state: Player configuration.
        source: Public server URL.
        prefix: Chart prefix.
        background: First compiled background, the base of every level background.
        no_scope: Scope-less background configuration used for uploaded backgrounds.
        engines: Engine items keyed by name.
        particle: Particle item from the configuration, None for the engine default.
        skins: Compiled skins.
    """

    state: RequestState
    source: str
    prefix: str
    background: BackgroundItem
    no_scope: Srl | None
    engines: dict[str, EngineItem]
    particle: ParticleItem | None
    skins: list[CompiledSkin]

    def engine(self, name: str) -> EngineItem:
        """Return an engine item or fail with 404.

        Args:
            name: Engine name.

        Returns:
            EngineItem: The engine.
        """
        engine = self.engines.get(name)
        if engine is None:
            raise SonolusError(404, self.state.loc.item_not_found("Engine", name))
        return engine

    def _skin(self, engine_name: str) -> SkinItem | None:
        """Pick the skin of the player's chosen theme for an engine, preferring their language.

        Args:
            engine_name: Engine the level uses.

        Returns:
            SkinItem | None: The skin, or None for the engine default.
        """
        candidates = [
            skin
            for skin in self.skins
            if skin.themes
            and self.state.skin in skin.themes
            and (not skin.engines or engine_name in skin.engines)
        ]
        if not candidates:
            return None
        for skin in candidates:
            if skin.locale == self.state.localization:
                return skin.item
        for skin in candidates:
            if skin.locale is None:
                return skin.item
        return candidates[0].item

    def _background(self, chart: Chart) -> BackgroundItem:
        """Build a level's background from the configured background choice.

        Args:
            chart: The chart.

        Returns:
            BackgroundItem: The background.
        """
        loc = self.state.loc
        kind = self.state.levelbg
        uploaded = kind.startswith("default_or_")
        file: FileRef | None = None
        if uploaded:
            kind = kind.removeprefix("default_or_")
            file = chart.files.background
        if not file:
            uploaded = False
            file = chart.files.background_v1 if kind == "v1" else chart.files.background_v3
        update: dict[str, object] = {
            "image": srl(file),
            "thumbnail": srl(chart.files.jacket),
            "name": "configured",
        }
        if not uploaded and kind == "v3":
            title = loc.background.V3
        elif not uploaded and kind == "v1":
            title = loc.background.V1
        else:
            title = loc.background.UPLOADED
            update["configuration"] = self.no_scope
        update["title"] = self.state.owo(title)
        return self.background.model_copy(update=update)

    def _tags(self, chart: Chart, context: LevelContext) -> list[Tag]:
        """Build a level's tags.

        Args:
            chart: The chart.
            context: ``list`` for listings, ``level`` for the details page.

        Returns:
            list[Tag]: The tags.
        """
        state = self.state
        loc = state.loc
        elapsed = time_ago(chart.published_at or chart.created_at)
        date = state.owo(
            loc.time_ago(elapsed) if chart.published_at else loc.time_ago_not_published(elapsed)
        )
        metadata = [
            Tag(title=date, icon="clock"),
            Tag(title=str(chart.like_count), icon="heart" if chart.liked else "heartHollow"),
            Tag(title=str(chart.comment_count), icon="comment"),
        ]
        if context == "list":
            tags = metadata + [Tag(title=state.owo(tag)) for tag in chart.tags]
        else:
            visibility = {
                "PUBLIC": Tag(title="#PUBLIC", icon="globe"),
                "PRIVATE": Tag(title="#PRIVATE", icon="lock"),
                "UNLISTED": Tag(title=loc.search.VISIBILITY_UNLISTED, icon="unlock"),
            }
            tags = (
                [visibility[chart.status]]
                + metadata
                + [Tag(title=state.owo(tag), icon="tag") for tag in chart.tags]
            )
        if chart.staff_pick:
            tags.insert(0, Tag(title=loc.staff_pick if context == "level" else None, icon="trophy"))
        return tags

    def level(
        self, chart: Chart, context: LevelContext = "list", use_engine: str | None = None
    ) -> LevelItem:
        """Turn a chart into a level item, owoifying its title, artists and tags.

        Args:
            chart: The chart.
            context: ``list`` for listings, ``level`` for the details page.
            use_engine: Engine to use instead of the configured one.

        Returns:
            LevelItem: The level.
        """
        state = self.state
        engine_name = use_engine or state.engine
        engine = self.engine(engine_name)
        skin = None if state.skin == ENGINE_DEFAULT else self._skin(engine_name)
        files = chart.files
        return LevelItem(
            name=f"{self.prefix}{chart.id}",
            source=self.source,
            version=1,
            rating=rating_number(chart.rating),
            title=state.owo(chart.title),
            artists=state.owo(chart.artists or ""),
            author=f"{chart.charter}#{chart.owner.handle}",
            authorUser=UserItem(
                name=chart.owner.id,
                title=chart.charter,
                handle=str(chart.owner.handle),
                tags=[],
            ),
            tags=self._tags(chart, context),
            engine=engine,
            useSkin=(
                UseItemUseDefaultTrue(useDefault=True)
                if skin is None
                else UseItemUseDefaultFalse[SkinItem](useDefault=False, item=skin)
            ),
            useBackground=UseItemUseDefaultFalse[BackgroundItem](
                useDefault=False, item=self._background(chart)
            ),
            useEffect=UseItemUseDefaultTrue(useDefault=True),
            useParticle=(
                UseItemUseDefaultTrue(useDefault=True)
                if self.particle is None
                else UseItemUseDefaultFalse[ParticleItem](useDefault=False, item=self.particle)
            ),
            cover=srl(files.jacket),
            bgm=srl(files.music),
            preview=srl(files.preview) if files.preview else srl(files.music),
            data=srl(files.chart),
        )


async def level_kit(context: AppContext, state: RequestState) -> LevelKit:
    """Collect the compiled resources needed to build level items.

    Args:
        context: App context.
        state: Player configuration.

    Returns:
        LevelKit: The resources.
    """
    resources = context.resources
    backgrounds = await resources.backgrounds(state.localization)
    engines = await resources.engines(state.localization)
    particle: ParticleItem | None = None
    if state.particle != ENGINE_DEFAULT:
        particle = next(
            item.item for item in await resources.particles() if item.item.name == state.particle
        )
    return LevelKit(
        state=state,
        source=context.config.server.public_url,
        prefix=context.config.sonolus.chart_prefix,
        background=backgrounds[0],
        no_scope=resources.background_no_scope,
        engines={engine.item.name: engine.item for engine in engines},
        particle=particle,
        skins=await resources.skins(),
    )


def comment_item(
    comment: Comment, state: RequestState, can_moderate: bool
) -> ServerItemCommunityComment:
    """Turn a backend comment into a community comment.

    Args:
        comment: The comment.
        state: Player configuration.
        can_moderate: Whether the viewer may delete any comment.

    Returns:
        ServerItemCommunityComment: The comment.
    """
    author = comment.author
    username = f"{author.username}#{author.handle}" if author else ""
    if comment.deleted:
        content = (
            DELETED_COMMENT
            if comment.content is None
            else DELETED_COMMENT_MOD_VIEW + comment.content
        )
    else:
        content = comment.content or ""
    return ServerItemCommunityComment(
        name=str(comment.id),
        author=state.owo(username, symbols=False),
        authorUser=user_item(author) if author else None,
        time=epoch_ms(comment.created_at),
        content=state.owo(content),
        actions=[delete_form()] if (comment.is_own or can_moderate) and not comment.deleted else [],
    )


def notification_post(notification: Notification, state: RequestState, source: str) -> PostItem:
    """Turn a notification into a post item.

    Args:
        notification: The notification.
        state: Player configuration.
        source: Public server URL.

    Returns:
        PostItem: The post.
    """
    loc = state.loc
    return PostItem(
        name=f"notification-{notification.id}",
        source=source,
        version=1,
        title=notification.title,
        time=epoch_ms(notification.created_at),
        author=NOTIFICATION_AUTHOR,
        tags=[
            Tag(title=loc.notification.READ_STATUS, icon="envelopeOpen")
            if notification.is_read
            else Tag(title=loc.notification.UNREAD_STATUS, icon="envelope")
        ],
    )


def notification_description(notification: Notification, state: RequestState) -> str | None:
    """Render a notification body, filling the templates of staff notifications.

    Args:
        notification: The notification with its content.
        state: Player configuration.

    Returns:
        str | None: The body, None without content.
    """
    content = notification.content
    if content is None:
        return None
    templates = state.loc.notification.templates
    lines = content.splitlines()
    if not lines or not lines[0].startswith("#"):
        return content
    kind, rest = lines[0], lines[1:]
    match kind:
        case "#CHART_DELETED":
            return templates.CHART_DELETED(chart_name="\n".join(rest))
        case "#CHART_VISIBILITY_CHANGED":
            status = rest[0] if rest else ""
            return templates.CHART_VISIBILITY_CHANGED(
                visibility_status=status, chart_name="\n".join(rest[1:])
            )
        case "#COMMENT_DELETED":
            return templates.COMMENT_DELETED(comment_content="\n".join(rest))
        case "#LEADERBOARD_SCORE_DELETED":
            return templates.LEADERBOARD_SCORE_DELETED(chart_name="\n".join(rest))
    return content


def speed_multiplier(speed: float | None) -> float:
    """Return the arcade score multiplier of a playback speed.

    Args:
        speed: Playback speed, None for 1.0.

    Returns:
        float: The multiplier.
    """
    if speed is None:
        return 1.0
    tier = int(speed * 10) / 10
    if tier < 1:
        return tier - 0.4
    return 1.0 + ((tier - 1.0) * 0.075)


def record_value(record: LeaderboardRecord, leaderboard_type: str) -> int:
    """Return the value a leaderboard ranks a record by.

    Args:
        record: The record.
        leaderboard_type: Ranking.

    Returns:
        int: The value.
    """
    match leaderboard_type:
        case "arcade_score_speed":
            return int(record.arcade_score * speed_multiplier(record.speed))
        case "accuracy_score":
            return record.accuracy_score
        case "arcade_score_no_speed":
            return record.arcade_score
        case "rank_match":
            return 3 * record.perfect + 2 * record.great + record.good
        case "least_combo_breaks":
            return record.good + record.miss
        case "least_misses":
            return record.miss
        case _:
            return record.perfect


def speed_text(speed: float | None) -> str:
    """Describe a non-default playback speed.

    Args:
        speed: Playback speed, None for 1.0.

    Returns:
        str: Text like `` | 1.25x``, empty at 1x.
    """
    value = 1.0 if speed is None else speed
    return f" | {round(value, 2)}x" if value != 1 else ""


def record_items(
    records: list[LeaderboardRecord],
    leaderboard_type: str,
    rank_offset: int,
    prefix: str,
) -> list[ServerItemLeaderboardRecord]:
    """Turn backend records into leaderboard records.

    Args:
        records: Records in rank order.
        leaderboard_type: Ranking.
        rank_offset: Rank of the first record minus one.
        prefix: Chart prefix.

    Returns:
        list[ServerItemLeaderboardRecord]: The records.
    """
    items: list[ServerItemLeaderboardRecord] = []
    for index, record in enumerate(records):
        value = record_value(record, leaderboard_type)
        shown = "727 WYSI" if value == 727 else str(value)
        grade = GRADES.get(record.grade, record.grade)
        items.append(
            ServerItemLeaderboardRecord(
                name=f"{prefix}{record.chart_id}-{record.id}",
                rank=f"#{index + rank_offset + 1}",
                player=record.display_name,
                playerUser=user_item(record.submitter) if record.submitter else None,
                value=f"{grade} | {shown}{speed_text(record.speed)}",
            )
        )
    return items


def replay_item(kit: LevelKit, record: LeaderboardRecord, chart: Chart) -> ReplayItem:
    """Turn a record and its chart into a replay item.

    Args:
        kit: Level resources.
        record: The record.
        chart: The record's chart.

    Returns:
        ReplayItem: The replay.
    """
    level = kit.level(chart, use_engine=record.engine)
    grade = GRADES.get(record.grade, record.grade)
    subtitle = (
        f"{grade} | {record.arcade_score} / {record.accuracy_score} | "
        f"{record.perfect} / {record.great} / {record.good} / {record.miss}"
        f"{speed_text(record.speed)}"
    )
    loc = kit.state.loc
    return ReplayItem(
        name=f"{level.name}-{record.id}",
        source=kit.source,
        version=1,
        title=level.title,
        subtitle=subtitle,
        author=record.display_name,
        authorUser=user_item(record.submitter) if record.submitter else None,
        tags=[Tag(title=kit.state.owo(loc.time_ago(time_ago(record.created_at))), icon="clock")],
        level=level,
        data=srl(record.replay.data),
        configuration=srl(record.replay.configuration),
    )
