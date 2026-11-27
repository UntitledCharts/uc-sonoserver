import logging
from collections.abc import Awaitable
from typing import Literal, TypeVar
from urllib.parse import parse_qs

import aiohttp
from fastapi import Response
from pydantic import BaseModel, ConfigDict, ValidationError

from app.backend.client import BackendError
from app.backend.error_text import Site, invalid_chart_id, to_sonolus_error
from app.context import AppContext
from app.errors import SonolusError
from app.localization import Loc
from app.names import chart_id
from app.sonolus_core import (
    BackgroundItem,
    EffectItem,
    EngineItem,
    LevelItem,
    ParticleItem,
    PlaylistItem,
    PostItem,
    ReplayItem,
    ServerItemSectionTyped,
    ServerSelectOption,
    ServerSelectOptionValue,
    ServerSliderOption,
    ServerTextAreaOption,
    ServerTextOption,
    ServerToggleOption,
    SkinItem,
    SonolusModel,
)
from app.state import RequestState

OUT_OF_RANGE = "hi stop hitting our api thanks"
NOTIFY_PERMISSION = "notification.send"

logger = logging.getLogger("uc.sonoserver")

ResultT = TypeVar("ResultT")
FormT = TypeVar("FormT", bound=BaseModel)

BackgroundSection = ServerItemSectionTyped[Literal["background"], BackgroundItem]
EffectSection = ServerItemSectionTyped[Literal["effect"], EffectItem]
EngineSection = ServerItemSectionTyped[Literal["engine"], EngineItem]
LevelSection = ServerItemSectionTyped[Literal["level"], LevelItem]
ParticleSection = ServerItemSectionTyped[Literal["particle"], ParticleItem]
PlaylistSection = ServerItemSectionTyped[Literal["playlist"], PlaylistItem]
PostSection = ServerItemSectionTyped[Literal["post"], PostItem]
ReplaySection = ServerItemSectionTyped[Literal["replay"], ReplayItem]
SkinSection = ServerItemSectionTyped[Literal["skin"], SkinItem]


class GenericAction(BaseModel):
    """Values submitted from a form with no options.

    Attributes:
        model_config: Ignores unknown values.
        type: Action type.
    """

    model_config = ConfigDict(extra="ignore")

    type: str


def respond(model: SonolusModel) -> Response:
    """Serialize a Sonolus model the way the old server did, leaving out every null.

    Args:
        model: Response model.

    Returns:
        Response: The JSON response.
    """
    return Response(model.model_dump_json(exclude_none=True), media_type="application/json")


async def backend(call: Awaitable[ResultT], site: Site, loc: Loc) -> ResultT:
    """Await a backend call, turning its errors into what players saw at that site.

    Args:
        call: The backend call.
        site: Where the call is made.
        loc: Player locale.

    Returns:
        ResultT: The call's result.
    """
    try:
        return await call
    except BackendError as error:
        raise to_sonolus_error(error, site, loc) from None


async def can_notify(context: AppContext, session: str) -> bool:
    """Check whether the acting player may send staff notifications.

    Args:
        context: App context.
        session: Session of the acting player.

    Returns:
        bool: True when the account holds the notification permission.
    """
    try:
        me = await context.backend.me(session)
    except (BackendError, aiohttp.ClientError, TimeoutError) as error:
        logger.warning("could not check the notification permission: %s", error)
        return False
    return NOTIFY_PERMISSION in me.account.permissions


async def notify(
    context: AppContext, session: str, account_id: str, title: str, content: str
) -> None:
    """Send a staff notification, logging instead of failing the finished action.

    Args:
        context: App context.
        session: Session of the acting staff member.
        account_id: Recipient account id.
        title: Notification title.
        content: Notification body.
    """
    try:
        await context.backend.send_notification(session, account_id, title, content)
    except (BackendError, aiohttp.ClientError, TimeoutError) as error:
        logger.warning("could not send the %r notification to %s: %s", title, account_id, error)


def require_chart_id(name: str, prefix: str, site: Site, loc: Loc) -> str:
    """Validate a level name before it reaches a backend URL.

    Args:
        name: Item name from the path.
        prefix: Chart prefix.
        site: Call site the chart is used at, deciding the error text.
        loc: Player locale.

    Returns:
        str: The chart id.
    """
    parsed = chart_id(name, prefix)
    if parsed is None:
        raise to_sonolus_error(invalid_chart_id(), site, loc)
    return parsed


def require_session(state: RequestState) -> str:
    """Return the player's session or fail with the not logged in message.

    Args:
        state: Player configuration.

    Returns:
        str: The session.
    """
    if not state.session:
        raise SonolusError(401, state.loc.not_logged_in)
    return state.session


def parse_values(values: str) -> dict[str, str]:
    """Parse submitted form values, keeping the first value and dropping blanks.

    Args:
        values: Query-string encoded form values.

    Returns:
        dict[str, str]: The values.
    """
    return {key: items[0] for key, items in parse_qs(values).items()}


def parse_form(model: type[FormT], values: str) -> FormT:
    """Parse submitted form values into a model.

    Args:
        model: Form model.
        values: Query-string encoded form values.

    Returns:
        FormT: The form, a 400 error when it is malformed.
    """
    try:
        return model.model_validate(parse_values(values))
    except ValidationError:
        raise SonolusError(400) from None


def check_page(page: int, max_page: int) -> None:
    """Reject page numbers past the configured maximum before they reach the backend.

    Args:
        page: Requested page.
        max_page: Highest page accepted.
    """
    if page > max_page:
        raise SonolusError(404, OUT_OF_RANGE)


def invalid_page(loc: Loc, page: int, page_count: int) -> SonolusError:
    """Build the error for a page past the last one.

    Args:
        loc: Player locale.
        page: Requested page.
        page_count: Number of pages.

    Returns:
        SonolusError: The 400 error.
    """
    if page_count == 1:
        return SonolusError(400, loc.invalid_page_singular(page, page_count))
    return SonolusError(400, loc.invalid_page_plural(page, page_count))


def text_option(
    query: str,
    name: str,
    default: str,
    placeholder: str,
    limit: int,
    description: str | None = None,
    required: bool = False,
    shortcuts: list[str] | None = None,
) -> ServerTextOption:
    """Build a text option.

    Args:
        query: Query key.
        name: Shown name.
        default: Default value.
        placeholder: Placeholder text.
        limit: Longest value.
        description: Shown description.
        required: Whether a value is required.
        shortcuts: Quick values.

    Returns:
        ServerTextOption: The option.
    """
    return ServerTextOption(
        query=query,
        name=name,
        description=description,
        required=required,
        type="text",
        def_=default,
        placeholder=placeholder,
        limit=limit,
        shortcuts=shortcuts or [],
    )


def text_area_option(
    query: str, name: str, placeholder: str, limit: int, required: bool
) -> ServerTextAreaOption:
    """Build an empty text area option.

    Args:
        query: Query key.
        name: Shown name.
        placeholder: Placeholder text.
        limit: Longest value.
        required: Whether a value is required.

    Returns:
        ServerTextAreaOption: The option.
    """
    return ServerTextAreaOption(
        query=query,
        name=name,
        required=required,
        type="textArea",
        def_="",
        placeholder=placeholder,
        limit=limit,
        shortcuts=[],
    )


def slider_option(
    query: str, name: str, default: int, low: int, high: int, required: bool = False
) -> ServerSliderOption:
    """Build a slider option with a step of one.

    Args:
        query: Query key.
        name: Shown name.
        default: Default value.
        low: Lowest value.
        high: Highest value.
        required: Whether a value is required.

    Returns:
        ServerSliderOption: The option.
    """
    return ServerSliderOption(
        query=query,
        name=name,
        required=required,
        type="slider",
        def_=default,
        min=low,
        max=high,
        step=1,
    )


def toggle_option(
    query: str,
    name: str,
    default: bool,
    description: str | None = None,
    required: bool = False,
) -> ServerToggleOption:
    """Build a toggle option.

    Args:
        query: Query key.
        name: Shown name.
        default: Default state.
        description: Shown description.
        required: Whether the toggle is required.

    Returns:
        ServerToggleOption: The option.
    """
    return ServerToggleOption(
        query=query,
        name=name,
        description=description,
        required=required,
        type="toggle",
        def_=default,
    )


def select_option(
    query: str,
    name: str,
    default: str,
    values: list[tuple[str, str]],
    description: str | None = None,
    required: bool = False,
) -> ServerSelectOption:
    """Build a select option.

    Args:
        query: Query key.
        name: Shown name.
        default: Default value name.
        values: Value names and titles.
        description: Shown description.
        required: Whether a value is required.

    Returns:
        ServerSelectOption: The option.
    """
    return ServerSelectOption(
        query=query,
        name=name,
        description=description,
        required=required,
        type="select",
        def_=default,
        values=[ServerSelectOptionValue(name=value, title=title) for value, title in values],
    )


def staff_pick_values(loc: Loc, with_default: bool) -> list[tuple[str, str]]:
    """Return the staff pick filter values.

    Args:
        loc: Player locale.
        with_default: Include the ``default`` value first.

    Returns:
        list[tuple[str, str]]: Value names and titles.
    """
    values = [
        ("off", loc.search.STAFF_PICK_OFF),
        ("true", loc.search.STAFF_PICK_TRUE),
        ("false", loc.search.STAFF_PICK_FALSE),
    ]
    return [("default", "#DEFAULT"), *values] if with_default else values
