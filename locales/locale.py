import json


class Loc:
    class Leaderboards:
        def __init__(self, parent: "Loc") -> None:
            self._parent = parent

        def _get(self, key: str) -> str:
            try:
                return self._parent._data["leaderboard"][key]
            except KeyError:
                return self._parent._default["leaderboard"][key]

        @property
        def YOU_ARE_BANNED(self) -> str:
            """
            You are banned
            """
            return self._get("YOU_ARE_BANNED")

        @property
        def ARCADE_SCORE_SPEED(self) -> str:
            """
            Arcade Score
            """
            return self._get("ARCADE_SCORE_SPEED")

        @property
        def ACCURACY_SCORE(self) -> str:
            """
            Accuracy Score
            """
            return self._get("ACCURACY_SCORE")

        @property
        def ARCADE_SCORE_NO_SPEED(self) -> str:
            """
            Arcade Score (no speed bonus)
            """
            return self._get("ARCADE_SCORE_NO_SPEED")

        @property
        def RANK_MATCH(self) -> str:
            """
            Rank Match
            """
            return self._get("RANK_MATCH")

        @property
        def LEAST_COMBO_BREAKS(self) -> str:
            """
            Least Combo breaks
            """
            return self._get("LEAST_COMBO_BREAKS")

        @property
        def LEAST_MISSES(self) -> str:
            """
            Least Misses
            """
            return self._get("LEAST_MISSES")

        @property
        def PERFECT(self) -> str:
            """
            Perfect count
            """
            return self._get("PERFECT")

        def BAD_ENGINE(self, engine_name: str) -> str:
            """
            Score submission is not supported for engine {engine_name}
            """
            return self._get("BAD_ENGINE").format(engine_name=engine_name)

    class Playlist:
        def __init__(self, parent: "Loc"):
            self._parent = parent

        def _get(self, key: str) -> str:
            try:
                return self._parent._data["playlist"][key]
            except KeyError:
                return self._parent._default["playlist"][key]

        @property
        def UPLOADED(self) -> str:
            """
            Your Uploaded Charts
            """
            return self._get("UPLOADED")

        @property
        def UPLOADEDSUB(self) -> str:
            """
            View all your uploaded charts.
            """
            return self._get("UPLOADEDSUB")

    class Background:
        def __init__(self, parent: "Loc"):
            self._parent = parent

        def _get(self, key: str) -> str:
            try:
                return self._parent._data["background"][key]
            except KeyError:
                return self._parent._default["background"][key]

        @property
        def UPLOADED(self) -> str:
            """
            User Uploaded Background
            """
            return self._get("UPLOADED")

        @property
        def USEBACKGROUNDDESC(self) -> str:
            """
            Select a background to use! Uploaded means the charter uploaded background, if exists.
            """
            return self._get("USEBACKGROUNDDESC")

        @property
        def USEBACKGROUND(self) -> str:
            """
            Select Level Background
            """
            return self._get("USEBACKGROUND")

        @property
        def V1(self) -> str:
            """
            PJSK V1
            """
            return self._get("V1")

        @property
        def V3(self) -> str:
            """
            PJSK V3
            """
            return self._get("V3")

        @property
        def DEF_OR_V1(self) -> str:
            """
            Uploaded OR PJSK V1
            """
            return self._get("DEF_OR_V1")

        @property
        def DEF_OR_V3(self) -> str:
            """
            Uploaded OR PJSK V3
            """
            return self._get("DEF_OR_V3")

        @property
        def BACKGROUNDSELECT(self) -> str:
            """
            Background Selection
            """
            return self._get("BACKGROUNDSELECT")

        @property
        def BACKGROUNDSELECTSUB(self) -> str:
            """
            Please select a background in Configuration.
            """
            return self._get("BACKGROUNDSELECTSUB")

    class Search:
        def __init__(self, parent: "Loc"):
            self._parent = parent

        def _get(self, key: str) -> str:
            try:
                return self._parent._data["search"][key]
            except KeyError:
                return self._parent._default["search"][key]

        def FILTERS(self, page: int, max_page: int) -> str:
            """
            Filters (Page {page}/{pageCount})
            """
            return self._get("FILTERS").format(
                page=f"{page:,}", pageCount=f"{max_page:,}"
            )

        @property
        def VISIBILITY(self) -> str:
            """
            Visibility
            """
            return self._get("VISIBILITY")

        @property
        def VISIBILITY_ALL(self) -> str:
            """
            All
            """
            return self._get("VISIBILITY_ALL")

        @property
        def VISIBILITY_PUBLIC(self) -> str:
            """
            Public
            """
            return self._get("VISIBILITY_PUBLIC")

        @property
        def VISIBILITY_UNLISTED(self) -> str:
            """
            Unlisted
            """
            return self._get("VISIBILITY_UNLISTED")

        @property
        def VISIBILITY_PRIVATE(self) -> str:
            """
            Private
            """
            return self._get("VISIBILITY_PRIVATE")

        @property
        def ADVANCED_SEARCH(self) -> str:
            """
            Advanced Search
            """
            return self._get("ADVANCED_SEARCH")

        @property
        def MIN_RATING(self) -> str:
            """
            Minimum Rating
            """
            return self._get("MIN_RATING")

        @property
        def MAX_RATING(self) -> str:
            """
            Maximum Rating
            """
            return self._get("MAX_RATING")

        @property
        def TITLE_CONTAINS(self) -> str:
            """
            Title Contains
            """
            return self._get("TITLE_CONTAINS")

        @property
        def DESCRIPTION_CONTAINS(self) -> str:
            """
            Description Contains
            """
            return self._get("DESCRIPTION_CONTAINS")

        @property
        def ARTISTS_CONTAINS(self) -> str:
            """
            Artists Contains
            """
            return self._get("ARTISTS_CONTAINS")

        @property
        def AUTHOR_CONTAINS(self) -> str:
            """
            Chart Author Name Contains
            """
            return self._get("AUTHOR_CONTAINS")

        @property
        def ONLY_LEVELS_I_LIKED(self) -> str:
            """
            Only Levels I've Liked
            """
            return self._get("ONLY_LEVELS_I_LIKED")

        @property
        def MIN_LIKES(self) -> str:
            """
            Minimum Likes
            """
            return self._get("MIN_LIKES")

        @property
        def MAX_LIKES(self) -> str:
            """
            Maximum Likes
            """
            return self._get("MAX_LIKES")

        @property
        def STAFF_PICK_DESC(self) -> str:
            """
            Filter by staff picks? (You can set default behavior in Configuration)
            """
            return self._get("STAFF_PICK_SEARCH_DESC")

        @property
        def STAFF_PICK_CONFIG_DESC(self) -> str:
            """
            Filter by staff picks? By default, every chart is shown.

            NOTE: We will always show you one opposite of whatever you pick in Levels, for some variety. For example, turning off Staff Picks will always show one in Levels, while turning on Staff Picks will always show you a non-staff pick in Levels.
            """
            return self._get("STAFF_PICK_CONFIG_DESC")

        @property
        def STAFF_PICK_OFF(self) -> str:
            """
            Don't Filter by Staff Pick
            """
            return self._get("STAFF_PICK_OFF")

        @property
        def STAFF_PICK_TRUE(self) -> str:
            """
            Only Staff Picks
            """
            return self._get("STAFF_PICK_TRUE")

        @property
        def STAFF_PICK_FALSE(self) -> str:
            """
            Only Not Staff Picks
            """
            return self._get("STAFF_PICK_FALSE")

        @property
        def ONLY_LEVELS_I_COMMENTED_ON(self) -> str:
            """
            Only Levels I've Commented On
            """
            return self._get("ONLY_LEVELS_I_COMMENTED_ON")

        @property
        def COMMENTS(self) -> str:
            """
            Comments Count
            """
            return self._get("COMMENTS")

        @property
        def MIN_COMMENTS(self) -> str:
            """
            Minimum Comments
            """
            return self._get("MIN_COMMENTS")

        @property
        def MAX_COMMENTS(self) -> str:
            """
            Maximum Comments
            """
            return self._get("MAX_COMMENTS")

        @property
        def TAGS_COMMA_SEPARATED(self) -> str:
            """
            Tags (comma-separated)
            """
            return self._get("TAGS_COMMA_SEPARATED")

        @property
        def ENTER_TEXT(self) -> str:
            """
            Enter text
            """
            return self._get("ENTER_TEXT")

        @property
        def ENTER_TAGS(self) -> str:
            """
            Enter tags
            """
            return self._get("ENTER_TAGS")

        @property
        def SORT_BY(self) -> str:
            """
            Sort By
            """
            return self._get("SORT_BY")

        @property
        def SORT_BY_DESCRIPTION(self) -> str:
            """
            Sort by options.
            Note: Title is sorted from A-Z when descending.
            """
            return self._get("SORT_BY_DESCRIPTION")

        @property
        def DATE_CREATED(self) -> str:
            """
            Date Uploaded
            """
            return self._get("DATE_CREATED")

        @property
        def DATE_PUBLISHED(self) -> str:
            """
            Date Published
            """
            return self._get("DATE_PUBLISHED")

        @property
        def RATING(self) -> str:
            """
            Rating
            """
            return self._get("RATING")

        @property
        def LIKES(self) -> str:
            """
            Likes
            """
            return self._get("LIKES")

        @property
        def DECAYING_LIKES(self) -> str:
            """
            Trending
            """
            return self._get("DECAYING_LIKES")

        @property
        def TITLE_A_Z(self) -> str:
            """
            Title (A-Z)
            """
            return self._get("TITLE_A_Z")

        @property
        def SORT_ORDER(self) -> str:
            """
            Sort Order
            """
            return self._get("SORT_ORDER")

        @property
        def DESCENDING(self) -> str:
            """
            Descending
            """
            return self._get("DESCENDING")

        @property
        def ASCENDING(self) -> str:
            """
            Ascending
            """
            return self._get("ASCENDING")

    class Notification:
        class Templates:
            def __init__(self, parent: "Loc"):
                self._parent = parent

            def _get(self, key: str) -> str:
                try:
                    return self._parent._data["notification"]["templates"][key]
                except KeyError:
                    return self._parent._default["notification"]["templates"][key]

            def CHART_VISIBILITY_CHANGED(
                self, chart_name: str, visibility_status: str
            ) -> str:
                """
                The visibility of your chart \"{chart_name}\" has been updated to {visibility_status}. Please review our upload policies to see why this change was necessary. If you fix your chart to comply, you can change it back to Public. Otherwise, keep it as it is now, or else we may be forced to delete it.
                """
                return self._get("CHART_VISIBILITY_CHANGED").format(
                    chart_name=chart_name, visibility_status=visibility_status
                )

            def COMMENT_DELETED(self, comment_content: str) -> str:
                """
                Your comment was deleted because it violated our comment policy. Please make sure all comments adhere to our community guidelines.

                ----------------------
                COMMENT:

                {comment_content}
                """
                return self._get("COMMENT_DELETED").format(
                    comment_content=comment_content
                )

            def CHART_DELETED(self, chart_name: str) -> str:
                """
                Your chart \"{chart_name}\" was deleted for violating our upload rules. Please take a moment to review our chart upload guidelines for more information.
                """
                return self._get("CHART_DELETED").format(chart_name=chart_name)

            def LEADERBOARD_SCORE_DELETED(self, chart_name: str) -> str:
                """
                Your score on the chart \"{chart_name}\" was deleted for violating our rules. Please take a moment to review our guidelines for more information.
                """
                return self._get("LEADERBOARD_SCORE_DELETED").format(
                    chart_name=chart_name
                )

        def __init__(self, parent: "Loc"):
            self._parent = parent
            self.templates = self.Templates(parent)

        def _get(self, key: str) -> str:
            try:
                return self._parent._data["notification"][key]
            except KeyError:
                return self._parent._default["notification"][key]

        @property
        def READ_STATUS(self) -> str:
            """
            Read
            """
            return self._get("READ_STATUS")

        @property
        def UNREAD_STATUS(self) -> str:
            """
            Unread
            """
            return self._get("UNREAD_STATUS")

        @property
        def NOTIFICATION(self) -> str:
            """
            Notifications
            """
            return self._get("NOTIFICATION")

        @property
        def NOTIFICATION_DESC_UNREAD(self) -> str:
            """
            You can find all your past notifications and announcements by clicking \"More\". You have unread notifications that need to be read.
            """
            return self._get("NOTIFICATION_DESC_UNREAD")

        @property
        def NOTIFICATION_DESC(self) -> str:
            """
            You can find all your past notifications and announcements by clicking \"More\". You do not currently have any unread notifications.
            """
            return self._get("NOTIFICATION_DESC")

        @property
        def UNREAD(self) -> str:
            """
            Unread Notifications
            """
            return self._get("UNREAD")

        @property
        def none(self) -> str:
            """
            You don't have any unread notifications.
            """
            return self._get("none")

        @property
        def none_past(self) -> str:
            """
            You don't have any past notifications.
            """
            return self._get("none_past")

    def __init__(self, data: dict, default: dict):
        self._data = data
        self._default = default
        self.search = self.Search(self)
        self.playlist = self.Playlist(self)
        self.background = self.Background(self)
        self.notification = self.Notification(self)
        self.leaderboards = self.Leaderboards(self)

    def _get(self, value: str) -> str:
        try:
            return self._data[value]
        except KeyError:
            return self._default[value]

    def invalid_page_plural(self, page: int, max_page: int) -> str:
        """
        Page {page} does not exist! There are {max_page} pages.
        """
        return self._get("invalid_page_plural").format(
            page=f"{page:,}", max_page=f"{max_page:,}"
        )

    def invalid_page_singular(self, page: int, max_page: int) -> str:
        """
        Page {page} does not exist! There are {max_page} page.
        """
        return self._get("invalid_page_singular").format(
            page=f"{page:,}", max_page=f"{max_page:,}"
        )

    @property
    def not_mod(self) -> str:
        """
        You are not a moderator!
        """
        return self._get("not_mod")

    @property
    def not_mod_or_owner(self) -> str:
        """
        You are not a moderator or the owner!
        """
        return self._get("not_mod_or_owner")

    @property
    def is_mod(self) -> str:
        """
        You are a moderator!
        """
        return self._get("is_mod")

    @property
    def not_admin(self) -> str:
        """
        You are not an administrator!
        """
        return self._get("not_admin")

    @property
    def is_admin(self) -> str:
        """
        You are an administrator!
        """
        return self._get("is_admin")

    @property
    def not_admin_or_owner(self) -> str:
        """
        You are not an administrator or the owner!
        """
        return self._get("not_admin_or_owner")

    @property
    def staff_pick(self) -> str:
        """
        Staff Pick
        """
        return self._get("staff_pick")

    @property
    def off(self) -> str:
        """
        Off
        """
        return self._get("off")

    @property
    def on(self) -> str:
        """
        On
        """
        return self._get("on")

    def like(self, num: int) -> str:
        """
        Like ({num})
        """
        return self._get("like").format(num=f"{num:,}")

    def unlike(self, num: int) -> str:
        """
        Unlike ({num})
        """
        return self._get("unlike").format(num=f"{num:,}")

    def notifications_singular(self, num: int) -> str:
        """
        You have {num} new notification!
        Please read them to continue to the server.
        """
        return self._get("notifications_singular").format(num=f"{num:,}")

    def notifications_plural(self, num: int) -> str:
        """
        You have {num} new notifications!
        Please read them to continue to the server.
        """
        return self._get("notifications_plural").format(num=f"{num:,}")

    @property
    def find_in_playlists(self) -> str:
        """
        You can find your own uploaded levels in Playlists.
        """
        return self._get("find_in_playlists")

    @property
    def staff_pick_desc(self) -> str:
        """
        Staff picks are charts we've reviewed and found both fun and playable!
        """
        return self._get("staff_pick_desc")

    @property
    def non_staff_pick_desc(self) -> str:
        """
        Random non-staff pick level, because you have only staff picks enabled.
        """
        return self._get("non_staff_pick_desc")

    @property
    def staff_pick_notice(self) -> str:
        """
        Do not beg to be added: this happens automatically. At most, you may ask for a review.
        """
        return self._get("staff_pick_notice")

    @property
    def staff_pick_confirm(self) -> str:
        """
        Please confirm this chart is fun, rated accurately (+-1 range), and playable.
        """
        return self._get("staff_pick_confirm")

    @property
    def staff_pick_add(self) -> str:
        """
        Add Staff Pick
        """
        return self._get("staff_pick_add")

    @property
    def staff_pick_remove(self) -> str:
        """
        Remove Staff Pick
        """
        return self._get("staff_pick_remove")

    @property
    def ban(self) -> str:
        """
        Ban User
        """
        return self._get("ban")

    @property
    def unban(self) -> str:
        """
        Unban User
        """
        return self._get("unban")

    @property
    def ban_confirm(self) -> str:
        """
        Please confirm this user is breaking the rules. They will lose access to the server.
        """
        return self._get("ban_confirm")

    @property
    def ban_delete(self) -> str:
        """
        Delete their charts
        """
        return self._get("ban_delete")

    @property
    def ban_delete_desc(self) -> str:
        """
        Also delete every chart they uploaded, along with all of their files. This cannot be undone.
        """
        return self._get("ban_delete_desc")

    @property
    def random_staff_pick(self) -> str:
        """
        Random Staff Pick
        """
        return self._get("random_staff_pick")

    @property
    def random_non_staff_pick(self) -> str:
        """
        Random Non-Staff Pick
        """
        return self._get("random_non_staff_pick")

    @property
    def mod_powers(self) -> str:
        """
        - Delete rule-breaking comments
        - Review charts for staff picks!
        - Change the visibility of rule-breaking charts
        """
        lines = self._get("mod_powers")
        return "\n".join(f"- {line}" for line in lines)

    @property
    def admin_powers(self) -> str:
        """
        - Delete rule-breaking charts
        """
        lines = self._get("admin_powers")
        return "\n".join(f"- {line}" for line in lines)

    @property
    def server_description(self) -> str:
        """
        https://discord.gg/UntitledCharts
        The official UntitledCharts custom server!
        """
        return self._get("server_description")

    def welcome(self, username: str) -> str:
        """
        Welcome! Logged in as {username}.
        """
        return self._get("welcome").format(username=username)

    def item_not_found(self, item: str, name: str) -> str:
        """
        {item} item \"{name}\" not found.
        """
        return self._get("item_not_found").format(item=item, name=name)

    def item_type_not_found(self, item: str) -> str:
        """
        Item \"{item}\" not found.
        """
        return self._get("item_type_not_found").format(item=item)

    def items_not_found(self, item: str) -> str:
        """
        Could not find any {item}.
        """
        return self._get("items_not_found").format(item=item)

    def items_not_found_search(self, item: str) -> str:
        """
        Could not find any {item} matching your search.
        """
        return self._get("items_not_found_search").format(item=item)

    @property
    def not_logged_in(self) -> str:
        """
        You are not logged in!
        """
        return self._get("not_logged_in")

    @property
    def not_found(self) -> str:
        """
        Not found.
        """
        return self._get("not_found")

    @property
    def unknown_error(self) -> str:
        """
        Unknown error!
        """
        return self._get("unknown_error")

    @property
    def you(self) -> str:
        """
        You
        """
        return self._get("you")

    @property
    def default_particle(self) -> str:
        """
        Default Level Particle
        """
        return self._get("default_particle")

    @property
    def default_particle_desc(self) -> str:
        """
        Choose your default level particle that will be applied!
        """
        return self._get("default_particle_desc")

    @property
    def default_engine(self) -> str:
        """
        Server Engine
        """
        return self._get("default_engine")

    @property
    def default_engine_desc(self) -> str:
        """
        Choose the server engine to use!
        """
        return self._get("default_engine_desc")

    @property
    def default_skin(self) -> str:
        """
        Server Skin
        """
        return self._get("default_skin")

    @property
    def default_skin_desc(self) -> str:
        """
        Choose the default skin type to use! The skin will be different depending on the engine (eg. V1 skin is slightly different on Rush compared to Next), but will apply to all engines.

        NOTE: if an engine does not have the supported skin, it'll use the engine default.
        """
        return self._get("default_skin_desc")

    @property
    def uwu(self) -> str:
        """
        UwU >.<
        """
        return self._get("uwu")

    @property
    def uwu_desc(self) -> str:
        """
        UwUify your menu (EN/TR ONLY)
        """
        return self._get("uwu_desc")

    @property
    def slightly(self) -> str:
        """
        Slightly
        """
        return self._get("slightly")

    @property
    def a_lot(self) -> str:
        """
        A Lot
        """
        return self._get("a_lot")

    @property
    def extreme(self) -> str:
        """
        Extreme
        """
        return self._get("extreme")

    @property
    def max_uwu(self) -> str:
        """
        Maximum
        """
        return self._get("max_uwu")

    @property
    def invalid_constant(self) -> str:
        """
        Invalid constant! Must have a maximum of 4 decimals between -999 and 999
        """
        return self._get("invalid_constant")

    @property
    def rerate(self) -> str:
        """
        Rerate
        """
        return self._get("rerate")

    @property
    def rerate_desc(self) -> str:
        """
        Rerate the level, optionally adding constants.
        """
        return self._get("rerate_desc")

    @property
    def show_resource_buttons(self) -> str:
        """
        Show Server Resource Buttons
        """
        return self._get("show_resource_buttons")

    @property
    def announcements(self) -> str:
        """
        Announcements
        """
        return self._get("announcements")

    def time_ago(self, time_str: str) -> str:
        """
        {time_ago} ago
        """
        return self._get("time_ago").format(time_ago=time_str)

    def time_ago_not_published(self, time_str: str) -> str:
        """
        {time_ago} ago (uploaded, not published)
        """
        return self._get("time_ago_not_published").format(time_ago=time_str)

    def use_website_to_upload(self, website: str) -> str:
        """
        Please login on our website to upload a new level.
        We do not support uploading levels in-game.

        {url}
        """
        return self._get("use_website_to_upload").format(url=website)


class LocaleManager:
    def __init__(self, default_locale: str):
        self.default_locale = default_locale
        self.locales: dict[str, Loc] = {}

        self._default_locale = None
        self._default_locale = self.load_locale("en", overwrite_default={})

    def load_locale(self, locale: str, overwrite_default: dict = None) -> Loc:
        if locale == "zhs":
            locale = "zh-cn"
        elif locale == "zht":
            locale = "zh-TW"
        if locale in self.locales:
            return self.locales[locale]
        try:
            with open(f"locales/locales/{locale}.json", "r", encoding="utf8") as f:
                d = json.load(f)
            locale_class = Loc(
                d,
                (
                    overwrite_default
                    if overwrite_default != None
                    else self._default_locale._data
                ),
            )
            self.locales[locale] = locale_class
            return locale_class
        except FileNotFoundError:
            return self._default_locale

    def assert_supported(self, locale: str):
        supported = [
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
        ]
        if locale not in supported:
            raise AssertionError(f"Locale '{locale}' is not supported.")

    def get_messages(self, locale: str) -> tuple[Loc, str]:
        if locale == "zhs":
            locale = "zh-cn"
        elif locale == "zht":
            locale = "zh-TW"
        try:
            self.assert_supported(locale)
        except AssertionError:
            locale = "en"
        locale_class = self.load_locale(locale)
        return locale_class, locale


Locale = LocaleManager(default_locale="en")
