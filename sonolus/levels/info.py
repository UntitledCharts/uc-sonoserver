import asyncio

from fastapi import APIRouter
from core import SonolusRequest
from helpers.models.sonolus.item_section import LevelItemSection
from helpers.models.sonolus.response import ServerItemInfo
from helpers.models.sonolus.options import (
    ServerForm,
    ServerTextOption,
    ServerSelectOption,
    ServerOption_Value,
    ServerSliderOption,
    ServerToggleOption,
)

from helpers.data_compilers import compile_banner

router = APIRouter()

from helpers.owoify import handle_uwu, handle_item_uwu


@router.get("/", response_model=ServerItemInfo)
async def main(request: SonolusRequest):
    locale = request.state.loc
    uwu_level = request.state.uwu
    auth = request.headers.get("Sonolus-Session")

    creates = [
        ServerForm(
            type="level",
            title="#UPLOAD",
            icon="level",
            requireConfirmation=True,
            options=[],
            description=locale.use_website_to_upload("https://untitledcharts.com"),
        )
    ]
    staff_pick = request.state.staff_pick

    random_response, newest_response, staffpick_req, popular_response, promo_response = (
        await asyncio.gather(
            request.app.api.get_random_charts(staff_pick).send(auth),
            request.app.api.get_newest_charts(staff_pick).send(auth),
            request.app.api.get_random_staff_picks(staff_pick in ("off", "false")).send(
                auth
            ),
            request.app.api.get_popular_charts(staff_pick).send(auth),
            request.app.api.serve_promotion().send(auth),
        )
    )

    asset_base_url = random_response.data.asset_base_url.removesuffix("/")
    random_staff_pick = (
        await request.app.run_blocking(
            staffpick_req.data.data[0].to_level_item,
            request,
            asset_base_url,
            request.state.levelbg,
        )
        if staffpick_req.data.data
        else None
    )

    random = await asyncio.gather(
        *[
            request.app.run_blocking(
                chart.to_level_item,
                request,
                asset_base_url,
                request.state.levelbg,
            )
            for chart in random_response.data.data[:3]
        ]
    )
    newest = await asyncio.gather(
        *[
            request.app.run_blocking(
                chart.to_level_item,
                request,
                asset_base_url,
                request.state.levelbg,
            )
            for chart in newest_response.data.data[:3]
        ]
    )
    popular = await asyncio.gather(
        *[
            request.app.run_blocking(
                chart.to_level_item,
                request,
                asset_base_url,
                request.state.levelbg,
            )
            for chart in popular_response.data.data[:3]
        ]
    )

    promoted_section = None
    if (
        promo_response.data
        and promo_response.data.promotion
        and promo_response.data.data
    ):
        promo = promo_response.data
        promo_asset_base = (
            promo.asset_base_url.removesuffix("/")
            if promo.asset_base_url
            else asset_base_url
        )
        promo_item = await request.app.run_blocking(
            promo.data.to_level_item,
            request,
            promo_asset_base,
            request.state.levelbg,
        )
        promo_item = handle_item_uwu(
            [promo_item], request.state.localization, uwu_level
        )[0]
        # click tracking: the level page reverts this to UnCh-{id} on open
        promo_item.name = f"UnCh-{promo.promotion.chart_id}-{promo.promotion.view_code}"
        promoted_section = LevelItemSection(
            title=locale.promoted,
            icon="trophy",
            items=[promo_item],
        )

    sections = [
        LevelItemSection(
            title=(
                locale.random_staff_pick
                if staff_pick in ["off", "false"]
                else locale.random_non_staff_pick
            ),
            icon="trophy",
            description=handle_uwu(
                (
                    locale.staff_pick_desc
                    if staff_pick in ["off", "false"]
                    else locale.non_staff_pick_desc
                ),
                request.state.localization,
                uwu_level,
            ),
            items=handle_item_uwu(
                [random_staff_pick] if random_staff_pick else [],
                request.state.localization,
                uwu_level,
            ),
        ),
        LevelItemSection(
            title="#NEWEST",
            icon="level",
            items=handle_item_uwu(newest, request.state.localization, uwu_level),
        ),
        LevelItemSection(
            title="#RANDOM",
            icon="level",
            items=handle_item_uwu(random, request.state.localization, uwu_level),
        ),
        LevelItemSection(
            title="#POPULAR",
            icon="level",
            items=handle_item_uwu(popular, request.state.localization, uwu_level),
        ),
    ]

    if promoted_section:
        sections.insert(0, promoted_section)

    options = [
        ServerTextOption(
            query="keywords",
            name="#KEYWORDS",
            required=False,
            default="",
            placeholder=locale.search.ENTER_TEXT,
            limit=100,
            shortcuts=[],
        ),
        ServerSelectOption(
            query="staff_pick",
            name=locale.staff_pick,
            required=False,
            description=handle_uwu(
                locale.search.STAFF_PICK_DESC, request.state.localization, uwu_level
            ),
            default="default",
            values=[
                ServerOption_Value(name="default", title="#DEFAULT"),
                ServerOption_Value(name="off", title=locale.search.STAFF_PICK_OFF),
                ServerOption_Value(name="true", title=locale.search.STAFF_PICK_TRUE),
                ServerOption_Value(name="false", title=locale.search.STAFF_PICK_FALSE),
            ],
        ),
        ServerSliderOption(
            query="min_rating",
            name=locale.search.MIN_RATING,
            required=False,
            default=-999,
            min=-999,
            max=999,
            step=1,
        ),
        ServerSliderOption(
            query="max_rating",
            name=locale.search.MAX_RATING,
            required=False,
            default=999,
            min=-999,
            max=999,
            step=1,
        ),
        ServerTextOption(
            query="title_includes",
            name=locale.search.TITLE_CONTAINS,
            required=False,
            default="",
            placeholder=locale.search.ENTER_TEXT,
            limit=100,
            shortcuts=[],
        ),
        ServerTextOption(
            query="author_includes",
            name=locale.search.AUTHOR_CONTAINS,
            required=False,
            default="",
            placeholder=locale.search.ENTER_TEXT,
            limit=60,
            shortcuts=[],
        ),
        ServerTextOption(
            query="description_includes",
            name=locale.search.DESCRIPTION_CONTAINS,
            required=False,
            default="",
            placeholder=locale.search.ENTER_TEXT,
            limit=200,
            shortcuts=[],
        ),
        ServerTextOption(
            query="artists_includes",
            name=locale.search.ARTISTS_CONTAINS,
            required=False,
            default="",
            placeholder=locale.search.ENTER_TEXT,
            limit=100,
            shortcuts=[],
        ),
    ]

    if auth:
        options.append(
            ServerToggleOption(
                query="liked_by",
                name=locale.search.ONLY_LEVELS_I_LIKED,
                required=False,
                default=False,
            )
        )
        options.append(
            ServerToggleOption(
                query="commented_on",
                name=locale.search.ONLY_LEVELS_I_COMMENTED_ON,
                required=False,
                default=False,
            )
        )

    options.append(
        ServerSliderOption(
            query="min_likes",
            name=locale.search.MIN_LIKES,
            required=False,
            default=0,
            min=0,
            max=9999,
            step=1,
        )
    )
    options.append(
        ServerSliderOption(
            query="max_likes",
            name=locale.search.MAX_LIKES,
            required=False,
            default=9999,
            min=0,
            max=9999,
            step=1,
        )
    )
    options.append(
        ServerSliderOption(
            query="min_comments",
            name=locale.search.MIN_COMMENTS,
            required=False,
            default=0,
            min=0,
            max=9999,
            step=1,
        )
    )
    options.append(
        ServerSliderOption(
            query="max_comments",
            name=locale.search.MAX_COMMENTS,
            required=False,
            default=9999,
            min=0,
            max=9999,
            step=1,
        )
    )
    options.append(
        ServerTextOption(
            query="tags",
            name=locale.search.TAGS_COMMA_SEPARATED,
            required=False,
            default="",
            placeholder=locale.search.ENTER_TAGS,
            limit=200,
            shortcuts=[],
        )
    )
    options.append(
        ServerSelectOption(
            query="sort_by",
            name=locale.search.SORT_BY,
            description=handle_uwu(
                locale.search.SORT_BY_DESCRIPTION,
                request.state.localization,
                uwu_level,
            ),
            required=False,
            default="published_at",
            values=[
                ServerOption_Value(
                    name="published_at", title=locale.search.DATE_PUBLISHED
                ),
                ServerOption_Value(name="created_at", title=locale.search.DATE_CREATED),
                ServerOption_Value(name="random", title="#RANDOM"),
                ServerOption_Value(name="rating", title=locale.search.RATING),
                ServerOption_Value(name="likes", title=locale.search.LIKES),
                ServerOption_Value(name="comments", title=locale.search.COMMENTS),
                ServerOption_Value(
                    name="decaying_likes", title=locale.search.DECAYING_LIKES
                ),
                ServerOption_Value(name="abc", title=locale.search.TITLE_A_Z),
            ],
        )
    )
    options.append(
        ServerSelectOption(
            query="sort_order",
            name=locale.search.SORT_ORDER,
            required=False,
            default="desc",
            values=[
                ServerOption_Value(name="desc", title=locale.search.DESCENDING),
                ServerOption_Value(name="asc", title=locale.search.ASCENDING),
            ],
        )
    )

    return ServerItemInfo(
        creates=creates,
        searches=[
            ServerForm(
                type="advanced",
                title=locale.search.ADVANCED_SEARCH,
                requireConfirmation=False,
                options=options,
            )
        ],
        sections=sections,
        banner=await request.app.run_blocking(compile_banner),
    )
