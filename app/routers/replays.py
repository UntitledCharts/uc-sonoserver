import asyncio
from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.backend.error_text import Site
from app.backend.models import GlobalRecord
from app.context import AppContext
from app.errors import SonolusError
from app.items import delete_form, level_kit, replay_item, uwu_replays
from app.names import record_name
from app.routers.common import (
    GenericAction,
    ReplaySection,
    backend,
    can_notify,
    check_page,
    invalid_page,
    notify,
    parse_form,
    respond,
    toggle_option,
)
from app.sonolus_core import (
    ReplayItem,
    ServerForm,
    ServerItemDetails,
    ServerItemInfo,
    ServerItemList,
    ServerSubmitItemActionRequest,
    ServerSubmitItemActionResponse,
)
from app.state import Context, RequestState, State

router = APIRouter()
item_router = APIRouter()


async def replay_items(
    context: AppContext, state: RequestState, records: list[GlobalRecord]
) -> list[ReplayItem]:
    """Turn global records into owoified replay items.

    Args:
        context: App context.
        state: Player configuration.
        records: Records with their charts.

    Returns:
        list[ReplayItem]: The replays.
    """
    kit = await level_kit(context, state)
    return uwu_replays([replay_item(kit, item.record, item.chart) for item in records], state)


@router.get("/sonolus/replays/info")
async def replays_info(context: Context, state: State) -> Response:
    """Return random and newest replays.

    Args:
        context: App context.
        state: Player configuration.

    Returns:
        Response: The replay info.
    """
    loc = state.loc
    size = context.constants.lists.replay_section_size
    random_records, recent = await asyncio.gather(
        backend(context.backend.random_records(size), Site.DETAIL, loc),
        backend(context.backend.recent_records(0, size), Site.DETAIL, loc),
    )
    return respond(
        ServerItemInfo(
            searches=[
                ServerForm(
                    type="advanced",
                    title="#ADVANCED",
                    requireConfirmation=False,
                    options=[toggle_option("random", "#RANDOM", False)],
                )
            ],
            sections=[
                ReplaySection(
                    title="#RANDOM",
                    icon="replay",
                    itemType="replay",
                    items=await replay_items(context, state, random_records),
                ),
                ReplaySection(
                    title="#NEWEST",
                    icon="replay",
                    itemType="replay",
                    items=await replay_items(context, state, recent.items),
                ),
            ],
            banner=await context.resources.banner(),
        )
    )


@router.get("/sonolus/replays/list")
async def replays_list(
    context: Context,
    state: State,
    page: Annotated[int, Query(ge=0)] = 0,
    random: bool = False,
) -> Response:
    """Return a page of the newest replays, or random ones.

    Args:
        context: App context.
        state: Player configuration.
        page: Zero-based page.
        random: Pick random replays instead.

    Returns:
        Response: The page of replays.
    """
    loc = state.loc
    check_page(page, context.constants.lists.max_page)
    size = context.constants.lists.replay_page_size
    if random:
        records = await backend(context.backend.random_records(size), Site.DETAIL, loc)
        page_count = page + 2 if len(records) == size else int(len(records) != 0)
    else:
        result = await backend(context.backend.recent_records(page, size), Site.DETAIL, loc)
        records = result.items
        page_count = result.page_count
    if page > page_count:
        raise invalid_page(loc, page, page_count)
    return respond(
        ServerItemList[ReplayItem](
            pageCount=page_count, items=await replay_items(context, state, records)
        )
    )


@item_router.get("/sonolus/replays/{item_name}")
async def replay_details(item_name: str, context: Context, state: State) -> Response:
    """Return a replay with its delete action when the viewer may delete it.

    Args:
        item_name: Replay name ``<prefix><chart id>-<record id>``.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The replay details.
    """
    loc = state.loc
    name = record_name(item_name, context.config.sonolus.chart_prefix)
    if name is None:
        raise SonolusError(404)
    details = await backend(
        context.backend.record(state.session, name.chart_id, name.record_id), Site.BARE, loc
    )
    kit = await level_kit(context, state)
    replay = replay_item(kit, details.record, details.chart)
    return respond(
        ServerItemDetails[ReplayItem](
            item=uwu_replays([replay], state)[0],
            actions=[delete_form()] if details.can_delete else [],
            hasCommunity=False,
            leaderboards=[],
            sections=[],
        )
    )


@item_router.post("/sonolus/replays/{item_name}/submit")
async def replay_submit(
    item_name: str, context: Context, state: State, body: ServerSubmitItemActionRequest
) -> Response:
    """Delete a replay's record, notifying its player when staff deletes it.

    Args:
        item_name: Replay name.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: Tells the client to remove the replay.
    """
    loc = state.loc
    form = parse_form(GenericAction, body.values)
    name = record_name(item_name, context.config.sonolus.chart_prefix)
    if name is None:
        raise SonolusError(404)
    if form.type != "delete":
        raise SonolusError(404, loc.not_found)
    deleted = await backend(
        context.backend.delete_record(state.session, name.chart_id, name.record_id),
        Site.RECORD_DELETE,
        loc,
    )
    submitter = deleted.record.submitter
    session = state.session
    if (
        not deleted.record.is_own
        and submitter is not None
        and session
        and await can_notify(context, session)
    ):
        await notify(
            context,
            session,
            submitter.id,
            "Leaderboard Score Deleted",
            f"#LEADERBOARD_SCORE_DELETED\n{deleted.chart.title}",
        )
    return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldRemoveItem=True))
