import json
from pathlib import Path
from typing import Any

SUPPORTED_LOCALES = (
    "el",
    "en",
    "es",
    "fr",
    "id",
    "it",
    "ja",
    "ko",
    "ru",
    "tr",
    "pt",
    "zh-cn",
    "zh-TW",
    "vi",
    "tl",
)

LOCALE_ALIASES = {"zhs": "zh-cn", "zht": "zh-TW"}


class _Group:
    """Nested group of locale texts with a per-key English fallback.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading from the root mapping to this group.
    """

    def __init__(
        self, data: dict[str, Any], default: dict[str, Any], path: tuple[str, ...]
    ) -> None:
        """Create a group view.

        Args:
            data: Whole mapping of the locale.
            default: Whole English mapping used as the fallback.
            path: Keys leading from the root mapping to this group.
        """
        self._data = data
        self._default = default
        self._path = path

    @staticmethod
    def _lookup(mapping: dict[str, Any], path: tuple[str, ...], key: str) -> Any:
        """Read a key below a group path, raising KeyError when any part is missing.

        Args:
            mapping: Root mapping.
            path: Group keys.
            key: Text key.

        Returns:
            Any: The stored value.
        """
        node: Any = mapping
        for part in path:
            node = node[part]
        return node[key]

    def _get(self, key: str) -> str:
        """Read a text, falling back to English when the locale lacks it.

        Args:
            key: Text key.

        Returns:
            str: The text.
        """
        try:
            return self._lookup(self._data, self._path, key)
        except KeyError:
            return self._lookup(self._default, self._path, key)


class LeaderboardTexts(_Group):
    """Texts of the ``leaderboard`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
    """

    @property
    def YOU_ARE_BANNED(self) -> str:
        """The ``YOU_ARE_BANNED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("YOU_ARE_BANNED")

    @property
    def ARCADE_SCORE_SPEED(self) -> str:
        """The ``ARCADE_SCORE_SPEED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ARCADE_SCORE_SPEED")

    @property
    def ACCURACY_SCORE(self) -> str:
        """The ``ACCURACY_SCORE`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ACCURACY_SCORE")

    @property
    def ARCADE_SCORE_NO_SPEED(self) -> str:
        """The ``ARCADE_SCORE_NO_SPEED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ARCADE_SCORE_NO_SPEED")

    @property
    def RANK_MATCH(self) -> str:
        """The ``RANK_MATCH`` text.

        Returns:
            str: The localized text.
        """
        return self._get("RANK_MATCH")

    @property
    def LEAST_COMBO_BREAKS(self) -> str:
        """The ``LEAST_COMBO_BREAKS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("LEAST_COMBO_BREAKS")

    @property
    def LEAST_MISSES(self) -> str:
        """The ``LEAST_MISSES`` text.

        Returns:
            str: The localized text.
        """
        return self._get("LEAST_MISSES")

    @property
    def PERFECT(self) -> str:
        """The ``PERFECT`` text.

        Returns:
            str: The localized text.
        """
        return self._get("PERFECT")

    def BAD_ENGINE(self, engine_name: str) -> str:
        """The ``BAD_ENGINE`` text with its placeholders filled.

        Args:
            engine_name: Engine name.

        Returns:
            str: The localized text.
        """
        return self._get("BAD_ENGINE").format(engine_name=engine_name)


class PlaylistTexts(_Group):
    """Texts of the ``playlist`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
    """

    @property
    def UPLOADED(self) -> str:
        """The ``UPLOADED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("UPLOADED")

    @property
    def UPLOADEDSUB(self) -> str:
        """The ``UPLOADEDSUB`` text.

        Returns:
            str: The localized text.
        """
        return self._get("UPLOADEDSUB")


class BackgroundTexts(_Group):
    """Texts of the ``background`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
    """

    @property
    def UPLOADED(self) -> str:
        """The ``UPLOADED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("UPLOADED")

    @property
    def USEBACKGROUNDDESC(self) -> str:
        """The ``USEBACKGROUNDDESC`` text.

        Returns:
            str: The localized text.
        """
        return self._get("USEBACKGROUNDDESC")

    @property
    def USEBACKGROUND(self) -> str:
        """The ``USEBACKGROUND`` text.

        Returns:
            str: The localized text.
        """
        return self._get("USEBACKGROUND")

    @property
    def V1(self) -> str:
        """The ``V1`` text.

        Returns:
            str: The localized text.
        """
        return self._get("V1")

    @property
    def V3(self) -> str:
        """The ``V3`` text.

        Returns:
            str: The localized text.
        """
        return self._get("V3")

    @property
    def DEF_OR_V1(self) -> str:
        """The ``DEF_OR_V1`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DEF_OR_V1")

    @property
    def DEF_OR_V3(self) -> str:
        """The ``DEF_OR_V3`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DEF_OR_V3")

    @property
    def BACKGROUNDSELECT(self) -> str:
        """The ``BACKGROUNDSELECT`` text.

        Returns:
            str: The localized text.
        """
        return self._get("BACKGROUNDSELECT")

    @property
    def BACKGROUNDSELECTSUB(self) -> str:
        """The ``BACKGROUNDSELECTSUB`` text.

        Returns:
            str: The localized text.
        """
        return self._get("BACKGROUNDSELECTSUB")


class SearchTexts(_Group):
    """Texts of the ``search`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
    """

    def FILTERS(self, page: int, max_page: int) -> str:
        """The ``FILTERS`` text with its placeholders filled.

        Args:
            page: Page number.
            max_page: Page count.

        Returns:
            str: The localized text.
        """
        return self._get("FILTERS").format(page=f"{page:,}", pageCount=f"{max_page:,}")

    @property
    def VISIBILITY(self) -> str:
        """The ``VISIBILITY`` text.

        Returns:
            str: The localized text.
        """
        return self._get("VISIBILITY")

    @property
    def VISIBILITY_ALL(self) -> str:
        """The ``VISIBILITY_ALL`` text.

        Returns:
            str: The localized text.
        """
        return self._get("VISIBILITY_ALL")

    @property
    def VISIBILITY_PUBLIC(self) -> str:
        """The ``VISIBILITY_PUBLIC`` text.

        Returns:
            str: The localized text.
        """
        return self._get("VISIBILITY_PUBLIC")

    @property
    def VISIBILITY_UNLISTED(self) -> str:
        """The ``VISIBILITY_UNLISTED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("VISIBILITY_UNLISTED")

    @property
    def VISIBILITY_PRIVATE(self) -> str:
        """The ``VISIBILITY_PRIVATE`` text.

        Returns:
            str: The localized text.
        """
        return self._get("VISIBILITY_PRIVATE")

    @property
    def ADVANCED_SEARCH(self) -> str:
        """The ``ADVANCED_SEARCH`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ADVANCED_SEARCH")

    @property
    def MIN_RATING(self) -> str:
        """The ``MIN_RATING`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MIN_RATING")

    @property
    def MAX_RATING(self) -> str:
        """The ``MAX_RATING`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MAX_RATING")

    @property
    def TITLE_CONTAINS(self) -> str:
        """The ``TITLE_CONTAINS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("TITLE_CONTAINS")

    @property
    def DESCRIPTION_CONTAINS(self) -> str:
        """The ``DESCRIPTION_CONTAINS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DESCRIPTION_CONTAINS")

    @property
    def ARTISTS_CONTAINS(self) -> str:
        """The ``ARTISTS_CONTAINS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ARTISTS_CONTAINS")

    @property
    def AUTHOR_CONTAINS(self) -> str:
        """The ``AUTHOR_CONTAINS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("AUTHOR_CONTAINS")

    @property
    def ONLY_LEVELS_I_LIKED(self) -> str:
        """The ``ONLY_LEVELS_I_LIKED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ONLY_LEVELS_I_LIKED")

    @property
    def MIN_LIKES(self) -> str:
        """The ``MIN_LIKES`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MIN_LIKES")

    @property
    def MAX_LIKES(self) -> str:
        """The ``MAX_LIKES`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MAX_LIKES")

    @property
    def STAFF_PICK_DESC(self) -> str:
        """The ``STAFF_PICK_SEARCH_DESC`` text.

        Returns:
            str: The localized text.
        """
        return self._get("STAFF_PICK_SEARCH_DESC")

    @property
    def STAFF_PICK_CONFIG_DESC(self) -> str:
        """The ``STAFF_PICK_CONFIG_DESC`` text.

        Returns:
            str: The localized text.
        """
        return self._get("STAFF_PICK_CONFIG_DESC")

    @property
    def STAFF_PICK_OFF(self) -> str:
        """The ``STAFF_PICK_OFF`` text.

        Returns:
            str: The localized text.
        """
        return self._get("STAFF_PICK_OFF")

    @property
    def STAFF_PICK_TRUE(self) -> str:
        """The ``STAFF_PICK_TRUE`` text.

        Returns:
            str: The localized text.
        """
        return self._get("STAFF_PICK_TRUE")

    @property
    def STAFF_PICK_FALSE(self) -> str:
        """The ``STAFF_PICK_FALSE`` text.

        Returns:
            str: The localized text.
        """
        return self._get("STAFF_PICK_FALSE")

    @property
    def ONLY_LEVELS_I_COMMENTED_ON(self) -> str:
        """The ``ONLY_LEVELS_I_COMMENTED_ON`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ONLY_LEVELS_I_COMMENTED_ON")

    @property
    def COMMENTS(self) -> str:
        """The ``COMMENTS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("COMMENTS")

    @property
    def MIN_COMMENTS(self) -> str:
        """The ``MIN_COMMENTS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MIN_COMMENTS")

    @property
    def MAX_COMMENTS(self) -> str:
        """The ``MAX_COMMENTS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("MAX_COMMENTS")

    @property
    def TAGS_COMMA_SEPARATED(self) -> str:
        """The ``TAGS_COMMA_SEPARATED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("TAGS_COMMA_SEPARATED")

    @property
    def ENTER_TEXT(self) -> str:
        """The ``ENTER_TEXT`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ENTER_TEXT")

    @property
    def ENTER_TAGS(self) -> str:
        """The ``ENTER_TAGS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ENTER_TAGS")

    @property
    def SORT_BY(self) -> str:
        """The ``SORT_BY`` text.

        Returns:
            str: The localized text.
        """
        return self._get("SORT_BY")

    @property
    def SORT_BY_DESCRIPTION(self) -> str:
        """The ``SORT_BY_DESCRIPTION`` text.

        Returns:
            str: The localized text.
        """
        return self._get("SORT_BY_DESCRIPTION")

    @property
    def DATE_CREATED(self) -> str:
        """The ``DATE_CREATED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DATE_CREATED")

    @property
    def DATE_PUBLISHED(self) -> str:
        """The ``DATE_PUBLISHED`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DATE_PUBLISHED")

    @property
    def RATING(self) -> str:
        """The ``RATING`` text.

        Returns:
            str: The localized text.
        """
        return self._get("RATING")

    @property
    def LIKES(self) -> str:
        """The ``LIKES`` text.

        Returns:
            str: The localized text.
        """
        return self._get("LIKES")

    @property
    def DECAYING_LIKES(self) -> str:
        """The ``DECAYING_LIKES`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DECAYING_LIKES")

    @property
    def TITLE_A_Z(self) -> str:
        """The ``TITLE_A_Z`` text.

        Returns:
            str: The localized text.
        """
        return self._get("TITLE_A_Z")

    @property
    def SORT_ORDER(self) -> str:
        """The ``SORT_ORDER`` text.

        Returns:
            str: The localized text.
        """
        return self._get("SORT_ORDER")

    @property
    def DESCENDING(self) -> str:
        """The ``DESCENDING`` text.

        Returns:
            str: The localized text.
        """
        return self._get("DESCENDING")

    @property
    def ASCENDING(self) -> str:
        """The ``ASCENDING`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ASCENDING")


class NotificationTemplateTexts(_Group):
    """Texts of the ``notification.templates`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
    """

    def CHART_VISIBILITY_CHANGED(self, chart_name: str, visibility_status: str) -> str:
        """The ``CHART_VISIBILITY_CHANGED`` text with its placeholders filled.

        Args:
            chart_name: Chart title.
            visibility_status: New visibility.

        Returns:
            str: The localized text.
        """
        return self._get("CHART_VISIBILITY_CHANGED").format(
            chart_name=chart_name, visibility_status=visibility_status
        )

    def COMMENT_DELETED(self, comment_content: str) -> str:
        """The ``COMMENT_DELETED`` text with its placeholders filled.

        Args:
            comment_content: Deleted comment text.

        Returns:
            str: The localized text.
        """
        return self._get("COMMENT_DELETED").format(comment_content=comment_content)

    def CHART_DELETED(self, chart_name: str) -> str:
        """The ``CHART_DELETED`` text with its placeholders filled.

        Args:
            chart_name: Chart title.

        Returns:
            str: The localized text.
        """
        return self._get("CHART_DELETED").format(chart_name=chart_name)

    def LEADERBOARD_SCORE_DELETED(self, chart_name: str) -> str:
        """The ``LEADERBOARD_SCORE_DELETED`` text with its placeholders filled.

        Args:
            chart_name: Chart title.

        Returns:
            str: The localized text.
        """
        return self._get("LEADERBOARD_SCORE_DELETED").format(chart_name=chart_name)


class NotificationTexts(_Group):
    """Texts of the ``notification`` group.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Keys leading to this group.
        templates: Notification body templates.
    """

    def __init__(
        self, data: dict[str, Any], default: dict[str, Any], path: tuple[str, ...]
    ) -> None:
        """Create the group view and its templates.

        Args:
            data: Whole mapping of the locale.
            default: Whole English mapping used as the fallback.
            path: Keys leading from the root mapping to this group.
        """
        super().__init__(data, default, path)
        self.templates = NotificationTemplateTexts(data, default, (*path, "templates"))

    @property
    def READ_STATUS(self) -> str:
        """The ``READ_STATUS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("READ_STATUS")

    @property
    def UNREAD_STATUS(self) -> str:
        """The ``UNREAD_STATUS`` text.

        Returns:
            str: The localized text.
        """
        return self._get("UNREAD_STATUS")

    @property
    def NOTIFICATION(self) -> str:
        """The ``NOTIFICATION`` text.

        Returns:
            str: The localized text.
        """
        return self._get("NOTIFICATION")

    @property
    def NOTIFICATION_DESC_UNREAD(self) -> str:
        """The ``NOTIFICATION_DESC_UNREAD`` text.

        Returns:
            str: The localized text.
        """
        return self._get("NOTIFICATION_DESC_UNREAD")

    @property
    def NOTIFICATION_DESC(self) -> str:
        """The ``NOTIFICATION_DESC`` text.

        Returns:
            str: The localized text.
        """
        return self._get("NOTIFICATION_DESC")

    @property
    def UNREAD(self) -> str:
        """The ``UNREAD`` text.

        Returns:
            str: The localized text.
        """
        return self._get("UNREAD")

    @property
    def none(self) -> str:
        """The ``none`` text.

        Returns:
            str: The localized text.
        """
        return self._get("none")

    @property
    def none_past(self) -> str:
        """The ``none_past`` text.

        Returns:
            str: The localized text.
        """
        return self._get("none_past")


class Loc(_Group):
    """Every text of one locale, falling back to English per key.

    Attributes:
        _data: Whole mapping of the locale.
        _default: Whole English mapping used as the fallback.
        _path: Empty, the root group.
        search: Search form texts.
        playlist: Playlist texts.
        background: Background texts.
        notification: Notification texts.
        leaderboards: Leaderboard texts.
    """

    def __init__(self, data: dict[str, Any], default: dict[str, Any]) -> None:
        """Create the locale and its groups.

        Args:
            data: Mapping read from the locale file.
            default: English mapping used as the fallback, empty for English itself.
        """
        super().__init__(data, default, ())
        self.search = SearchTexts(data, default, ("search",))
        self.playlist = PlaylistTexts(data, default, ("playlist",))
        self.background = BackgroundTexts(data, default, ("background",))
        self.notification = NotificationTexts(data, default, ("notification",))
        self.leaderboards = LeaderboardTexts(data, default, ("leaderboard",))

    @property
    def data(self) -> dict[str, Any]:
        """The raw mapping read from the locale file.

        Returns:
            dict[str, Any]: The mapping.
        """
        return self._data

    def _lines(self, key: str) -> list[str]:
        """Read a list of lines, falling back to English.

        Args:
            key: Text key.

        Returns:
            list[str]: The lines.
        """
        try:
            return self._data[key]
        except KeyError:
            return self._default[key]

    def invalid_page_plural(self, page: int, max_page: int) -> str:
        """The ``invalid_page_plural`` text with its placeholders filled.

        Args:
            page: Page number.
            max_page: Page count.

        Returns:
            str: The localized text.
        """
        return self._get("invalid_page_plural").format(page=f"{page:,}", max_page=f"{max_page:,}")

    def invalid_page_singular(self, page: int, max_page: int) -> str:
        """The ``invalid_page_singular`` text with its placeholders filled.

        Args:
            page: Page number.
            max_page: Page count.

        Returns:
            str: The localized text.
        """
        return self._get("invalid_page_singular").format(page=f"{page:,}", max_page=f"{max_page:,}")

    @property
    def not_mod(self) -> str:
        """The ``not_mod`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_mod")

    @property
    def not_mod_or_owner(self) -> str:
        """The ``not_mod_or_owner`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_mod_or_owner")

    @property
    def is_mod(self) -> str:
        """The ``is_mod`` text.

        Returns:
            str: The localized text.
        """
        return self._get("is_mod")

    @property
    def not_admin(self) -> str:
        """The ``not_admin`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_admin")

    @property
    def is_admin(self) -> str:
        """The ``is_admin`` text.

        Returns:
            str: The localized text.
        """
        return self._get("is_admin")

    @property
    def not_admin_or_owner(self) -> str:
        """The ``not_admin_or_owner`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_admin_or_owner")

    @property
    def staff_pick(self) -> str:
        """The ``staff_pick`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick")

    @property
    def off(self) -> str:
        """The ``off`` text.

        Returns:
            str: The localized text.
        """
        return self._get("off")

    @property
    def on(self) -> str:
        """The ``on`` text.

        Returns:
            str: The localized text.
        """
        return self._get("on")

    def like(self, num: int) -> str:
        """The ``like`` text with its placeholders filled.

        Args:
            num: Count.

        Returns:
            str: The localized text.
        """
        return self._get("like").format(num=f"{num:,}")

    def unlike(self, num: int) -> str:
        """The ``unlike`` text with its placeholders filled.

        Args:
            num: Count.

        Returns:
            str: The localized text.
        """
        return self._get("unlike").format(num=f"{num:,}")

    def notifications_singular(self, num: int) -> str:
        """The ``notifications_singular`` text with its placeholders filled.

        Args:
            num: Count.

        Returns:
            str: The localized text.
        """
        return self._get("notifications_singular").format(num=f"{num:,}")

    def notifications_plural(self, num: int) -> str:
        """The ``notifications_plural`` text with its placeholders filled.

        Args:
            num: Count.

        Returns:
            str: The localized text.
        """
        return self._get("notifications_plural").format(num=f"{num:,}")

    @property
    def find_in_playlists(self) -> str:
        """The ``find_in_playlists`` text.

        Returns:
            str: The localized text.
        """
        return self._get("find_in_playlists")

    @property
    def staff_pick_desc(self) -> str:
        """The ``staff_pick_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick_desc")

    @property
    def non_staff_pick_desc(self) -> str:
        """The ``non_staff_pick_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("non_staff_pick_desc")

    @property
    def staff_pick_notice(self) -> str:
        """The ``staff_pick_notice`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick_notice")

    @property
    def staff_pick_confirm(self) -> str:
        """The ``staff_pick_confirm`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick_confirm")

    @property
    def staff_pick_add(self) -> str:
        """The ``staff_pick_add`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick_add")

    @property
    def staff_pick_remove(self) -> str:
        """The ``staff_pick_remove`` text.

        Returns:
            str: The localized text.
        """
        return self._get("staff_pick_remove")

    @property
    def undelete(self) -> str:
        """The ``undelete`` text.

        Returns:
            str: The localized text.
        """
        return self._get("undelete")

    @property
    def promoted(self) -> str:
        """The ``promoted`` text.

        Returns:
            str: The localized text.
        """
        return self._get("promoted")

    @property
    def make_public(self) -> str:
        """The ``make_public`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public")

    @property
    def make_public_confirm_finished(self) -> str:
        """The ``make_public_confirm_finished`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_finished")

    @property
    def make_public_confirm_jacket(self) -> str:
        """The ``make_public_confirm_jacket`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_jacket")

    @property
    def make_public_confirm_title(self) -> str:
        """The ``make_public_confirm_title`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_title")

    @property
    def make_public_confirm_bpm(self) -> str:
        """The ``make_public_confirm_bpm`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_bpm")

    @property
    def make_public_confirm_desc(self) -> str:
        """The ``make_public_confirm_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_desc")

    @property
    def make_public_confirm_bpm_desc(self) -> str:
        """The ``make_public_confirm_bpm_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_bpm_desc")

    @property
    def make_public_confirm_required(self) -> str:
        """The ``make_public_confirm_required`` text.

        Returns:
            str: The localized text.
        """
        return self._get("make_public_confirm_required")

    @property
    def ban(self) -> str:
        """The ``ban`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ban")

    @property
    def unban(self) -> str:
        """The ``unban`` text.

        Returns:
            str: The localized text.
        """
        return self._get("unban")

    @property
    def ban_confirm(self) -> str:
        """The ``ban_confirm`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ban_confirm")

    @property
    def ban_delete(self) -> str:
        """The ``ban_delete`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ban_delete")

    @property
    def ban_delete_desc(self) -> str:
        """The ``ban_delete_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("ban_delete_desc")

    @property
    def random_staff_pick(self) -> str:
        """The ``random_staff_pick`` text.

        Returns:
            str: The localized text.
        """
        return self._get("random_staff_pick")

    @property
    def random_non_staff_pick(self) -> str:
        """The ``random_non_staff_pick`` text.

        Returns:
            str: The localized text.
        """
        return self._get("random_non_staff_pick")

    @property
    def mod_powers(self) -> str:
        """The ``mod_powers`` lines as a bulleted list.

        Returns:
            str: One ``- line`` per entry.
        """
        return "\n".join(f"- {line}" for line in self._lines("mod_powers"))

    @property
    def admin_powers(self) -> str:
        """The ``admin_powers`` lines as a bulleted list.

        Returns:
            str: One ``- line`` per entry.
        """
        return "\n".join(f"- {line}" for line in self._lines("admin_powers"))

    @property
    def server_description(self) -> str:
        """The ``server_description`` text.

        Returns:
            str: The localized text.
        """
        return self._get("server_description")

    def welcome(self, username: str) -> str:
        """The ``welcome`` text with its placeholders filled.

        Args:
            username: Account name.

        Returns:
            str: The localized text.
        """
        return self._get("welcome").format(username=username)

    def item_not_found(self, item: str, name: str) -> str:
        """The ``item_not_found`` text with its placeholders filled.

        Args:
            item: Item kind.
            name: Item name.

        Returns:
            str: The localized text.
        """
        return self._get("item_not_found").format(item=item, name=name)

    def item_type_not_found(self, item: str) -> str:
        """The ``item_type_not_found`` text with its placeholders filled.

        Args:
            item: Item kind.

        Returns:
            str: The localized text.
        """
        return self._get("item_type_not_found").format(item=item)

    def items_not_found(self, item: str) -> str:
        """The ``items_not_found`` text with its placeholders filled.

        Args:
            item: Item kind.

        Returns:
            str: The localized text.
        """
        return self._get("items_not_found").format(item=item)

    def items_not_found_search(self, item: str) -> str:
        """The ``items_not_found_search`` text with its placeholders filled.

        Args:
            item: Item kind.

        Returns:
            str: The localized text.
        """
        return self._get("items_not_found_search").format(item=item)

    @property
    def not_logged_in(self) -> str:
        """The ``not_logged_in`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_logged_in")

    @property
    def not_found(self) -> str:
        """The ``not_found`` text.

        Returns:
            str: The localized text.
        """
        return self._get("not_found")

    @property
    def unknown_error(self) -> str:
        """The ``unknown_error`` text.

        Returns:
            str: The localized text.
        """
        return self._get("unknown_error")

    @property
    def you(self) -> str:
        """The ``you`` text.

        Returns:
            str: The localized text.
        """
        return self._get("you")

    @property
    def default_particle(self) -> str:
        """The ``default_particle`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_particle")

    @property
    def default_particle_desc(self) -> str:
        """The ``default_particle_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_particle_desc")

    @property
    def default_engine(self) -> str:
        """The ``default_engine`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_engine")

    @property
    def default_engine_desc(self) -> str:
        """The ``default_engine_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_engine_desc")

    @property
    def default_skin(self) -> str:
        """The ``default_skin`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_skin")

    @property
    def default_skin_desc(self) -> str:
        """The ``default_skin_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("default_skin_desc")

    @property
    def uwu(self) -> str:
        """The ``uwu`` text.

        Returns:
            str: The localized text.
        """
        return self._get("uwu")

    @property
    def uwu_desc(self) -> str:
        """The ``uwu_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("uwu_desc")

    @property
    def slightly(self) -> str:
        """The ``slightly`` text.

        Returns:
            str: The localized text.
        """
        return self._get("slightly")

    @property
    def a_lot(self) -> str:
        """The ``a_lot`` text.

        Returns:
            str: The localized text.
        """
        return self._get("a_lot")

    @property
    def extreme(self) -> str:
        """The ``extreme`` text.

        Returns:
            str: The localized text.
        """
        return self._get("extreme")

    @property
    def max_uwu(self) -> str:
        """The ``max_uwu`` text.

        Returns:
            str: The localized text.
        """
        return self._get("max_uwu")

    @property
    def invalid_constant(self) -> str:
        """The ``invalid_constant`` text.

        Returns:
            str: The localized text.
        """
        return self._get("invalid_constant")

    @property
    def rerate(self) -> str:
        """The ``rerate`` text.

        Returns:
            str: The localized text.
        """
        return self._get("rerate")

    @property
    def rerate_desc(self) -> str:
        """The ``rerate_desc`` text.

        Returns:
            str: The localized text.
        """
        return self._get("rerate_desc")

    @property
    def show_resource_buttons(self) -> str:
        """The ``show_resource_buttons`` text.

        Returns:
            str: The localized text.
        """
        return self._get("show_resource_buttons")

    @property
    def announcements(self) -> str:
        """The ``announcements`` text.

        Returns:
            str: The localized text.
        """
        return self._get("announcements")

    def time_ago(self, time_str: str) -> str:
        """The ``time_ago`` text with its placeholders filled.

        Args:
            time_str: Elapsed time like ``5m``.

        Returns:
            str: The localized text.
        """
        return self._get("time_ago").format(time_ago=time_str)

    def time_ago_not_published(self, time_str: str) -> str:
        """The ``time_ago_not_published`` text with its placeholders filled.

        Args:
            time_str: Elapsed time like ``5m``.

        Returns:
            str: The localized text.
        """
        return self._get("time_ago_not_published").format(time_ago=time_str)

    def use_website_to_upload(self, website: str) -> str:
        """The ``use_website_to_upload`` text with its placeholders filled.

        Args:
            website: Website URL.

        Returns:
            str: The localized text.
        """
        return self._get("use_website_to_upload").format(url=website)


class LocaleManager:
    """Loads locale files and resolves Sonolus localization codes.

    Attributes:
        _directory: Folder holding ``<code>.json`` files.
        _locales: Loaded locales keyed by code.
        _english: The English locale, also the fallback for missing files.
    """

    def __init__(self, directory: Path) -> None:
        """Load English and every supported locale.

        Args:
            directory: Folder holding ``<code>.json`` files.
        """
        self._directory = directory
        self._locales: dict[str, Loc] = {}
        self._english = self._read("en", {})
        self._locales["en"] = self._english
        for code in SUPPORTED_LOCALES:
            self.load(code)

    def _read(self, code: str, default: dict[str, Any]) -> Loc:
        """Read one locale file.

        Args:
            code: Locale code.
            default: Fallback mapping.

        Returns:
            Loc: The locale.
        """
        with (self._directory / f"{code}.json").open("r", encoding="utf-8") as handle:
            return Loc(json.load(handle), default)

    def load(self, code: str) -> Loc:
        """Return a locale, using English when its file doesn't exist.

        Args:
            code: Locale code, ``zhs`` and ``zht`` allowed.

        Returns:
            Loc: The locale.
        """
        code = LOCALE_ALIASES.get(code, code)
        if code in self._locales:
            return self._locales[code]
        try:
            loc = self._read(code, self._english.data)
        except FileNotFoundError:
            return self._english
        self._locales[code] = loc
        return loc

    def get_messages(self, code: str) -> tuple[Loc, str]:
        """Resolve a requested code to a supported locale.

        Args:
            code: Requested code.

        Returns:
            tuple[Loc, str]: The locale and the normalized code, ``en`` when unsupported.
        """
        code = LOCALE_ALIASES.get(code, code)
        if code not in SUPPORTED_LOCALES:
            code = "en"
        return self.load(code), code
