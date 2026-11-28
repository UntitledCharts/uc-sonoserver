from fastapi import APIRouter, Response

from app.errors import SonolusError
from app.state import Context

router = APIRouter()


@router.get("/sonolus/repository/{digest}")
async def repository_file(digest: str, context: Context) -> Response:
    """Serve a stored blob by hash, without a content type like before.

    Args:
        digest: SHA-1 of the blob.
        context: App context.

    Returns:
        Response: The blob bytes.
    """
    data = await context.repository.get_file(digest)
    if not data:
        raise SonolusError(404)
    return Response(content=data)
