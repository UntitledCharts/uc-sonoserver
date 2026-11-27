import asyncio
import math
from typing import Annotated, Literal

from fastapi import APIRouter, Query, Response

from app.backend.error_text import Site
from app.backend.models import Notification
from app.context import AppContext
from app.errors import SonolusError
from app.items import notification_description, notification_post, uwu_items
from app.names import row_id
from app.routers.common import (
    OUT_OF_RANGE,
    PostSection,
    backend,
    check_page,
    respond,
    select_option,
)
from app.sonolus_core import PostItem, ServerForm, ServerItemDetails, ServerItemInfo, ServerItemList
from app.state import Context, RequestState, State

router = APIRouter()
item_router = APIRouter()

NOTIFICATION_PREFIX = "notification-"


def newest_first(posts: list[PostItem]) -> list[PostItem]:
    """Sort posts newest first, keeping the order of equal times.

    Args:
        posts: Posts to sort.

    Returns:
        list[PostItem]: The sorted posts.
    """
    return sorted(posts, key=lambda post: post.time, reverse=True)


async def static_posts(context: AppContext) -> list[PostItem]:
    """Return the announcements newest first.

    Args:
        context: App context.

    Returns:
        list[PostItem]: The announcements.
    """
    return newest_first([post.item for post in await context.resources.static_posts()])


@router.get("/sonolus/posts/info")
async def posts_info(
    context: Context, state: State, type: Literal["announcements", "notifications"]
) -> Response:
    """Return the newest announcements or the player's unread notifications.

    Args:
        context: App context.
        state: Player configuration.
        type: Which posts to show.

    Returns:
        Response: The post info.
    """
    loc = state.loc
    banner = await context.resources.banner()
    if type == "announcements":
        size = context.constants.lists.resource_section_size
        posts = await static_posts(context)
        section = PostSection(
            title="#NEWEST", icon="post", itemType="post", items=uwu_items(posts[:size], state)
        )
    else:
        page = await backend(
            context.backend.notifications(state.session, 0, only_unread=True), Site.DETAIL, loc
        )
        source = context.config.server.public_url
        notifications = [notification_post(item, state, source) for item in page.items]
        if notifications:
            section = PostSection(
                title=loc.notification.UNREAD,
                icon="bell",
                description=loc.notification.NOTIFICATION_DESC_UNREAD,
                itemType="post",
                items=notifications,
            )
        else:
            section = PostSection(
                title=loc.notification.NOTIFICATION,
                icon="bell",
                description=loc.notification.NOTIFICATION_DESC,
                itemType="post",
                items=[],
            )
    return respond(
        ServerItemInfo(
            sections=[section],
            searches=[
                ServerForm(
                    type="advanced",
                    title="#ADVANCED",
                    icon="advanced",
                    requireConfirmation=False,
                    options=[
                        select_option(
                            "post_type",
                            "#TYPE",
                            "all",
                            [
                                ("all", "#ALL"),
                                ("announcements", loc.announcements),
                                ("notifications", loc.notification.NOTIFICATION),
                            ],
                        )
                    ],
                )
            ],
            banner=banner,
        )
    )


async def _notification_window(
    context: AppContext, state: RequestState, offset: int, size: int
) -> tuple[list[Notification], int]:
    """Load a window of the player's notifications and their total count.

    Args:
        context: App context.
        state: Player configuration.
        offset: Index of the first notification, newest first.
        size: Notifications wanted.

    Returns:
        tuple[list[Notification], int]: The window and the total number of notifications.
    """
    loc = state.loc
    client = context.backend
    chunk = context.constants.lists.backend_max_limit
    calls = [
        backend(
            client.notification_window(state.session, index, min(chunk, offset + size - index)),
            Site.DETAIL,
            loc,
        )
        for index in range(offset, offset + size, chunk)
    ]
    counter = backend(client.notification_window(state.session, 0, 1), Site.DETAIL, loc)
    total_page, *pages = await asyncio.gather(counter, *calls)
    return [item for page in pages for item in page.items], total_page.page_count


def merge_page(
    statics: list[PostItem],
    window: list[PostItem],
    window_start: int,
    total: int,
    start: int,
    end: int,
) -> list[PostItem]:
    """Pick the posts of one page from announcements merged into newest-first notifications.

    Args:
        statics: Every announcement, newest first.
        window: Notifications from window_start on, covering every one that can reach the page.
        window_start: Index of the first window notification.
        total: Total number of notifications.
        start: First merged position of the page.
        end: Merged position after the page.

    Returns:
        list[PostItem]: The page, newest first, announcements before notifications of equal time.
    """
    placed: list[tuple[int, PostItem]] = []
    for offset, post in enumerate(window):
        newer_statics = sum(1 for static in statics if static.time >= post.time)
        placed.append((window_start + offset + newer_statics, post))
    for rank, static in enumerate(statics):
        older = next(
            (
                window_start + offset
                for offset, post in enumerate(window)
                if post.time <= static.time
            ),
            None,
        )
        if older is None:
            if window_start + len(window) < total:
                continue
            older = total
        elif older == window_start and window_start > 0:
            continue
        placed.append((older + rank, static))
    placed.sort(key=lambda entry: entry[0])
    return [post for position, post in placed if start <= position < end]


@router.get("/sonolus/posts/list")
async def posts_list(
    context: Context,
    state: State,
    page: Annotated[int, Query(ge=0)] = 0,
    post_type: Literal["all", "announcements", "notifications"] | None = None,
) -> Response:
    """Return a page of announcements and notifications, newest first.

    Args:
        context: App context.
        state: Player configuration.
        page: Zero-based page.
        post_type: Which posts to list, all when absent.

    Returns:
        Response: The page of posts.
    """
    lists = context.constants.lists
    check_page(page, lists.max_page)
    per_page = lists.per_page("posts")
    start = page * per_page
    end = start + per_page
    statics: list[PostItem] = []
    if post_type in ("all", "announcements", None):
        statics = await static_posts(context)
    wants_notifications = post_type in ("all", "notifications", None)
    if wants_notifications and not state.session and post_type == "notifications":
        raise SonolusError(401)
    if wants_notifications and state.session:
        window_start = max(0, start - len(statics))
        notifications, count = await _notification_window(
            context, state, window_start, end - window_start
        )
        source = context.config.server.public_url
        window = [notification_post(item, state, source) for item in notifications]
        items = merge_page(statics, window, window_start, count, start, end)
        total = len(statics) + count
    else:
        items = statics[start:end]
        total = len(statics)
    page_count = math.ceil(total / per_page)
    if page_count == 0:
        return respond(ServerItemList[PostItem](pageCount=0, items=[]))
    if page >= page_count:
        raise SonolusError(404, OUT_OF_RANGE)
    return respond(ServerItemList[PostItem](pageCount=page_count, items=uwu_items(items, state)))


@item_router.get("/sonolus/posts/{item_name}")
async def post_details(item_name: str, context: Context, state: State) -> Response:
    """Return an announcement or one of the player's notifications.

    Args:
        item_name: Post name, ``notification-<id>`` for notifications.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The post details.
    """
    loc = state.loc
    if item_name.startswith(NOTIFICATION_PREFIX):
        if not state.session:
            raise SonolusError(401, loc.not_logged_in)
        notification_id = row_id(item_name.removeprefix(NOTIFICATION_PREFIX))
        if notification_id is None:
            raise SonolusError(422, loc.not_found)
        notification = await backend(
            context.backend.notification(state.session, notification_id),
            Site.NOTIFICATION_OPEN,
            loc,
        )
        item = notification_post(notification, state, context.config.server.public_url)
        description = notification_description(notification, state)
    else:
        found = next(
            (
                post
                for post in await context.resources.static_posts()
                if post.item.name == item_name
            ),
            None,
        )
        if found is None:
            raise SonolusError(404, loc.not_found)
        item = found.item
        description = found.description
    return respond(
        ServerItemDetails[PostItem](
            item=item,
            description=description,
            actions=[],
            hasCommunity=False,
            leaderboards=[],
            sections=[],
        )
    )
