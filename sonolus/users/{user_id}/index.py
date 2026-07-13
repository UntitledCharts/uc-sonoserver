from fastapi import APIRouter, HTTPException, status

from core import SonolusRequest
from helpers.models.sonolus.item import UserItem
from helpers.models.sonolus.item_section import LevelItemSection
from helpers.models.sonolus.misc import Tag
from helpers.models.sonolus.options import ServerForm, ServerToggleOption
from helpers.models.sonolus.response import ServerItemDetails
from helpers.owoify import handle_item_uwu

router = APIRouter()


@router.get("/", response_model=ServerItemDetails)
async def main(request: SonolusRequest, user_id: str):
    locale = request.state.loc
    auth = request.headers.get("Sonolus-Session")

    profile = await request.app.api.get_user_profile(user_id).send()

    tags = []
    actions = []

    if profile.status == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if profile.data.account.admin:
        tags.append(Tag(title="#ADMIN", icon="crown"))
    elif profile.data.account.mod:
        tags.append(Tag(title="#MODERATOR", icon="crown"))

    if profile.data.account.banned:
        tags.append(Tag(title="#BANNED", icon="lock"))

    if auth and not profile.data.account.admin:
        account = await request.app.api.get_account().send(auth)

        if (
            account.data
            and account.data.admin
            and account.data.sonolus_id != profile.data.account.sonolus_id
        ):
            if profile.data.account.banned:
                actions.append(
                    ServerForm(
                        type="unban",
                        title=locale.unban,
                        icon="unlock",
                        requireConfirmation=True,
                        options=[],
                    )
                )
            else:
                actions.append(
                    ServerForm(
                        type="ban",
                        title=locale.ban,
                        icon="lock",
                        requireConfirmation=True,
                        options=[
                            ServerToggleOption(
                                query="delete",
                                name=locale.ban_delete,
                                description=locale.ban_delete_desc,
                                required=False,
                                default=True,
                            ),
                            ServerToggleOption(
                                query="_",
                                name="#CONFIRM",
                                description=locale.ban_confirm,
                                required=True,
                                default=False,
                            ),
                        ],
                    )
                )

    return ServerItemDetails(
        item=UserItem(
            name=profile.data.account.sonolus_id,
            title=profile.data.account.sonolus_username,
            handle=str(profile.data.account.sonolus_handle),
            tags=tags,
        ),
        actions=actions,
        hasCommunity=False,
        leaderboards=[],
        sections=[
            LevelItemSection(
                title="#POPULAR",
                icon="level",
                items=handle_item_uwu(
                    [
                        await request.app.run_blocking(
                            chart.to_level_item,
                            request,
                            profile.data.asset_base_url,
                            request.state.levelbg,
                        )
                        for chart in profile.data.charts
                    ],
                    request.state.localization,
                    request.state.uwu,
                ),
            )
        ],
    )
