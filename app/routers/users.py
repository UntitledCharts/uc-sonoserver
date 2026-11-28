from fastapi import APIRouter, Response
from pydantic import BaseModel, ConfigDict, Field

from app.backend.client import BackendError
from app.backend.error_text import Site, to_sonolus_error
from app.errors import SonolusError
from app.items import account_tags, level_kit, uwu_levels
from app.names import ACCOUNT_ID_PATTERN
from app.routers.common import (
    LevelSection,
    backend,
    parse_form,
    require_session,
    respond,
    toggle_option,
)
from app.sonolus_core import (
    ServerForm,
    ServerItemDetails,
    ServerSubmitItemActionRequest,
    ServerSubmitItemActionResponse,
    UserItem,
)
from app.state import Context, State

item_router = APIRouter()


class UserAction(BaseModel):
    """Values submitted from a user action form.

    Attributes:
        model_config: Ignores unknown values.
        type: Action type.
        delete: Also delete the account's content when banning.
        confirmed: The ``#CONFIRM`` toggle.
    """

    model_config = ConfigDict(extra="ignore")

    type: str
    delete: bool = False
    confirmed: bool = Field(default=False, alias="_")


@item_router.get("/sonolus/users/{user_id}")
async def user_details(user_id: str, context: Context, state: State) -> Response:
    """Return a user with their most liked levels and the ban actions for admins.

    Args:
        user_id: Sonolus account id.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The user details.
    """
    loc = state.loc
    if not ACCOUNT_ID_PATTERN.fullmatch(user_id):
        raise SonolusError(404)
    try:
        profile = await context.backend.profile(user_id)
    except BackendError as error:
        if error.status == 404:
            raise SonolusError(404) from None
        raise to_sonolus_error(error, Site.DETAIL, loc) from None
    account = profile.account
    actions: list[ServerForm] = []
    if state.session and not account.is_admin:
        try:
            me = await context.backend.me(state.session)
        except BackendError:
            me = None
        if me is not None and me.account.is_admin and me.account.id != account.id:
            if account.banned:
                actions.append(
                    ServerForm(
                        type="unban",
                        title=loc.unban,
                        icon="unlock",
                        requireConfirmation=True,
                        options=[],
                    )
                )
            else:
                actions.append(
                    ServerForm(
                        type="ban",
                        title=loc.ban,
                        icon="lock",
                        requireConfirmation=True,
                        options=[
                            toggle_option(
                                "delete",
                                loc.ban_delete,
                                True,
                                description=loc.ban_delete_desc,
                            ),
                            toggle_option(
                                "_",
                                "#CONFIRM",
                                False,
                                description=loc.ban_confirm,
                                required=True,
                            ),
                        ],
                    )
                )
    kit = await level_kit(context, state)
    levels = uwu_levels([kit.level(chart) for chart in profile.charts], state)
    return respond(
        ServerItemDetails[UserItem](
            item=UserItem(
                name=account.id,
                title=account.username,
                handle=str(account.handle),
                tags=account_tags(account),
            ),
            actions=actions,
            hasCommunity=False,
            leaderboards=[],
            sections=[LevelSection(title="#POPULAR", icon="level", itemType="level", items=levels)],
        )
    )


@item_router.post("/sonolus/users/{user_id}/submit")
async def user_submit(
    user_id: str, context: Context, state: State, body: ServerSubmitItemActionRequest
) -> Response:
    """Ban or unban a user.

    Args:
        user_id: Sonolus account id.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: Tells the client to refresh the user.
    """
    loc = state.loc
    session = require_session(state)
    form = parse_form(UserAction, body.values)
    if form.type in ("ban", "unban") and not ACCOUNT_ID_PATTERN.fullmatch(user_id):
        raise to_sonolus_error(
            BackendError(404, "error.account.not_found"), Site.ACCOUNT_MODERATION, loc
        )
    match form.type:
        case "ban":
            if not form.confirmed:
                raise SonolusError(400, loc.ban_confirm)
            await backend(
                context.backend.ban(session, user_id, form.delete),
                Site.ACCOUNT_MODERATION,
                loc,
            )
        case "unban":
            await backend(context.backend.unban(session, user_id), Site.ACCOUNT_MODERATION, loc)
        case _:
            raise SonolusError(404, loc.not_found)
    return respond(ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True))
