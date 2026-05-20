from aiohttp import ClientSession, ClientResponse, FormData
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any, Callable, TypeVar, Generic, Awaitable
import decimal

from helpers.models.api.comments import *
from helpers.models.api.charts import *
from helpers.models.api.misc import *
from helpers.models.api.notifications import *
from helpers.models.api.leaderboards import *
from helpers.models.sonolus.account import ServiceUserProfile

T = TypeVar("T", bound=BaseModel | None)


class Response(ClientResponse, Generic[T]):
    data: T


class Request(Generic[T]):
    def __init__(
        self,
        client_session: ClientSession,
        method: str,
        url: str,
        cast_to: type[T] | None,
        json: Any = None,
        params: dict[str, Any] | None = None,
        content: FormData | None = None,
        use_app_auth: tuple[str, str] | None = None,
        not_ok_callback: Callable[[ClientResponse], Awaitable[None]] | None = None,
    ):
        self.client_session = client_session
        self.method = method
        self.url = url
        self.cast_to = cast_to
        self.json = json
        self.params = params
        self.content = content
        self.use_app_auth = use_app_auth
        self.not_ok_callback = not_ok_callback

    async def send(
        self,
        auth: str | None = None,
    ) -> Response[T]:
        headers: dict[str, str] = {}
        if auth:
            headers["authorization"] = auth
        if self.use_app_auth:
            headers[self.use_app_auth[0]] = self.use_app_auth[1]

        async with self.client_session.request(
            self.method,
            self.url,
            params=self.params,
            json=self.json,
            headers=headers,
            data=self.content,
        ) as resp:
            resp: Response[T]

            try:
                if resp.ok and self.cast_to:
                    resp.data = self.cast_to.model_validate(await resp.json())
                    return resp
            except Exception:
                pass

            if not resp.ok and self.not_ok_callback:
                await self.not_ok_callback(resp)

            if resp.status == 422:
                print(await resp.text())

            resp.data = None
            return resp


class API:
    def __init__(self, base_url: str, app_auth_header: str, app_auth: str):
        self._client_session = ClientSession(base_url=base_url)
        self._use_app_auth = (app_auth_header, app_auth)

    def delete_comment(
        self, item_name: str, comment_id: int
    ) -> Request[DeleteCommentResponse]:
        return Request(
            self._client_session,
            "DELETE",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/comment/{comment_id}/",
            DeleteCommentResponse,
        )

    def send_notification(
        self,
        title: str,
        user_id: str | None = None,
        chart_id: str | None = None,
        content: str | None = None,
    ) -> Request[None]:
        return Request(
            self._client_session,
            "POST",
            "/api/accounts/notifications/",
            None,
            json={
                "user_id": user_id,
                "title": title,
                "chart_id": chart_id,
                "content": content,
            },
        )

    def get_comments(
        self, item_name: str, page: int | None = None
    ) -> Request[CommentList]:
        return Request(
            self._client_session,
            "GET",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/comment/",
            CommentList,
            params={"page": str(page)} if page else None,
        )

    def send_comment(self, item_name: str, content: str) -> Request[None]:
        return Request(
            self._client_session,
            "POST",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/comment/",
            None,
            json={"content": content},
        )

    def delete_chart(self, item_name: str) -> Request[DeleteChartResponse]:
        return Request(
            self._client_session,
            "DELETE",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/delete/",
            DeleteChartResponse,
        )

    def like_chart(
        self, item_name: str, type: Literal["like", "unlike"]
    ) -> Request[None]:
        return Request(
            self._client_session,
            "POST",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/like/",
            None,
            json={"type": type},
        )

    def rerate_chart(self, item_name: str, constant: str) -> Request[None]:
        return Request(
            self._client_session,
            "PATCH",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/constant_rate/",
            None,
            json={
                "constant": float(
                    decimal.Decimal(constant).quantize(
                        decimal.Decimal("0.0001"),
                        rounding=decimal.ROUND_HALF_UP,
                    )
                )
            },
        )

    def staff_pick_chart(self, item_name: str, pick: bool) -> Request[None]:
        return Request(
            self._client_session,
            "PATCH",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/stpick/",
            None,
            json={"value": pick},
        )

    def change_chart_visibility(
        self, item_name: str, visibility: Literal["UNLISTED", "PRIVATE", "PUBLIC"]
    ) -> Request[VisibilityChangeResponse]:
        return Request(
            self._client_session,
            "PATCH",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/visibility/",
            VisibilityChangeResponse,
            json={"status": visibility},
        )

    async def _get_chart_not_ok_callback(self, response: ClientResponse):
        data = await response.json()
        detail = data.get("detail") or data.get("message") or "Unknown error"
        raise HTTPException(
            status_code=response.status,
            detail=detail,
        )

    def get_chart(self, item_name: str) -> Request[GetChartResponse]:
        return Request(
            self._client_session,
            "GET",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/",
            GetChartResponse,
            not_ok_callback=self._get_chart_not_ok_callback,
        )

    def get_random_charts(
        self, staff_pick: Literal["off", "true", "false"]
    ) -> Request[RandomChartList]:
        params: dict[str, Any] = {"type": "random"}

        match staff_pick:
            case "true":
                params["staff_pick"] = 1
            case "false":
                params["staff_pick"] = 0

        return Request(
            self._client_session, "GET", "/api/charts/", RandomChartList, params=params
        )

    def get_newest_charts(
        self, staff_pick: Literal["off", "true", "false"]
    ) -> Request[ChartList]:
        params: dict[str, Any] = {"type": "advanced", "sort_by": "published_at"}

        match staff_pick:
            case "true":
                params["staff_pick"] = 1
            case "false":
                params["staff_pick"] = 0

        return Request(
            self._client_session, "GET", "/api/charts/", ChartList, params=params
        )

    def get_random_staff_picks(self, staff_pick: bool) -> Request[RandomChartList]:
        """
        could be replaced with get_random_charts(...) but it's kinda unintuitive
        """
        return Request(
            self._client_session,
            "GET",
            "/api/charts/",
            RandomChartList,
            params={"type": "random", "staff_pick": int(staff_pick)},
        )

    def get_popular_charts(
        self, staff_pick: Literal["off", "true", "false"]
    ) -> Request[ChartList]:
        params: dict[str, Any] = {
            "type": "advanced",
            "sort_by": "decaying_likes",
        }

        match staff_pick:
            case "true":
                params["staff_pick"] = 1
            case "false":
                params["staff_pick"] = 0

        return Request(
            self._client_session, "GET", "/api/charts/", ChartList, params=params
        )

    def charts_quick_search(
        self,
        page: int,
        meta_includes: str | None,
        sort_by: Literal[
            "created_at",
            "published_at",
            "rating",
            "likes",
            "comments",
            "decaying_likes",
            "abc",
            "random",
        ],
        staff_pick: Literal["off", "true", "false", None],
    ) -> Request[ChartList]:
        params: dict[str, Any] = {"type": "quick", "page": page, "sort_by": sort_by}

        if meta_includes:
            params["meta_includes"] = meta_includes
        match staff_pick:
            case "true":
                params["staff_pick"] = 1
            case "false":
                params["staff_pick"] = 0

        return Request(
            self._client_session, "GET", "/api/charts/", ChartList, params=params
        )

    def charts_advanced_search(
        self,
        page: int,
        staff_pick: bool | None,
        min_rating: int | None,
        max_rating: int | None,
        status: Literal["PUBLIC", "PUBLIC_MINE", "UNLISTED", "PRIVATE", "ALL"],
        tags: list[str] | None,
        min_likes: int | None,
        max_likes: int | None,
        min_comments: int | None,
        max_comments: int | None,
        liked_by: bool | None,
        commented_on: bool | None,
        title_includes: str | None,
        description_includes: str | None,
        author_includes: str | None,
        artists_includes: str | None,
        sort_by: Literal[
            "created_at",
            "published_at",
            "rating",
            "likes",
            "comments",
            "decaying_likes",
            "abc",
            "random",
        ],
        sort_order: Literal["desc", "asc", None],
        meta_includes: str | None,
    ) -> Request[ChartList]:
        params = {
            "type": "advanced",
            "page": page if sort_by != "random" else 1,
            "staff_pick": int(staff_pick) if staff_pick is not None else None,
            "min_rating": min_rating,
            "max_rating": max_rating,
            "status": status,
            "tags": tags,
            "min_likes": min_likes,
            "max_likes": max_likes,
            "min_comments": min_comments,
            "max_comments": max_comments,
            "liked_by": int(liked_by) if liked_by is not None else None,
            "commented_on": int(commented_on) if commented_on is not None else None,
            "title_includes": title_includes,
            "description_includes": description_includes,
            "author_includes": author_includes,
            "artists_includes": artists_includes,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "meta_includes": meta_includes,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return Request(
            self._client_session, "GET", "/api/charts/", ChartList, params=params
        )

    def get_notification(self, item_name: str) -> Request[Notification]:
        return Request(
            self._client_session,
            "GET",
            f"/api/accounts/notifications/{item_name.removeprefix('notification-')}/",
            Notification,
        )

    def get_notifications(self, only_unread: bool) -> Request[NotificationList]:
        return Request(
            self._client_session,
            "GET",
            f"/api/accounts/notifications/",
            NotificationList,
            params={"only_unread": int(only_unread)},
        )

    def authenticate(self, profile: ServiceUserProfile) -> Request[AuthenticationData]:
        json = profile.model_dump()
        json["type"] = "game"

        return Request(
            self._client_session,
            "POST",
            "/api/accounts/session/",
            AuthenticationData,
            json=json,
            use_app_auth=self._use_app_auth,
        )

    def authenticate_external(
        self, profile: ServiceUserProfile, id_key: str
    ) -> Request[None]:
        json = profile.model_dump()
        json["type"] = "external"
        json["id_key"] = id_key

        return Request(
            self._client_session,
            "POST",
            "/api/accounts/session/external/",
            None,
            json=json,
            use_app_auth=self._use_app_auth,
        )

    def get_account(self) -> Request[Account]:
        return Request(
            self._client_session, "GET", "/api/accounts/session/account/", Account
        )

    def upload_replay(
        self,
        replay_data: bytes,
        replay_configuration: bytes,
        chart_name: str,
        user_id: str,
        display_name: str,
        engine_name: str,
        speed: float | None,
    ) -> Request[None]:
        content = FormData()

        content.add_field(
            "replay_data", replay_data, content_type="data/gzip", filename="replay_data"
        )
        content.add_field(
            "replay_config",
            replay_configuration,
            content_type="data/gzip",
            filename="replay_configuration",
        )
        content.add_field("user_id", user_id)
        content.add_field("engine_name", engine_name)
        content.add_field("display_name", display_name)

        if speed:
            content.add_field("speed", str(speed))

        return Request(
            self._client_session,
            "POST",
            f"/api/charts/{chart_name.removeprefix('UnCh-')}/leaderboards/",
            None,
            content=content,
            use_app_auth=self._use_app_auth,
        )

    def get_leaderboard_info(
        self, item_name: str, leaderboard_type: leaderboard_type
    ) -> Request[LeaderboardInfo]:
        return Request(
            self._client_session,
            "GET",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/leaderboards/",
            LeaderboardInfo,
            params={"page": 0, "limit": 3, "leaderboard_type": leaderboard_type},
        )

    def get_leaderboards(
        self, item_name: str, leaderboard_type: leaderboard_type, page: int
    ) -> Request[LeaderboardInfo]:
        return Request(
            self._client_session,
            "GET",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/leaderboards/",
            LeaderboardInfo,
            params={"page": page, "limit": 10, "leaderboard_type": leaderboard_type},
        )

    def get_leaderboard_record(
        self, item_name: str, id: int
    ) -> Request[LeaderboardRecordInfo]:
        return Request(
            self._client_session,
            "GET",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/leaderboards/{id}/",
            LeaderboardRecordInfo,
        )

    def delete_leaderboard_record(
        self, item_name: str, id: int
    ) -> Request[DeleteLeaderboardRecord]:
        return Request(
            self._client_session,
            "DELETE",
            f"/api/charts/{item_name.removeprefix('UnCh-')}/leaderboards/{id}/",
            DeleteLeaderboardRecord,
        )

    def get_random_leaderboard_records(
        self, limit: Literal[3, 10]
    ) -> Request[PublicLeaderboardRecordList]:
        return Request(
            self._client_session,
            "GET",
            "/api/charts/leaderboards/random/",
            PublicLeaderboardRecordList,
            params={"limit": limit},
        )

    def get_recent_leaderboard_records(self) -> Request[PublicLeaderboardRecordList]:
        return Request(
            self._client_session,
            "GET",
            "/api/charts/leaderboards/",
            PublicLeaderboardRecordList,
            params={"limit": 3, "page": 0},
        )

    def get_public_leaderboard_records(
        self, page: int
    ) -> Request[PublicLeaderboardRecordList]:
        return Request(
            self._client_session,
            "GET",
            "/api/charts/leaderboards/",
            PublicLeaderboardRecordList,
            params={"limit": 10, "page": page},
        )

    def get_user_profile(self, id: str) -> Request[UserProfile]:
        return Request(self._client_session, "GET", f"/api/accounts/{id}/", UserProfile)
