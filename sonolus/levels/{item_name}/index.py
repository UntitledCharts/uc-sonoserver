import asyncio

from fastapi import APIRouter

from core import SonolusRequest
from helpers.models.sonolus.response import ServerItemDetails
from helpers.models.sonolus.options import (
    ServerForm,
    ServerOption_Value,
    ServerSelectOption,
    ServerTextOption,
    ServerToggleOption,
)
from helpers.models.sonolus.item import LevelItem, ServerItemLeaderboard

router = APIRouter()

from helpers.owoify import handle_item_uwu, handle_uwu


@router.get("/", response_model=ServerItemDetails)
async def main(request: SonolusRequest, item_name: str):
    locale = request.state.loc
    item_data: LevelItem = None
    auth = request.headers.get("Sonolus-Session")
    actions = []

    # a promoted level opens as UnCh-{id}-{view_code}; register the click and open
    # the real chart, whose response carries the plain UnCh-{id} name back to the client
    clean_item_name = item_name
    promo_chart_id = None
    promo_view_code = None
    if item_name.startswith("UnCh-"):
        rest = item_name[len("UnCh-") :]
        if "-" in rest:
            chart_id_part, code_part = rest.split("-", 1)
            if len(chart_id_part) == 32 and chart_id_part.isalnum() and code_part:
                clean_item_name = f"UnCh-{chart_id_part}"
                promo_chart_id = chart_id_part
                promo_view_code = code_part

    if promo_chart_id and promo_view_code:
        response, _ = await asyncio.gather(
            request.app.api.get_chart(clean_item_name).send(auth),
            request.app.api.click_promotion(promo_chart_id, promo_view_code).send(auth),
        )
    else:
        response = await request.app.api.get_chart(clean_item_name).send(auth)

    asset_base_url = response.data.asset_base_url.removesuffix("/")
    liked = response.data.data.liked
    like_count = response.data.data.like_count
    item_data, desc = await request.app.run_blocking(
        response.data.data.to_level_item,
        request,
        asset_base_url,
        request.state.levelbg,
        include_description=True,
        context="level",
    )

    if auth:
        if liked:
            actions.append(
                ServerForm(
                    type="unlike",
                    title=locale.unlike(like_count),
                    icon="heart",
                    requireConfirmation=False,
                    options=[],
                ),
            )
        else:
            actions.append(
                ServerForm(
                    type="like",
                    title=locale.like(like_count),
                    icon="heartHollow",
                    requireConfirmation=False,
                    options=[],
                ),
            )
    if response.data.mod or response.data.owner:
        if response.data.data.deleted_at is not None:
            # only mods/admins can reach a chart pending deletion, and only they restore it
            if response.data.mod:
                actions.append(
                    ServerForm(
                        type="undelete",
                        title=locale.undelete,
                        icon="restore",
                        requireConfirmation=True,
                        options=[],
                    )
                )
        elif response.data.owner or response.data.mod:
            actions.append(
                ServerForm(
                    type="delete",
                    title="#DELETE",
                    icon="delete",
                    requireConfirmation=True,
                    options=[],
                )
            )

        VISIBILITIES = {
            "PUBLIC": {"title": "#PUBLIC", "icon": "globe"},
            "PRIVATE": {"title": "#PRIVATE", "icon": "lock"},
            "UNLISTED": {
                "title": locale.search.VISIBILITY_UNLISTED,
                "icon": "unlock",  # XXX maybe "hide" would be better
            },
        }
        current = response.data.data.status

        if response.data.owner:
            select_statuses = ["PRIVATE", "UNLISTED"]
            select_default = current if current in select_statuses else "PRIVATE"
        else:
            select_statuses = ["PUBLIC", "PRIVATE", "UNLISTED"]
            select_default = current

        visibility_values = [
            ServerOption_Value(name=s, title=VISIBILITIES[s]["title"])
            for s in select_statuses
        ]

        actions.append(
            ServerForm(
                type="visibility",
                title=locale.search.VISIBILITY,
                icon=VISIBILITIES[current]["icon"],
                requireConfirmation=True,
                options=[
                    ServerSelectOption(
                        query="visibility",
                        name=locale.search.VISIBILITY,
                        required=True,
                        default=select_default,
                        values=visibility_values,
                    )
                ],
            )
        )

        if response.data.owner and current != "PUBLIC":
            actions.append(
                ServerForm(
                    type="make_public",
                    title=locale.make_public,
                    icon="globe",
                    requireConfirmation=True,
                    description=locale.make_public_confirm_desc,
                    options=[
                        ServerToggleOption(
                            query="confirm_finished",
                            name=locale.make_public_confirm_finished,
                            description=locale.make_public_confirm_desc,
                            required=True,
                            default=False,
                        ),
                        ServerToggleOption(
                            query="confirm_jacket",
                            name=locale.make_public_confirm_jacket,
                            description=locale.make_public_confirm_desc,
                            required=True,
                            default=False,
                        ),
                        ServerToggleOption(
                            query="confirm_title",
                            name=locale.make_public_confirm_title,
                            description=locale.make_public_confirm_desc,
                            required=True,
                            default=False,
                        ),
                        ServerToggleOption(
                            query="confirm_bpm",
                            name=locale.make_public_confirm_bpm,
                            description=locale.make_public_confirm_bpm_desc,
                            required=True,
                            default=False,
                        ),
                    ],
                )
            )
        if response.data.mod:
            actions.append(
                ServerForm(
                    type="rerate",
                    title=locale.rerate,
                    icon="plus",
                    requireConfirmation=True,
                    options=[
                        ServerTextOption(
                            query="constant",
                            name="#RATING",
                            required=True,
                            default="",
                            placeholder=str(response.data.data.rating),
                            description=locale.rerate_desc,
                            shortcuts=[str(response.data.data.rating)],
                            limit=9,  # -999.1234, 9 max possible characters
                        )
                    ],
                )
            )
            if response.data.data.staff_pick:
                actions.append(
                    ServerForm(
                        type="staff_pick_delete",
                        title=locale.staff_pick_remove,
                        icon="delete",
                        requireConfirmation=True,
                        options=[
                            ServerToggleOption(
                                query="_",
                                name="#CONFIRM",
                                description=locale.staff_pick_confirm,  # no uwu
                                required=True,
                                default=False,
                            )
                        ],
                    )
                )
            else:
                actions.append(
                    ServerForm(
                        type="staff_pick_add",
                        title=locale.staff_pick_add,
                        icon="trophy",
                        requireConfirmation=True,
                        options=[
                            ServerToggleOption(
                                query="_",
                                name="#CONFIRM",
                                required=True,
                                default=False,
                                description=locale.staff_pick_confirm,
                            )
                        ],
                    )
                )

    data: LevelItem = handle_item_uwu(
        [item_data], request.state.localization, request.state.uwu
    )[0]

    return ServerItemDetails(
        item=data,
        description=desc,
        actions=actions,
        hasCommunity=True,
        leaderboards=[
            ServerItemLeaderboard(
                name="arcade_score_speed",
                title=handle_uwu(
                    locale.leaderboards.ARCADE_SCORE_SPEED,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="accuracy_score",
                title=handle_uwu(
                    locale.leaderboards.ACCURACY_SCORE,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="arcade_score_no_speed",
                title=handle_uwu(
                    locale.leaderboards.ARCADE_SCORE_NO_SPEED,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="rank_match",
                title=handle_uwu(
                    locale.leaderboards.RANK_MATCH,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="least_combo_breaks",
                title=handle_uwu(
                    locale.leaderboards.LEAST_COMBO_BREAKS,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="least_misses",
                title=handle_uwu(
                    locale.leaderboards.LEAST_MISSES,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
            ServerItemLeaderboard(
                name="perfect",
                title=handle_uwu(
                    locale.leaderboards.PERFECT,
                    request.state.localization,
                    request.state.uwu,
                ),
            ),
        ],
        sections=[],
    )
