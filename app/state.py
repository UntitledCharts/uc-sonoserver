from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request

from app.context import AppContext, get_context
from app.localization import Loc
from app.owoify import handle_uwu

UWU_LOCALES = ("tr", "en")
UWU_LEVELS = ("off", "uwu", "owo", "uvu", "max")
LEVEL_BACKGROUNDS = ("default_or_v3", "default_or_v1", "v1", "v3")
STAFF_PICK_MODES = ("off", "true", "false")
CONFIG_QUERIES = (
    "localization",
    "uwu",
    "levelbg",
    "stpickconfig",
    "defaultparticle",
    "defaultengine",
    "defaultskin",
)
ENGINE_DEFAULT = "engine_default"


@dataclass(frozen=True)
class RequestState:
    """Player configuration read from the query string of one request.

    Attributes:
        localization: Normalized locale code.
        loc: Player locale texts.
        uwu: Owoify level.
        levelbg: Level background choice.
        staff_pick: Staff pick filter of the configuration.
        particle: Default particle name or ``engine_default``.
        show_resource_buttons: ``1`` to show the resource buttons.
        skin: Default skin theme or ``engine_default``.
        engine: Server engine name.
        session: Value of the Sonolus-Session header, None when absent.
        query_params: Query values other than the configuration ones.
    """

    localization: str
    loc: Loc
    uwu: str
    levelbg: str
    staff_pick: str
    particle: str
    show_resource_buttons: str
    skin: str
    engine: str
    session: str | None
    query_params: dict[str, str]

    def owo(self, text: str, symbols: bool = True) -> str:
        """Owoify a text at the player's level.

        Args:
            text: Text to change.
            symbols: Whether brackets and punctuation may be replaced.

        Returns:
            str: The text, unchanged when owoify is off.
        """
        return handle_uwu(text, self.localization, self.uwu, symbols)


async def build_state(context: AppContext, request: Request) -> RequestState:
    """Read and validate the player's configuration.

    Args:
        context: App context.
        request: Current request.

    Returns:
        RequestState: The configuration.
    """
    query = request.query_params
    raw_locale = query.get("localization", "en").lower()
    uwu = query.get("uwu", "off").lower() if raw_locale in UWU_LOCALES else "off"
    levelbg = query.get("levelbg", "default_or_v3").lower()
    staff_pick = query.get("stpickconfig", "off").lower()
    particle = query.get("defaultparticle", ENGINE_DEFAULT).lower()
    show_resource_buttons = query.get("showresourcebuttons", "0")
    skin = query.get("defaultskin", ENGINE_DEFAULT).lower()
    loc, localization = context.locales.get_messages(raw_locale)
    resources = context.resources
    skins = await resources.skins()
    supported_skins = {theme for compiled in skins for theme in compiled.themes}
    engines = await resources.engines(localization)
    engine = query.get("defaultengine", engines[0].item.name)
    particles = await resources.particles()
    if show_resource_buttons not in ("0", "1"):
        show_resource_buttons = "0"
    if levelbg not in LEVEL_BACKGROUNDS:
        levelbg = "default_or_v3"
    if uwu not in UWU_LEVELS:
        uwu = "off"
    if staff_pick not in STAFF_PICK_MODES:
        staff_pick = "off"
    if particle != ENGINE_DEFAULT and particle not in {item.item.name for item in particles}:
        particle = ENGINE_DEFAULT
    if engine not in {item.item.name for item in engines}:
        engine = engines[0].item.name
    if skin != ENGINE_DEFAULT and skin not in supported_skins:
        skin = ENGINE_DEFAULT
    session = request.headers.get("Sonolus-Session") or None
    return RequestState(
        localization=localization,
        loc=loc,
        uwu=uwu,
        levelbg=levelbg,
        staff_pick=staff_pick,
        particle=particle,
        show_resource_buttons=show_resource_buttons,
        skin=skin,
        engine=engine,
        session=session,
        query_params={key: value for key, value in query.items() if key not in CONFIG_QUERIES},
    )


async def get_state(request: Request) -> RequestState:
    """Dependency returning the player's configuration.

    Args:
        request: Current request.

    Returns:
        RequestState: The configuration.
    """
    return await build_state(get_context(request), request)


State = Annotated[RequestState, Depends(get_state)]
Context = Annotated[AppContext, Depends(get_context)]
