import logging

import aiohttp
from fastapi import APIRouter, Response
from pydantic import ValidationError

from app.backend.client import BackendError
from app.sonolus_core import (
    ServerConfiguration,
    ServerInfo,
    ServerInfoAuthenticationButton,
    ServerInfoConfigurationButton,
    ServerInfoItemButton,
    ServerOption,
)
from app.routers.common import respond, select_option, staff_pick_values, toggle_option
from app.state import UWU_LOCALES, Context, State

router = APIRouter()
logger = logging.getLogger("uc.sonoserver")

ServerInfoButton = (
    ServerInfoAuthenticationButton | ServerInfoConfigurationButton | ServerInfoItemButton
)

SEPARATOR = "\n\n" + "-" * 40 + "\n"


@router.get("/sonolus/info")
async def server_info(context: Context, state: State) -> Response:
    """Return the server info with buttons, configuration and the welcome text.

    Args:
        context: App context.
        state: Player configuration.

    Returns:
        Response: The server info.
    """
    loc = state.loc
    resources = context.resources
    logged_in = bool(state.session)
    banner = await context.banner.get()
    buttons: list[ServerInfoButton] = [
        ServerInfoAuthenticationButton(type="authentication"),
        ServerInfoItemButton(
            type="post",
            title=loc.announcements,
            icon="announcement",
            infoType="announcements",
        ),
    ]
    if logged_in:
        buttons.append(
            ServerInfoItemButton(
                type="post",
                title=loc.notification.NOTIFICATION,
                icon="comment",
                infoType="notifications",
            )
        )
    buttons += [
        ServerInfoItemButton(type="level"),
        ServerInfoItemButton(type="replay"),
        ServerInfoConfigurationButton(type="configuration"),
    ]
    if logged_in:
        buttons.append(ServerInfoItemButton(type="playlist"))
    if state.show_resource_buttons == "1":
        buttons += [
            ServerInfoItemButton(type=kind)
            for kind in ("skin", "background", "effect", "particle", "engine")
        ]

    options: list[ServerOption] = []
    if state.localization in UWU_LOCALES:
        options.append(
            select_option(
                "uwu",
                loc.uwu,
                "off",
                [
                    ("off", loc.off),
                    ("owo", loc.slightly),
                    ("uwu", loc.a_lot),
                    ("uvu", loc.extreme),
                    ("max", loc.max_uwu),
                ],
                description=state.owo(loc.uwu_desc),
            )
        )
    options.append(
        select_option(
            "levelbg",
            loc.background.USEBACKGROUND,
            "default_or_v3",
            [
                ("default_or_v3", loc.background.DEF_OR_V3),
                ("v3", loc.background.V3),
                ("default_or_v1", loc.background.DEF_OR_V1),
                ("v1", loc.background.V1),
            ],
            description=state.owo(loc.background.USEBACKGROUNDDESC),
        )
    )
    engines = await resources.engines(state.localization)
    options.append(
        select_option(
            "defaultengine",
            loc.default_engine,
            engines[0].item.name,
            [(engine.item.name, engine.item.title) for engine in engines],
            description=state.owo(loc.default_engine_desc),
        )
    )
    skins = await resources.skins()
    themes = sorted({theme for skin in skins for theme in skin.themes})
    options.append(
        select_option(
            "defaultskin",
            loc.default_skin,
            "engine_default",
            [("engine_default", "#DEFAULT"), *((theme, theme) for theme in themes)],
            description=state.owo(loc.default_skin_desc),
        )
    )
    particles = await resources.particles()
    options.append(
        select_option(
            "defaultparticle",
            loc.default_particle,
            "engine_default",
            [
                ("engine_default", "#DEFAULT"),
                *(
                    (particle.item.name, particle.item.title)
                    for particle in particles
                    if not particle.engine_specific
                ),
            ],
            description=state.owo(loc.default_particle_desc),
        )
    )
    options.append(
        select_option(
            "stpickconfig",
            loc.staff_pick,
            "off",
            staff_pick_values(loc, with_default=False),
            description=state.owo(loc.search.STAFF_PICK_CONFIG_DESC + "\n" + loc.staff_pick_desc),
        )
    )
    options.append(toggle_option("showresourcebuttons", loc.show_resource_buttons, False))

    base_description = loc.server_description or context.config.sonolus.description
    description: str | None = None
    if state.session:
        try:
            me = await context.backend.me(state.session)
        except BackendError:
            me = None
        except (aiohttp.ClientError, TimeoutError, ValidationError):
            logger.exception("could not load the account for the server info")
            me = None
        if me is not None:
            unread = me.unread_notifications
            description = base_description + SEPARATOR + "\n" + loc.welcome(me.account.username)
            if unread == 1:
                notice = loc.notifications_singular(unread)
            elif unread > 0:
                notice = loc.notifications_plural(unread)
            else:
                notice = loc.notification.none
            description += "\n\n" + notice
            if unread > 0:
                buttons = [
                    ServerInfoItemButton(
                        type="post",
                        title=loc.notification.NOTIFICATION,
                        icon="comment",
                        badgeCount=unread,
                        infoType="notifications",
                    )
                ]
            description += SEPARATOR + "\n" + loc.find_in_playlists
            if me.account.is_mod:
                description += SEPARATOR
                if me.account.is_admin:
                    description += f"\n{loc.is_admin}\n\n{loc.admin_powers}\n{loc.mod_powers}"
                else:
                    description += f"\n{loc.is_mod}\n\n{loc.mod_powers}"
    if description is None:
        description = base_description + SEPARATOR + "\n" + loc.not_logged_in

    return respond(
        ServerInfo(
            title=context.config.sonolus.title,
            description=state.owo(description),
            buttons=buttons,
            configuration=ServerConfiguration(options=options),
            banner=banner,
        )
    )
