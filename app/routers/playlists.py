from fastapi import APIRouter, Response

from app.backend.client import QueryValue
from app.backend.error_text import Site
from app.errors import SonolusError
from app.items import level_kit, uwu_items
from app.playlist_filter import Filter, merge_filter, parse_filter
from app.routers.common import (
    PlaylistSection,
    backend,
    check_page,
    invalid_page,
    respond,
    select_option,
    slider_option,
    staff_pick_values,
    text_option,
    toggle_option,
)
from app.settings import Constants
from app.sonolus_core import (
    PlaylistItem,
    ServerForm,
    ServerItemDetails,
    ServerItemInfo,
    ServerOption,
    ServerSubmitItemActionRequest,
    ServerSubmitItemActionResponse,
)
from app.state import Context, RequestState, State

router = APIRouter()
item_router = APIRouter()

DEFAULT_PLAYLIST = "uploaded"
DEFAULT_FILTER_NAME = "uploaded_cGFnZT0x"


@router.get("/sonolus/playlists/info")
async def playlists_info(context: Context, state: State) -> Response:
    """Return the playlist home page.

    Args:
        context: App context.
        state: Player configuration.

    Returns:
        Response: The playlist info.
    """
    loc = state.loc
    resources = context.resources
    banner = await resources.banner()
    playlists = await resources.playlists(state.localization)
    size = context.constants.lists.resource_section_size
    return respond(
        ServerItemInfo(
            sections=[
                PlaylistSection(
                    title="#PLAYLIST",
                    icon="playlist",
                    description=state.owo(
                        loc.server_description or context.config.sonolus.description
                    ),
                    itemType="playlist",
                    items=uwu_items(playlists[:size], state),
                )
            ],
            banner=banner,
        )
    )


@router.get("/sonolus/playlists/list")
async def playlists_list(state: State) -> Response:
    """Reject playlist listing, which this server doesn't offer.

    Args:
        state: Player configuration.

    Returns:
        Response: Never returns; always a 404 error.
    """
    raise SonolusError(404, state.loc.item_type_not_found("playlists"))


def filter_options(
    state: RequestState, constants: Constants, params: Filter, page: int, page_count: int
) -> list[ServerOption]:
    """Build the uploaded charts filter form, prefilled with the current filters.

    Args:
        state: Player configuration.
        constants: Tunables.
        params: Current filters.
        page: Current one-based page.
        page_count: Number of pages.

    Returns:
        list[ServerOption]: The options.
    """
    loc = state.loc
    search = loc.search
    limits = constants.search
    staff_default = (
        "default"
        if params["is_default_staff_pick"]
        else {None: "off", True: "true", False: "false"}[params["staff_pick"]]
    )
    return [
        slider_option("page", "Page", page, 1, page_count),
        select_option(
            "level_status",
            search.VISIBILITY,
            params["level_status"] or "ALL",
            [
                ("ALL", search.VISIBILITY_ALL),
                ("PUBLIC_MINE", search.VISIBILITY_PUBLIC),
                ("UNLISTED", search.VISIBILITY_UNLISTED),
                ("PRIVATE", search.VISIBILITY_PRIVATE),
            ],
        ),
        select_option(
            "staff_pick",
            loc.staff_pick,
            staff_default,
            staff_pick_values(loc, with_default=True),
            description=state.owo(search.STAFF_PICK_DESC),
        ),
        text_option(
            "keywords",
            "#KEYWORDS",
            params["keywords"] or "",
            search.ENTER_TEXT,
            limits.keywords_limit,
        ),
        slider_option(
            "min_rating",
            search.MIN_RATING,
            params["min_rating"] or limits.min_rating,
            limits.min_rating,
            limits.max_rating,
        ),
        slider_option(
            "max_rating",
            search.MAX_RATING,
            params["max_rating"] or limits.max_rating,
            limits.min_rating,
            limits.max_rating,
        ),
        text_option(
            "title_includes",
            search.TITLE_CONTAINS,
            params["title_includes"] or "",
            search.ENTER_TEXT,
            limits.title_limit,
        ),
        text_option(
            "author_includes",
            search.AUTHOR_CONTAINS,
            params["author_includes"] or "",
            search.ENTER_TEXT,
            limits.author_limit,
        ),
        text_option(
            "description_includes",
            search.DESCRIPTION_CONTAINS,
            params["description_includes"] or "",
            search.ENTER_TEXT,
            limits.description_limit,
        ),
        text_option(
            "artists_includes",
            search.ARTISTS_CONTAINS,
            params["artists_includes"] or "",
            search.ENTER_TEXT,
            limits.artists_limit,
        ),
        toggle_option(
            "liked_by",
            search.ONLY_LEVELS_I_LIKED,
            params["liked_by"] if params["liked_by"] is not None else False,
        ),
        toggle_option(
            "commented_on",
            search.ONLY_LEVELS_I_COMMENTED_ON,
            params["commented_on"] if params["commented_on"] is not None else False,
        ),
        slider_option("min_likes", search.MIN_LIKES, params["min_likes"] or 0, 0, limits.max_count),
        slider_option(
            "max_likes",
            search.MAX_LIKES,
            params["max_likes"] or limits.max_count,
            0,
            limits.max_count,
        ),
        slider_option(
            "min_comments", search.MIN_COMMENTS, params["min_comments"] or 0, 0, limits.max_count
        ),
        slider_option(
            "max_comments",
            search.MAX_COMMENTS,
            params["max_comments"] or limits.max_count,
            0,
            limits.max_count,
        ),
        text_option(
            "tags",
            search.TAGS_COMMA_SEPARATED,
            ", ".join(params["tags"]) if params["tags"] else "",
            search.ENTER_TAGS,
            limits.tags_limit,
        ),
        select_option(
            "sort_by",
            search.SORT_BY,
            params["sort_by"] or "created_at",
            [
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
            params["sort_order"] or "desc",
            [("desc", search.DESCENDING), ("asc", search.ASCENDING)],
        ),
    ]


def search_query(params: Filter, page: int) -> list[tuple[str, QueryValue]]:
    """Build the backend search of the player's own charts.

    Args:
        params: Filters.
        page: One-based page.

    Returns:
        list[tuple[str, QueryValue]]: Query values.
    """
    values: dict[str, QueryValue | None] = {
        "page": 0 if params["sort_by"] == "random" else page - 1,
        "staff_pick": params["staff_pick"],
        "min_rating": params["min_rating"],
        "max_rating": params["max_rating"],
        "status": params["level_status"] or "ALL",
        "min_likes": params["min_likes"],
        "max_likes": params["max_likes"],
        "min_comments": params["min_comments"],
        "max_comments": params["max_comments"],
        "liked_by": True if params["liked_by"] else None,
        "commented_on": True if params["commented_on"] else None,
        "title_includes": params["title_includes"],
        "description_includes": params["description_includes"],
        "author_includes": params["author_includes"],
        "artists_includes": params["artists_includes"],
        "sort_by": params["sort_by"],
        "sort_order": params["sort_order"],
        "meta_includes": params["keywords"],
    }
    query: list[tuple[str, QueryValue]] = [
        (key, value) for key, value in values.items() if value is not None
    ]
    query += [("tags", tag) for tag in params["tags"] or []]
    return query


@item_router.get("/sonolus/playlists/{item_name}")
async def playlist_details(item_name: str, context: Context, state: State) -> Response:
    """Return the player's uploaded charts filtered by the filters encoded in the name.

    Args:
        item_name: ``uploaded`` or ``uploaded_<base64url filters>``.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The playlist with its filter form.
    """
    loc = state.loc
    if not state.session:
        raise SonolusError(400, loc.not_logged_in)
    max_length = context.constants.search.max_playlist_name_length
    if item_name == DEFAULT_PLAYLIST:
        item_name = DEFAULT_FILTER_NAME
    head, separator, encoded = item_name.partition("_")
    if head != DEFAULT_PLAYLIST or not separator or len(item_name) > max_length:
        raise SonolusError(400, "huh")
    params = parse_filter(encoded)
    page = params["page"] or 1
    check_page(page, context.constants.lists.max_page)
    result = await backend(
        context.backend.list_charts(state.session, search_query(params, page)), Site.DETAIL, loc
    )
    kit = await level_kit(context, state)
    levels = [kit.level(chart) for chart in result.items]
    page_count = result.page_count
    full_page = len(result.items) == context.constants.lists.backend_page_size
    if params["sort_by"] == "random" and page_count != 0 and full_page:
        page_count = page + 2
    shown_pages = max(page_count, 1)
    if page > shown_pages:
        raise invalid_page(loc, page, page_count)
    playlist = (await context.resources.playlists(state.localization))[0]
    item = playlist.model_copy(update={"name": item_name, "levels": levels})
    return respond(
        ServerItemDetails[PlaylistItem](
            item=uwu_items([item], state)[0],
            actions=[
                ServerForm(
                    type="filter",
                    title=loc.search.FILTERS(page, shown_pages),
                    requireConfirmation=False,
                    options=filter_options(state, context.constants, params, page, shown_pages),
                )
            ],
            hasCommunity=False,
            leaderboards=[],
            sections=[],
        )
    )


@item_router.post("/sonolus/playlists/{item_name}/submit")
async def playlist_submit(
    item_name: str, context: Context, state: State, body: ServerSubmitItemActionRequest
) -> Response:
    """Apply the filter form, navigating to the playlist named after the new filters.

    Args:
        item_name: Current playlist name.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: The playlist to navigate to.
    """
    max_length = context.constants.search.max_playlist_name_length
    if not item_name.startswith(DEFAULT_PLAYLIST):
        raise SonolusError(404, state.loc.not_found)
    if len(item_name) > max_length:
        raise SonolusError(400, "why so long")
    _, _, previous = item_name.partition("_")
    encoded = merge_filter(previous, body.values, max_length)
    return respond(
        ServerSubmitItemActionResponse(
            key="", hashes=[], shouldNavigateToItem=f"{DEFAULT_PLAYLIST}_{encoded}"
        )
    )
