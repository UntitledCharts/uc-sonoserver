from typing import Annotated, Literal

from fastapi import APIRouter, Query, Response

from app.backend.error_text import Site
from app.errors import SonolusError
from app.items import level_kit, record_items, replay_item, uwu_replays
from app.names import row_id
from app.routers.common import backend, check_page, require_chart_id, respond
from app.sonolus_core import (
    ServerItemLeaderboardDetails,
    ServerItemLeaderboardRecordDetails,
    ServerItemLeaderboardRecordList,
)
from app.state import Context, State

item_router = APIRouter()

LeaderboardType = Literal[
    "arcade_score_speed",
    "accuracy_score",
    "arcade_score_no_speed",
    "rank_match",
    "least_combo_breaks",
    "least_misses",
    "perfect",
]


@item_router.get("/sonolus/levels/{item_name}/leaderboards/{leaderboard_type}")
async def leaderboard_details(
    item_name: str, leaderboard_type: LeaderboardType, context: Context, state: State
) -> Response:
    """Return a level's top records.

    Args:
        item_name: Level name.
        leaderboard_type: Ranking.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The top records.
    """
    loc = state.loc
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.BARE, loc)
    lists = context.constants.lists
    page = await backend(
        context.backend.leaderboard(
            state.session, chart, leaderboard_type, 0, lists.leaderboard_top_records
        ),
        Site.BARE,
        loc,
    )
    return respond(
        ServerItemLeaderboardDetails(
            topRecords=record_items(
                page.items,
                leaderboard_type,
                0,
                context.config.sonolus.chart_prefix,
            )
        )
    )


@item_router.get("/sonolus/levels/{item_name}/leaderboards/{leaderboard_type}/records/list")
async def leaderboard_records(
    item_name: str,
    leaderboard_type: LeaderboardType,
    context: Context,
    state: State,
    page: Annotated[int, Query(ge=0)] = 0,
) -> Response:
    """Return a page of a level's leaderboard.

    Args:
        item_name: Level name.
        leaderboard_type: Ranking.
        context: App context.
        state: Player configuration.
        page: Zero-based page.

    Returns:
        Response: The records.
    """
    loc = state.loc
    check_page(page, context.constants.lists.max_page)
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.BARE, loc)
    size = context.constants.lists.leaderboard_page_size
    result = await backend(
        context.backend.leaderboard(state.session, chart, leaderboard_type, page, size),
        Site.BARE,
        loc,
    )
    return respond(
        ServerItemLeaderboardRecordList(
            pageCount=result.page_count,
            records=record_items(
                result.items,
                leaderboard_type,
                page * size,
                context.config.sonolus.chart_prefix,
            ),
        )
    )


@item_router.get("/sonolus/levels/{item_name}/leaderboards/{leaderboard_type}/records/{name}")
async def leaderboard_record(
    item_name: str,
    leaderboard_type: LeaderboardType,
    name: str,
    context: Context,
    state: State,
) -> Response:
    """Return the replay of a leaderboard record.

    Args:
        item_name: Level name.
        leaderboard_type: Ranking.
        name: Record name ending in ``-<record id>``.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The record's replay.
    """
    loc = state.loc
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.BARE, loc)
    record_id = row_id(name.rsplit("-", maxsplit=1)[-1])
    if record_id is None:
        raise SonolusError(400)
    details = await backend(context.backend.record(state.session, chart, record_id), Site.BARE, loc)
    kit = await level_kit(context, state)
    replay = replay_item(kit, details.record, details.chart)
    return respond(ServerItemLeaderboardRecordDetails(replays=uwu_replays([replay], state)))
