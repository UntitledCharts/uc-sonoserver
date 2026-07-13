import base64
from typing import Literal
from urllib.parse import parse_qs
from pydantic import BaseModel, SerializerFunctionWrapHandler, model_serializer
from fastapi import HTTPException, status

from core import SonolusRequest
from helpers.models.sonolus.item import ReplayItem


class ServerSubmitItemActionRequest(BaseModel):
    values: str


class _ParsedGenericActionRequest(BaseModel):
    type: str


class GenericActionRequest(ServerSubmitItemActionRequest):
    def parse(self) -> _ParsedGenericActionRequest:
        return _ParsedGenericActionRequest.model_validate(
            {k: v[0] for k, v in parse_qs(self.values).items()}
        )


class _ParsedServerSubmitCommentActionRequest(BaseModel):
    type: str
    content: str


class ServerSubmitCommentActionRequest(ServerSubmitItemActionRequest):
    def parse(self) -> _ParsedServerSubmitCommentActionRequest:
        return _ParsedServerSubmitCommentActionRequest.model_validate(
            {k: v[0] for k, v in parse_qs(self.values).items()}
        )


class _ParsedServerSubmitLevelActionRequest(BaseModel):
    type: str
    visibility: Literal["UNLISTED", "PRIVATE", "PUBLIC", None] = None
    constant: str | None = None


class ServerSubmitLevelActionRequest(ServerSubmitItemActionRequest):
    def parse(self) -> _ParsedServerSubmitLevelActionRequest:
        return _ParsedServerSubmitLevelActionRequest.model_validate(
            {k: v[0] for k, v in parse_qs(self.values).items()}
        )


class _ParsedServerSubmitUserActionRequest(BaseModel):
    type: str
    # unchecked toggles aren't submitted, so this must default to off
    delete: bool = False


class ServerSubmitUserActionRequest(ServerSubmitItemActionRequest):
    def parse(self) -> _ParsedServerSubmitUserActionRequest:
        return _ParsedServerSubmitUserActionRequest.model_validate(
            {k: v[0] for k, v in parse_qs(self.values).items()}
        )


class _ParsedServerSubmitPlaylistActionRequest(BaseModel):
    sort_by: Literal[
        "created_at",
        "rating",
        "likes",
        "comments",
        "decaying_likes",
        "abc",
        "random",
        None,
    ]
    page: int | None
    staff_pick: Literal[True, False, None]
    is_default_staff_pick: bool | None
    min_rating: int | None
    max_rating: int | None
    tags: list[str] | None
    min_likes: int | None
    max_likes: int | None
    min_comments: int | None
    max_comments: int | None
    liked_by: bool | None
    commented_on: bool | None
    title_includes: str | None
    description_includes: str | None
    author_includes: str | None
    artists_includes: str | None
    sort_order: Literal["desc", "asc", None]
    level_status: Literal["ALL", "PUBLIC_MINE", "UNLISTED", "PRIVATE", None]
    keywords: str | None

    @staticmethod
    def _is_int(val: str) -> bool:
        """
        (int).isdigit returns False if the nubmer is negative
        """
        try:
            int(val)
            return True
        except ValueError:
            return False

    @model_serializer(mode="wrap")
    def dump(self, handler: SerializerFunctionWrapHandler, _info):
        data = handler(self)

        data = {k: v for k, v in data.items() if v is not None}

        if data.get("sort_by") == "random" and "page" in data:
            del data["page"]

        if "staff_pick" in data and data["staff_pick"] in (None, True, False):
            data["staff_pick"] = {None: "off", True: "true", False: "false"}[
                data["staff_pick"]
            ]

        if "tags" in data:
            if isinstance(data["tags"], list):
                data["tags"] = ",".join(data["tags"])

        if "liked_by" in data:
            data["liked_by"] = str(int(data["liked_by"]))

        if "commented_on" in data:
            data["commented_on"] = str(int(data["commented_on"]))

        return data

    @classmethod
    def parse(cls, qs: str, request: SonolusRequest, plain_json: bool = False):
        parsed_qs = parse_qs(
            base64.urlsafe_b64decode(qs.encode()) if not plain_json else qs
        )

        if plain_json:
            flattened_data = {k: v[0] for k, v in parsed_qs.items()}
        else:
            flattened_data = {k.decode(): v[0].decode() for k, v in parsed_qs.items()}

        sort_by = flattened_data.get("sort_by")
        allowed_sort_by = [
            "created_at",
            "rating",
            "likes",
            "comments",
            "decaying_likes",
            "abc",
            "random",
        ]
        if sort_by not in allowed_sort_by and sort_by is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value for sort_by. Allowed values are: {', '.join(allowed_sort_by)}.",
            )

        page = flattened_data.get("page") if sort_by != "random" else 1
        if page is not None:
            if isinstance(page, str) and page.isdigit():
                page = int(page)
            if not isinstance(page, int) or page < 1:
                raise HTTPException(
                    status_code=400, detail="page must be a non-negative integer."
                )

        staff_pick = flattened_data.get("staff_pick")

        is_default_staff_pick = staff_pick and staff_pick == "default"

        if staff_pick not in ["off", "default", "true", "false", None]:
            raise HTTPException(status_code=400, detail="Invalid staff_pick.")
        staff_pick = {"off": None, "true": True, "false": False, None: None}[staff_pick]

        min_rating = flattened_data.get("min_rating")
        max_rating = flattened_data.get("max_rating")
        if min_rating is not None:
            if cls._is_int(min_rating):
                min_rating = int(min_rating)
            if not isinstance(min_rating, int):
                raise HTTPException(
                    status_code=400, detail="min_rating must be an integer."
                )
        if max_rating is not None:
            if cls._is_int(max_rating):
                max_rating = int(max_rating)
            if not isinstance(max_rating, int):
                raise HTTPException(
                    status_code=400, detail="max_rating must be an integer."
                )
        if (
            min_rating is not None
            and max_rating is not None
            and min_rating > max_rating
        ):
            raise HTTPException(
                status_code=400,
                detail="min_rating cannot be greater than max_rating.",
            )

        tags = flattened_data.get("tags")
        if tags is not None:
            if not isinstance(tags, str):
                raise HTTPException(
                    status_code=400,
                    detail="tags must be a strings, having comma-separated elements.",
                )
            tags = [tag.strip() for tag in tags.split(",")]

        min_likes = flattened_data.get("min_likes")
        max_likes = flattened_data.get("max_likes")
        if min_likes is not None:
            if min_likes.isdigit():
                min_likes = int(min_likes)
            if not isinstance(min_likes, int) or min_likes < 0:
                raise HTTPException(
                    status_code=400, detail="min_likes must be a non-negative integer."
                )
        if max_likes is not None:
            if max_likes.isdigit():
                max_likes = int(max_likes)
            if not isinstance(max_likes, int) or max_likes < 0:
                raise HTTPException(
                    status_code=400, detail="max_likes must be a non-negative integer."
                )
        if min_likes is not None and max_likes is not None and min_likes > max_likes:
            raise HTTPException(
                status_code=400,
                detail="min_likes cannot be greater than max_likes.",
            )

        min_comments = flattened_data.get("min_comments")
        max_comments = flattened_data.get("max_comments")
        if min_comments is not None:
            if min_comments.isdigit():
                min_comments = int(min_comments)
            if not isinstance(min_comments, int) or min_comments < 0:
                raise HTTPException(
                    status_code=400,
                    detail="min_comments must be a non-negative integer.",
                )
        if max_comments is not None:
            if max_comments.isdigit():
                max_comments = int(max_comments)
            if not isinstance(max_comments, int) or max_comments < 0:
                raise HTTPException(
                    status_code=400,
                    detail="max_comments must be a non-negative integer.",
                )
        if (
            min_comments is not None
            and max_comments is not None
            and min_comments > max_comments
        ):
            raise HTTPException(
                status_code=400,
                detail="min_comments cannot be greater than max_comments.",
            )

        liked_by = flattened_data.get("liked_by")
        if type(liked_by) == str and liked_by.isdigit():
            liked_by = liked_by != "0"
        if not isinstance(liked_by, bool) and liked_by is not None:
            raise HTTPException(status_code=400, detail="liked_by must be a boolean.")

        commented_on = flattened_data.get("commented_on")
        if type(commented_on) == str and commented_on.isdigit():
            commented_on = commented_on != "0"
        if not isinstance(commented_on, bool) and commented_on is not None:
            raise HTTPException(
                status_code=400, detail="commented_on must be a boolean."
            )

        title_includes = flattened_data.get("title_includes")
        if title_includes is not None:
            if not isinstance(title_includes, str):
                raise HTTPException(
                    status_code=400, detail="title_includes must be a string."
                )

        description_includes = flattened_data.get("description_includes")
        if description_includes is not None:
            if not isinstance(description_includes, str):
                raise HTTPException(
                    status_code=400, detail="description_includes must be a string."
                )

        author_includes = flattened_data.get("author_includes")
        if author_includes is not None:
            if not isinstance(author_includes, str):
                raise HTTPException(
                    status_code=400, detail="author_includes must be a string."
                )

        artists_includes = flattened_data.get("artists_includes")
        if artists_includes is not None:
            if not isinstance(artists_includes, str):
                raise HTTPException(
                    status_code=400, detail="artists_includes must be a string."
                )

        sort_order = flattened_data.get("sort_order")
        allowed_sort_order = ["desc", "asc", None]
        if sort_order not in allowed_sort_order:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value for sort_order. Allowed values are: {', '.join(allowed_sort_order)}.",
            )

        level_status = flattened_data.get("level_status")
        if level_status not in ["ALL", "PUBLIC_MINE", "UNLISTED", "PRIVATE", None]:
            raise HTTPException(status_code=400, detail="Invalid level_status.")

        keywords = flattened_data.get("keywords")
        if keywords is not None:
            if not isinstance(keywords, str):
                raise HTTPException(
                    status_code=400, detail="keywords must be a string."
                )

        return _ParsedServerSubmitPlaylistActionRequest(
            sort_by=sort_by,
            page=page,
            staff_pick=staff_pick,
            is_default_staff_pick=is_default_staff_pick,
            min_rating=min_rating,
            max_rating=max_rating,
            tags=tags,
            min_likes=min_likes,
            max_likes=max_likes,
            min_comments=min_comments,
            max_comments=max_comments,
            liked_by=liked_by,
            commented_on=commented_on,
            title_includes=title_includes,
            description_includes=description_includes,
            author_includes=author_includes,
            artists_includes=artists_includes,
            sort_order=sort_order,
            level_status=level_status,
            keywords=keywords,
        )


class ServerSubmitPlaylistActionRequest(ServerSubmitItemActionRequest):
    def parse(
        self, request: SonolusRequest, plain_json: bool = False
    ) -> _ParsedServerSubmitPlaylistActionRequest:
        if len(self.values) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="why so long"
            )

        return _ParsedServerSubmitPlaylistActionRequest.parse(
            self.values, request, plain_json
        )


class ServerSubmitLevelResultRequest(BaseModel):
    replay: ReplayItem
    values: str
