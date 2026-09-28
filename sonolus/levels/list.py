import asyncio

from fastapi import APIRouter, Query
from fastapi import HTTPException, status

from typing import Literal

from core import SonolusRequest
from helpers.models.sonolus.response import ServerItemList
from helpers.models.sonolus.misc import Tag

router = APIRouter()

from helpers.owoify import handle_item_uwu

type_func = type


@router.get("/", response_model=ServerItemList)
async def main(
    request: SonolusRequest,
    type: Literal["quick", "advanced"] = Query("quick"),
    page: int = Query(0, ge=0),
    staff_pick: Literal["default", "off", "true", "false", None] = Query("default"),
    min_rating: int | None = Query(None),
    max_rating: int | None = Query(None),
    tags: str | None = Query(None),
    min_likes: int | None = Query(None),
    max_likes: int | None = Query(None),
    min_comments: int | None = Query(None),
    max_comments: int | None = Query(None),
    liked_by: bool | None = Query(False),
    commented_on: bool | None = Query(False),
    title_includes: str | None = Query(None),
    description_includes: str | None = Query(None),
    author_includes: str | None = Query(None),
    artists_includes: str | None = Query(None),
    sort_by: Literal[
        "created_at",
        "published_at",
        "rating",
        "likes",
        "comments",
        "decaying_likes",
        "abc",
        "random",
    ] = Query("published_at"),
    sort_order: Literal["desc", "asc", None] = Query("desc"),
    level_status: Literal["PUBLIC", None] = Query(
        "PUBLIC"
    ),  # will only ever be PUBLIC here. anything else, go to playlists
    keywords: str | None = Query(None),
):
    locale = request.state.loc
    uwu_level = request.state.uwu
    auth = request.headers.get("Sonolus-Session")

    if type == "quick":
        response = await request.app.api.charts_quick_search(
            page=page,
            meta_includes=keywords,
            sort_by="published_at",
            staff_pick=(
                staff_pick
                if staff_pick not in ["default", None]
                else request.state.staff_pick
            ),
        ).send(auth)
    else:
        response = await request.app.api.charts_advanced_search(
            page=page,
            staff_pick={"off": None, "true": True, "false": False}[
                (
                    staff_pick
                    if staff_pick not in ["default", None]
                    else request.state.staff_pick
                )
            ],
            min_rating=min_rating,
            max_rating=max_rating,
            status=level_status,
            tags=[tag.strip() for tag in tags.split(",")] if tags else None,
            min_likes=min_likes,
            max_likes=max_likes,
            min_comments=min_comments,
            max_comments=max_comments,
            liked_by=liked_by,
            commented_on=commented_on,
            title_includes=title_includes,
            description_includes=description_includes,
            author_includes=author_includes,
            artists_includes=artists_includes,
            sort_by=sort_by,
            sort_order=sort_order,
            meta_includes=keywords,
        ).send(auth)

    pageCount = response.data.pageCount
    if sort_by == "random" and pageCount != 0 and len(response.data.data) == 10:
        pageCount = (
            page + 2
        )  # always have one extra page, random will not run out and there may be duplicates
        # only if pageCount isn't 0 of course, and the api actually returned a full list (so there likely is more)
    if page > pageCount or page < 0:
        raise HTTPException(
            status_code=400,
            detail=(
                locale.invalid_page_plural(page, pageCount)
                if pageCount != 1
                else locale.invalid_page_singular(page, pageCount)
            ),
        )
    elif pageCount == 0:
        raise HTTPException(
            status_code=400, detail=locale.items_not_found_search("level")
        )
    asset_base_url = response.data.asset_base_url.removesuffix("/")
    data = await asyncio.gather(
        *[
            request.app.run_blocking(
                item.to_level_item,
                request,
                asset_base_url,
                request.state.levelbg,
            )
            for item in response.data.data
        ]
    )
    num_pages = pageCount
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=locale.items_not_found("level"),
        )
    page_data = handle_item_uwu(data, request.state.localization, uwu_level)

    # first page only: an optional promoted level, prepended as the first item and
    # tagged PROMOTED (same chance/targeting as the homepage promoted section)
    if page == 0:
        promo_response = await request.app.api.serve_promotion().send(auth)
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
            promo_item.name = (
                f"UnCh-{promo.promotion.chart_id}-{promo.promotion.view_code}"
            )
            promo_item.tags.insert(0, Tag(title=locale.promoted))
            page_data = [promo_item] + page_data

    return ServerItemList(pageCount=num_pages, items=page_data)
