import json
from collections.abc import Mapping, Sequence
from typing import Any, TypeVar
from urllib.parse import quote

import aiohttp
from pydantic import BaseModel, TypeAdapter
from yarl import URL

from app.backend.models import (
    Chart,
    ChartDetails,
    Comment,
    CommentPage,
    GlobalRecord,
    LeaderboardPage,
    Me,
    NewSession,
    Notification,
    NotificationPage,
    Page,
    Profile,
    PromotionServe,
    RecordDetails,
    ReplaySaved,
)

ModelT = TypeVar("ModelT", bound=BaseModel)
QueryValue = str | int | float | bool
Query = Sequence[tuple[str, QueryValue]] | Mapping[str, QueryValue | None]

CHART_LIST = TypeAdapter(list[Chart])
GLOBAL_RECORD_LIST = TypeAdapter(list[GlobalRecord])

SONOSERVER_KEY_HEADER = "X-SonoServer-Key"
VIEWER_IP_HEADER = "X-Viewer-IP"


class BackendError(Exception):
    """Error response from the chart backend.

    Attributes:
        status: HTTP status of the response.
        code: Error code such as ``error.chart.not_found``.
        params: Error parameters.
    """

    def __init__(self, status: int, code: str, params: dict[str, Any] | None = None) -> None:
        """Create a backend error.

        Args:
            status: HTTP status of the response.
            code: Error code.
            params: Error parameters.
        """
        super().__init__(f"{status} {code}")
        self.status = status
        self.code = code
        self.params = params or {}


def segment(value: str | int) -> str:
    """Percent-encode one URL path segment, dots too when the segment is only dots.

    Args:
        value: Segment value.

    Returns:
        str: The encoded segment.
    """
    encoded = quote(str(value), safe="")
    return encoded.replace(".", "%2E") if encoded in (".", "..") else encoded


def _query_pairs(query: Query | None) -> list[tuple[str, str]]:
    """Turn query values into encoded-ready string pairs, dropping None.

    Args:
        query: Query values.

    Returns:
        list[tuple[str, str]]: The pairs.
    """
    if query is None:
        return []
    items = query.items() if isinstance(query, Mapping) else query
    pairs: list[tuple[str, str]] = []
    for key, value in items:
        if value is None:
            continue
        if isinstance(value, bool):
            pairs.append((key, "true" if value else "false"))
        else:
            pairs.append((key, str(value)))
    return pairs


class BackendClient:
    """Typed calls to the chart backend over one shared session.

    Attributes:
        _http: Shared aiohttp session.
        _base_url: Backend base URL.
        _sonoserver_key: Value of the X-SonoServer-Key header.
    """

    def __init__(self, http: aiohttp.ClientSession, base_url: str, sonoserver_key: str) -> None:
        """Create the client.

        Args:
            http: Shared aiohttp session.
            base_url: Backend base URL without a trailing slash.
            sonoserver_key: Value of the X-SonoServer-Key header.
        """
        self._http = http
        self._base_url = base_url.rstrip("/")
        self._sonoserver_key = sonoserver_key

    async def _request(
        self,
        method: str,
        path: str,
        *,
        session: str | None = None,
        query: Query | None = None,
        json_body: Any = None,
        data: bytes | aiohttp.FormData | None = None,
        headers: dict[str, str] | None = None,
        internal: bool = False,
        viewer_ip: str | None = None,
    ) -> bytes:
        """Send a request and return the body of a successful response.

        Args:
            method: HTTP method.
            path: Path with every dynamic segment already encoded.
            session: Player session forwarded as a bearer token.
            query: Query values.
            json_body: JSON body.
            data: Raw or multipart body.
            headers: Extra headers.
            internal: Send the X-SonoServer-Key header.
            viewer_ip: Player address sent as X-Viewer-IP with internal calls.

        Returns:
            bytes: Response body.
        """
        request_headers = dict(headers or {})
        if session:
            request_headers["Authorization"] = f"Bearer {session}"
        if internal:
            request_headers[SONOSERVER_KEY_HEADER] = self._sonoserver_key
            if viewer_ip:
                request_headers[VIEWER_IP_HEADER] = viewer_ip
        url = URL(self._base_url + path, encoded=True)
        async with self._http.request(
            method,
            url,
            params=_query_pairs(query) or None,
            json=json_body,
            data=data,
            headers=request_headers,
        ) as response:
            body = await response.read()
            if 200 <= response.status < 300:
                return body
            code = "error.unknown"
            params: dict[str, Any] = {}
            try:
                parsed = json.loads(body)
            except ValueError:
                parsed = None
            if isinstance(parsed, dict) and isinstance(parsed.get("error"), str):
                code = parsed["error"]
                if isinstance(parsed.get("params"), dict):
                    params = parsed["params"]
            raise BackendError(response.status, code, params)

    async def me(self, session: str | None) -> Me:
        """Return the logged-in account.

        Args:
            session: Player session.

        Returns:
            Me: The account.
        """
        body = await self._request("GET", "/v1/me", session=session)
        return Me.model_validate_json(body)

    async def chart(
        self, session: str | None, chart_id: str, preview: bool = False
    ) -> ChartDetails:
        """Return a chart with the viewer's permissions.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            preview: Don't count the request as opening the chart.

        Returns:
            ChartDetails: The chart.
        """
        body = await self._request(
            "GET",
            f"/v1/charts/{segment(chart_id)}",
            session=session,
            query={"is_preview": True} if preview else None,
        )
        return ChartDetails.model_validate_json(body)

    async def list_charts(self, session: str | None, query: Query) -> Page[Chart]:
        """Search charts.

        Args:
            session: Player session.
            query: Listing filters.

        Returns:
            Page[Chart]: The page.
        """
        body = await self._request("GET", "/v1/charts", session=session, query=query)
        return Page[Chart].model_validate_json(body)

    async def random_charts(self, session: str | None, staff_pick: bool | None) -> list[Chart]:
        """Pick random public charts.

        Args:
            session: Player session.
            staff_pick: Only picked or unpicked charts, None for both.

        Returns:
            list[Chart]: The charts.
        """
        body = await self._request(
            "GET", "/v1/charts/random", session=session, query={"staff_pick": staff_pick}
        )
        return CHART_LIST.validate_json(body)

    async def set_like(self, session: str | None, chart_id: str, liked: bool) -> None:
        """Like or unlike a chart.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            liked: True to like, False to unlike.
        """
        await self._request(
            "PUT" if liked else "DELETE",
            f"/v1/charts/{segment(chart_id)}/like",
            session=session,
        )

    async def delete_chart(self, session: str | None, chart_id: str) -> None:
        """Delete a chart.

        Args:
            session: Player session.
            chart_id: Validated chart id.
        """
        await self._request("DELETE", f"/v1/charts/{segment(chart_id)}", session=session)

    async def restore_chart(self, session: str | None, chart_id: str) -> None:
        """Restore a deleted chart.

        Args:
            session: Player session.
            chart_id: Validated chart id.
        """
        await self._request("POST", f"/v1/charts/{segment(chart_id)}/restore", session=session)

    async def set_visibility(self, session: str | None, chart_id: str, status: str) -> None:
        """Change a chart's visibility.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            status: PUBLIC, UNLISTED or PRIVATE.
        """
        await self._request(
            "PUT",
            f"/v1/charts/{segment(chart_id)}/visibility",
            session=session,
            json_body={"status": status},
        )

    async def set_rating(self, session: str | None, chart_id: str, rating: float) -> None:
        """Change a chart's rating as staff.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            rating: New rating.
        """
        await self._request(
            "PUT",
            f"/v1/charts/{segment(chart_id)}/rating",
            session=session,
            json_body={"rating": rating},
        )

    async def set_staff_pick(self, session: str | None, chart_id: str, value: bool) -> None:
        """Staff pick or unpick a chart.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            value: New flag.
        """
        await self._request(
            "PUT",
            f"/v1/charts/{segment(chart_id)}/staff-pick",
            session=session,
            json_body={"value": value},
        )

    async def comments(self, session: str | None, chart_id: str, page: int) -> CommentPage:
        """List a chart's comments.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            page: Zero-based page.

        Returns:
            CommentPage: The page.
        """
        body = await self._request(
            "GET",
            f"/v1/charts/{segment(chart_id)}/comments",
            session=session,
            query={"page": page} if page else None,
        )
        return CommentPage.model_validate_json(body)

    async def post_comment(self, session: str | None, chart_id: str, content: str) -> None:
        """Post a comment.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            content: Comment text.
        """
        await self._request(
            "POST",
            f"/v1/charts/{segment(chart_id)}/comments",
            session=session,
            json_body={"content": content},
        )

    async def delete_comment(self, session: str | None, chart_id: str, comment_id: int) -> Comment:
        """Delete a comment.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            comment_id: Comment id.

        Returns:
            Comment: The deleted comment with its text.
        """
        body = await self._request(
            "DELETE",
            f"/v1/charts/{segment(chart_id)}/comments/{segment(comment_id)}",
            session=session,
        )
        return Comment.model_validate_json(body)

    async def leaderboard(
        self, session: str | None, chart_id: str, leaderboard_type: str, page: int, limit: int
    ) -> LeaderboardPage:
        """List a chart's leaderboard.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            leaderboard_type: Ranking.
            page: Zero-based page.
            limit: Records per page.

        Returns:
            LeaderboardPage: The page.
        """
        body = await self._request(
            "GET",
            f"/v1/charts/{segment(chart_id)}/leaderboards",
            session=session,
            query={"page": page, "limit": limit, "leaderboard_type": leaderboard_type},
        )
        return LeaderboardPage.model_validate_json(body)

    async def record(self, session: str | None, chart_id: str, record_id: int) -> RecordDetails:
        """Return a leaderboard record.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            record_id: Record id.

        Returns:
            RecordDetails: The record.
        """
        body = await self._request(
            "GET",
            f"/v1/charts/{segment(chart_id)}/leaderboards/{segment(record_id)}",
            session=session,
        )
        return RecordDetails.model_validate_json(body)

    async def delete_record(
        self, session: str | None, chart_id: str, record_id: int
    ) -> RecordDetails:
        """Delete a leaderboard record.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            record_id: Record id.

        Returns:
            RecordDetails: The deleted record.
        """
        body = await self._request(
            "DELETE",
            f"/v1/charts/{segment(chart_id)}/leaderboards/{segment(record_id)}",
            session=session,
        )
        return RecordDetails.model_validate_json(body)

    async def recent_records(self, page: int, limit: int) -> Page[GlobalRecord]:
        """List the newest public records.

        Args:
            page: Zero-based page.
            limit: Records per page.

        Returns:
            Page[GlobalRecord]: The page.
        """
        body = await self._request(
            "GET", "/v1/leaderboards/recent", query={"page": page, "limit": limit}
        )
        return Page[GlobalRecord].model_validate_json(body)

    async def random_records(self, limit: int) -> list[GlobalRecord]:
        """Pick random public records.

        Args:
            limit: Records to return.

        Returns:
            list[GlobalRecord]: The records.
        """
        body = await self._request("GET", "/v1/leaderboards/random", query={"limit": limit})
        return GLOBAL_RECORD_LIST.validate_json(body)

    async def notifications(
        self, session: str | None, page: int, only_unread: bool
    ) -> NotificationPage:
        """List the player's notifications.

        Args:
            session: Player session.
            page: Zero-based page.
            only_unread: Only unread notifications.

        Returns:
            NotificationPage: The page.
        """
        body = await self._request(
            "GET",
            "/v1/me/notifications",
            session=session,
            query={"page": page, "only_unread": only_unread},
        )
        return NotificationPage.model_validate_json(body)

    async def notification_window(
        self, session: str | None, offset: int, limit: int
    ) -> NotificationPage:
        """List the player's notifications from an offset, newest first.

        Args:
            session: Player session.
            offset: Index of the first notification.
            limit: Notifications to return, at most the backend's maximum.

        Returns:
            NotificationPage: The notifications, with its page count counted in pages of limit.
        """
        body = await self._request(
            "GET",
            "/v1/me/notifications",
            session=session,
            query={"offset": offset, "limit": limit, "only_unread": False},
        )
        return NotificationPage.model_validate_json(body)

    async def notification(self, session: str | None, notification_id: int) -> Notification:
        """Open a notification, marking it read.

        Args:
            session: Player session.
            notification_id: Notification id.

        Returns:
            Notification: The notification with its content.
        """
        body = await self._request(
            "GET", f"/v1/me/notifications/{segment(notification_id)}", session=session
        )
        return Notification.model_validate_json(body)

    async def send_notification(
        self, session: str | None, account_id: str, title: str, content: str
    ) -> None:
        """Send a notification as staff.

        Args:
            session: Player session of the acting staff member.
            account_id: Recipient account id.
            title: Title.
            content: Body text.
        """
        await self._request(
            "POST",
            "/v1/notifications",
            session=session,
            json_body={"account_id": account_id, "title": title, "content": content},
        )

    async def profile(self, account_id: str) -> Profile:
        """Return a public profile.

        Args:
            account_id: Account id.

        Returns:
            Profile: The profile.
        """
        body = await self._request("GET", f"/v1/accounts/{segment(account_id)}")
        return Profile.model_validate_json(body)

    async def ban(self, session: str | None, account_id: str, delete: bool) -> None:
        """Ban an account.

        Args:
            session: Player session of the acting admin.
            account_id: Account id.
            delete: Also schedule the account's content for deletion.
        """
        await self._request(
            "PUT",
            f"/v1/accounts/{segment(account_id)}/ban",
            session=session,
            json_body={"delete": delete},
        )

    async def unban(self, session: str | None, account_id: str) -> None:
        """Unban an account.

        Args:
            session: Player session of the acting admin.
            account_id: Account id.
        """
        await self._request("DELETE", f"/v1/accounts/{segment(account_id)}/ban", session=session)

    async def game_session(self, body: bytes, signature: str | None) -> NewSession:
        """Log in with a body Sonolus signed.

        Args:
            body: Raw request body exactly as received.
            signature: Sonolus-Signature header.

        Returns:
            NewSession: The game session.
        """
        headers = {"Content-Type": "application/json"}
        if signature is not None:
            headers["Sonolus-Signature"] = signature
        response = await self._request("POST", "/v1/sessions/game", data=body, headers=headers)
        return NewSession.model_validate_json(response)

    async def approve_login(self, request_id: str, body: bytes, signature: str | None) -> None:
        """Approve a website login with a body Sonolus signed.

        Args:
            request_id: Login request id.
            body: Raw request body exactly as received.
            signature: Sonolus-Signature header.
        """
        headers = {"Content-Type": "application/json"}
        if signature is not None:
            headers["Sonolus-Signature"] = signature
        await self._request(
            "POST",
            f"/v1/sessions/website/login-requests/{segment(request_id)}/approve",
            data=body,
            headers=headers,
        )

    async def serve_promotion(self, session: str | None, viewer_ip: str | None) -> PromotionServe:
        """Maybe pick a promotion for the player.

        Args:
            session: Player session.
            viewer_ip: Player address.

        Returns:
            PromotionServe: The promotion, or none.
        """
        body = await self._request(
            "POST",
            "/v1/promotions/serve",
            session=session,
            internal=True,
            viewer_ip=viewer_ip,
        )
        return PromotionServe.model_validate_json(body)

    async def click_promotion(self, session: str | None, chart_id: str, view_code: str) -> None:
        """Count the player opening a served promotion.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            view_code: View code from the serve response.
        """
        await self._request(
            "POST",
            "/v1/promotions/clicks",
            session=session,
            json_body={"chart_id": chart_id, "view_code": view_code},
        )

    async def submit_replay(
        self,
        session: str | None,
        chart_id: str,
        display_name: str,
        engine_name: str,
        replay_data: bytes,
        replay_config: bytes,
        speed: float,
    ) -> ReplaySaved:
        """Save the player's replay as their record if it beats the old one.

        Args:
            session: Player session.
            chart_id: Validated chart id.
            display_name: Name shown on the leaderboard.
            engine_name: Engine the replay was played on.
            replay_data: Gzipped replay data.
            replay_config: Gzipped replay configuration.
            speed: Playback speed.

        Returns:
            ReplaySaved: Whether the record changed.
        """
        form = aiohttp.FormData()
        form.add_field("chart_id", chart_id)
        form.add_field("display_name", display_name)
        form.add_field("engine_name", engine_name)
        form.add_field("speed", str(speed))
        form.add_field(
            "replay_data", replay_data, content_type="application/gzip", filename="replay_data"
        )
        form.add_field(
            "replay_config",
            replay_config,
            content_type="application/gzip",
            filename="replay_configuration",
        )
        body = await self._request(
            "POST", "/v1/internal/replays", session=session, data=form, internal=True
        )
        return ReplaySaved.model_validate_json(body)
