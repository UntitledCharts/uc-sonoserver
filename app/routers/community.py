from typing import Annotated

from fastapi import APIRouter, Query, Response
from pydantic import BaseModel, ConfigDict

from app.backend.client import BackendError
from app.backend.error_text import Site, to_sonolus_error
from app.errors import SonolusError
from app.items import comment_item
from app.names import MAX_ROW_ID
from app.routers.common import (
    GenericAction,
    backend,
    can_notify,
    check_page,
    invalid_page,
    notify,
    parse_form,
    require_chart_id,
    respond,
    text_area_option,
)
from app.sonolus_core import (
    ServerForm,
    ServerItemCommunityCommentList,
    ServerItemCommunityInfo,
    ServerSubmitItemCommunityActionRequest,
    ServerSubmitItemCommunityActionResponse,
    ServerSubmitItemCommunityCommentActionRequest,
    ServerSubmitItemCommunityCommentActionResponse,
)
from app.state import Context, State

item_router = APIRouter()


class CommentAction(BaseModel):
    """Values submitted from the comment form.

    Attributes:
        model_config: Ignores unknown values.
        type: Action type.
        content: Comment text.
    """

    model_config = ConfigDict(extra="ignore")

    type: str
    content: str


@item_router.get("/sonolus/levels/{item_name}/community/info")
async def community_info(item_name: str, context: Context, state: State) -> Response:
    """Return a level's newest comments and the comment form.

    Args:
        item_name: Level name.
        context: App context.
        state: Player configuration.

    Returns:
        Response: The community info.
    """
    loc = state.loc
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.DETAIL, loc)
    page = await backend(context.backend.comments(state.session, chart, 0), Site.DETAIL, loc)
    actions: list[ServerForm] = []
    if state.session:
        actions.append(
            ServerForm(
                type="comment",
                title="#COMMENT",
                icon="comment",
                requireConfirmation=False,
                options=[
                    text_area_option(
                        "content",
                        "#COMMENT",
                        "#COMMENT_PLACEHOLDER",
                        context.constants.moderation.comment_limit,
                        required=True,
                    )
                ],
            )
        )
    return respond(
        ServerItemCommunityInfo(
            actions=actions,
            topComments=[comment_item(comment, state, page.can_moderate) for comment in page.items],
        )
    )


@item_router.get("/sonolus/levels/{item_name}/community/comments/list")
async def comments_list(
    item_name: str,
    context: Context,
    state: State,
    page: Annotated[int, Query(ge=0)] = 0,
) -> Response:
    """Return a page of a level's comments.

    Args:
        item_name: Level name.
        context: App context.
        state: Player configuration.
        page: Zero-based page.

    Returns:
        Response: The comments.
    """
    loc = state.loc
    check_page(page, context.constants.lists.max_page)
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.DETAIL, loc)
    result = await backend(context.backend.comments(state.session, chart, page), Site.DETAIL, loc)
    if page > result.page_count:
        raise invalid_page(loc, page, result.page_count)
    return respond(
        ServerItemCommunityCommentList(
            pageCount=result.page_count,
            comments=[
                comment_item(comment, state, result.can_moderate) for comment in result.items
            ],
        )
    )


@item_router.post("/sonolus/levels/{item_name}/community/submit")
async def community_submit(
    item_name: str,
    context: Context,
    state: State,
    body: ServerSubmitItemCommunityActionRequest,
) -> Response:
    """Post a comment on a level.

    Args:
        item_name: Level name.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: Tells the client to refresh the comments.
    """
    loc = state.loc
    form = parse_form(CommentAction, body.values)
    if not state.session:
        raise SonolusError(401, loc.not_logged_in)
    if form.type != "comment":
        raise SonolusError(404, loc.not_found)
    chart = require_chart_id(item_name, context.config.sonolus.chart_prefix, Site.COMMENT_POST, loc)
    await backend(
        context.backend.post_comment(state.session, chart, form.content),
        Site.COMMENT_POST,
        loc,
    )
    return respond(
        ServerSubmitItemCommunityActionResponse(key="", hashes=[], shouldUpdateComments=True)
    )


@item_router.post("/sonolus/levels/{item_name}/community/comments/{comment_id}/submit")
async def comment_submit(
    item_name: str,
    comment_id: int,
    context: Context,
    state: State,
    body: ServerSubmitItemCommunityCommentActionRequest,
) -> Response:
    """Delete a comment, notifying its author when staff deletes it.

    Args:
        item_name: Level name.
        comment_id: Comment id.
        context: App context.
        state: Player configuration.
        body: Submitted form values.

    Returns:
        Response: Tells the client to refresh the comments.
    """
    loc = state.loc
    form = parse_form(GenericAction, body.values)
    session = state.session
    if not session:
        raise SonolusError(401, loc.not_logged_in)
    if form.type != "delete":
        raise SonolusError(404, loc.not_found)
    chart = require_chart_id(
        item_name, context.config.sonolus.chart_prefix, Site.COMMENT_DELETE, loc
    )
    if not 0 < comment_id <= MAX_ROW_ID:
        raise to_sonolus_error(
            BackendError(404, "error.comment.not_found"), Site.COMMENT_DELETE, loc
        )
    deleted = await backend(
        context.backend.delete_comment(session, chart, comment_id),
        Site.COMMENT_DELETE,
        loc,
    )
    author = deleted.author
    if not deleted.is_own and author is not None and await can_notify(context, session):
        await notify(
            context,
            session,
            author.id,
            "Comment Deleted",
            f"#COMMENT_DELETED\n{deleted.content or ''}",
        )
    return respond(
        ServerSubmitItemCommunityCommentActionResponse(key="", hashes=[], shouldUpdateComments=True)
    )
