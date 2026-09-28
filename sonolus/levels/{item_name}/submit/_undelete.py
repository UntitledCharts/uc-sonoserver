from core import SonolusRequest
from helpers.models.sonolus.response import ServerSubmitItemActionResponse
from fastapi import HTTPException
from locales.locale import Loc


async def undelete(
    auth: str, request: SonolusRequest, item_name: str, locale: Loc
) -> ServerSubmitItemActionResponse:
    response = await request.app.api.undelete_chart(item_name).send(auth)

    if response.status != 200:
        raise HTTPException(status_code=response.status, detail=locale.not_mod)

    return ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True)
