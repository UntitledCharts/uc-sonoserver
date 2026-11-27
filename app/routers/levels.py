import asyncio
import decimal
from typing import Annotated, Literal

import aiohttp
from fastapi import APIRouter, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from app.backend.client import BackendError, QueryValue
from app.backend.error_text import Site
from app.backend.models import ChartDetails, ServedPromotion
from app.client_ip import client_ip
from app.context import AppContext
from app.errors import SonolusError
from app.items import LevelKit, level_kit, rating_text, uwu_levels
from app.localization import Loc
from app.names import promoted_name
from app.routers.common import (
    LevelSection,
    NOTIFY_PERMISSION,
    backend,
    check_page,
    invalid_page,
    notify,
    parse_form,
    require_chart_id,
    require_session,
    respond,
    select_option,
    slider_option,
    staff_pick_values,
    text_option,
    toggle_option,
)
from app.settings import Constants
from app.sonolus_core import (
    LevelItem,
    ServerForm,
    ServerItemDetails,
    ServerItemInfo,
    ServerItemLeaderboard,
    ServerItemList,
    ServerOption,
    ServerSubmitItemActionRequest,
    ServerSubmitItemActionResponse,
    Tag,
)
from app.state import Context, RequestState, State

router = APIRouter()
item_router = APIRouter()

SortBy = Literal[
    "created_at", "published_at", "rating", "likes", "comments", "decaying_likes", "abc", "random"
]
LEADERBOARD_TYPES = (
    ("arcade_score_speed", "ARCADE_SCORE_SPEED"),
    ("accuracy_score", "ACCURACY_SCORE"),
    ("arcade_score_no_speed", "ARCADE_SCORE_NO_SPEED"),
    ("rank_match", "RANK_MATCH"),
    ("least_combo_breaks", "LEAST_COMBO_BREAKS"),
    ("least_misses", "LEAST_MISSES"),
    ("perfect", "PERFECT"),
)
VISIBILITY_ICONS = {"PUBLIC": "globe", "PRIVATE": "lock", "UNLISTED": "unlock"}


class LevelAction(BaseModel):
    """Values submitted from a level action form.

    Attributes:
        model_config: Ignores unknown values.
        type: Action type.
        visibility: Chosen visibility.
        constant: New rating text.
        confirm_finished: Make public confirmation.
        confirm_jacket: Make public confirmation.
        confirm_title: Make public confirmation.
        confirm_bpm: Make public confirmation.
        confirmed: The ``#CONFIRM`` toggle.
    """

    model_config = ConfigDict(extra="ignore")

    type: str
    visibility: Literal["UNLISTED", "PRIVATE", "PUBLIC"] | None = None
    constant: str | None = None
    confirm_finished: bool = False
    confirm_jacket: bool = False
    confirm_title: bool = False
    confirm_bpm: bool = False
    confirmed: bool = Field(default=False, alias="_")


def staff_pick_filter(mode: str) -> bool | None:
    """Turn a staff pick mode into the backend filter.

    Args:
        mode: ``off``, ``true`` or ``false``.

    Returns:
        bool | None: The filter, None for no filter.
    """
    return {"true": True, "false": False}.get(mode)


async def served_promotion(
    context: AppContext, state: RequestState, request: Request
) -> ServedPromotion | None:
    """Ask the backend for a promotion, treating any failure as none.

    Args:
        context: App context.
        state: Player configuration.
        request: Current request, for the player's address.

    Returns:
        ServedPromotion | None: The promotion.
    """
    address = client_ip(request, context.config.server.trusted_proxies)
    try:
        served = await context.backend.serve_promotion(state.session, address)
    except (BackendError, aiohttp.ClientError, TimeoutError):
        return None
    return served.promotion


def promoted_item(
    kit: LevelKit, promotion: ServedPromotion, prefix: str, state: RequestState
) -> LevelItem:
    """Build a promoted level named so that opening it reports the click.

    Args:
        kit: Level resources.
        promotion: The promotion.
        prefix: Chart prefix.
        state: Player configuration.

    Returns:
        LevelItem: The level.
    """
    item = uwu_levels([kit.level(promotion.chart)], state)[0]
    return item.model_copy(update={"name": f"{prefix}{promotion.chart.id}-{promotion.view_code}"})


def search_options(state: RequestState, constants: Constants) -> list[ServerOption]:
    """Build the advanced level search options.

    Args:
        state: Player configuration.
        constants: Tunables.

    Returns:
        list[ServerOption]: The options.
    """
    loc = state.loc
    search = loc.search
    limits = constants.search
    options: list[ServerOption] = [
        text_option("keywords", "#KEYWORDS", "", search.ENTER_TEXT, limits.keywords_limit),
        select_option(
            "staff_pick",
            loc.staff_pick,
            "default",
            staff_pick_values(loc, with_default=True),
            description=state.owo(search.STAFF_PICK_DESC),
        ),
        slider_option(
            "min_rating", search.MIN_RATING, limits.min_rating, limits.min_rating, limits.max_rating
        ),
        slider_option(
            "max_rating", search.MAX_RATING, limits.max_rating, limits.min_rating, limits.max_rating
        ),
        text_option(
            "title_includes", search.TITLE_CONTAINS, "", search.ENTER_TEXT, limits.title_limit
        ),
        text_option(
            "author_includes", search.AUTHOR_CONTAINS, "", search.ENTER_TEXT, limits.author_limit
        ),
        text_option(
            "description_includes",
            search.DESCRIPTION_CONTAINS,
            "",
            search.ENTER_TEXT,
            limits.description_limit,
        ),
        text_option(
            "artists_includes",
            search.ARTISTS_CONTAINS,
            "",
            search.ENTER_TEXT,
            limits.artists_limit,
        ),
    ]
    if state.session:
        options.append(toggle_option("liked_by", search.ONLY_LEVELS_I_LIKED, False))
        options.append(toggle_option("commented_on", search.ONLY_LEVELS_I_COMMENTED_ON, False))
    options += [
        slider_option("min_likes", search.MIN_LIKES, 0, 0, limits.max_count),
        slider_option("max_likes", search.MAX_LIKES, limits.max_count, 0, limits.max_count),
        slider_option("min_comments", search.MIN_COMMENTS, 0, 0, limits.max_count),
        slider_option("max_comments", search.MAX_COMMENTS, limits.max_count, 0, limits.max_count),
        text_option("tags", search.TAGS_COMMA_SEPARATED, "", search.ENTER_TAGS, limits.tags_limit),
        select_option(
            "sort_by",
            search.SORT_BY,
            "published_at",
            [
                ("published_at", search.DATE_PUBLISHED),
                ("created_at", search.DATE_CREATED),
                ("random", "#RANDOM"),
                ("rating", search.RATING),
                ("likes", search.LIKES),
                ("comments", search.COMMENTS),
                ("decaying_likes", search.DECAYING_LIKES),
                ("abc", search.TITLE_A_Z),
            ],
            description=state.owo(search.SORT_BY_DESCRIPTION),
        ),
        select_option(
            "sort_order",
            search.SORT_ORDER,
            "desc",
            [("desc", search.DESCENDING), ("asc", search.ASCENDING)],
        ),
    ]
    return options


@router.get("/sonolus/levels/info")
async def levels_info(context: Context, state: State, request: Request) -> Response:
    """Return the level home page with promoted, staff pick, newest, random and popular levels.

    Args:
        context: App context.
        state: Player configuration.
        request: Current request.

    Returns:
        Response: The level info.
    """
    loc = state.loc
    session = state.session
    client = context.backend
    mode = state.staff_pick
    staff_filter = staff_pick_filter(mode)
    picks_only = mode in ("off", "false")
    random_charts, newest, picks, popular, promotion = await asyncio.gather(
        backend(client.random_charts(session, staff_filter), Site.DETAIL, loc),
        backend(
            client.list_charts(session, {"sort_by": "published_at", "staff_pick": staff_filter}),
            Site.DETAIL,
            loc,
        ),
        backend(client.random_charts(session, picks_only), Site.DETAIL, loc),
        backend(
            client.list_charts(session, {"sort_by": "decaying_likes", "staff_pick": staff_filter}),
            Site.DETAIL,
            loc,
        ),
        served_promotion(context, state, request),
    )
    kit = await level_kit(context, state)
    size = context.constants.lists.level_section_size
    prefix = context.config.sonolus.chart_prefix
    sections: list[LevelSection] = []
    if promotion is not None:
        sections.append(
            LevelSection(
                title=loc.promoted,
                icon="trophy",
                itemType="level",
                items=[promoted_item(kit, promotion, prefix, state)],
            )
        )
    sections += [
        LevelSection(
            title=loc.random_staff_pick if picks_only else loc.random_non_staff_pick,
            icon="trophy",
            description=state.owo(loc.staff_pick_desc if picks_only else loc.non_staff_pick_desc),
            itemType="level",
            items=uwu_levels([kit.level(picks[0])] if picks else [], state),
        ),
        LevelSection(
            title="#NEWEST",
            icon="level",
            itemType="level",
            items=uwu_levels([kit.level(chart) for chart in newest.items[:size]], state),
        ),
        LevelSection(
            title="#RANDOM",
            icon="level",
            itemType="level",
            items=uwu_levels([kit.level(chart) for chart in random_charts[:size]], state),
        ),
        LevelSection(
            title="#POPULAR",
            icon="level",
            itemType="level",
            items=uwu_levels([kit.level(chart) for chart in popular.items[:size]], state),
        ),
    ]
    return respond(
        ServerItemInfo(
            creates=[
                ServerForm(
                    type="level",
                    title="#UPLOAD",
                    icon="level",
                    description=loc.use_website_to_upload(context.constants.website_url),
                    requireConfirmation=True,
                    options=[],
                )
            ],
            searches=[
                ServerForm(
                    type="advanced",
                    title=loc.search.ADVANCED_SEARCH,
                    requireConfirmation=False,
                    options=search_options(state, context.constants),
                )
            ],
            sections=sections,
            banner=await context.resources.banner(),
        )
    )


@router.get("/sonolus/levels/list")
async def levels_list(
    context: Context,
    state: State,
    request: Request,
    type: Literal["quick", "advanced"] = "quick",
    page: Annotated[int, Query(ge=0)] = 0,
    staff_pick: Literal["default", "off", "true", "false"] = "default",
    min_rating: int | None = None,
    max_rating: int | None = None,
    tags: str | None = None,
    min_likes: int | None = None,
    max_likes: int | None = None,
    min_comments: int | None = None,
    max_comments: int | None = None,
    liked_by: bool = False,
    commented_on: bool = False,
    title_includes: str | None = None,
    description_includes: str | None = None,
    author_includes: str | None = None,
    artists_includes: str | None = None,
    sort_by: SortBy = "published_at",
    sort_order: Literal["desc", "asc"] = "desc",
    level_status: Literal["PUBLIC"] = "PUBLIC",
    keywords: str | None = None,
) -> Response:
    """Search public levels, with a promoted level first on the first page.

    Args:
        context: App context.
        state: Player configuration.
        request: Current request.
        type: ``quick`` keyword search or ``advanced`` search.
        page: Zero-based page.
        staff_pick: Staff pick filter, ``default`` for the configured one.
        min_rating: Lowest rating.
        max_rating: Highest rating.
        tags: Comma-separated tags.
        min_likes: Fewest likes.
        max_likes: Most likes.
        min_comments: Fewest comments.
        max_comments: Most comments.
        liked_by: Only levels the player liked, ignored without a session.
        commented_on: Only levels the player commented on, ignored without a session.
        title_includes: Title substring.
        description_includes: Description substring.
        author_includes: Author substring.
        artists_includes: Artists substring.
        sort_by: Sort key.
        sort_order: Sort direction.
        level_status: Always PUBLIC.
        keywords: Substring of any text field.

    Returns:
        Response: The page of levels.
    """
    loc = state.loc
    check_page(page, context.constants.lists.max_page)
    mode = staff_pick if staff_pick != "default" else state.staff_pick
    staff_filter = staff_pick_filter(mode)
    query: list[tuple[str, QueryValue]] = []
    if type == "quick":
        query += [("page", page), ("sort_by", "published_at")]
        if keywords:
            query.append(("meta_includes", keywords))
        if staff_filter is not None:
            query.append(("staff_pick", staff_filter))
    else:
        values: dict[str, QueryValue | None] = {
            "page": 0 if sort_by == "random" else page,
            "staff_pick": staff_filter,
            "min_rating": min_rating,
            "max_rating": max_rating,
            "status": level_status,
            "min_likes": min_likes,
            "max_likes": max_likes,
            "min_comments": min_comments,
            "max_comments": max_comments,
            "liked_by": True if liked_by and state.session else None,
            "commented_on": True if commented_on and state.session else None,
            "title_includes": title_includes,
            "description_includes": description_includes,
            "author_includes": author_includes,
            "artists_includes": artists_includes,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "meta_includes": keywords,
        }
        query += [(key, value) for key, value in values.items() if value is not None]
        if tags:
            query += [("tags", tag.strip()) for tag in tags.split(",")]
    search = backend(context.backend.list_charts(state.session, query), Site.DETAIL, loc)
    if page == 0:
        result, promotion = await asyncio.gather(search, served_promotion(context, state, request))
    else:
        result, promotion = await search, None
    page_count = result.page_count
    full_page = len(result.items) == context.constants.lists.backend_page_size
    if sort_by == "random" and page_count != 0 and full_page:
        page_count = page + 2
    if page > page_count:
        raise invalid_page(loc, page, page_count)
    kit = await level_kit(context, state)
    items = uwu_levels([kit.level(chart) for chart in result.items], state)
    if promotion is not None:
        promoted = promoted_item(kit, promotion, context.config.sonolus.chart_prefix, state)
        promoted = promoted.model_copy(update={"tags": [Tag(title=loc.promoted), *promoted.tags]})
        items = [promoted, *items]
    return respond(ServerItemList[LevelItem](pageCount=page_count, items=items))


@router.post("/sonolus/levels/create")
async def levels_create(context: Context, state: State) -> Response:
    """Reject in-game uploads, pointing players to the website.

    Args:
        context: App context.
        state: Player configuration.

    Returns:
        Response: Never returns; always a 400 error.
    """
    raise SonolusError(400, state.loc.use_website_to_upload(context.constants.website_url))


def level_actions(
    details: ChartDetails, state: RequestState, constants: Constants
) -> list[ServerForm]:
    """Build the actions the viewer may use on a level.

    Args:
        details: The chart with the viewer's permissions.
        state: Player configuration.
        constants: Tunables.

    Returns:
        list[ServerForm]: The actions.
    """
    loc = state.loc
    viewer = details.viewer
    actions: list[ServerForm] = []
    if state.session:
        if details.liked:
            actions.append(
                ServerForm(
                    type="unlike",
                    title=loc.unlike(details.like_count),
                    icon="heart",
                    requireConfirmation=False,
                    options=[],
                )
            )
        else:
            actions.append(
                ServerForm(
                    type="like",
                    title=loc.like(details.like_count),
                    icon="heartHollow",
                    requireConfirmation=False,
                    options=[],
                )
            )
    staff_visibility = viewer.staff("chart.visibility")
    manages = viewer.manages_visibility
    if (
        viewer.is_owner
        or manages
        or staff_visibility
        or viewer.staff("chart.delete")
        or viewer.staff("chart.restore")
    ):
        if details.deleted_at is not None:
            if viewer.staff("chart.restore"):
                actions.append(
                    ServerForm(
                        type="undelete",
                        title=loc.undelete,
                        icon="restore",
                        requireConfirmation=True,
                        options=[],
                    )
                )
        elif viewer.is_owner or viewer.staff("chart.delete"):
            actions.append(
                ServerForm(
                    type="delete",
                    title="#DELETE",
                    icon="delete",
                    requireConfirmation=True,
                    options=[],
                )
            )
        titles = {
            "PUBLIC": "#PUBLIC",
            "PRIVATE": "#PRIVATE",
            "UNLISTED": loc.search.VISIBILITY_UNLISTED,
        }
        current = details.status
        if manages or staff_visibility:
            if manages:
                statuses = ["PRIVATE", "UNLISTED"]
                default = current if current in statuses else "PRIVATE"
            else:
                statuses = ["PUBLIC", "PRIVATE", "UNLISTED"]
                default = current
            actions.append(
                ServerForm(
                    type="visibility",
                    title=loc.search.VISIBILITY,
                    icon=VISIBILITY_ICONS[current],
                    requireConfirmation=True,
                    options=[
                        select_option(
                            "visibility",
                            loc.search.VISIBILITY,
                            default,
                            [(status, titles[status]) for status in statuses],
                            required=True,
                        )
                    ],
                )
            )
        if manages and current != "PUBLIC":
            actions.append(
                ServerForm(
                    type="make_public",
                    title=loc.make_public,
                    icon="globe",
                    description=loc.make_public_confirm_desc,
                    requireConfirmation=True,
                    options=[
                        toggle_option(
                            "confirm_finished",
                            loc.make_public_confirm_finished,
                            False,
                            description=loc.make_public_confirm_desc,
                            required=True,
                        ),
                        toggle_option(
                            "confirm_jacket",
                            loc.make_public_confirm_jacket,
                            False,
                            description=loc.make_public_confirm_desc,
                            required=True,
                        ),
                        toggle_option(
                            "confirm_title",
                            loc.make_public_confirm_title,
                            False,
                            description=loc.make_public_confirm_desc,
                            required=True,
                        ),
                        toggle_option(
                            "confirm_bpm",
                            loc.make_public_confirm_bpm,
                            False,
                            description=loc.make_public_confirm_bpm_desc,
                            required=True,
                        ),
                    ],
                )
            )
    if viewer.staff("chart.rerate"):
        rating = rating_text(details.rating)
        actions.append(
            ServerForm(
                type="rerate",
                title=loc.rerate,
                icon="plus",
                requireConfirmation=True,
                options=[
                    text_option(
                        "constant",
                        "#RATING",
                        "",
                        rating,
                        constants.moderation.rerate_limit,
                        description=loc.rerate_desc,
                        required=True,
                        shortcuts=[rating],
                    )
                ],
            )
        )
    if viewer.staff("chart.staff_pick"):
        confirm = toggle_option(
            "_", "#CONFIRM", False, description=loc.staff_pick_confirm, required=True
        )
        if details.staff_pick:
            actions.append(
                ServerForm(
                    type="staff_pick_delete",
                    title=loc.staff_pick_remove,
                    icon="delete",
                    requireConfirmation=True,
                    options=[confirm],
                )
            )
        else:
            actions.append(
                ServerForm(
                    type="staff_pick_add",
                    title=loc.staff_pick_add,
                    icon="trophy",
                    requireConfirmation=True,
                    options=[confirm],
                )
            )
    return actions


async def _click(context: AppContext, session: str | None, chart_id: str, view_code: str) -> None:
    """Report a promotion click, ignoring failures.

    Args:
        context: App context.
        session: Player session.
        chart_id: Promoted chart id.
        view_code: View code from the level name.
    """
    try:
        await context.backend.click_promotion(session, chart_id, view_code)
    except (BackendError, aiohttp.ClientError, TimeoutError):
        return


@item_router.get("/sonolus/levels/{item_name}")
async def level_details(item_name: str, context: Context, state: State) -> Response:
    """Return a level with its actions and leaderboards, counting promotion clicks.

    Args:
        item_name: Level name, optionally with a promotion view code.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The level details.
    """
    loc = state.loc
    prefix = context.config.sonolus.chart_prefix
    promoted = promoted_name(item_name, prefix)
    if promoted is not None:
        details, _ = await asyncio.gather(
            backend(context.backend.chart(state.session, promoted.chart_id), Site.DETAIL, loc),
            _click(context, state.session, promoted.chart_id, promoted.view_code),
        )
    else:
        chart = require_chart_id(item_name, prefix, Site.DETAIL, loc)
        details = await backend(context.backend.chart(state.session, chart), Site.DETAIL, loc)
    kit = await level_kit(context, state)
    item = uwu_levels([kit.level(details, context="level")], state)[0]
    leaderboards = [
        ServerItemLeaderboard(name=name, title=state.owo(getattr(loc.leaderboards, key)))
        for name, key in LEADERBOARD_TYPES
    ]
    return respond(
        ServerItemDetails[LevelItem](
            item=item,
            description=details.description,
            actions=level_actions(details, state, context.constants),
            hasCommunity=True,
            leaderboards=leaderboards,
            sections=[],
        )
    )


def valid_constant(value: str | None, constants: Constants) -> bool:
    """Check a rerate value: a number strictly inside the bounds with few decimals.

    Args:
        value: Submitted text.
        constants: Tunables.

    Returns:
        bool: Whether the value is accepted.
    """
    limits = constants.moderation
    if not isinstance(value, str):
        return False
    try:
        number = decimal.Decimal(value)
        if not (-limits.rerate_bound < number < limits.rerate_bound):
            return False
    except (decimal.InvalidOperation, ValueError):
        return False
    if "." in value and len(value.split(".")[1].rstrip("0")) > limits.rerate_max_decimals:
        return False
    return True


async def _change_visibility(
    context: AppContext,
    state: RequestState,
    session: str,
    item_name: str,
    target: str | None,
    confirmed: bool,
) -> None:
    """Change a level's visibility, notifying the owner when staff hides it.

    Args:
        context: App context.
        state: Player configuration.
        session: Player session.
        item_name: Level name.
        target: New visibility.
        confirmed: Whether every make public confirmation was given.
    """
    loc = state.loc
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.VISIBILITY, loc)
    if target is None:
        raise SonolusError(422, loc.not_mod_or_owner)
    needs_confirmation = target == "PUBLIC" and not confirmed
    details = await backend(
        context.backend.chart(session, chart, preview=True),
        Site.DETAIL if needs_confirmation else Site.VISIBILITY,
        loc,
    )
    if needs_confirmation and details.viewer.manages_visibility:
        raise SonolusError(400, loc.make_public_confirm_required)
    await backend(context.backend.set_visibility(session, chart, target), Site.VISIBILITY, loc)
    viewer = details.viewer
    if target != "PUBLIC" and not viewer.manages_visibility and viewer.staff(NOTIFY_PERMISSION):
        await notify(
            context,
            session,
            details.owner.id,
            "Chart Visibility Update",
            f"#CHART_VISIBILITY_CHANGED\n{target}\n{details.title}",
        )


async def _delete(context: AppContext, loc: Loc, session: str, item_name: str) -> None:
    """Delete a level, notifying the owner when staff deletes it.

    Args:
        context: App context.
        loc: Player locale.
        session: Player session.
        item_name: Level name.
    """
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.CHART_DELETE, loc)
    details = await backend(
        context.backend.chart(session, chart, preview=True), Site.CHART_DELETE, loc
    )
    await backend(context.backend.delete_chart(session, chart), Site.CHART_DELETE, loc)
    if not details.viewer.is_owner and details.viewer.staff(NOTIFY_PERMISSION):
        await notify(
            context, session, details.owner.id, "Chart Deleted", f"#CHART_DELETED\n{details.title}"
        )


@item_router.post("/sonolus/levels/{item_name}/submit")
async def level_submit(
    item_name: str, context: Context, state: State, body: ServerSubmitItemActionRequest
) -> Response:
    """Run a level action: like, delete, restore, visibility, rerate or staff pick.

    Args:
        item_name: Level name.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: What the client should refresh.
    """
    loc = state.loc
    session = require_session(state)
    form = parse_form(LevelAction, body.values)
    prefix = context.config.sonolus.chart_prefix
    client = context.backend
    match form.type:
        case "like" | "unlike":
            chart = require_chart_id(item_name, prefix, Site.LIKE, loc)
            await backend(client.set_like(session, chart, form.type == "like"), Site.LIKE, loc)
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
        case "delete":
            await _delete(context, loc, session, item_name)
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldRemoveItem=True))
        case "undelete":
            chart = require_chart_id(item_name, prefix, Site.CHART_RESTORE, loc)
            await backend(client.restore_chart(session, chart), Site.CHART_RESTORE, loc)
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
        case "visibility" | "make_public":
            confirmed = all(
                (form.confirm_finished, form.confirm_jacket, form.confirm_title, form.confirm_bpm)
            )
            target = form.visibility if form.type == "visibility" else "PUBLIC"
            await _change_visibility(context, state, session, item_name, target, confirmed)
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
        case "rerate":
            if not valid_constant(form.constant, context.constants):
                raise SonolusError(400, loc.invalid_constant)
            assert form.constant is not None
            chart = require_chart_id(item_name, prefix, Site.RERATE, loc)
            rating = float(
                decimal.Decimal(form.constant).quantize(
                    decimal.Decimal("0.0001"), rounding=decimal.ROUND_HALF_UP
                )
            )
            await backend(client.set_rating(session, chart, rating), Site.RERATE, loc)
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
        case "staff_pick_add" | "staff_pick_delete":
            if not form.confirmed:
                raise SonolusError(400, loc.staff_pick_confirm)
            chart = require_chart_id(item_name, prefix, Site.STAFF_PICK, loc)
            await backend(
                client.set_staff_pick(session, chart, form.type == "staff_pick_add"),
                Site.STAFF_PICK,
                loc,
            )
            return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
    raise SonolusError(404, loc.not_found)
