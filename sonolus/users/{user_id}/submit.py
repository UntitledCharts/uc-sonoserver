from fastapi import APIRouter, HTTPException, status

from core import SonolusRequest
from helpers.models.sonolus.response import ServerSubmitItemActionResponse
from helpers.models.sonolus.submit import ServerSubmitUserActionRequest

router = APIRouter()


@router.post("/", response_model=ServerSubmitItemActionResponse)
async def submit(
    request: SonolusRequest, user_id: str, data: ServerSubmitUserActionRequest
):
    locale = request.state.loc
    auth = request.headers.get("Sonolus-Session")

    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=locale.not_logged_in
        )

    parsed_data = data.parse()

    match parsed_data.type:
        case "ban":
            response = await request.app.api.ban_user(user_id, parsed_data.delete).send(
                auth
            )
        case "unban":
            response = await request.app.api.unban_user(user_id).send(auth)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=locale.not_found
            )

    if response.status != 200:
        raise HTTPException(status_code=response.status, detail=locale.not_admin)

    return ServerSubmitItemActionResponse(key="", hashes=[], shouldUpdateItem=True)
