"""Pydantic models generated from @sonolus/core 7.16.0."""

from __future__ import annotations

from typing import Annotated, Generic, Literal, TypeAlias, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypeAliasType

T = TypeVar("T")
TItem = TypeVar("TItem")
TItemType = TypeVar("TItemType")


class SonolusModel(BaseModel):
    """Base model shared by every @sonolus/core 7.16.0 model."""

    model_config = ConfigDict(
        populate_by_name=True, serialize_by_alias=True, extra="ignore"
    )


class EffectClipName:
    """EffectClipName from @sonolus/core 7.16.0."""

    Miss = "#MISS"
    Perfect = "#PERFECT"
    Great = "#GREAT"
    Good = "#GOOD"
    Hold = "#HOLD"
    MissAlternative = "#MISS_ALTERNATIVE"
    PerfectAlternative = "#PERFECT_ALTERNATIVE"
    GreatAlternative = "#GREAT_ALTERNATIVE"
    GoodAlternative = "#GOOD_ALTERNATIVE"
    HoldAlternative = "#HOLD_ALTERNATIVE"
    Stage = "#STAGE"


class EngineArchetypeDataName:
    """EngineArchetypeDataName from @sonolus/core 7.16.0."""

    Beat = "#BEAT"
    Bpm = "#BPM"
    TimeScale = "#TIMESCALE"
    Judgment = "#JUDGMENT"
    Accuracy = "#ACCURACY"


class EngineArchetypeName:
    """EngineArchetypeName from @sonolus/core 7.16.0."""

    BpmChange = "#BPM_CHANGE"
    TimeScaleChange = "#TIMESCALE_CHANGE"


class Icon:
    """Icon from @sonolus/core 7.16.0."""

    Advanced = "advanced"
    AngleDown = "angleDown"
    AngleLeft = "angleLeft"
    AngleRight = "angleRight"
    AnglesDown = "anglesDown"
    AnglesLeft = "anglesLeft"
    AnglesRight = "anglesRight"
    AnglesUp = "anglesUp"
    AngleUp = "angleUp"
    Announcement = "announcement"
    ArrowDown = "arrowDown"
    ArrowLeft = "arrowLeft"
    ArrowRight = "arrowRight"
    ArrowsLeftRight = "arrowsLeftRight"
    ArrowsUpDown = "arrowsUpDown"
    ArrowsUpLeft = "arrowsUpLeft"
    ArrowUp = "arrowUp"
    Award = "award"
    Background = "background"
    Bell = "bell"
    BellSlash = "bellSlash"
    Book = "book"
    Bookmark = "bookmark"
    BookmarkHollow = "bookmarkHollow"
    Broom = "broom"
    Check = "check"
    Clock = "clock"
    Comment = "comment"
    Crown = "crown"
    CustomServer = "customServer"
    Delete = "delete"
    Edit = "edit"
    Effect = "effect"
    Engine = "engine"
    Envelope = "envelope"
    EnvelopeOpen = "envelopeOpen"
    Filter = "filter"
    Globe = "globe"
    Hand = "hand"
    Heart = "heart"
    HeartHollow = "heartHollow"
    Hide = "hide"
    IceCream = "iceCream"
    Information = "information"
    Level = "level"
    Lock = "lock"
    Medal = "medal"
    Message = "message"
    Minus = "minus"
    Options = "options"
    Particle = "particle"
    Pin = "pin"
    Player = "player"
    Playlist = "playlist"
    Plus = "plus"
    Post = "post"
    Question = "question"
    Ranking = "ranking"
    Replay = "replay"
    Reply = "reply"
    Restore = "restore"
    Room = "room"
    Scissors = "scissors"
    Search = "search"
    Settings = "settings"
    Show = "show"
    Shuffle = "shuffle"
    Skin = "skin"
    Sort = "sort"
    SortDown = "sortDown"
    SortDown19 = "sortDown19"
    SortDown91 = "sortDown91"
    SortDownAZ = "sortDownAZ"
    SortDownShortWide = "sortDownShortWide"
    SortDownWideShort = "sortDownWideShort"
    SortDownZA = "sortDownZA"
    SortUp = "sortUp"
    SortUp19 = "sortUp19"
    SortUp91 = "sortUp91"
    SortUpAZ = "sortUpAZ"
    SortUpShortWide = "sortUpShortWide"
    SortUpWideShort = "sortUpWideShort"
    SortUpZA = "sortUpZA"
    Star = "star"
    StarHalf = "starHalf"
    StarHollow = "starHollow"
    Stopwatch = "stopwatch"
    Tag = "tag"
    ThumbsDown = "thumbsDown"
    ThumbsDownHollow = "thumbsDownHollow"
    ThumbsUp = "thumbsUp"
    ThumbsUpHollow = "thumbsUpHollow"
    Trophy = "trophy"
    Unlock = "unlock"
    User = "user"
    Warning = "warning"
    XMark = "xMark"


class InstructionIconName:
    """InstructionIconName from @sonolus/core 7.16.0."""

    Hand = "#HAND"
    Arrow = "#ARROW"


class ParticleEffectName:
    """ParticleEffectName from @sonolus/core 7.16.0."""

    NoteCircularTapNeutral = "#NOTE_CIRCULAR_TAP_NEUTRAL"
    NoteCircularTapRed = "#NOTE_CIRCULAR_TAP_RED"
    NoteCircularTapGreen = "#NOTE_CIRCULAR_TAP_GREEN"
    NoteCircularTapBlue = "#NOTE_CIRCULAR_TAP_BLUE"
    NoteCircularTapYellow = "#NOTE_CIRCULAR_TAP_YELLOW"
    NoteCircularTapPurple = "#NOTE_CIRCULAR_TAP_PURPLE"
    NoteCircularTapCyan = "#NOTE_CIRCULAR_TAP_CYAN"
    NoteCircularAlternativeNeutral = "#NOTE_CIRCULAR_ALTERNATIVE_NEUTRAL"
    NoteCircularAlternativeRed = "#NOTE_CIRCULAR_ALTERNATIVE_RED"
    NoteCircularAlternativeGreen = "#NOTE_CIRCULAR_ALTERNATIVE_GREEN"
    NoteCircularAlternativeBlue = "#NOTE_CIRCULAR_ALTERNATIVE_BLUE"
    NoteCircularAlternativeYellow = "#NOTE_CIRCULAR_ALTERNATIVE_YELLOW"
    NoteCircularAlternativePurple = "#NOTE_CIRCULAR_ALTERNATIVE_PURPLE"
    NoteCircularAlternativeCyan = "#NOTE_CIRCULAR_ALTERNATIVE_CYAN"
    NoteCircularHoldNeutral = "#NOTE_CIRCULAR_HOLD_NEUTRAL"
    NoteCircularHoldRed = "#NOTE_CIRCULAR_HOLD_RED"
    NoteCircularHoldGreen = "#NOTE_CIRCULAR_HOLD_GREEN"
    NoteCircularHoldBlue = "#NOTE_CIRCULAR_HOLD_BLUE"
    NoteCircularHoldYellow = "#NOTE_CIRCULAR_HOLD_YELLOW"
    NoteCircularHoldPurple = "#NOTE_CIRCULAR_HOLD_PURPLE"
    NoteCircularHoldCyan = "#NOTE_CIRCULAR_HOLD_CYAN"
    NoteLinearTapNeutral = "#NOTE_LINEAR_TAP_NEUTRAL"
    NoteLinearTapRed = "#NOTE_LINEAR_TAP_RED"
    NoteLinearTapGreen = "#NOTE_LINEAR_TAP_GREEN"
    NoteLinearTapBlue = "#NOTE_LINEAR_TAP_BLUE"
    NoteLinearTapYellow = "#NOTE_LINEAR_TAP_YELLOW"
    NoteLinearTapPurple = "#NOTE_LINEAR_TAP_PURPLE"
    NoteLinearTapCyan = "#NOTE_LINEAR_TAP_CYAN"
    NoteLinearAlternativeNeutral = "#NOTE_LINEAR_ALTERNATIVE_NEUTRAL"
    NoteLinearAlternativeRed = "#NOTE_LINEAR_ALTERNATIVE_RED"
    NoteLinearAlternativeGreen = "#NOTE_LINEAR_ALTERNATIVE_GREEN"
    NoteLinearAlternativeBlue = "#NOTE_LINEAR_ALTERNATIVE_BLUE"
    NoteLinearAlternativeYellow = "#NOTE_LINEAR_ALTERNATIVE_YELLOW"
    NoteLinearAlternativePurple = "#NOTE_LINEAR_ALTERNATIVE_PURPLE"
    NoteLinearAlternativeCyan = "#NOTE_LINEAR_ALTERNATIVE_CYAN"
    NoteLinearHoldNeutral = "#NOTE_LINEAR_HOLD_NEUTRAL"
    NoteLinearHoldRed = "#NOTE_LINEAR_HOLD_RED"
    NoteLinearHoldGreen = "#NOTE_LINEAR_HOLD_GREEN"
    NoteLinearHoldBlue = "#NOTE_LINEAR_HOLD_BLUE"
    NoteLinearHoldYellow = "#NOTE_LINEAR_HOLD_YELLOW"
    NoteLinearHoldPurple = "#NOTE_LINEAR_HOLD_PURPLE"
    NoteLinearHoldCyan = "#NOTE_LINEAR_HOLD_CYAN"
    LaneCircular = "#LANE_CIRCULAR"
    LaneLinear = "#LANE_LINEAR"
    SlotCircular = "#SLOT_CIRCULAR"
    SlotLinear = "#SLOT_LINEAR"
    JudgeLineCircular = "#JUDGE_LINE_CIRCULAR"
    JudgeLineLinear = "#JUDGE_LINE_LINEAR"


class RuntimeFunction:
    """RuntimeFunction from @sonolus/core 7.16.0."""

    Abs = "Abs"
    Add = "Add"
    AddLifeScheduled = "AddLifeScheduled"
    And = "And"
    Arccos = "Arccos"
    Arcsin = "Arcsin"
    Arctan = "Arctan"
    Arctan2 = "Arctan2"
    BeatToBPM = "BeatToBPM"
    BeatToStartingBeat = "BeatToStartingBeat"
    BeatToStartingTime = "BeatToStartingTime"
    BeatToTime = "BeatToTime"
    Block = "Block"
    Break = "Break"
    Ceil = "Ceil"
    Clamp = "Clamp"
    Copy = "Copy"
    Cos = "Cos"
    Cosh = "Cosh"
    DebugLog = "DebugLog"
    DebugPause = "DebugPause"
    DecrementPost = "DecrementPost"
    DecrementPostPointed = "DecrementPostPointed"
    DecrementPostShifted = "DecrementPostShifted"
    DecrementPre = "DecrementPre"
    DecrementPrePointed = "DecrementPrePointed"
    DecrementPreShifted = "DecrementPreShifted"
    Degree = "Degree"
    DestroyParticleEffect = "DestroyParticleEffect"
    Divide = "Divide"
    DoWhile = "DoWhile"
    Draw = "Draw"
    DrawCurvedB = "DrawCurvedB"
    DrawCurvedBT = "DrawCurvedBT"
    DrawCurvedL = "DrawCurvedL"
    DrawCurvedLR = "DrawCurvedLR"
    DrawCurvedR = "DrawCurvedR"
    DrawCurvedT = "DrawCurvedT"
    EaseInBack = "EaseInBack"
    EaseInCirc = "EaseInCirc"
    EaseInCubic = "EaseInCubic"
    EaseInElastic = "EaseInElastic"
    EaseInExpo = "EaseInExpo"
    EaseInOutBack = "EaseInOutBack"
    EaseInOutCirc = "EaseInOutCirc"
    EaseInOutCubic = "EaseInOutCubic"
    EaseInOutElastic = "EaseInOutElastic"
    EaseInOutExpo = "EaseInOutExpo"
    EaseInOutQuad = "EaseInOutQuad"
    EaseInOutQuart = "EaseInOutQuart"
    EaseInOutQuint = "EaseInOutQuint"
    EaseInOutSine = "EaseInOutSine"
    EaseInQuad = "EaseInQuad"
    EaseInQuart = "EaseInQuart"
    EaseInQuint = "EaseInQuint"
    EaseInSine = "EaseInSine"
    EaseOutBack = "EaseOutBack"
    EaseOutCirc = "EaseOutCirc"
    EaseOutCubic = "EaseOutCubic"
    EaseOutElastic = "EaseOutElastic"
    EaseOutExpo = "EaseOutExpo"
    EaseOutInBack = "EaseOutInBack"
    EaseOutInCirc = "EaseOutInCirc"
    EaseOutInCubic = "EaseOutInCubic"
    EaseOutInElastic = "EaseOutInElastic"
    EaseOutInExpo = "EaseOutInExpo"
    EaseOutInQuad = "EaseOutInQuad"
    EaseOutInQuart = "EaseOutInQuart"
    EaseOutInQuint = "EaseOutInQuint"
    EaseOutInSine = "EaseOutInSine"
    EaseOutQuad = "EaseOutQuad"
    EaseOutQuart = "EaseOutQuart"
    EaseOutQuint = "EaseOutQuint"
    EaseOutSine = "EaseOutSine"
    Equal = "Equal"
    Execute = "Execute"
    Execute0 = "Execute0"
    ExportValue = "ExportValue"
    Floor = "Floor"
    Frac = "Frac"
    Get = "Get"
    GetPointed = "GetPointed"
    GetShifted = "GetShifted"
    Greater = "Greater"
    GreaterOr = "GreaterOr"
    HasEffectClip = "HasEffectClip"
    HasParticleEffect = "HasParticleEffect"
    HasSkinSprite = "HasSkinSprite"
    If = "If"
    IncrementPost = "IncrementPost"
    IncrementPostPointed = "IncrementPostPointed"
    IncrementPostShifted = "IncrementPostShifted"
    IncrementPre = "IncrementPre"
    IncrementPrePointed = "IncrementPrePointed"
    IncrementPreShifted = "IncrementPreShifted"
    Judge = "Judge"
    JudgeSimple = "JudgeSimple"
    JumpLoop = "JumpLoop"
    Lerp = "Lerp"
    LerpClamped = "LerpClamped"
    Less = "Less"
    LessOr = "LessOr"
    Log = "Log"
    Max = "Max"
    Min = "Min"
    Mod = "Mod"
    MoveParticleEffect = "MoveParticleEffect"
    Multiply = "Multiply"
    Negate = "Negate"
    Not = "Not"
    NotEqual = "NotEqual"
    Or = "Or"
    Paint = "Paint"
    Play = "Play"
    PlayLooped = "PlayLooped"
    PlayLoopedScheduled = "PlayLoopedScheduled"
    PlayScheduled = "PlayScheduled"
    Power = "Power"
    Print = "Print"
    Radian = "Radian"
    Random = "Random"
    RandomInteger = "RandomInteger"
    Rem = "Rem"
    Remap = "Remap"
    RemapClamped = "RemapClamped"
    Round = "Round"
    Set = "Set"
    SetAdd = "SetAdd"
    SetAddPointed = "SetAddPointed"
    SetAddShifted = "SetAddShifted"
    SetDivide = "SetDivide"
    SetDividePointed = "SetDividePointed"
    SetDivideShifted = "SetDivideShifted"
    SetMod = "SetMod"
    SetModPointed = "SetModPointed"
    SetModShifted = "SetModShifted"
    SetMultiply = "SetMultiply"
    SetMultiplyPointed = "SetMultiplyPointed"
    SetMultiplyShifted = "SetMultiplyShifted"
    SetPointed = "SetPointed"
    SetPower = "SetPower"
    SetPowerPointed = "SetPowerPointed"
    SetPowerShifted = "SetPowerShifted"
    SetRem = "SetRem"
    SetRemPointed = "SetRemPointed"
    SetRemShifted = "SetRemShifted"
    SetShifted = "SetShifted"
    SetSubtract = "SetSubtract"
    SetSubtractPointed = "SetSubtractPointed"
    SetSubtractShifted = "SetSubtractShifted"
    Sign = "Sign"
    Sin = "Sin"
    Sinh = "Sinh"
    Spawn = "Spawn"
    SpawnParticleEffect = "SpawnParticleEffect"
    StackEnter = "StackEnter"
    StackGet = "StackGet"
    StackGetFrame = "StackGetFrame"
    StackGetFramePointer = "StackGetFramePointer"
    StackGetPointer = "StackGetPointer"
    StackGrow = "StackGrow"
    StackInit = "StackInit"
    StackLeave = "StackLeave"
    StackPop = "StackPop"
    StackPush = "StackPush"
    StackSet = "StackSet"
    StackSetFrame = "StackSetFrame"
    StackSetFramePointer = "StackSetFramePointer"
    StackSetPointer = "StackSetPointer"
    StopLooped = "StopLooped"
    StopLoopedScheduled = "StopLoopedScheduled"
    StreamGetNextKey = "StreamGetNextKey"
    StreamGetPreviousKey = "StreamGetPreviousKey"
    StreamGetValue = "StreamGetValue"
    StreamHas = "StreamHas"
    StreamSet = "StreamSet"
    Subtract = "Subtract"
    Switch = "Switch"
    SwitchInteger = "SwitchInteger"
    SwitchIntegerWithDefault = "SwitchIntegerWithDefault"
    SwitchWithDefault = "SwitchWithDefault"
    Tan = "Tan"
    Tanh = "Tanh"
    TimeToScaledTime = "TimeToScaledTime"
    TimeToStartingScaledTime = "TimeToStartingScaledTime"
    TimeToStartingTime = "TimeToStartingTime"
    TimeToTimeScale = "TimeToTimeScale"
    Trunc = "Trunc"
    Unlerp = "Unlerp"
    UnlerpClamped = "UnlerpClamped"
    While = "While"


class SkinSpriteName:
    """SkinSpriteName from @sonolus/core 7.16.0."""

    NoteHeadNeutral = "#NOTE_HEAD_NEUTRAL"
    NoteHeadRed = "#NOTE_HEAD_RED"
    NoteHeadGreen = "#NOTE_HEAD_GREEN"
    NoteHeadBlue = "#NOTE_HEAD_BLUE"
    NoteHeadYellow = "#NOTE_HEAD_YELLOW"
    NoteHeadPurple = "#NOTE_HEAD_PURPLE"
    NoteHeadCyan = "#NOTE_HEAD_CYAN"
    NoteTickNeutral = "#NOTE_TICK_NEUTRAL"
    NoteTickRed = "#NOTE_TICK_RED"
    NoteTickGreen = "#NOTE_TICK_GREEN"
    NoteTickBlue = "#NOTE_TICK_BLUE"
    NoteTickYellow = "#NOTE_TICK_YELLOW"
    NoteTickPurple = "#NOTE_TICK_PURPLE"
    NoteTickCyan = "#NOTE_TICK_CYAN"
    NoteTailNeutral = "#NOTE_TAIL_NEUTRAL"
    NoteTailRed = "#NOTE_TAIL_RED"
    NoteTailGreen = "#NOTE_TAIL_GREEN"
    NoteTailBlue = "#NOTE_TAIL_BLUE"
    NoteTailYellow = "#NOTE_TAIL_YELLOW"
    NoteTailPurple = "#NOTE_TAIL_PURPLE"
    NoteTailCyan = "#NOTE_TAIL_CYAN"
    NoteConnectionNeutral = "#NOTE_CONNECTION_NEUTRAL"
    NoteConnectionRed = "#NOTE_CONNECTION_RED"
    NoteConnectionGreen = "#NOTE_CONNECTION_GREEN"
    NoteConnectionBlue = "#NOTE_CONNECTION_BLUE"
    NoteConnectionYellow = "#NOTE_CONNECTION_YELLOW"
    NoteConnectionPurple = "#NOTE_CONNECTION_PURPLE"
    NoteConnectionCyan = "#NOTE_CONNECTION_CYAN"
    NoteConnectionNeutralSeamless = "#NOTE_CONNECTION_NEUTRAL_SEAMLESS"
    NoteConnectionRedSeamless = "#NOTE_CONNECTION_RED_SEAMLESS"
    NoteConnectionGreenSeamless = "#NOTE_CONNECTION_GREEN_SEAMLESS"
    NoteConnectionBlueSeamless = "#NOTE_CONNECTION_BLUE_SEAMLESS"
    NoteConnectionYellowSeamless = "#NOTE_CONNECTION_YELLOW_SEAMLESS"
    NoteConnectionPurpleSeamless = "#NOTE_CONNECTION_PURPLE_SEAMLESS"
    NoteConnectionCyanSeamless = "#NOTE_CONNECTION_CYAN_SEAMLESS"
    SimultaneousConnectionNeutral = "#SIMULTANEOUS_CONNECTION_NEUTRAL"
    SimultaneousConnectionRed = "#SIMULTANEOUS_CONNECTION_RED"
    SimultaneousConnectionGreen = "#SIMULTANEOUS_CONNECTION_GREEN"
    SimultaneousConnectionBlue = "#SIMULTANEOUS_CONNECTION_BLUE"
    SimultaneousConnectionYellow = "#SIMULTANEOUS_CONNECTION_YELLOW"
    SimultaneousConnectionPurple = "#SIMULTANEOUS_CONNECTION_PURPLE"
    SimultaneousConnectionCyan = "#SIMULTANEOUS_CONNECTION_CYAN"
    SimultaneousConnectionNeutralSeamless = "#SIMULTANEOUS_CONNECTION_NEUTRAL_SEAMLESS"
    SimultaneousConnectionRedSeamless = "#SIMULTANEOUS_CONNECTION_RED_SEAMLESS"
    SimultaneousConnectionGreenSeamless = "#SIMULTANEOUS_CONNECTION_GREEN_SEAMLESS"
    SimultaneousConnectionBlueSeamless = "#SIMULTANEOUS_CONNECTION_BLUE_SEAMLESS"
    SimultaneousConnectionYellowSeamless = "#SIMULTANEOUS_CONNECTION_YELLOW_SEAMLESS"
    SimultaneousConnectionPurpleSeamless = "#SIMULTANEOUS_CONNECTION_PURPLE_SEAMLESS"
    SimultaneousConnectionCyanSeamless = "#SIMULTANEOUS_CONNECTION_CYAN_SEAMLESS"
    DirectionalMarkerNeutral = "#DIRECTIONAL_MARKER_NEUTRAL"
    DirectionalMarkerRed = "#DIRECTIONAL_MARKER_RED"
    DirectionalMarkerGreen = "#DIRECTIONAL_MARKER_GREEN"
    DirectionalMarkerBlue = "#DIRECTIONAL_MARKER_BLUE"
    DirectionalMarkerYellow = "#DIRECTIONAL_MARKER_YELLOW"
    DirectionalMarkerPurple = "#DIRECTIONAL_MARKER_PURPLE"
    DirectionalMarkerCyan = "#DIRECTIONAL_MARKER_CYAN"
    SimultaneousMarkerNeutral = "#SIMULTANEOUS_MARKER_NEUTRAL"
    SimultaneousMarkerRed = "#SIMULTANEOUS_MARKER_RED"
    SimultaneousMarkerGreen = "#SIMULTANEOUS_MARKER_GREEN"
    SimultaneousMarkerBlue = "#SIMULTANEOUS_MARKER_BLUE"
    SimultaneousMarkerYellow = "#SIMULTANEOUS_MARKER_YELLOW"
    SimultaneousMarkerPurple = "#SIMULTANEOUS_MARKER_PURPLE"
    SimultaneousMarkerCyan = "#SIMULTANEOUS_MARKER_CYAN"
    StageMiddle = "#STAGE_MIDDLE"
    StageLeftBorder = "#STAGE_LEFT_BORDER"
    StageRightBorder = "#STAGE_RIGHT_BORDER"
    StageTopBorder = "#STAGE_TOP_BORDER"
    StageBottomBorder = "#STAGE_BOTTOM_BORDER"
    StageLeftBorderSeamless = "#STAGE_LEFT_BORDER_SEAMLESS"
    StageRightBorderSeamless = "#STAGE_RIGHT_BORDER_SEAMLESS"
    StageTopBorderSeamless = "#STAGE_TOP_BORDER_SEAMLESS"
    StageBottomBorderSeamless = "#STAGE_BOTTOM_BORDER_SEAMLESS"
    StageTopLeftCorner = "#STAGE_TOP_LEFT_CORNER"
    StageTopRightCorner = "#STAGE_TOP_RIGHT_CORNER"
    StageBottomLeftCorner = "#STAGE_BOTTOM_LEFT_CORNER"
    StageBottomRightCorner = "#STAGE_BOTTOM_RIGHT_CORNER"
    Lane = "#LANE"
    LaneSeamless = "#LANE_SEAMLESS"
    LaneAlternative = "#LANE_ALTERNATIVE"
    LaneAlternativeSeamless = "#LANE_ALTERNATIVE_SEAMLESS"
    JudgmentLine = "#JUDGMENT_LINE"
    NoteSlot = "#NOTE_SLOT"
    StageCover = "#STAGE_COVER"
    GridNeutral = "#GRID_NEUTRAL"
    GridRed = "#GRID_RED"
    GridGreen = "#GRID_GREEN"
    GridBlue = "#GRID_BLUE"
    GridYellow = "#GRID_YELLOW"
    GridPurple = "#GRID_PURPLE"
    GridCyan = "#GRID_CYAN"


class Text:
    """Text from @sonolus/core 7.16.0."""

    PrefixList = "#PREFIX_LIST"
    PrefixQuote = "#PREFIX_QUOTE"
    SeparatorSpace = "#SEPARATOR_SPACE"
    SeparatorComma = "#SEPARATOR_COMMA"
    SeparatorColon = "#SEPARATOR_COLON"
    SeparatorAnd = "#SEPARATOR_AND"
    SeparatorPlus = "#SEPARATOR_PLUS"
    SeparatorSlash = "#SEPARATOR_SLASH"
    SeparatorLesser = "#SEPARATOR_LESSER"
    SeparatorGreater = "#SEPARATOR_GREATER"
    SeparatorQuoteSingleLeft = "#SEPARATOR_QUOTE_SINGLE_LEFT"
    SeparatorQuoteSingleRight = "#SEPARATOR_QUOTE_SINGLE_RIGHT"
    SeparatorQuoteDoubleLeft = "#SEPARATOR_QUOTE_DOUBLE_LEFT"
    SeparatorQuoteDoubleRight = "#SEPARATOR_QUOTE_DOUBLE_RIGHT"
    SeparatorParenthesisLeft = "#SEPARATOR_PARENTHESIS_LEFT"
    SeparatorParenthesisRight = "#SEPARATOR_PARENTHESIS_RIGHT"
    SeparatorBracketLeft = "#SEPARATOR_BRACKET_LEFT"
    SeparatorBracketRight = "#SEPARATOR_BRACKET_RIGHT"
    SurroundQuotesSingle = "#SURROUND_QUOTES_SINGLE"
    SurroundQuotesDouble = "#SURROUND_QUOTES_DOUBLE"
    SurroundParentheses = "#SURROUND_PARENTHESES"
    SurroundBrackets = "#SURROUND_BRACKETS"
    CustomServer = "#CUSTOM_SERVER"
    Collection = "#COLLECTION"
    Server = "#SERVER"
    Address = "#ADDRESS"
    Expiration = "#EXPIRATION"
    Storage = "#STORAGE"
    Log = "#LOG"
    Inquiry = "#INQUIRY"
    Banner = "#BANNER"
    Icon = "#ICON"
    Post = "#POST"
    Playlist = "#PLAYLIST"
    Level = "#LEVEL"
    Skin = "#SKIN"
    Background = "#BACKGROUND"
    Effect = "#EFFECT"
    Particle = "#PARTICLE"
    Engine = "#ENGINE"
    Replay = "#REPLAY"
    User = "#USER"
    Room = "#ROOM"
    PostThumbnail = "#POST_THUMBNAIL"
    PlaylistThumbnail = "#PLAYLIST_THUMBNAIL"
    LevelCover = "#LEVEL_COVER"
    LevelBgm = "#LEVEL_BGM"
    LevelPreview = "#LEVEL_PREVIEW"
    LevelData = "#LEVEL_DATA"
    SkinThumbnail = "#SKIN_THUMBNAIL"
    SkinData = "#SKIN_DATA"
    SkinTexture = "#SKIN_TEXTURE"
    BackgroundThumbnail = "#BACKGROUND_THUMBNAIL"
    BackgroundImage = "#BACKGROUND_IMAGE"
    BackgroundData = "#BACKGROUND_DATA"
    BackgroundConfiguration = "#BACKGROUND_CONFIGURATION"
    EffectThumbnail = "#EFFECT_THUMBNAIL"
    EffectData = "#EFFECT_DATA"
    EffectAudio = "#EFFECT_AUDIO"
    ParticleThumbnail = "#PARTICLE_THUMBNAIL"
    ParticleData = "#PARTICLE_DATA"
    ParticleTexture = "#PARTICLE_TEXTURE"
    EngineThumbnail = "#ENGINE_THUMBNAIL"
    EnginePlaydata = "#ENGINE_PLAYDATA"
    EngineWatchdata = "#ENGINE_WATCHDATA"
    EnginePreviewdata = "#ENGINE_PREVIEWDATA"
    EngineTutorialdata = "#ENGINE_TUTORIALDATA"
    EngineRom = "#ENGINE_ROM"
    EngineConfiguration = "#ENGINE_CONFIGURATION"
    ReplayData = "#REPLAY_DATA"
    ReplayConfiguration = "#REPLAY_CONFIGURATION"
    RoomCover = "#ROOM_COVER"
    RoomBgm = "#ROOM_BGM"
    RoomPreview = "#ROOM_PREVIEW"
    Grade = "#GRADE"
    ArcadeScore = "#ARCADE_SCORE"
    AccuracyScore = "#ACCURACY_SCORE"
    Combo = "#COMBO"
    Perfect = "#PERFECT"
    Great = "#GREAT"
    Good = "#GOOD"
    Miss = "#MISS"
    Judgment = "#JUDGMENT"
    Accuracy = "#ACCURACY"
    Filter = "#FILTER"
    Sort = "#SORT"
    SortBy = "#SORT_BY"
    SortOrder = "#SORT_ORDER"
    Keywords = "#KEYWORDS"
    Name = "#NAME"
    Source = "#SOURCE"
    Rating = "#RATING"
    RatingMinimum = "#RATING_MINIMUM"
    RatingMaximum = "#RATING_MAXIMUM"
    Title = "#TITLE"
    Subtitle = "#SUBTITLE"
    Artists = "#ARTISTS"
    Time = "#TIME"
    Author = "#AUTHOR"
    Coauthor = "#COAUTHOR"
    Collaborator = "#COLLABORATOR"
    Lyricist = "#LYRICIST"
    Composer = "#COMPOSER"
    Arranger = "#ARRANGER"
    Description = "#DESCRIPTION"
    Genre = "#GENRE"
    Type = "#TYPE"
    Category = "#CATEGORY"
    Status = "#STATUS"
    Language = "#LANGUAGE"
    Difficulty = "#DIFFICULTY"
    Version = "#VERSION"
    Length = "#LENGTH"
    LengthMinimum = "#LENGTH_MINIMUM"
    LengthMaximum = "#LENGTH_MAXIMUM"
    AdditionalInformation = "#ADDITIONAL_INFORMATION"
    Timezone = "#TIMEZONE"
    Region = "#REGION"
    Tag = "#TAG"
    IncludeTag = "#INCLUDE_TAG"
    ExcludeTag = "#EXCLUDE_TAG"
    Content = "#CONTENT"
    Comment = "#COMMENT"
    Message = "#MESSAGE"
    Notification = "#NOTIFICATION"
    Role = "#ROLE"
    Permission = "#PERMISSION"
    Graphics = "#GRAPHICS"
    Audio = "#AUDIO"
    Gameplay = "#GAMEPLAY"
    Miscellaneous = "#MISCELLANEOUS"
    Speed = "#SPEED"
    Mirror = "#MIRROR"
    Random = "#RANDOM"
    Hidden = "#HIDDEN"
    JudgmentStrict = "#JUDGMENT_STRICT"
    JudgmentLoose = "#JUDGMENT_LOOSE"
    EffectAuto = "#EFFECT_AUTO"
    Haptic = "#HAPTIC"
    Stage = "#STAGE"
    StagePosition = "#STAGE_POSITION"
    StageSize = "#STAGE_SIZE"
    StageRotation = "#STAGE_ROTATION"
    StageDirection = "#STAGE_DIRECTION"
    StageAlpha = "#STAGE_ALPHA"
    StageAnimation = "#STAGE_ANIMATION"
    StageTilt = "#STAGE_TILT"
    StageCover = "#STAGE_COVER"
    StageCoverVertical = "#STAGE_COVER_VERTICAL"
    StageCoverHorizontal = "#STAGE_COVER_HORIZONTAL"
    StageCoverAlpha = "#STAGE_COVER_ALPHA"
    StageAspectratioLock = "#STAGE_ASPECTRATIO_LOCK"
    StageEffect = "#STAGE_EFFECT"
    StageEffectPosition = "#STAGE_EFFECT_POSITION"
    StageEffectSize = "#STAGE_EFFECT_SIZE"
    StageEffectRotation = "#STAGE_EFFECT_ROTATION"
    StageEffectDirection = "#STAGE_EFFECT_DIRECTION"
    StageEffectAlpha = "#STAGE_EFFECT_ALPHA"
    Lane = "#LANE"
    LanePosition = "#LANE_POSITION"
    LaneSize = "#LANE_SIZE"
    LaneRotation = "#LANE_ROTATION"
    LaneDirection = "#LANE_DIRECTION"
    LaneAlpha = "#LANE_ALPHA"
    LaneAnimation = "#LANE_ANIMATION"
    LaneEffect = "#LANE_EFFECT"
    LaneEffectPosition = "#LANE_EFFECT_POSITION"
    LaneEffectSize = "#LANE_EFFECT_SIZE"
    LaneEffectRotation = "#LANE_EFFECT_ROTATION"
    LaneEffectDirection = "#LANE_EFFECT_DIRECTION"
    LaneEffectAlpha = "#LANE_EFFECT_ALPHA"
    Judgeline = "#JUDGELINE"
    JudgelinePosition = "#JUDGELINE_POSITION"
    JudgelineSize = "#JUDGELINE_SIZE"
    JudgelineRotation = "#JUDGELINE_ROTATION"
    JudgelineDirection = "#JUDGELINE_DIRECTION"
    JudgelineAlpha = "#JUDGELINE_ALPHA"
    JudgelineAnimation = "#JUDGELINE_ANIMATION"
    JudgelineEffect = "#JUDGELINE_EFFECT"
    JudgelineEffectPosition = "#JUDGELINE_EFFECT_POSITION"
    JudgelineEffectSize = "#JUDGELINE_EFFECT_SIZE"
    JudgelineEffectRotation = "#JUDGELINE_EFFECT_ROTATION"
    JudgelineEffectDirection = "#JUDGELINE_EFFECT_DIRECTION"
    JudgelineEffectAlpha = "#JUDGELINE_EFFECT_ALPHA"
    Slot = "#SLOT"
    SlotPosition = "#SLOT_POSITION"
    SlotSize = "#SLOT_SIZE"
    SlotRotation = "#SLOT_ROTATION"
    SlotDirection = "#SLOT_DIRECTION"
    SlotAlpha = "#SLOT_ALPHA"
    SlotAnimation = "#SLOT_ANIMATION"
    SlotEffect = "#SLOT_EFFECT"
    SlotEffectPosition = "#SLOT_EFFECT_POSITION"
    SlotEffectSize = "#SLOT_EFFECT_SIZE"
    SlotEffectRotation = "#SLOT_EFFECT_ROTATION"
    SlotEffectDirection = "#SLOT_EFFECT_DIRECTION"
    SlotEffectAlpha = "#SLOT_EFFECT_ALPHA"
    Note = "#NOTE"
    NoteSpeed = "#NOTE_SPEED"
    NoteSpeedRandom = "#NOTE_SPEED_RANDOM"
    NotePosition = "#NOTE_POSITION"
    NoteSize = "#NOTE_SIZE"
    NoteRotation = "#NOTE_ROTATION"
    NoteDirection = "#NOTE_DIRECTION"
    NoteColor = "#NOTE_COLOR"
    NoteAlpha = "#NOTE_ALPHA"
    NoteAnimation = "#NOTE_ANIMATION"
    NoteEffect = "#NOTE_EFFECT"
    NoteEffectPosition = "#NOTE_EFFECT_POSITION"
    NoteEffectSize = "#NOTE_EFFECT_SIZE"
    NoteEffectRotation = "#NOTE_EFFECT_ROTATION"
    NoteEffectDirection = "#NOTE_EFFECT_DIRECTION"
    NoteEffectColor = "#NOTE_EFFECT_COLOR"
    NoteEffectAlpha = "#NOTE_EFFECT_ALPHA"
    Marker = "#MARKER"
    MarkerPosition = "#MARKER_POSITION"
    MarkerSize = "#MARKER_SIZE"
    MarkerRotation = "#MARKER_ROTATION"
    MarkerDirection = "#MARKER_DIRECTION"
    MarkerColor = "#MARKER_COLOR"
    MarkerAlpha = "#MARKER_ALPHA"
    MarkerAnimation = "#MARKER_ANIMATION"
    Connector = "#CONNECTOR"
    ConnectorPosition = "#CONNECTOR_POSITION"
    ConnectorSize = "#CONNECTOR_SIZE"
    ConnectorRotation = "#CONNECTOR_ROTATION"
    ConnectorDirection = "#CONNECTOR_DIRECTION"
    ConnectorColor = "#CONNECTOR_COLOR"
    ConnectorAlpha = "#CONNECTOR_ALPHA"
    ConnectorAnimation = "#CONNECTOR_ANIMATION"
    Simline = "#SIMLINE"
    SimlinePosition = "#SIMLINE_POSITION"
    SimlineSize = "#SIMLINE_SIZE"
    SimlineRotation = "#SIMLINE_ROTATION"
    SimlineDirection = "#SIMLINE_DIRECTION"
    SimlineColor = "#SIMLINE_COLOR"
    SimlineAlpha = "#SIMLINE_ALPHA"
    SimlineAnimation = "#SIMLINE_ANIMATION"
    PreviewScaleVertical = "#PREVIEW_SCALE_VERTICAL"
    PreviewScaleHorizontal = "#PREVIEW_SCALE_HORIZONTAL"
    PreviewTime = "#PREVIEW_TIME"
    PreviewScore = "#PREVIEW_SCORE"
    PreviewBpm = "#PREVIEW_BPM"
    PreviewTimescale = "#PREVIEW_TIMESCALE"
    PreviewBeat = "#PREVIEW_BEAT"
    PreviewMeasure = "#PREVIEW_MEASURE"
    PreviewCombo = "#PREVIEW_COMBO"
    BeatLine = "#BEAT_LINE"
    MeasureLine = "#MEASURE_LINE"
    Ui = "#UI"
    UiMetric = "#UI_METRIC"
    UiPrimaryMetric = "#UI_PRIMARY_METRIC"
    UiSecondaryMetric = "#UI_SECONDARY_METRIC"
    UiJudgment = "#UI_JUDGMENT"
    UiCombo = "#UI_Combo"
    UiMenu = "#UI_Menu"
    On = "#ON"
    Off = "#OFF"
    None_ = "#NONE"
    Any = "#ANY"
    All = "#ALL"
    Others = "#OTHERS"
    Short = "#SHORT"
    Long = "#LONG"
    High = "#HIGH"
    Mid = "#MID"
    Low = "#LOW"
    Small = "#SMALL"
    Medium = "#MEDIUM"
    Large = "#LARGE"
    Left = "#LEFT"
    Right = "#RIGHT"
    Up = "#UP"
    Down = "#DOWN"
    Front = "#FRONT"
    Back = "#BACK"
    Center = "#CENTER"
    Top = "#TOP"
    Bottom = "#BOTTOM"
    TopLeft = "#TOP_LEFT"
    TopCenter = "#TOP_CENTER"
    TopRight = "#TOP_RIGHT"
    CenterLeft = "#CENTER_LEFT"
    CenterRight = "#CENTER_RIGHT"
    BottomLeft = "#BOTTOM_LEFT"
    BottomCenter = "#BOTTOM_CENTER"
    BottomRight = "#BOTTOM_RIGHT"
    Clockwise = "#CLOCKWISE"
    Counterclockwise = "#COUNTERCLOCKWISE"
    Forward = "#FORWARD"
    Backward = "#BACKWARD"
    Ascending = "#ASCENDING"
    Descending = "#DESCENDING"
    Default = "#DEFAULT"
    Neutral = "#NEUTRAL"
    Red = "#RED"
    Green = "#GREEN"
    Blue = "#BLUE"
    Yellow = "#YELLOW"
    Purple = "#PURPLE"
    Cyan = "#CYAN"
    Simple = "#SIMPLE"
    Easy = "#EASY"
    Normal = "#NORMAL"
    Hard = "#HARD"
    Expert = "#EXPERT"
    Master = "#MASTER"
    Pro = "#PRO"
    Technical = "#TECHNICAL"
    Special = "#SPECIAL"
    Append = "#APPEND"
    IconPlaceholder = "#ICON_PLACEHOLDER"
    PostPlaceholder = "#POST_PLACEHOLDER"
    PlaylistPlaceholder = "#PLAYLIST_PLACEHOLDER"
    LevelPlaceholder = "#LEVEL_PLACEHOLDER"
    SkinPlaceholder = "#SKIN_PLACEHOLDER"
    BackgroundPlaceholder = "#BACKGROUND_PLACEHOLDER"
    EffectPlaceholder = "#EFFECT_PLACEHOLDER"
    ParticlePlaceholder = "#PARTICLE_PLACEHOLDER"
    EnginePlaceholder = "#ENGINE_PLACEHOLDER"
    ReplayPlaceholder = "#REPLAY_PLACEHOLDER"
    UserPlaceholder = "#USER_PLACEHOLDER"
    RoomPlaceholder = "#ROOM_PLACEHOLDER"
    KeywordsPlaceholder = "#KEYWORDS_PLACEHOLDER"
    NamePlaceholder = "#NAME_PLACEHOLDER"
    RatingPlaceholder = "#RATING_PLACEHOLDER"
    RatingMinimumPlaceholder = "#RATING_MINIMUM_PLACEHOLDER"
    RatingMaximumPlaceholder = "#RATING_MAXIMUM_PLACEHOLDER"
    TitlePlaceholder = "#TITLE_PLACEHOLDER"
    SubtitlePlaceholder = "#SUBTITLE_PLACEHOLDER"
    ArtistsPlaceholder = "#ARTISTS_PLACEHOLDER"
    TimePlaceholder = "#TIME_PLACEHOLDER"
    AuthorPlaceholder = "#AUTHOR_PLACEHOLDER"
    CoauthorPlaceholder = "#COAUTHOR_PLACEHOLDER"
    CollaboratorPlaceholder = "#COLLABORATOR_PLACEHOLDER"
    DescriptionPlaceholder = "#DESCRIPTION_PLACEHOLDER"
    GenrePlaceholder = "#GENRE_PLACEHOLDER"
    TypePlaceholder = "#TYPE_PLACEHOLDER"
    CategoryPlaceholder = "#CATEGORY_PLACEHOLDER"
    LanguagePlaceholder = "#LANGUAGE_PLACEHOLDER"
    DifficultyPlaceholder = "#DIFFICULTY_PLACEHOLDER"
    LengthPlaceholder = "#LENGTH_PLACEHOLDER"
    LengthMinimumPlaceholder = "#LENGTH_MINIMUM_PLACEHOLDER"
    LengthMaximumPlaceholder = "#LENGTH_MAXIMUM_PLACEHOLDER"
    AdditionalInformationPlaceholder = "#ADDITIONAL_INFORMATION_PLACEHOLDER"
    TimezonePlaceholder = "#TIMEZONE_PLACEHOLDER"
    RegionPlaceholder = "#REGION_PLACEHOLDER"
    ContentPlaceholder = "#CONTENT_PLACEHOLDER"
    CommentPlaceholder = "#COMMENT_PLACEHOLDER"
    ReviewPlaceholder = "#REVIEW_PLACEHOLDER"
    ReplyPlaceholder = "#REPLY_PLACEHOLDER"
    MessagePlaceholder = "#MESSAGE_PLACEHOLDER"
    RolePlaceholder = "#ROLE_PLACEHOLDER"
    PermissionPlaceholder = "#PERMISSION_PLACEHOLDER"
    PercentageUnit = "#PERCENTAGE_UNIT"
    YearUnit = "#YEAR_UNIT"
    MonthUnit = "#MONTH_UNIT"
    DayUnit = "#DAY_UNIT"
    HourUnit = "#HOUR_UNIT"
    MinuteUnit = "#MINUTE_UNIT"
    SecondUnit = "#SECOND_UNIT"
    MillisecondUnit = "#MILLISECOND_UNIT"
    YearPast = "#YEAR_PAST"
    MonthPast = "#MONTH_PAST"
    DayPast = "#DAY_PAST"
    HourPast = "#HOUR_PAST"
    MinutePast = "#MINUTE_PAST"
    SecondPast = "#SECOND_PAST"
    MillisecondPast = "#MILLISECOND_PAST"
    YearFuture = "#YEAR_FUTURE"
    MonthFuture = "#MONTH_FUTURE"
    DayFuture = "#DAY_FUTURE"
    HourFuture = "#HOUR_FUTURE"
    MinuteFuture = "#MINUTE_FUTURE"
    SecondFuture = "#SECOND_FUTURE"
    MillisecondFuture = "#MILLISECOND_FUTURE"
    Tap = "#TAP"
    TapHold = "#TAP_HOLD"
    TapRelease = "#TAP_RELEASE"
    TapFlick = "#TAP_FLICK"
    TapSlide = "#TAP_SLIDE"
    Hold = "#HOLD"
    HoldSlide = "#HOLD_SLIDE"
    HoldFollow = "#HOLD_FOLLOW"
    Release = "#RELEASE"
    Flick = "#FLICK"
    Slide = "#SLIDE"
    SlideFlick = "#SLIDE_FLICK"
    Avoid = "#AVOID"
    Jiggle = "#JIGGLE"
    Newest = "#NEWEST"
    Oldest = "#OLDEST"
    Recommended = "#RECOMMENDED"
    Popular = "#POPULAR"
    Featured = "#FEATURED"
    Competitive = "#COMPETITIVE"
    Tournament = "#TOURNAMENT"
    Holiday = "#HOLIDAY"
    Limited = "#LIMITED"
    Announcement = "#ANNOUNCEMENT"
    Information = "#INFORMATION"
    Help = "#HELP"
    Maintenance = "#MAINTENANCE"
    Event = "#EVENT"
    Update = "#UPDATE"
    Search = "#SEARCH"
    Advanced = "#ADVANCED"
    Related = "#RELATED"
    SameAuthor = "#SAME_AUTHOR"
    SameArtists = "#SAME_ARTISTS"
    SameRating = "#SAME_RATING"
    SameCategory = "#SAME_CATEGORY"
    SameDifficulty = "#SAME_DIFFICULTY"
    SameGenre = "#SAME_GENRE"
    SameVersion = "#SAME_VERSION"
    OtherAuthors = "#OTHER_AUTHORS"
    OtherArtists = "#OTHER_ARTISTS"
    OtherRatings = "#OTHER_RATINGS"
    OtherCategories = "#OTHER_CATEGORIES"
    OtherDifficulties = "#OTHER_DIFFICULTIES"
    OtherGenres = "#OTHER_GENRES"
    OtherVersions = "#OTHER_VERSIONS"
    Draft = "#DRAFT"
    Public = "#PUBLIC"
    Private = "#PRIVATE"
    Favorite = "#FAVORITE"
    Pop = "#POP"
    Rock = "#ROCK"
    Hiphop = "#HIPHOP"
    Country = "#COUNTRY"
    Electronic = "#ELECTRONIC"
    Metal = "#METAL"
    Classical = "#CLASSICAL"
    Folk = "#FOLK"
    Indie = "#INDIE"
    Anime = "#ANIME"
    Vocaloid = "#VOCALOID"
    Remix = "#REMIX"
    Instrumental = "#INSTRUMENTAL"
    ShortVersion = "#SHORT_VERSION"
    LongVersion = "#LONG_VERSION"
    CutVersion = "#CUT_VERSION"
    FullVersion = "#FULL_VERSION"
    ExtendedVersion = "#EXTENDED_VERSION"
    LiveVersion = "#LIVE_VERSION"
    Medley = "#MEDLEY"
    Explicit = "#EXPLICIT"
    MultiFinger = "#MULTI_FINGER"
    FullHand = "#FULL_HAND"
    CrossHand = "#CROSS_HAND"
    Gimmick = "#GIMMICK"
    Epilepsy = "#EPILEPSY"
    Collaboration = "#COLLABORATION"
    Report = "#REPORT"
    Reason = "#REASON"
    IllegalActivities = "#ILLEGAL_ACTIVITIES"
    Cheating = "#CHEATING"
    Afk = "#AFK"
    Spamming = "#SPAMMING"
    VerbalAbuse = "#VERBAL_ABUSE"
    InappropriateLanguage = "#INAPPROPRIATE_LANGUAGE"
    NegativeAttitude = "#NEGATIVE_ATTITUDE"
    Dnf = "#DNF"
    Suggestions = "#SUGGESTIONS"
    SuggestionsPerPlayer = "#SUGGESTIONS_PER_PLAYER"
    MatchScoring = "#MATCH_SCORING"
    MatchTiebreaker = "#MATCH_TIEBREAKER"
    MatchCount = "#MATCH_COUNT"
    MatchLimit = "#MATCH_LIMIT"
    RoundScoring = "#ROUND_SCORING"
    RoundTiebreaker = "#ROUND_TIEBREAKER"
    RoundCount = "#ROUND_COUNT"
    RoundLimit = "#ROUND_LIMIT"
    TeamScoring = "#TEAM_SCORING"
    TeamTiebreaker = "#TEAM_TIEBREAKER"
    TeamCount = "#TEAM_COUNT"
    TeamLimit = "#TEAM_LIMIT"
    Qualified = "#QUALIFIED"
    Disqualified = "#DISQUALIFIED"
    Ranking = "#RANKING"
    Score = "#SCORE"
    Owner = "#OWNER"
    Admin = "#ADMIN"
    Developer = "#DEVELOPER"
    Moderator = "#MODERATOR"
    Reviewer = "#REVIEWER"
    Banned = "#BANNED"
    Player = "#PLAYER"
    Spectator = "#SPECTATOR"
    Referee = "#REFEREE"
    Eliminated = "#ELIMINATED"
    Finalist = "#FINALIST"
    Finished = "#FINISHED"
    Winner = "#WINNER"
    GoldMedal = "#GOLD_MEDAL"
    SilverMedal = "#SILVER_MEDAL"
    BronzeMedal = "#BRONZE_MEDAL"
    Team1 = "#TEAM_1"
    Team2 = "#TEAM_2"
    Team3 = "#TEAM_3"
    Team4 = "#TEAM_4"
    Team5 = "#TEAM_5"
    Team6 = "#TEAM_6"
    Team7 = "#TEAM_7"
    Team8 = "#TEAM_8"
    TeamRed = "#TEAM_RED"
    TeamGreen = "#TEAM_GREEN"
    TeamBlue = "#TEAM_BLUE"
    TeamYellow = "#TEAM_YELLOW"
    TeamPurple = "#TEAM_PURPLE"
    TeamCyan = "#TEAM_CYAN"
    TeamWhite = "#TEAM_WHITE"
    TeamBlack = "#TEAM_BLACK"
    Add = "#ADD"
    Added = "#ADDED"
    Create = "#CREATE"
    Created = "#CREATED"
    Reply = "#REPLY"
    Replied = "#REPLIED"
    Review = "#REVIEW"
    Reviewing = "#REVIEWING"
    Reviewed = "#REVIEWED"
    Verify = "#VERIFY"
    Verifying = "#VERIFYING"
    Verified = "#VERIFIED"
    Upload = "#UPLOAD"
    Uploading = "#UPLOADING"
    Uploaded = "#UPLOADED"
    Submit = "#SUBMIT"
    Submitting = "#SUBMITTING"
    Submitted = "#SUBMITTED"
    Edit = "#EDIT"
    Editing = "#EDITING"
    Edited = "#EDITED"
    Like = "#LIKE"
    Liked = "#LIKED"
    Dislike = "#DISLIKE"
    Disliked = "#DISLIKED"
    Bookmark = "#BOOKMARK"
    Bookmarked = "#BOOKMARKED"
    Delete = "#DELETE"
    Deleting = "#DELETING"
    Deleted = "#DELETED"
    Remove = "#REMOVE"
    Removing = "#REMOVING"
    Removed = "#REMOVED"
    Restore = "#RESTORE"
    Restoring = "#RESTORING"
    Restored = "#RESTORED"
    Confirm = "#CONFIRM"
    Confirmed = "#CONFIRMED"
    Cancel = "#CANCEL"
    Canceled = "#CANCELED"
    Increase = "#INCREASE"
    Decrease = "#DECREASE"
    Upvote = "#UPVOTE"
    Upvoted = "#UPVOTED"
    Downvote = "#DOWNVOTE"
    Downvoted = "#DOWNVOTED"
    Agree = "#AGREE"
    Agreed = "#AGREED"
    Disagree = "#DISAGREE"
    Disagreed = "#DISAGREED"
    Lock = "#LOCK"
    Locked = "#LOCKED"
    Unlock = "#UNLOCK"
    Unlocked = "#UNLOCKED"
    Pin = "#PIN"
    Pinned = "#PINNED"
    Unpin = "#UNPIN"
    Unpinned = "#UNPINNED"
    Follow = "#FOLLOW"
    Following = "#FOLLOWING"
    Followed = "#FOLLOWED"
    Unfollow = "#UNFOLLOW"
    Subscribe = "#SUBSCRIBE"
    Subscribing = "#SUBSCRIBING"
    Subscribed = "#SUBSCRIBED"
    Unsubscribe = "#UNSUBSCRIBE"
    Publish = "#PUBLISH"
    Publishing = "#PUBLISHING"
    Published = "#PUBLISHED"
    Unpublish = "#UNPUBLISH"
    Show = "#SHOW"
    Hide = "#HIDE"
    Allow = "#ALLOW"
    Allowed = "#ALLOWED"
    Disallow = "#DISALLOW"
    Disallowed = "#DISALLOWED"
    Approve = "#APPROVE"
    Approved = "#APPROVED"
    Deny = "#DENY"
    Denied = "#DENIED"
    Accept = "#ACCEPT"
    Accepted = "#ACCEPTED"
    Reject = "#REJECT"
    Rejected = "#REJECTED"
    Star = "#STAR"
    Starred = "#STARRED"


class TextFunction:
    """TextFunction from @sonolus/core 7.16.0."""

    Escape = "##"
    TimeFull = "##TIME_FULL"
    TimeRelative = "##TIME_RELATIVE"
    Localize = "##LOCALIZE"


class AddChatMessageCommand(SonolusModel):
    """AddChatMessageCommand from @sonolus/core 7.16.0."""

    type: Literal["addChatMessage"]
    nonce: int | float
    message: ChatMessage


class AddChatMessageEvent(SonolusModel):
    """AddChatMessageEvent from @sonolus/core 7.16.0."""

    type: Literal["addChatMessage"]
    nonce: int | float | None = None
    message: ChatMessage


class AddResultEvent(SonolusModel):
    """AddResultEvent from @sonolus/core 7.16.0."""

    type: Literal["addResult"]
    result: ResultEntry


class AddSuggestionCommand(SonolusModel):
    """AddSuggestionCommand from @sonolus/core 7.16.0."""

    type: Literal["addSuggestion"]
    level: Sil


class AddSuggestionEvent(SonolusModel):
    """AddSuggestionEvent from @sonolus/core 7.16.0."""

    type: Literal["addSuggestion"]
    suggestion: Suggestion


class AddUserEvent(SonolusModel):
    """AddUserEvent from @sonolus/core 7.16.0."""

    type: Literal["addUser"]
    user: RoomUser


class ArrangeScoreboardSectionScoresEvent(SonolusModel):
    """ArrangeScoreboardSectionScoresEvent from @sonolus/core 7.16.0."""

    type: Literal["arrangeScoreboardSectionScores"]
    sectionIndex: int | float
    indexes: list[int | float]


class BackgroundConfiguration(SonolusModel):
    """BackgroundConfiguration from @sonolus/core 7.16.0."""

    scope: str | None = None
    blur: int | float
    mask: str


class BackgroundData(SonolusModel):
    """BackgroundData from @sonolus/core 7.16.0."""

    aspectRatio: int | float | None = None
    fit: Literal["contain", "cover", "height", "width"]
    color: str
    scaleX: int | float | None = None
    scaleY: int | float | None = None


class BackgroundItem(SonolusModel):
    """BackgroundItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[2]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    image: Srl
    configuration: Srl


class ClearSuggestionsCommand(SonolusModel):
    """ClearSuggestionsCommand from @sonolus/core 7.16.0."""

    type: Literal["clearSuggestions"]


class ClearSuggestionsEvent(SonolusModel):
    """ClearSuggestionsEvent from @sonolus/core 7.16.0."""

    type: Literal["clearSuggestions"]


class Database(SonolusModel):
    """Database from @sonolus/core 7.16.0."""

    info: DatabaseServerInfo
    posts: list[DatabasePostItem]
    playlists: list[DatabasePlaylistItem]
    levels: list[DatabaseLevelItem]
    skins: list[DatabaseSkinItem]
    backgrounds: list[DatabaseBackgroundItem]
    effects: list[DatabaseEffectItem]
    particles: list[DatabaseParticleItem]
    engines: list[DatabaseEngineItem]
    replays: list[DatabaseReplayItem]


class DatabaseBackgroundItem(SonolusModel):
    """DatabaseBackgroundItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[2]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    thumbnail: Srl
    data: Srl
    image: Srl
    configuration: Srl


class DatabaseEffectItem(SonolusModel):
    """DatabaseEffectItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[5]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    thumbnail: Srl
    data: Srl
    audio: Srl


class DatabaseEngineItem(SonolusModel):
    """DatabaseEngineItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[13]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    skin: str
    background: str
    effect: str
    particle: str
    thumbnail: Srl
    playData: Srl
    watchData: Srl
    previewData: Srl
    tutorialData: Srl
    rom: Srl | None = None
    configuration: Srl


class DatabaseLevelItem(SonolusModel):
    """DatabaseLevelItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[1]
    rating: int | float
    title: LocalizationText
    artists: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    engine: str
    useSkin: DatabaseUseItem
    useBackground: DatabaseUseItem
    useEffect: DatabaseUseItem
    useParticle: DatabaseUseItem
    cover: Srl
    bgm: Srl
    preview: Srl | None = None
    data: Srl


class DatabaseParticleItem(SonolusModel):
    """DatabaseParticleItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[3]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    thumbnail: Srl
    data: Srl
    texture: Srl


class DatabasePlaylistItem(SonolusModel):
    """DatabasePlaylistItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[1]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    levels: list[str]
    thumbnail: Srl | None = None


class DatabasePostItem(SonolusModel):
    """DatabasePostItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[1]
    title: LocalizationText
    time: int | float
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    thumbnail: Srl | None = None


class DatabaseReplayItem(SonolusModel):
    """DatabaseReplayItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[1]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    level: str
    data: Srl
    configuration: Srl


class DatabaseServerInfo(SonolusModel):
    """DatabaseServerInfo from @sonolus/core 7.16.0."""

    title: LocalizationText
    description: LocalizationText | None = None
    banner: Srl | None = None


class DatabaseSkinItem(SonolusModel):
    """DatabaseSkinItem from @sonolus/core 7.16.0."""

    name: str
    version: Literal[4]
    title: LocalizationText
    subtitle: LocalizationText
    author: LocalizationText
    tags: list[DatabaseTag]
    description: LocalizationText | None = None
    thumbnail: Srl
    data: Srl
    texture: Srl


class DatabaseTag(SonolusModel):
    """DatabaseTag from @sonolus/core 7.16.0."""

    title: LocalizationText | None = None
    icon: str | None = None


class DatabaseUseItemUseDefaultFalse(SonolusModel):
    """DatabaseUseItem variant from @sonolus/core 7.16.0."""

    useDefault: Literal[False]
    item: str


class DatabaseUseItemUseDefaultTrue(SonolusModel):
    """DatabaseUseItem variant from @sonolus/core 7.16.0."""

    useDefault: Literal[True]


class EffectData(SonolusModel):
    """EffectData from @sonolus/core 7.16.0."""

    clips: list[EffectDataClip]


class EffectDataClip(SonolusModel):
    """EffectDataClip from @sonolus/core 7.16.0."""

    name: str
    filename: str


class EffectItem(SonolusModel):
    """EffectItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[5]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    audio: Srl


class EngineConfiguration(SonolusModel):
    """EngineConfiguration from @sonolus/core 7.16.0."""

    optionCategories: list[EngineConfigurationOptionCategory] | None = None
    options: list[EngineConfigurationOption]
    ui: EngineConfigurationUI
    replayFallbackOptionNames: list[str] | None = None


class EngineConfigurationAnimation(SonolusModel):
    """EngineConfigurationAnimation from @sonolus/core 7.16.0."""

    scale: EngineConfigurationAnimationTween
    alpha: EngineConfigurationAnimationTween


class EngineConfigurationAnimationTween(SonolusModel):
    """EngineConfigurationAnimationTween from @sonolus/core 7.16.0."""

    from_: int | float = Field(alias="from")
    to: int | float
    duration: int | float
    ease: Literal[
        "inBack",
        "inCirc",
        "inCubic",
        "inElastic",
        "inExpo",
        "inOutBack",
        "inOutCirc",
        "inOutCubic",
        "inOutElastic",
        "inOutExpo",
        "inOutQuad",
        "inOutQuart",
        "inOutQuint",
        "inOutSine",
        "inQuad",
        "inQuart",
        "inQuint",
        "inSine",
        "linear",
        "none",
        "outBack",
        "outCirc",
        "outCubic",
        "outElastic",
        "outExpo",
        "outInBack",
        "outInCirc",
        "outInCubic",
        "outInElastic",
        "outInExpo",
        "outInQuad",
        "outInQuart",
        "outInQuint",
        "outInSine",
        "outQuad",
        "outQuart",
        "outQuint",
        "outSine",
    ]


class EngineConfigurationOptionCategory(SonolusModel):
    """EngineConfigurationOptionCategory from @sonolus/core 7.16.0."""

    name: str
    title: str


class EngineConfigurationSelectOption(SonolusModel):
    """EngineConfigurationSelectOption from @sonolus/core 7.16.0."""

    name: str
    category: str | None = None
    title: str | None = None
    description: str | None = None
    standard: bool | None = None
    advanced: bool | None = None
    scope: str | None = None
    type: Literal["select"]
    def_: int | float = Field(alias="def")
    values: list[str]


class EngineConfigurationSliderOption(SonolusModel):
    """EngineConfigurationSliderOption from @sonolus/core 7.16.0."""

    name: str
    category: str | None = None
    title: str | None = None
    description: str | None = None
    standard: bool | None = None
    advanced: bool | None = None
    scope: str | None = None
    type: Literal["slider"]
    def_: int | float = Field(alias="def")
    min: int | float
    max: int | float
    step: int | float
    unit: str | None = None


class EngineConfigurationToggleOption(SonolusModel):
    """EngineConfigurationToggleOption from @sonolus/core 7.16.0."""

    name: str
    category: str | None = None
    title: str | None = None
    description: str | None = None
    standard: bool | None = None
    advanced: bool | None = None
    scope: str | None = None
    type: Literal["toggle"]
    def_: Literal[0, 1] = Field(alias="def")


class EngineConfigurationUI(SonolusModel):
    """EngineConfigurationUI from @sonolus/core 7.16.0."""

    scope: str | None = None
    primaryMetric: EngineConfigurationMetric
    secondaryMetric: EngineConfigurationMetric
    menuVisibility: EngineConfigurationVisibility
    judgmentVisibility: EngineConfigurationVisibility
    comboVisibility: EngineConfigurationVisibility
    primaryMetricVisibility: EngineConfigurationVisibility
    secondaryMetricVisibility: EngineConfigurationVisibility
    progressVisibility: EngineConfigurationVisibility
    tutorialNavigationVisibility: EngineConfigurationVisibility
    tutorialInstructionVisibility: EngineConfigurationVisibility
    judgmentAnimation: EngineConfigurationAnimation
    comboAnimation: EngineConfigurationAnimation
    judgmentErrorStyle: EngineConfigurationJudgmentErrorStyle
    judgmentErrorPlacement: EngineConfigurationJudgmentErrorPlacement
    judgmentErrorMin: int | float


class EngineConfigurationVisibility(SonolusModel):
    """EngineConfigurationVisibility from @sonolus/core 7.16.0."""

    scale: int | float
    alpha: int | float


class EngineDataBucket(SonolusModel):
    """EngineDataBucket from @sonolus/core 7.16.0."""

    sprites: list[EngineDataBucketSprite]
    unit: str | None = None


class EngineDataBucketSprite(SonolusModel):
    """EngineDataBucketSprite from @sonolus/core 7.16.0."""

    id: int | float
    fallbackId: int | float | None = None
    x: int | float
    y: int | float
    w: int | float
    h: int | float
    rotation: int | float


class EngineDataFunctionNode(SonolusModel):
    """EngineDataFunctionNode from @sonolus/core 7.16.0."""

    func: Literal[
        "Abs",
        "Add",
        "AddLifeScheduled",
        "And",
        "Arccos",
        "Arcsin",
        "Arctan",
        "Arctan2",
        "BeatToBPM",
        "BeatToStartingBeat",
        "BeatToStartingTime",
        "BeatToTime",
        "Block",
        "Break",
        "Ceil",
        "Clamp",
        "Copy",
        "Cos",
        "Cosh",
        "DebugLog",
        "DebugPause",
        "DecrementPost",
        "DecrementPostPointed",
        "DecrementPostShifted",
        "DecrementPre",
        "DecrementPrePointed",
        "DecrementPreShifted",
        "Degree",
        "DestroyParticleEffect",
        "Divide",
        "DoWhile",
        "Draw",
        "DrawCurvedB",
        "DrawCurvedBT",
        "DrawCurvedL",
        "DrawCurvedLR",
        "DrawCurvedR",
        "DrawCurvedT",
        "EaseInBack",
        "EaseInCirc",
        "EaseInCubic",
        "EaseInElastic",
        "EaseInExpo",
        "EaseInOutBack",
        "EaseInOutCirc",
        "EaseInOutCubic",
        "EaseInOutElastic",
        "EaseInOutExpo",
        "EaseInOutQuad",
        "EaseInOutQuart",
        "EaseInOutQuint",
        "EaseInOutSine",
        "EaseInQuad",
        "EaseInQuart",
        "EaseInQuint",
        "EaseInSine",
        "EaseOutBack",
        "EaseOutCirc",
        "EaseOutCubic",
        "EaseOutElastic",
        "EaseOutExpo",
        "EaseOutInBack",
        "EaseOutInCirc",
        "EaseOutInCubic",
        "EaseOutInElastic",
        "EaseOutInExpo",
        "EaseOutInQuad",
        "EaseOutInQuart",
        "EaseOutInQuint",
        "EaseOutInSine",
        "EaseOutQuad",
        "EaseOutQuart",
        "EaseOutQuint",
        "EaseOutSine",
        "Equal",
        "Execute",
        "Execute0",
        "ExportValue",
        "Floor",
        "Frac",
        "Get",
        "GetPointed",
        "GetShifted",
        "Greater",
        "GreaterOr",
        "HasEffectClip",
        "HasParticleEffect",
        "HasSkinSprite",
        "If",
        "IncrementPost",
        "IncrementPostPointed",
        "IncrementPostShifted",
        "IncrementPre",
        "IncrementPrePointed",
        "IncrementPreShifted",
        "Judge",
        "JudgeSimple",
        "JumpLoop",
        "Lerp",
        "LerpClamped",
        "Less",
        "LessOr",
        "Log",
        "Max",
        "Min",
        "Mod",
        "MoveParticleEffect",
        "Multiply",
        "Negate",
        "Not",
        "NotEqual",
        "Or",
        "Paint",
        "Play",
        "PlayLooped",
        "PlayLoopedScheduled",
        "PlayScheduled",
        "Power",
        "Print",
        "Radian",
        "Random",
        "RandomInteger",
        "Rem",
        "Remap",
        "RemapClamped",
        "Round",
        "Set",
        "SetAdd",
        "SetAddPointed",
        "SetAddShifted",
        "SetDivide",
        "SetDividePointed",
        "SetDivideShifted",
        "SetMod",
        "SetModPointed",
        "SetModShifted",
        "SetMultiply",
        "SetMultiplyPointed",
        "SetMultiplyShifted",
        "SetPointed",
        "SetPower",
        "SetPowerPointed",
        "SetPowerShifted",
        "SetRem",
        "SetRemPointed",
        "SetRemShifted",
        "SetShifted",
        "SetSubtract",
        "SetSubtractPointed",
        "SetSubtractShifted",
        "Sign",
        "Sin",
        "Sinh",
        "Spawn",
        "SpawnParticleEffect",
        "StackEnter",
        "StackGet",
        "StackGetFrame",
        "StackGetFramePointer",
        "StackGetPointer",
        "StackGrow",
        "StackInit",
        "StackLeave",
        "StackPop",
        "StackPush",
        "StackSet",
        "StackSetFrame",
        "StackSetFramePointer",
        "StackSetPointer",
        "StopLooped",
        "StopLoopedScheduled",
        "StreamGetNextKey",
        "StreamGetPreviousKey",
        "StreamGetValue",
        "StreamHas",
        "StreamSet",
        "Subtract",
        "Switch",
        "SwitchInteger",
        "SwitchIntegerWithDefault",
        "SwitchWithDefault",
        "Tan",
        "Tanh",
        "TimeToScaledTime",
        "TimeToStartingScaledTime",
        "TimeToStartingTime",
        "TimeToTimeScale",
        "Trunc",
        "Unlerp",
        "UnlerpClamped",
        "While",
    ]
    args: list[int | float]


class EngineDataValueNode(SonolusModel):
    """EngineDataValueNode from @sonolus/core 7.16.0."""

    value: int | float


class EngineItem(SonolusModel):
    """EngineItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[13]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    skin: SkinItem
    background: BackgroundItem
    effect: EffectItem
    particle: ParticleItem
    thumbnail: Srl
    playData: Srl
    watchData: Srl
    previewData: Srl
    tutorialData: Srl
    rom: Srl | None = None
    configuration: Srl


class EnginePlayData(SonolusModel):
    """EnginePlayData from @sonolus/core 7.16.0."""

    skin: EnginePlayDataSkin
    effect: EnginePlayDataEffect
    particle: EnginePlayDataParticle
    buckets: list[EngineDataBucket]
    archetypes: list[EnginePlayDataArchetype]
    nodes: list[EngineDataNode]
    entityMemoryLength: int | float | None = None
    entityDataLength: int | float | None = None
    entitySharedMemoryLength: int | float | None = None


class EnginePlayDataArchetype(SonolusModel):
    """EnginePlayDataArchetype from @sonolus/core 7.16.0."""

    name: str
    hasInput: bool
    preprocess: EnginePlayDataArchetypeCallback | None = None
    spawnOrder: EnginePlayDataArchetypeCallback | None = None
    shouldSpawn: EnginePlayDataArchetypeCallback | None = None
    initialize: EnginePlayDataArchetypeCallback | None = None
    updateSequential: EnginePlayDataArchetypeCallback | None = None
    touch: EnginePlayDataArchetypeCallback | None = None
    updateParallel: EnginePlayDataArchetypeCallback | None = None
    terminate: EnginePlayDataArchetypeCallback | None = None
    imports: list[EnginePlayDataArchetypeImport]
    exports: list[str]


class EnginePlayDataArchetypeCallback(SonolusModel):
    """EnginePlayDataArchetypeCallback from @sonolus/core 7.16.0."""

    index: int | float
    order: int | float | None = None


class EnginePlayDataArchetypeImport(SonolusModel):
    """EnginePlayDataArchetype["imports"][number] from @sonolus/core 7.16.0."""

    name: str
    index: int | float
    def_: int | float | None = Field(default=None, alias="def")


class EnginePlayDataEffect(SonolusModel):
    """EnginePlayData["effect"] from @sonolus/core 7.16.0."""

    clips: list[EnginePlayDataEffectClip]


class EnginePlayDataEffectClip(SonolusModel):
    """EnginePlayData["effect"]["clips"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EnginePlayDataParticle(SonolusModel):
    """EnginePlayData["particle"] from @sonolus/core 7.16.0."""

    effects: list[EnginePlayDataParticleEffect]


class EnginePlayDataParticleEffect(SonolusModel):
    """EnginePlayData["particle"]["effects"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EnginePlayDataSkin(SonolusModel):
    """EnginePlayData["skin"] from @sonolus/core 7.16.0."""

    renderMode: Literal["default", "lightweight", "standard"] | None = None
    sprites: list[EnginePlayDataSkinSprite]


class EnginePlayDataSkinSprite(SonolusModel):
    """EnginePlayData["skin"]["sprites"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EnginePreviewData(SonolusModel):
    """EnginePreviewData from @sonolus/core 7.16.0."""

    skin: EnginePreviewDataSkin
    archetypes: list[EnginePreviewDataArchetype]
    nodes: list[EngineDataNode]
    entityDataLength: int | float | None = None
    entitySharedMemoryLength: int | float | None = None


class EnginePreviewDataArchetype(SonolusModel):
    """EnginePreviewDataArchetype from @sonolus/core 7.16.0."""

    name: str
    preprocess: EnginePreviewDataArchetypeCallback | None = None
    render: EnginePreviewDataArchetypeCallback | None = None
    imports: list[EnginePreviewDataArchetypeImport]


class EnginePreviewDataArchetypeCallback(SonolusModel):
    """EnginePreviewDataArchetypeCallback from @sonolus/core 7.16.0."""

    index: int | float
    order: int | float | None = None


class EnginePreviewDataArchetypeImport(SonolusModel):
    """EnginePreviewDataArchetype["imports"][number] from @sonolus/core 7.16.0."""

    name: str
    index: int | float
    def_: int | float | None = Field(default=None, alias="def")


class EnginePreviewDataSkin(SonolusModel):
    """EnginePreviewData["skin"] from @sonolus/core 7.16.0."""

    renderMode: Literal["default", "lightweight", "standard"] | None = None
    sprites: list[EnginePreviewDataSkinSprite]


class EnginePreviewDataSkinSprite(SonolusModel):
    """EnginePreviewData["skin"]["sprites"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineTutorialData(SonolusModel):
    """EngineTutorialData from @sonolus/core 7.16.0."""

    skin: EngineTutorialDataSkin
    effect: EngineTutorialDataEffect
    particle: EngineTutorialDataParticle
    instruction: EngineTutorialDataInstruction
    preprocess: int | float | None = None
    navigate: int | float | None = None
    update: int | float | None = None
    nodes: list[EngineDataNode]


class EngineTutorialDataEffect(SonolusModel):
    """EngineTutorialData["effect"] from @sonolus/core 7.16.0."""

    clips: list[EngineTutorialDataEffectClip]


class EngineTutorialDataEffectClip(SonolusModel):
    """EngineTutorialData["effect"]["clips"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineTutorialDataInstruction(SonolusModel):
    """EngineTutorialData["instruction"] from @sonolus/core 7.16.0."""

    texts: list[EngineTutorialDataInstructionText]
    icons: list[EngineTutorialDataInstructionIcon]


class EngineTutorialDataInstructionIcon(SonolusModel):
    """EngineTutorialData["instruction"]["icons"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineTutorialDataInstructionText(SonolusModel):
    """EngineTutorialData["instruction"]["texts"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineTutorialDataParticle(SonolusModel):
    """EngineTutorialData["particle"] from @sonolus/core 7.16.0."""

    effects: list[EngineTutorialDataParticleEffect]


class EngineTutorialDataParticleEffect(SonolusModel):
    """EngineTutorialData["particle"]["effects"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineTutorialDataSkin(SonolusModel):
    """EngineTutorialData["skin"] from @sonolus/core 7.16.0."""

    renderMode: Literal["default", "lightweight", "standard"] | None = None
    sprites: list[EngineTutorialDataSkinSprite]


class EngineTutorialDataSkinSprite(SonolusModel):
    """EngineTutorialData["skin"]["sprites"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineWatchData(SonolusModel):
    """EngineWatchData from @sonolus/core 7.16.0."""

    skin: EngineWatchDataSkin
    effect: EngineWatchDataEffect
    particle: EngineWatchDataParticle
    buckets: list[EngineDataBucket]
    archetypes: list[EngineWatchDataArchetype]
    updateSpawn: int | float | None = None
    nodes: list[EngineDataNode]
    entityMemoryLength: int | float | None = None
    entityDataLength: int | float | None = None
    entitySharedMemoryLength: int | float | None = None


class EngineWatchDataArchetype(SonolusModel):
    """EngineWatchDataArchetype from @sonolus/core 7.16.0."""

    name: str
    hasInput: bool
    preprocess: EngineWatchDataArchetypeCallback | None = None
    spawnTime: EngineWatchDataArchetypeCallback | None = None
    despawnTime: EngineWatchDataArchetypeCallback | None = None
    initialize: EngineWatchDataArchetypeCallback | None = None
    updateSequential: EngineWatchDataArchetypeCallback | None = None
    updateParallel: EngineWatchDataArchetypeCallback | None = None
    terminate: EngineWatchDataArchetypeCallback | None = None
    imports: list[EngineWatchDataArchetypeImport]


class EngineWatchDataArchetypeCallback(SonolusModel):
    """EngineWatchDataArchetypeCallback from @sonolus/core 7.16.0."""

    index: int | float
    order: int | float | None = None


class EngineWatchDataArchetypeImport(SonolusModel):
    """EngineWatchDataArchetype["imports"][number] from @sonolus/core 7.16.0."""

    name: str
    index: int | float
    def_: int | float | None = Field(default=None, alias="def")


class EngineWatchDataEffect(SonolusModel):
    """EngineWatchData["effect"] from @sonolus/core 7.16.0."""

    clips: list[EngineWatchDataEffectClip]


class EngineWatchDataEffectClip(SonolusModel):
    """EngineWatchData["effect"]["clips"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineWatchDataParticle(SonolusModel):
    """EngineWatchData["particle"] from @sonolus/core 7.16.0."""

    effects: list[EngineWatchDataParticleEffect]


class EngineWatchDataParticleEffect(SonolusModel):
    """EngineWatchData["particle"]["effects"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class EngineWatchDataSkin(SonolusModel):
    """EngineWatchData["skin"] from @sonolus/core 7.16.0."""

    renderMode: Literal["default", "lightweight", "standard"] | None = None
    sprites: list[EngineWatchDataSkinSprite]


class EngineWatchDataSkinSprite(SonolusModel):
    """EngineWatchData["skin"]["sprites"][number] from @sonolus/core 7.16.0."""

    name: str
    id: int | float


class FinishGameplayCommand(SonolusModel):
    """FinishGameplayCommand from @sonolus/core 7.16.0."""

    type: Literal["finishGameplay"]
    state: str
    result: GameplayResult


class GameplayResult(SonolusModel):
    """GameplayResult from @sonolus/core 7.16.0."""

    grade: Literal["allPerfect", "fail", "fullCombo", "pass"]
    arcadeScore: int | float
    accuracyScore: int | float
    combo: int | float
    perfect: int | float
    great: int | float
    good: int | float
    miss: int | float
    totalCount: int | float


class InsertScoreboardSectionEvent(SonolusModel):
    """InsertScoreboardSectionEvent from @sonolus/core 7.16.0."""

    type: Literal["insertScoreboardSection"]
    index: int | float
    scoreboardSection: ScoreboardSection


class InsertScoreboardSectionScoreEvent(SonolusModel):
    """InsertScoreboardSectionScoreEvent from @sonolus/core 7.16.0."""

    type: Literal["insertScoreboardSectionScore"]
    sectionIndex: int | float
    index: int | float
    score: ScoreEntry


class LevelData(SonolusModel):
    """LevelData from @sonolus/core 7.16.0."""

    bgmOffset: int | float
    entities: list[LevelDataEntity]


class LevelDataEntity(SonolusModel):
    """LevelDataEntity from @sonolus/core 7.16.0."""

    name: str | None = None
    archetype: str
    data: list[LevelDataEntityDataRef | LevelDataEntityDataValue]


class LevelDataEntityDataRef(SonolusModel):
    """LevelDataEntity["data"][number] variant from @sonolus/core 7.16.0."""

    name: str
    ref: str


class LevelDataEntityDataValue(SonolusModel):
    """LevelDataEntity["data"][number] variant from @sonolus/core 7.16.0."""

    name: str
    value: int | float


class LevelItem(SonolusModel):
    """LevelItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[1]
    rating: int | float
    title: str
    artists: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    engine: EngineItem
    useSkin: UseItem[SkinItem]
    useBackground: UseItem[BackgroundItem]
    useEffect: UseItem[EffectItem]
    useParticle: UseItem[ParticleItem]
    cover: Srl
    bgm: Srl
    preview: Srl | None = None
    data: Srl


class LevelOptionEntry(SonolusModel):
    """LevelOptionEntry from @sonolus/core 7.16.0."""

    index: int | float
    value: int | float


class MergeScoreboardSectionScoresEvent(SonolusModel):
    """MergeScoreboardSectionScoresEvent from @sonolus/core 7.16.0."""

    type: Literal["mergeScoreboardSectionScores"]
    index: int | float
    scores: list[ScoreEntry]


class MoveScoreboardSectionEvent(SonolusModel):
    """MoveScoreboardSectionEvent from @sonolus/core 7.16.0."""

    type: Literal["moveScoreboardSection"]
    fromIndex: int | float
    toIndex: int | float


class MoveScoreboardSectionScoreEvent(SonolusModel):
    """MoveScoreboardSectionScoreEvent from @sonolus/core 7.16.0."""

    type: Literal["moveScoreboardSectionScore"]
    sectionIndex: int | float
    fromIndex: int | float
    toIndex: int | float


class PackageInfo(SonolusModel):
    """PackageInfo from @sonolus/core 7.16.0."""

    shouldUpdate: bool | None = None


class ParticleData(SonolusModel):
    """ParticleData from @sonolus/core 7.16.0."""

    width: int | float
    height: int | float
    interpolation: bool
    sprites: list[ParticleDataSprite]
    effects: list[ParticleDataEffect]


class ParticleDataEffect(SonolusModel):
    """ParticleDataEffect from @sonolus/core 7.16.0."""

    name: str
    transform: ParticleDataTransform
    groups: list[ParticleDataGroup]


class ParticleDataGroup(SonolusModel):
    """ParticleDataGroup from @sonolus/core 7.16.0."""

    count: int | float
    particles: list[ParticleDataGroupParticle]


class ParticleDataGroupParticle(SonolusModel):
    """ParticleDataGroupParticle from @sonolus/core 7.16.0."""

    sprite: int | float
    color: str
    start: int | float
    duration: int | float
    x: ParticleDataGroupParticleProperty
    y: ParticleDataGroupParticleProperty
    w: ParticleDataGroupParticleProperty
    h: ParticleDataGroupParticleProperty
    r: ParticleDataGroupParticleProperty
    a: ParticleDataGroupParticleProperty


class ParticleDataGroupParticleProperty(SonolusModel):
    """ParticleDataGroupParticleProperty from @sonolus/core 7.16.0."""

    from_: ParticleDataGroupParticlePropertyExpression | None = Field(
        default=None, alias="from"
    )
    to: ParticleDataGroupParticlePropertyExpression | None = None
    ease: (
        Literal[
            "inBack",
            "inCirc",
            "inCubic",
            "inElastic",
            "inExpo",
            "inOutBack",
            "inOutCirc",
            "inOutCubic",
            "inOutElastic",
            "inOutExpo",
            "inOutQuad",
            "inOutQuart",
            "inOutQuint",
            "inOutSine",
            "inQuad",
            "inQuart",
            "inQuint",
            "inSine",
            "linear",
            "none",
            "outBack",
            "outCirc",
            "outCubic",
            "outElastic",
            "outExpo",
            "outInBack",
            "outInCirc",
            "outInCubic",
            "outInElastic",
            "outInExpo",
            "outInQuad",
            "outInQuart",
            "outInQuint",
            "outInSine",
            "outQuad",
            "outQuart",
            "outQuint",
            "outSine",
        ]
        | None
    ) = None


class ParticleDataGroupParticlePropertyExpression(SonolusModel):
    """ParticleDataGroupParticlePropertyExpression from @sonolus/core 7.16.0."""

    c: int | float | None = None
    cosr1: int | float | None = None
    cosr2: int | float | None = None
    cosr3: int | float | None = None
    cosr4: int | float | None = None
    cosr5: int | float | None = None
    cosr6: int | float | None = None
    cosr7: int | float | None = None
    cosr8: int | float | None = None
    r1: int | float | None = None
    r2: int | float | None = None
    r3: int | float | None = None
    r4: int | float | None = None
    r5: int | float | None = None
    r6: int | float | None = None
    r7: int | float | None = None
    r8: int | float | None = None
    sinr1: int | float | None = None
    sinr2: int | float | None = None
    sinr3: int | float | None = None
    sinr4: int | float | None = None
    sinr5: int | float | None = None
    sinr6: int | float | None = None
    sinr7: int | float | None = None
    sinr8: int | float | None = None


class ParticleDataSprite(SonolusModel):
    """ParticleDataSprite from @sonolus/core 7.16.0."""

    x: int | float
    y: int | float
    w: int | float
    h: int | float


class ParticleDataTransform(SonolusModel):
    """ParticleDataTransform from @sonolus/core 7.16.0."""

    x1: ParticleDataTransformValue
    x2: ParticleDataTransformValue
    x3: ParticleDataTransformValue
    x4: ParticleDataTransformValue
    y1: ParticleDataTransformValue
    y2: ParticleDataTransformValue
    y3: ParticleDataTransformValue
    y4: ParticleDataTransformValue


class ParticleDataTransformValue(SonolusModel):
    """ParticleDataTransform[keyof ParticleDataTransform] from @sonolus/core 7.16.0."""

    c: int | float | None = None
    cosr1: int | float | None = None
    cosr2: int | float | None = None
    cosr3: int | float | None = None
    cosr4: int | float | None = None
    cosr5: int | float | None = None
    cosr6: int | float | None = None
    cosr7: int | float | None = None
    cosr8: int | float | None = None
    r1: int | float | None = None
    r2: int | float | None = None
    r3: int | float | None = None
    r4: int | float | None = None
    r5: int | float | None = None
    r6: int | float | None = None
    r7: int | float | None = None
    r8: int | float | None = None
    sinr1: int | float | None = None
    sinr2: int | float | None = None
    sinr3: int | float | None = None
    sinr4: int | float | None = None
    sinr5: int | float | None = None
    sinr6: int | float | None = None
    sinr7: int | float | None = None
    sinr8: int | float | None = None
    x1: int | float | None = None
    x2: int | float | None = None
    x3: int | float | None = None
    x4: int | float | None = None
    y1: int | float | None = None
    y2: int | float | None = None
    y3: int | float | None = None
    y4: int | float | None = None


class ParticleItem(SonolusModel):
    """ParticleItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[3]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    texture: Srl


class PlaylistItem(SonolusModel):
    """PlaylistItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[1]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    levels: list[LevelItem]
    thumbnail: Srl | None = None


class PostItem(SonolusModel):
    """PostItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[1]
    title: str
    time: int | float
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    thumbnail: Srl | None = None


class QuickChatMessage(SonolusModel):
    """QuickChatMessage from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    type: Literal["quick"]
    value: Literal["gg", "glhf", "hello", "ns", "ty"]


class RemoveScoreboardSectionEvent(SonolusModel):
    """RemoveScoreboardSectionEvent from @sonolus/core 7.16.0."""

    type: Literal["removeScoreboardSection"]
    index: int | float


class RemoveScoreboardSectionScoreEvent(SonolusModel):
    """RemoveScoreboardSectionScoreEvent from @sonolus/core 7.16.0."""

    type: Literal["removeScoreboardSectionScore"]
    sectionIndex: int | float
    index: int | float


class RemoveSuggestionCommand(SonolusModel):
    """RemoveSuggestionCommand from @sonolus/core 7.16.0."""

    type: Literal["removeSuggestion"]
    suggestion: Suggestion


class RemoveSuggestionEvent(SonolusModel):
    """RemoveSuggestionEvent from @sonolus/core 7.16.0."""

    type: Literal["removeSuggestion"]
    suggestion: Suggestion


class RemoveUserCommand(SonolusModel):
    """RemoveUserCommand from @sonolus/core 7.16.0."""

    type: Literal["removeUser"]
    userId: ServiceUserId


class RemoveUserEvent(SonolusModel):
    """RemoveUserEvent from @sonolus/core 7.16.0."""

    type: Literal["removeUser"]
    user: RoomUser


class ReplayConfiguration(SonolusModel):
    """ReplayConfiguration from @sonolus/core 7.16.0."""

    options: list[int | float]
    optionNames: list[str] | None = None


class ReplayData(SonolusModel):
    """ReplayData from @sonolus/core 7.16.0."""

    startTime: int | float
    saveTime: int | float
    duration: int | float
    inputOffset: int | float
    playArea: ReplayDataPlayArea
    result: GameplayResult
    inputs: ReplayDataInputs
    entities: list[ReplayDataEntity]
    touches: ReplayDataTouches
    streams: list[ReplayDataStream] | None = None


class ReplayDataEntity(SonolusModel):
    """ReplayData["entities"][number] from @sonolus/core 7.16.0."""

    data: list[ReplayDataEntityData]


class ReplayDataEntityData(SonolusModel):
    """ReplayData["entities"][number]["data"][number] from @sonolus/core 7.16.0."""

    name: str
    value: int | float


class ReplayDataInputs(SonolusModel):
    """ReplayData["inputs"] from @sonolus/core 7.16.0."""

    entityIndex: list[int | float]
    time: list[int | float]
    judgment: list[int | float]
    accuracy: list[int | float]


class ReplayDataPlayArea(SonolusModel):
    """ReplayData["playArea"] from @sonolus/core 7.16.0."""

    width: int | float
    height: int | float


class ReplayDataStream(SonolusModel):
    """ReplayData["streams"][number] from @sonolus/core 7.16.0."""

    id: int | float
    keys: list[int | float]
    values: list[int | float]


class ReplayDataTouches(SonolusModel):
    """ReplayData["touches"] from @sonolus/core 7.16.0."""

    l: list[int | float]
    t: list[int | float]
    x: list[int | float]
    y: list[int | float]


class ReplayItem(SonolusModel):
    """ReplayItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[1]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    level: LevelItem
    data: Srl
    configuration: Srl


class ReportUserCommand(SonolusModel):
    """ReportUserCommand from @sonolus/core 7.16.0."""

    type: Literal["reportUser"]
    userId: ServiceUserId
    optionValues: str


class ResetScoreboardCommand(SonolusModel):
    """ResetScoreboardCommand from @sonolus/core 7.16.0."""

    type: Literal["resetScoreboard"]


class ResultEntry(SonolusModel):
    """ResultEntry from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    result: GameplayResult


class RoomItem(SonolusModel):
    """RoomItem from @sonolus/core 7.16.0."""

    name: str
    title: str
    subtitle: str
    master: str
    masterUser: UserItem | None = None
    tags: list[Tag]
    cover: Srl | None = None
    bgm: Srl | None = None
    preview: Srl | None = None


class RoomTextChatMessage(SonolusModel):
    """RoomTextChatMessage from @sonolus/core 7.16.0."""

    userId: None
    type: Literal["text"]
    value: str


class RoomUser(SonolusModel):
    """RoomUser from @sonolus/core 7.16.0."""

    authentication: str
    signature: str


class ScoreEntry(SonolusModel):
    """ScoreEntry from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    value: str


class ScoreboardSection(SonolusModel):
    """ScoreboardSection from @sonolus/core 7.16.0."""

    title: str
    icon: str | None = None
    scores: list[ScoreEntry]


class ServerAuthenticateRequest(SonolusModel):
    """ServerAuthenticateRequest from @sonolus/core 7.16.0."""

    type: Literal["authenticateServer"]
    address: str
    time: int | float
    userProfile: ServiceUserProfile


class ServerAuthenticateResponse(SonolusModel):
    """ServerAuthenticateResponse from @sonolus/core 7.16.0."""

    session: str
    expiration: int | float


class ServerCollectionItemOption(SonolusModel):
    """ServerCollectionItemOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["collectionItem"]
    itemType: ItemType


class ServerConfiguration(SonolusModel):
    """ServerConfiguration from @sonolus/core 7.16.0."""

    options: list[ServerOption]


class ServerCreateItemRequest(SonolusModel):
    """ServerCreateItemRequest from @sonolus/core 7.16.0."""

    values: str


class ServerCreateItemResponse(SonolusModel):
    """ServerCreateItemResponse from @sonolus/core 7.16.0."""

    key: str
    hashes: list[str]
    shouldUpdateInfo: bool | None = None
    shouldNavigateToItem: str | None = None


class ServerCreateRoomRequest(SonolusModel):
    """ServerCreateRoomRequest from @sonolus/core 7.16.0."""


class ServerCreateRoomResponse(SonolusModel):
    """ServerCreateRoomResponse from @sonolus/core 7.16.0."""

    name: str
    key: str


class ServerFileOption(SonolusModel):
    """ServerFileOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["file"]
    def_: str = Field(alias="def")
    validation: (
        Annotated[
            ServerFileOptionValidationAudio[Literal["audio"]]
            | ServerFileOptionValidationAudio[Literal["levelBgm"]]
            | ServerFileOptionValidationAudio[Literal["levelPreview"]]
            | ServerFileOptionValidationAudio[Literal["roomBgm"]]
            | ServerFileOptionValidationAudio[Literal["roomPreview"]]
            | ServerFileOptionValidationFile[Literal["engineRom"]]
            | ServerFileOptionValidationFile[Literal["file"]]
            | ServerFileOptionValidationImage[Literal["backgroundImage"]]
            | ServerFileOptionValidationImage[Literal["backgroundThumbnail"]]
            | ServerFileOptionValidationImage[Literal["effectThumbnail"]]
            | ServerFileOptionValidationImage[Literal["engineThumbnail"]]
            | ServerFileOptionValidationImage[Literal["image"]]
            | ServerFileOptionValidationImage[Literal["levelCover"]]
            | ServerFileOptionValidationImage[Literal["particleTexture"]]
            | ServerFileOptionValidationImage[Literal["particleThumbnail"]]
            | ServerFileOptionValidationImage[Literal["playlistThumbnail"]]
            | ServerFileOptionValidationImage[Literal["postThumbnail"]]
            | ServerFileOptionValidationImage[Literal["roomCover"]]
            | ServerFileOptionValidationImage[Literal["serverBanner"]]
            | ServerFileOptionValidationImage[Literal["skinTexture"]]
            | ServerFileOptionValidationImage[Literal["skinThumbnail"]]
            | ServerFileOptionValidationJson[Literal["backgroundConfiguration"]]
            | ServerFileOptionValidationJson[Literal["backgroundData"]]
            | ServerFileOptionValidationJson[Literal["effectData"]]
            | ServerFileOptionValidationJson[Literal["engineConfiguration"]]
            | ServerFileOptionValidationJson[Literal["enginePlayData"]]
            | ServerFileOptionValidationJson[Literal["enginePreviewData"]]
            | ServerFileOptionValidationJson[Literal["engineTutorialData"]]
            | ServerFileOptionValidationJson[Literal["engineWatchData"]]
            | ServerFileOptionValidationJson[Literal["levelData"]]
            | ServerFileOptionValidationJson[Literal["particleData"]]
            | ServerFileOptionValidationJson[Literal["replayConfiguration"]]
            | ServerFileOptionValidationJson[Literal["replayData"]]
            | ServerFileOptionValidationJson[Literal["skinData"]]
            | ServerFileOptionValidationZip[Literal["effectAudio"]]
            | ServerFileOptionValidationZip[Literal["zip"]],
            Field(discriminator="type"),
        ]
        | None
    ) = None


class ServerFileOptionValidationAudio(SonolusModel, Generic[T]):
    """ServerFileOptionValidationAudio from @sonolus/core 7.16.0."""

    type: T
    minSize: int | float | None = None
    maxSize: int | float | None = None
    minLength: int | float | None = None
    maxLength: int | float | None = None


class ServerFileOptionValidationFile(SonolusModel, Generic[T]):
    """ServerFileOptionValidationFile from @sonolus/core 7.16.0."""

    type: T
    minSize: int | float | None = None
    maxSize: int | float | None = None


class ServerFileOptionValidationImage(SonolusModel, Generic[T]):
    """ServerFileOptionValidationImage from @sonolus/core 7.16.0."""

    type: T
    minSize: int | float | None = None
    maxSize: int | float | None = None
    minWidth: int | float | None = None
    maxWidth: int | float | None = None
    minHeight: int | float | None = None
    maxHeight: int | float | None = None


class ServerFileOptionValidationJson(SonolusModel, Generic[T]):
    """ServerFileOptionValidationJson from @sonolus/core 7.16.0."""

    type: T
    minSize: int | float | None = None
    maxSize: int | float | None = None


class ServerFileOptionValidationZip(SonolusModel, Generic[T]):
    """ServerFileOptionValidationZip from @sonolus/core 7.16.0."""

    type: T
    minSize: int | float | None = None
    maxSize: int | float | None = None


class ServerForm(SonolusModel):
    """ServerForm from @sonolus/core 7.16.0."""

    type: str
    title: str
    icon: str | None = None
    description: str | None = None
    help: str | None = None
    requireConfirmation: bool
    options: list[ServerOption]


class ServerInfo(SonolusModel):
    """ServerInfo from @sonolus/core 7.16.0."""

    title: str
    description: str | None = None
    buttons: list[ServerInfoButton]
    configuration: ServerConfiguration
    banner: Srl | None = None


class ServerInfoAuthenticationButton(SonolusModel):
    """ServerInfoAuthenticationButton from @sonolus/core 7.16.0."""

    type: Literal["authentication"]


class ServerInfoConfigurationButton(SonolusModel):
    """ServerInfoConfigurationButton from @sonolus/core 7.16.0."""

    type: Literal["configuration"]


class ServerInfoItemButton(SonolusModel):
    """ServerInfoItemButton from @sonolus/core 7.16.0."""

    type: Literal[
        "background",
        "effect",
        "engine",
        "level",
        "particle",
        "playlist",
        "post",
        "replay",
        "room",
        "skin",
        "user",
    ]
    title: str | None = None
    icon: str | None = None
    badgeCount: int | float | None = None
    infoType: str | None = None
    itemName: str | None = None


class ServerItemCommunityComment(SonolusModel):
    """ServerItemCommunityComment from @sonolus/core 7.16.0."""

    name: str
    author: str
    authorUser: UserItem | None = None
    time: int | float
    content: str
    actions: list[ServerForm]


class ServerItemCommunityCommentList(SonolusModel):
    """ServerItemCommunityCommentList from @sonolus/core 7.16.0."""

    pageCount: int | float
    cursor: str | None = None
    comments: list[ServerItemCommunityComment]


class ServerItemCommunityInfo(SonolusModel):
    """ServerItemCommunityInfo from @sonolus/core 7.16.0."""

    actions: list[ServerForm]
    topComments: list[ServerItemCommunityComment]


class ServerItemDetails(SonolusModel, Generic[T]):
    """ServerItemDetails from @sonolus/core 7.16.0."""

    item: T
    description: str | None = None
    actions: list[ServerForm]
    hasCommunity: bool
    leaderboards: list[ServerItemLeaderboard]
    sections: list[ServerItemSection]


class ServerItemInfo(SonolusModel):
    """ServerItemInfo from @sonolus/core 7.16.0."""

    title: str | None = None
    creates: list[ServerForm] | None = None
    searches: list[ServerForm] | None = None
    quickSearchValues: str | None = None
    sections: list[ServerItemSection]
    banner: Srl | None = None


class ServerItemLeaderboard(SonolusModel):
    """ServerItemLeaderboard from @sonolus/core 7.16.0."""

    name: str
    title: str
    description: str | None = None


class ServerItemLeaderboardDetails(SonolusModel):
    """ServerItemLeaderboardDetails from @sonolus/core 7.16.0."""

    topRecords: list[ServerItemLeaderboardRecord]


class ServerItemLeaderboardRecord(SonolusModel):
    """ServerItemLeaderboardRecord from @sonolus/core 7.16.0."""

    name: str
    rank: str
    player: str
    playerUser: UserItem | None = None
    value: str


class ServerItemLeaderboardRecordDetails(SonolusModel):
    """ServerItemLeaderboardRecordDetails from @sonolus/core 7.16.0."""

    replays: list[ReplayItem]


class ServerItemLeaderboardRecordList(SonolusModel):
    """ServerItemLeaderboardRecordList from @sonolus/core 7.16.0."""

    pageCount: int | float
    cursor: str | None = None
    records: list[ServerItemLeaderboardRecord]


class ServerItemList(SonolusModel, Generic[T]):
    """ServerItemList from @sonolus/core 7.16.0."""

    title: str | None = None
    pageCount: int | float
    cursor: str | None = None
    items: list[T]
    searches: list[ServerForm] | None = None
    quickSearchValues: str | None = None


class ServerItemSectionTyped(SonolusModel, Generic[TItemType, TItem]):
    """ServerItemSectionTyped from @sonolus/core 7.16.0."""

    title: str
    icon: str | None = None
    description: str | None = None
    help: str | None = None
    itemType: TItemType
    items: list[TItem]
    search: ServerForm | None = None
    searchValues: str | None = None


class ServerJoinRoomRequest(SonolusModel):
    """ServerJoinRoomRequest from @sonolus/core 7.16.0."""

    type: Literal["authenticateMultiplayer"]
    address: str
    room: str
    time: int | float
    userProfile: ServiceUserProfile


class ServerJoinRoomResponse(SonolusModel):
    """ServerJoinRoomResponse from @sonolus/core 7.16.0."""

    url: str
    type: Literal["round"]
    session: str


class ServerLevelResultInfo(SonolusModel):
    """ServerLevelResultInfo from @sonolus/core 7.16.0."""

    submits: list[ServerForm] | None = None


class ServerMessage(SonolusModel):
    """ServerMessage from @sonolus/core 7.16.0."""

    message: str | None = None


class ServerMultiOption(SonolusModel):
    """ServerMultiOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["multi"]
    def_: list[bool] = Field(alias="def")
    values: list[ServerMultiOptionValue]


class ServerMultiOptionValue(SonolusModel):
    """ServerMultiOption["values"][number] from @sonolus/core 7.16.0."""

    name: str
    title: str


class ServerSelectOption(SonolusModel):
    """ServerSelectOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["select"]
    def_: str = Field(alias="def")
    values: list[ServerSelectOptionValue]


class ServerSelectOptionValue(SonolusModel):
    """ServerSelectOption["values"][number] from @sonolus/core 7.16.0."""

    name: str
    title: str


class ServerServerItemOption(SonolusModel):
    """ServerServerItemOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["serverItem"]
    itemType: ItemType
    infoType: str | None = None
    def_: Sil | None = Field(alias="def")
    allowOtherServers: bool


class ServerServerItemsOption(SonolusModel):
    """ServerServerItemsOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["serverItems"]
    itemType: ItemType
    infoType: str | None = None
    def_: list[Sil] = Field(alias="def")
    allowOtherServers: bool
    limit: int | float


class ServerSliderOption(SonolusModel):
    """ServerSliderOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["slider"]
    def_: int | float = Field(alias="def")
    min: int | float
    max: int | float
    step: int | float
    unit: str | None = None


class ServerSubmitItemActionRequest(SonolusModel):
    """ServerSubmitItemActionRequest from @sonolus/core 7.16.0."""

    values: str


class ServerSubmitItemActionResponse(SonolusModel):
    """ServerSubmitItemActionResponse from @sonolus/core 7.16.0."""

    key: str
    hashes: list[str]
    shouldUpdateItem: bool | None = None
    shouldRemoveItem: bool | None = None
    shouldNavigateToItem: str | None = None


class ServerSubmitItemCommunityActionRequest(SonolusModel):
    """ServerSubmitItemCommunityActionRequest from @sonolus/core 7.16.0."""

    values: str


class ServerSubmitItemCommunityActionResponse(SonolusModel):
    """ServerSubmitItemCommunityActionResponse from @sonolus/core 7.16.0."""

    key: str
    hashes: list[str]
    shouldUpdateCommunity: bool | None = None
    shouldUpdateComments: bool | None = None
    shouldNavigateCommentsToPage: int | float | None = None


class ServerSubmitItemCommunityCommentActionRequest(SonolusModel):
    """ServerSubmitItemCommunityCommentActionRequest from @sonolus/core 7.16.0."""

    values: str


class ServerSubmitItemCommunityCommentActionResponse(SonolusModel):
    """ServerSubmitItemCommunityCommentActionResponse from @sonolus/core 7.16.0."""

    key: str
    hashes: list[str]
    shouldUpdateCommunity: bool | None = None
    shouldUpdateComments: bool | None = None
    shouldNavigateCommentsToPage: int | float | None = None


class ServerSubmitLevelResultRequest(SonolusModel):
    """ServerSubmitLevelResultRequest from @sonolus/core 7.16.0."""

    replay: ReplayItem
    values: str


class ServerSubmitLevelResultResponse(SonolusModel):
    """ServerSubmitLevelResultResponse from @sonolus/core 7.16.0."""

    key: str
    hashes: list[str]


class ServerTextAreaOption(SonolusModel):
    """ServerTextAreaOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["textArea"]
    def_: str = Field(alias="def")
    placeholder: str
    limit: int | float
    shortcuts: list[str]


class ServerTextOption(SonolusModel):
    """ServerTextOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["text"]
    def_: str = Field(alias="def")
    placeholder: str
    limit: int | float
    shortcuts: list[str]


class ServerToggleOption(SonolusModel):
    """ServerToggleOption from @sonolus/core 7.16.0."""

    query: str
    name: str
    description: str | None = None
    required: bool
    type: Literal["toggle"]
    def_: bool = Field(alias="def")


class ServerUploadItemActionResponse(SonolusModel):
    """ServerUploadItemActionResponse from @sonolus/core 7.16.0."""

    shouldUpdateItem: bool | None = None
    shouldRemoveItem: bool | None = None
    shouldNavigateToItem: str | None = None


class ServerUploadItemCommunityActionResponse(SonolusModel):
    """ServerUploadItemCommunityActionResponse from @sonolus/core 7.16.0."""

    shouldUpdateCommunity: bool | None = None
    shouldUpdateComments: bool | None = None
    shouldNavigateCommentsToPage: int | float | None = None


class ServerUploadItemCommunityCommentActionResponse(SonolusModel):
    """ServerUploadItemCommunityCommentActionResponse from @sonolus/core 7.16.0."""

    shouldUpdateCommunity: bool | None = None
    shouldUpdateComments: bool | None = None
    shouldNavigateCommentsToPage: int | float | None = None


class ServerUploadItemResponse(SonolusModel):
    """ServerUploadItemResponse from @sonolus/core 7.16.0."""

    shouldUpdateInfo: bool | None = None
    shouldNavigateToItem: str | None = None


class ServerUploadLevelResultResponse(ServerCreateRoomRequest):
    """ServerUploadLevelResultResponse from @sonolus/core 7.16.0."""


class ServiceAuthenticateExternalRequest(SonolusModel):
    """ServiceAuthenticateExternalRequest from @sonolus/core 7.16.0."""

    type: Literal["authenticateExternal"]
    url: str
    time: int | float
    userProfile: ServiceUserProfile


class ServiceAuthenticateExternalResponse(ServerMessage):
    """ServiceAuthenticateExternalResponse from @sonolus/core 7.16.0."""


class ServiceUserProfile(SonolusModel):
    """ServiceUserProfile from @sonolus/core 7.16.0."""

    id: ServiceUserId
    handle: str
    name: str
    avatarType: str
    avatarForegroundType: str
    avatarForegroundColor: str
    avatarBackgroundType: str
    avatarBackgroundColor: str
    bannerType: str
    aboutMe: str
    favorites: list[str]


class Sil(SonolusModel):
    """Sil from @sonolus/core 7.16.0."""

    address: str
    name: str


class SkinData(SonolusModel):
    """SkinData from @sonolus/core 7.16.0."""

    width: int | float
    height: int | float
    interpolation: bool
    sprites: list[SkinDataSprite]


class SkinDataExpression(SonolusModel):
    """SkinDataExpression from @sonolus/core 7.16.0."""

    x1: int | float | None = None
    x2: int | float | None = None
    x3: int | float | None = None
    x4: int | float | None = None
    y1: int | float | None = None
    y2: int | float | None = None
    y3: int | float | None = None
    y4: int | float | None = None


class SkinDataSprite(SonolusModel):
    """SkinDataSprite from @sonolus/core 7.16.0."""

    name: str
    x: int | float
    y: int | float
    w: int | float
    h: int | float
    transform: SkinDataTransform


class SkinDataTransform(SonolusModel):
    """SkinDataTransform from @sonolus/core 7.16.0."""

    x1: SkinDataExpression
    x2: SkinDataExpression
    x3: SkinDataExpression
    x4: SkinDataExpression
    y1: SkinDataExpression
    y2: SkinDataExpression
    y3: SkinDataExpression
    y4: SkinDataExpression


class SkinItem(SonolusModel):
    """SkinItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    version: Literal[4]
    title: str
    subtitle: str
    author: str
    authorUser: UserItem | None = None
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    texture: Srl


class Srl(SonolusModel):
    """Srl from @sonolus/core 7.16.0."""

    hash: str | None = None
    url: str | None = None


class StartGameplayCommand(SonolusModel):
    """StartGameplayCommand from @sonolus/core 7.16.0."""

    type: Literal["startGameplay"]
    state: str
    level: LevelItem


class StartRoundEvent(SonolusModel):
    """StartRoundEvent from @sonolus/core 7.16.0."""

    type: Literal["startRound"]
    state: str
    seed: int | float


class Suggestion(SonolusModel):
    """Suggestion from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    level: Sil


class SwapScoreboardSectionScoresEvent(SonolusModel):
    """SwapScoreboardSectionScoresEvent from @sonolus/core 7.16.0."""

    type: Literal["swapScoreboardSectionScores"]
    sectionIndex: int | float
    indexA: int | float
    indexB: int | float


class SwapScoreboardSectionsEvent(SonolusModel):
    """SwapScoreboardSectionsEvent from @sonolus/core 7.16.0."""

    type: Literal["swapScoreboardSections"]
    indexA: int | float
    indexB: int | float


class SwapSuggestionsCommand(SonolusModel):
    """SwapSuggestionsCommand from @sonolus/core 7.16.0."""

    type: Literal["swapSuggestions"]
    suggestionA: Suggestion
    suggestionB: Suggestion


class SwapSuggestionsEvent(SonolusModel):
    """SwapSuggestionsEvent from @sonolus/core 7.16.0."""

    type: Literal["swapSuggestions"]
    suggestionA: Suggestion
    suggestionB: Suggestion


class Tag(SonolusModel):
    """Tag from @sonolus/core 7.16.0."""

    title: str | None = None
    icon: str | None = None


class UpdateAutoExitCommand(SonolusModel):
    """UpdateAutoExitCommand from @sonolus/core 7.16.0."""

    type: Literal["updateAutoExit"]
    autoExit: AutoExit


class UpdateAutoExitEvent(SonolusModel):
    """UpdateAutoExitEvent from @sonolus/core 7.16.0."""

    type: Literal["updateAutoExit"]
    autoExit: AutoExit


class UpdateEvent(SonolusModel):
    """UpdateEvent from @sonolus/core 7.16.0."""

    type: Literal["update"]
    allowOtherServers: bool
    reportUserOptions: list[ServerForm]
    title: str
    status: RoomStatus
    master: ServiceUserId | None
    lead: ServiceUserId | None
    options: list[ServerForm]
    optionValues: str
    level: Sil | None
    levelOptions: list[LevelOptionEntry]
    autoExit: AutoExit
    isSuggestionsLocked: bool
    suggestions: list[Suggestion]
    scoreboardDescription: str | None = None
    scoreboardSections: list[ScoreboardSection]
    results: list[ResultEntry]
    users: list[RoomUser]
    userStatuses: list[UserStatusEntry]


class UpdateIsSuggestionsLockedCommand(SonolusModel):
    """UpdateIsSuggestionsLockedCommand from @sonolus/core 7.16.0."""

    type: Literal["updateIsSuggestionsLocked"]
    isSuggestionsLocked: bool


class UpdateIsSuggestionsLockedEvent(SonolusModel):
    """UpdateIsSuggestionsLockedEvent from @sonolus/core 7.16.0."""

    type: Literal["updateIsSuggestionsLocked"]
    isSuggestionsLocked: bool


class UpdateLeadCommand(SonolusModel):
    """UpdateLeadCommand from @sonolus/core 7.16.0."""

    type: Literal["updateLead"]
    lead: ServiceUserId


class UpdateLeadEvent(SonolusModel):
    """UpdateLeadEvent from @sonolus/core 7.16.0."""

    type: Literal["updateLead"]
    lead: ServiceUserId | None


class UpdateLevelCommand(SonolusModel):
    """UpdateLevelCommand from @sonolus/core 7.16.0."""

    type: Literal["updateLevel"]
    level: Sil


class UpdateLevelEvent(SonolusModel):
    """UpdateLevelEvent from @sonolus/core 7.16.0."""

    type: Literal["updateLevel"]
    level: Sil | None


class UpdateLevelOptionCommand(SonolusModel):
    """UpdateLevelOptionCommand from @sonolus/core 7.16.0."""

    type: Literal["updateLevelOption"]
    levelOption: LevelOptionEntry


class UpdateLevelOptionEvent(SonolusModel):
    """UpdateLevelOptionEvent from @sonolus/core 7.16.0."""

    type: Literal["updateLevelOption"]
    levelOption: LevelOptionEntry


class UpdateLevelOptionsEvent(SonolusModel):
    """UpdateLevelOptionsEvent from @sonolus/core 7.16.0."""

    type: Literal["updateLevelOptions"]
    levelOptions: list[LevelOptionEntry]


class UpdateMasterCommand(SonolusModel):
    """UpdateMasterCommand from @sonolus/core 7.16.0."""

    type: Literal["updateMaster"]
    master: ServiceUserId


class UpdateMasterEvent(SonolusModel):
    """UpdateMasterEvent from @sonolus/core 7.16.0."""

    type: Literal["updateMaster"]
    master: ServiceUserId | None


class UpdateOptionValuesCommand(SonolusModel):
    """UpdateOptionValuesCommand from @sonolus/core 7.16.0."""

    type: Literal["updateOptionValues"]
    optionValues: str


class UpdateOptionValuesEvent(SonolusModel):
    """UpdateOptionValuesEvent from @sonolus/core 7.16.0."""

    type: Literal["updateOptionValues"]
    optionValues: str


class UpdateOptionsEvent(SonolusModel):
    """UpdateOptionsEvent from @sonolus/core 7.16.0."""

    type: Literal["updateOptions"]
    options: list[ServerForm]
    optionValues: str


class UpdateScoreboardDescriptionEvent(SonolusModel):
    """UpdateScoreboardDescriptionEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardDescription"]
    scoreboardDescription: str | None = None


class UpdateScoreboardSectionEvent(SonolusModel):
    """UpdateScoreboardSectionEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSection"]
    index: int | float
    scoreboardSection: ScoreboardSection


class UpdateScoreboardSectionIconEvent(SonolusModel):
    """UpdateScoreboardSectionIconEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSectionIcon"]
    index: int | float
    icon: str | None = None


class UpdateScoreboardSectionScoresEvent(SonolusModel):
    """UpdateScoreboardSectionScoresEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSectionScores"]
    index: int | float
    scores: list[ScoreEntry]


class UpdateScoreboardSectionScoresValueEvent(SonolusModel):
    """UpdateScoreboardSectionScoresValueEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSectionScoresValue"]
    index: int | float
    values: list[str]


class UpdateScoreboardSectionTitleEvent(SonolusModel):
    """UpdateScoreboardSectionTitleEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSectionTitle"]
    index: int | float
    title: str


class UpdateScoreboardSectionsEvent(SonolusModel):
    """UpdateScoreboardSectionsEvent from @sonolus/core 7.16.0."""

    type: Literal["updateScoreboardSections"]
    scoreboardSections: list[ScoreboardSection]


class UpdateStatusCommand(SonolusModel):
    """UpdateStatusCommand from @sonolus/core 7.16.0."""

    type: Literal["updateStatus"]
    status: RoomStatus


class UpdateStatusEvent(SonolusModel):
    """UpdateStatusEvent from @sonolus/core 7.16.0."""

    type: Literal["updateStatus"]
    status: RoomStatus


class UpdateSuggestionsEvent(SonolusModel):
    """UpdateSuggestionsEvent from @sonolus/core 7.16.0."""

    type: Literal["updateSuggestions"]
    suggestions: list[Suggestion]


class UpdateTitleEvent(SonolusModel):
    """UpdateTitleEvent from @sonolus/core 7.16.0."""

    type: Literal["updateTitle"]
    title: str


class UpdateUserStatusCommand(SonolusModel):
    """UpdateUserStatusCommand from @sonolus/core 7.16.0."""

    type: Literal["updateUserStatus"]
    status: UserStatus


class UpdateUserStatusEvent(SonolusModel):
    """UpdateUserStatusEvent from @sonolus/core 7.16.0."""

    type: Literal["updateUserStatus"]
    userStatus: UserStatusEntry


class UpdateUserStatusesEvent(SonolusModel):
    """UpdateUserStatusesEvent from @sonolus/core 7.16.0."""

    type: Literal["updateUserStatuses"]
    userStatuses: list[UserStatusEntry]


class UpdateUsersEvent(SonolusModel):
    """UpdateUsersEvent from @sonolus/core 7.16.0."""

    type: Literal["updateUsers"]
    users: list[RoomUser]


class UseItemUseDefaultFalse(SonolusModel, Generic[T]):
    """UseItem variant from @sonolus/core 7.16.0."""

    useDefault: Literal[False]
    item: T


class UseItemUseDefaultTrue(SonolusModel):
    """UseItem variant from @sonolus/core 7.16.0."""

    useDefault: Literal[True]


class UserItem(SonolusModel):
    """UserItem from @sonolus/core 7.16.0."""

    name: str
    source: str | None = None
    title: str
    handle: str | None = None
    tags: list[Tag]


class UserStatusEntry(SonolusModel):
    """UserStatusEntry from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    status: UserStatus


class UserTextChatMessage(SonolusModel):
    """UserTextChatMessage from @sonolus/core 7.16.0."""

    userId: ServiceUserId
    type: Literal["text"]
    value: str


AutoExit: TypeAlias = Literal["allPerfect", "fullCombo", "off", "pass"]
ChatMessage: TypeAlias = QuickChatMessage | RoomTextChatMessage | UserTextChatMessage
Command: TypeAlias = Annotated[
    AddChatMessageCommand
    | AddSuggestionCommand
    | ClearSuggestionsCommand
    | FinishGameplayCommand
    | RemoveSuggestionCommand
    | RemoveUserCommand
    | ReportUserCommand
    | ResetScoreboardCommand
    | StartGameplayCommand
    | SwapSuggestionsCommand
    | UpdateAutoExitCommand
    | UpdateIsSuggestionsLockedCommand
    | UpdateLeadCommand
    | UpdateLevelCommand
    | UpdateLevelOptionCommand
    | UpdateMasterCommand
    | UpdateOptionValuesCommand
    | UpdateStatusCommand
    | UpdateUserStatusCommand,
    Field(discriminator="type"),
]
DatabaseUseItem: TypeAlias = (
    DatabaseUseItemUseDefaultFalse | DatabaseUseItemUseDefaultTrue
)
EngineConfigurationJudgmentErrorPlacement: TypeAlias = Literal[
    "bottom", "center", "left", "leftRight", "right", "top", "topBottom"
]
EngineConfigurationJudgmentErrorStyle: TypeAlias = Literal[
    "arrowDown",
    "arrowLeft",
    "arrowRight",
    "arrowUp",
    "early",
    "late",
    "minus",
    "none",
    "plus",
    "triangleDown",
    "triangleLeft",
    "triangleRight",
    "triangleUp",
]
EngineConfigurationMetric: TypeAlias = Literal[
    "accuracy",
    "accuracyPercentage",
    "arcade",
    "arcadePercentage",
    "errorHeatmap",
    "greatGoodMiss",
    "greatGoodMissPercentage",
    "life",
    "miss",
    "missPercentage",
    "perfect",
    "perfectPercentage",
    "time",
]
EngineConfigurationOption: TypeAlias = Annotated[
    EngineConfigurationSelectOption
    | EngineConfigurationSliderOption
    | EngineConfigurationToggleOption,
    Field(discriminator="type"),
]
EngineDataNode: TypeAlias = EngineDataFunctionNode | EngineDataValueNode
Event: TypeAlias = Annotated[
    AddChatMessageEvent
    | AddResultEvent
    | AddSuggestionEvent
    | AddUserEvent
    | ArrangeScoreboardSectionScoresEvent
    | ClearSuggestionsEvent
    | InsertScoreboardSectionEvent
    | InsertScoreboardSectionScoreEvent
    | MergeScoreboardSectionScoresEvent
    | MoveScoreboardSectionEvent
    | MoveScoreboardSectionScoreEvent
    | RemoveScoreboardSectionEvent
    | RemoveScoreboardSectionScoreEvent
    | RemoveSuggestionEvent
    | RemoveUserEvent
    | StartRoundEvent
    | SwapScoreboardSectionScoresEvent
    | SwapScoreboardSectionsEvent
    | SwapSuggestionsEvent
    | UpdateAutoExitEvent
    | UpdateEvent
    | UpdateIsSuggestionsLockedEvent
    | UpdateLeadEvent
    | UpdateLevelEvent
    | UpdateLevelOptionEvent
    | UpdateLevelOptionsEvent
    | UpdateMasterEvent
    | UpdateOptionValuesEvent
    | UpdateOptionsEvent
    | UpdateScoreboardDescriptionEvent
    | UpdateScoreboardSectionEvent
    | UpdateScoreboardSectionIconEvent
    | UpdateScoreboardSectionScoresEvent
    | UpdateScoreboardSectionScoresValueEvent
    | UpdateScoreboardSectionTitleEvent
    | UpdateScoreboardSectionsEvent
    | UpdateStatusEvent
    | UpdateSuggestionsEvent
    | UpdateTitleEvent
    | UpdateUserStatusEvent
    | UpdateUserStatusesEvent
    | UpdateUsersEvent,
    Field(discriminator="type"),
]
ItemType: TypeAlias = Literal[
    "background",
    "effect",
    "engine",
    "level",
    "particle",
    "playlist",
    "post",
    "replay",
    "room",
    "skin",
    "user",
]
LocalizationText: TypeAlias = str | dict[str, str]
RoomStatus: TypeAlias = Literal["playing", "preparing", "selecting"]
ServerInfoButton: TypeAlias = Annotated[
    ServerInfoAuthenticationButton
    | ServerInfoConfigurationButton
    | ServerInfoItemButton,
    Field(discriminator="type"),
]
ServerOption: TypeAlias = Annotated[
    ServerCollectionItemOption
    | ServerFileOption
    | ServerMultiOption
    | ServerSelectOption
    | ServerServerItemOption
    | ServerServerItemsOption
    | ServerSliderOption
    | ServerTextAreaOption
    | ServerTextOption
    | ServerToggleOption,
    Field(discriminator="type"),
]
ServiceUserId: TypeAlias = str
TextChatMessage: TypeAlias = RoomTextChatMessage | UserTextChatMessage
UseItem = TypeAliasType(
    "UseItem", UseItemUseDefaultFalse[T] | UseItemUseDefaultTrue, type_params=(T,)
)
ServerItemSection: TypeAlias = (
    ServerItemSectionTyped[Literal["background"], BackgroundItem]
    | ServerItemSectionTyped[Literal["effect"], EffectItem]
    | ServerItemSectionTyped[Literal["engine"], EngineItem]
    | ServerItemSectionTyped[Literal["level"], LevelItem]
    | ServerItemSectionTyped[Literal["particle"], ParticleItem]
    | ServerItemSectionTyped[Literal["playlist"], PlaylistItem]
    | ServerItemSectionTyped[Literal["post"], PostItem]
    | ServerItemSectionTyped[Literal["replay"], ReplayItem]
    | ServerItemSectionTyped[Literal["room"], RoomItem]
    | ServerItemSectionTyped[Literal["skin"], SkinItem]
    | ServerItemSectionTyped[Literal["user"], UserItem]
)
UserStatus: TypeAlias = Literal["playing", "ready", "skipped", "waiting"]


AddChatMessageCommand.model_rebuild()
AddChatMessageEvent.model_rebuild()
AddResultEvent.model_rebuild()
AddSuggestionCommand.model_rebuild()
AddSuggestionEvent.model_rebuild()
AddUserEvent.model_rebuild()
ArrangeScoreboardSectionScoresEvent.model_rebuild()
BackgroundConfiguration.model_rebuild()
BackgroundData.model_rebuild()
BackgroundItem.model_rebuild()
ClearSuggestionsCommand.model_rebuild()
ClearSuggestionsEvent.model_rebuild()
Database.model_rebuild()
DatabaseBackgroundItem.model_rebuild()
DatabaseEffectItem.model_rebuild()
DatabaseEngineItem.model_rebuild()
DatabaseLevelItem.model_rebuild()
DatabaseParticleItem.model_rebuild()
DatabasePlaylistItem.model_rebuild()
DatabasePostItem.model_rebuild()
DatabaseReplayItem.model_rebuild()
DatabaseServerInfo.model_rebuild()
DatabaseSkinItem.model_rebuild()
DatabaseTag.model_rebuild()
DatabaseUseItemUseDefaultFalse.model_rebuild()
DatabaseUseItemUseDefaultTrue.model_rebuild()
EffectData.model_rebuild()
EffectDataClip.model_rebuild()
EffectItem.model_rebuild()
EngineConfiguration.model_rebuild()
EngineConfigurationAnimation.model_rebuild()
EngineConfigurationAnimationTween.model_rebuild()
EngineConfigurationOptionCategory.model_rebuild()
EngineConfigurationSelectOption.model_rebuild()
EngineConfigurationSliderOption.model_rebuild()
EngineConfigurationToggleOption.model_rebuild()
EngineConfigurationUI.model_rebuild()
EngineConfigurationVisibility.model_rebuild()
EngineDataBucket.model_rebuild()
EngineDataBucketSprite.model_rebuild()
EngineDataFunctionNode.model_rebuild()
EngineDataValueNode.model_rebuild()
EngineItem.model_rebuild()
EnginePlayData.model_rebuild()
EnginePlayDataArchetype.model_rebuild()
EnginePlayDataArchetypeCallback.model_rebuild()
EnginePlayDataArchetypeImport.model_rebuild()
EnginePlayDataEffect.model_rebuild()
EnginePlayDataEffectClip.model_rebuild()
EnginePlayDataParticle.model_rebuild()
EnginePlayDataParticleEffect.model_rebuild()
EnginePlayDataSkin.model_rebuild()
EnginePlayDataSkinSprite.model_rebuild()
EnginePreviewData.model_rebuild()
EnginePreviewDataArchetype.model_rebuild()
EnginePreviewDataArchetypeCallback.model_rebuild()
EnginePreviewDataArchetypeImport.model_rebuild()
EnginePreviewDataSkin.model_rebuild()
EnginePreviewDataSkinSprite.model_rebuild()
EngineTutorialData.model_rebuild()
EngineTutorialDataEffect.model_rebuild()
EngineTutorialDataEffectClip.model_rebuild()
EngineTutorialDataInstruction.model_rebuild()
EngineTutorialDataInstructionIcon.model_rebuild()
EngineTutorialDataInstructionText.model_rebuild()
EngineTutorialDataParticle.model_rebuild()
EngineTutorialDataParticleEffect.model_rebuild()
EngineTutorialDataSkin.model_rebuild()
EngineTutorialDataSkinSprite.model_rebuild()
EngineWatchData.model_rebuild()
EngineWatchDataArchetype.model_rebuild()
EngineWatchDataArchetypeCallback.model_rebuild()
EngineWatchDataArchetypeImport.model_rebuild()
EngineWatchDataEffect.model_rebuild()
EngineWatchDataEffectClip.model_rebuild()
EngineWatchDataParticle.model_rebuild()
EngineWatchDataParticleEffect.model_rebuild()
EngineWatchDataSkin.model_rebuild()
EngineWatchDataSkinSprite.model_rebuild()
FinishGameplayCommand.model_rebuild()
GameplayResult.model_rebuild()
InsertScoreboardSectionEvent.model_rebuild()
InsertScoreboardSectionScoreEvent.model_rebuild()
LevelData.model_rebuild()
LevelDataEntity.model_rebuild()
LevelDataEntityDataRef.model_rebuild()
LevelDataEntityDataValue.model_rebuild()
LevelItem.model_rebuild()
LevelOptionEntry.model_rebuild()
MergeScoreboardSectionScoresEvent.model_rebuild()
MoveScoreboardSectionEvent.model_rebuild()
MoveScoreboardSectionScoreEvent.model_rebuild()
PackageInfo.model_rebuild()
ParticleData.model_rebuild()
ParticleDataEffect.model_rebuild()
ParticleDataGroup.model_rebuild()
ParticleDataGroupParticle.model_rebuild()
ParticleDataGroupParticleProperty.model_rebuild()
ParticleDataGroupParticlePropertyExpression.model_rebuild()
ParticleDataSprite.model_rebuild()
ParticleDataTransform.model_rebuild()
ParticleDataTransformValue.model_rebuild()
ParticleItem.model_rebuild()
PlaylistItem.model_rebuild()
PostItem.model_rebuild()
QuickChatMessage.model_rebuild()
RemoveScoreboardSectionEvent.model_rebuild()
RemoveScoreboardSectionScoreEvent.model_rebuild()
RemoveSuggestionCommand.model_rebuild()
RemoveSuggestionEvent.model_rebuild()
RemoveUserCommand.model_rebuild()
RemoveUserEvent.model_rebuild()
ReplayConfiguration.model_rebuild()
ReplayData.model_rebuild()
ReplayDataEntity.model_rebuild()
ReplayDataEntityData.model_rebuild()
ReplayDataInputs.model_rebuild()
ReplayDataPlayArea.model_rebuild()
ReplayDataStream.model_rebuild()
ReplayDataTouches.model_rebuild()
ReplayItem.model_rebuild()
ReportUserCommand.model_rebuild()
ResetScoreboardCommand.model_rebuild()
ResultEntry.model_rebuild()
RoomItem.model_rebuild()
RoomTextChatMessage.model_rebuild()
RoomUser.model_rebuild()
ScoreEntry.model_rebuild()
ScoreboardSection.model_rebuild()
ServerAuthenticateRequest.model_rebuild()
ServerAuthenticateResponse.model_rebuild()
ServerCollectionItemOption.model_rebuild()
ServerConfiguration.model_rebuild()
ServerCreateItemRequest.model_rebuild()
ServerCreateItemResponse.model_rebuild()
ServerCreateRoomRequest.model_rebuild()
ServerCreateRoomResponse.model_rebuild()
ServerFileOption.model_rebuild()
ServerFileOptionValidationAudio.model_rebuild()
ServerFileOptionValidationFile.model_rebuild()
ServerFileOptionValidationImage.model_rebuild()
ServerFileOptionValidationJson.model_rebuild()
ServerFileOptionValidationZip.model_rebuild()
ServerForm.model_rebuild()
ServerInfo.model_rebuild()
ServerInfoAuthenticationButton.model_rebuild()
ServerInfoConfigurationButton.model_rebuild()
ServerInfoItemButton.model_rebuild()
ServerItemCommunityComment.model_rebuild()
ServerItemCommunityCommentList.model_rebuild()
ServerItemCommunityInfo.model_rebuild()
ServerItemDetails.model_rebuild()
ServerItemInfo.model_rebuild()
ServerItemLeaderboard.model_rebuild()
ServerItemLeaderboardDetails.model_rebuild()
ServerItemLeaderboardRecord.model_rebuild()
ServerItemLeaderboardRecordDetails.model_rebuild()
ServerItemLeaderboardRecordList.model_rebuild()
ServerItemList.model_rebuild()
ServerItemSectionTyped.model_rebuild()
ServerJoinRoomRequest.model_rebuild()
ServerJoinRoomResponse.model_rebuild()
ServerLevelResultInfo.model_rebuild()
ServerMessage.model_rebuild()
ServerMultiOption.model_rebuild()
ServerMultiOptionValue.model_rebuild()
ServerSelectOption.model_rebuild()
ServerSelectOptionValue.model_rebuild()
ServerServerItemOption.model_rebuild()
ServerServerItemsOption.model_rebuild()
ServerSliderOption.model_rebuild()
ServerSubmitItemActionRequest.model_rebuild()
ServerSubmitItemActionResponse.model_rebuild()
ServerSubmitItemCommunityActionRequest.model_rebuild()
ServerSubmitItemCommunityActionResponse.model_rebuild()
ServerSubmitItemCommunityCommentActionRequest.model_rebuild()
ServerSubmitItemCommunityCommentActionResponse.model_rebuild()
ServerSubmitLevelResultRequest.model_rebuild()
ServerSubmitLevelResultResponse.model_rebuild()
ServerTextAreaOption.model_rebuild()
ServerTextOption.model_rebuild()
ServerToggleOption.model_rebuild()
ServerUploadItemActionResponse.model_rebuild()
ServerUploadItemCommunityActionResponse.model_rebuild()
ServerUploadItemCommunityCommentActionResponse.model_rebuild()
ServerUploadItemResponse.model_rebuild()
ServerUploadLevelResultResponse.model_rebuild()
ServiceAuthenticateExternalRequest.model_rebuild()
ServiceAuthenticateExternalResponse.model_rebuild()
ServiceUserProfile.model_rebuild()
Sil.model_rebuild()
SkinData.model_rebuild()
SkinDataExpression.model_rebuild()
SkinDataSprite.model_rebuild()
SkinDataTransform.model_rebuild()
SkinItem.model_rebuild()
Srl.model_rebuild()
StartGameplayCommand.model_rebuild()
StartRoundEvent.model_rebuild()
Suggestion.model_rebuild()
SwapScoreboardSectionScoresEvent.model_rebuild()
SwapScoreboardSectionsEvent.model_rebuild()
SwapSuggestionsCommand.model_rebuild()
SwapSuggestionsEvent.model_rebuild()
Tag.model_rebuild()
UpdateAutoExitCommand.model_rebuild()
UpdateAutoExitEvent.model_rebuild()
UpdateEvent.model_rebuild()
UpdateIsSuggestionsLockedCommand.model_rebuild()
UpdateIsSuggestionsLockedEvent.model_rebuild()
UpdateLeadCommand.model_rebuild()
UpdateLeadEvent.model_rebuild()
UpdateLevelCommand.model_rebuild()
UpdateLevelEvent.model_rebuild()
UpdateLevelOptionCommand.model_rebuild()
UpdateLevelOptionEvent.model_rebuild()
UpdateLevelOptionsEvent.model_rebuild()
UpdateMasterCommand.model_rebuild()
UpdateMasterEvent.model_rebuild()
UpdateOptionValuesCommand.model_rebuild()
UpdateOptionValuesEvent.model_rebuild()
UpdateOptionsEvent.model_rebuild()
UpdateScoreboardDescriptionEvent.model_rebuild()
UpdateScoreboardSectionEvent.model_rebuild()
UpdateScoreboardSectionIconEvent.model_rebuild()
UpdateScoreboardSectionScoresEvent.model_rebuild()
UpdateScoreboardSectionScoresValueEvent.model_rebuild()
UpdateScoreboardSectionTitleEvent.model_rebuild()
UpdateScoreboardSectionsEvent.model_rebuild()
UpdateStatusCommand.model_rebuild()
UpdateStatusEvent.model_rebuild()
UpdateSuggestionsEvent.model_rebuild()
UpdateTitleEvent.model_rebuild()
UpdateUserStatusCommand.model_rebuild()
UpdateUserStatusEvent.model_rebuild()
UpdateUserStatusesEvent.model_rebuild()
UpdateUsersEvent.model_rebuild()
UseItemUseDefaultFalse.model_rebuild()
UseItemUseDefaultTrue.model_rebuild()
UserItem.model_rebuild()
UserStatusEntry.model_rebuild()
UserTextChatMessage.model_rebuild()
