from typing import Annotated, Any, Literal

from fastapi import APIRouter, Query, Response

from app.context import AppContext
from app.errors import SonolusError
from app.items import uwu_items
from app.routers.common import (
    BackgroundSection,
    EffectSection,
    EngineSection,
    ParticleSection,
    SkinSection,
    OUT_OF_RANGE,
    respond,
)
from app.sonolus_core import (
    BackgroundItem,
    EffectItem,
    EngineItem,
    ParticleItem,
    ServerItemDetails,
    ServerItemInfo,
    ServerItemList,
    SkinItem,
    SonolusModel,
)
from app.state import Context, RequestState, State

router = APIRouter()
item_router = APIRouter()

ItemType = Literal[
    "posts",
    "playlists",
    "levels",
    "skins",
    "backgrounds",
    "effects",
    "particles",
    "engines",
    "replays",
    "rooms",
    "users",
]
ResourceItem = BackgroundItem | EffectItem | EngineItem | ParticleItem | SkinItem

ITEM_CLASSES: dict[str, type[SonolusModel]] = {
    "backgrounds": BackgroundItem,
    "effects": EffectItem,
    "engines": EngineItem,
    "particles": ParticleItem,
    "skins": SkinItem,
}
SECTIONS: dict[str, type[SonolusModel]] = {
    "backgrounds": BackgroundSection,
    "effects": EffectSection,
    "engines": EngineSection,
    "particles": ParticleSection,
    "skins": SkinSection,
}


async def resource_items(
    context: AppContext, state: RequestState, item_type: str, for_engine: bool
) -> list[Any] | None:
    """Return the compiled items of a resource type.

    Args:
        context: App context.
        state: Player configuration.
        item_type: Plural item type.
        for_engine: Keep only skins meant for the configured engine.

    Returns:
        list[Any] | None: The items, None for types this server doesn't list.
    """
    resources = context.resources
    match item_type:
        case "engines":
            return [engine.item for engine in await resources.engines(state.localization)]
        case "skins":
            return [
                skin.item
                for skin in await resources.skins()
                if not for_engine or not skin.engines or state.engine in skin.engines
            ]
        case "backgrounds":
            return list(await resources.backgrounds(state.localization))
        case "effects":
            return list(await resources.effects())
        case "particles":
            return [particle.item for particle in await resources.particles()]
    return None


@router.get("/sonolus/{item_type}/info")
async def resource_info(item_type: ItemType, context: Context, state: State) -> Response:
    """Return the home section of a resource type.

    Args:
        item_type: Plural item type.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The item info.
    """
    loc = state.loc
    banner = await context.banner.get()
    items = await resource_items(context, state, item_type, for_engine=True)
    if items is None:
        raise SonolusError(404, loc.item_type_not_found(item_type))
    singular = item_type[:-1]
    size = context.constants.lists.resource_section_size
    section = SECTIONS[item_type](
        title="#" + singular.upper(),
        icon=singular,
        description=state.owo(loc.server_description or context.config.sonolus.description),
        itemType=singular,
        items=uwu_items(items[:size], state),
    )
    return respond(ServerItemInfo(sections=[section], banner=banner))


@router.get("/sonolus/{item_type}/list")
async def resource_list(
    item_type: ItemType,
    context: Context,
    state: State,
    page: Annotated[int, Query(ge=0)] = 0,
) -> Response:
    """Return a page of a resource type.

    Args:
        item_type: Plural item type.
        context: App context.
        state: Player configuration.
        page: Zero-based page.

    Returns:
        Response: The page of items.
    """
    loc = state.loc
    items = await resource_items(context, state, item_type, for_engine=True)
    if items is None:
        raise SonolusError(404, loc.item_type_not_found(item_type))
    per_page = context.constants.lists.per_page(item_type)
    page_count = (len(items) + per_page - 1) // per_page
    if page_count == 0:
        raise SonolusError(404, loc.items_not_found(item_type))
    if page >= page_count:
        raise SonolusError(404, OUT_OF_RANGE)
    chunk = items[page * per_page : (page + 1) * per_page]
    model = ServerItemList[ITEM_CLASSES[item_type]]
    return respond(model(pageCount=page_count, items=uwu_items(chunk, state)))


@item_router.get("/sonolus/{item_type}/{item_name}")
async def resource_details(
    item_type: ItemType, item_name: str, context: Context, state: State
) -> Response:
    """Return one resource item.

    Args:
        item_type: Plural item type.
        item_name: Item name; any name resolves to the default background.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The item details.
    """
    loc = state.loc
    description: str | None = None
    if item_type == "backgrounds":
        item: Any = (await context.resources.backgrounds(state.localization))[0]
        if item.name != item_name:
            title = item_name.title()
            item = item.model_copy(update={"name": item_name, "title": title, "subtitle": title})
    else:
        items = await resource_items(context, state, item_type, for_engine=False)
        if items is None:
            raise SonolusError(404, loc.item_not_found(item_type, item_name))
        item = next((entry for entry in items if entry.name == item_name), None)
        if item is None:
            raise SonolusError(
                404,
                loc.item_not_found(item_type.capitalize().removesuffix("s"), item_name),
            )
        if item_type == "engines":
            engines = await context.resources.engines(state.localization)
            raw = next(engine.description for engine in engines if engine.item.name == item_name)
            description = state.owo(raw) if raw else None
    model = ServerItemDetails[ITEM_CLASSES[item_type]]
    return respond(
        model(
            item=uwu_items([item], state)[0],
            description=description,
            actions=[],
            hasCommunity=False,
            leaderboards=[],
            sections=[],
        )
    )
