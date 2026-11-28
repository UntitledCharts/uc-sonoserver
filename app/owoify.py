import collections.abc
import random
import re
from collections.abc import Callable, Iterable, Iterator
from typing import Any

Mapper = Callable[["Word"], "Word"]


def flatten(items: Iterable[Any]) -> Iterator[Any]:
    """Yield every leaf of nested iterables, keeping strings and bytes whole.

    Args:
        items: Possibly nested iterables.

    Returns:
        Iterator[Any]: The leaves in order.
    """
    for item in items:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


class Word:
    """One whitespace-free token being owoified.

    Attributes:
        replaced_words: Tokens produced by earlier replacements, never replaced again.
        word: Current text of the token.
    """

    def __init__(self, word: str) -> None:
        """Wrap a token.

        Args:
            word: Token text.
        """
        self.replaced_words: set[str] = set()
        self.word = word

    def __str__(self) -> str:
        """Return the current text.

        Returns:
            str: The token text.
        """
        return self.word

    def selector(self, text: str, search_value: re.Pattern[str], replace_value: str) -> bool:
        """Check whether replacing the first match in a token yields exactly the replacement.

        Args:
            text: Token to test.
            search_value: Pattern to search.
            replace_value: Replacement text.

        Returns:
            bool: True when the replaced token equals the replacement.
        """
        match = search_value.search(text)
        if match is not None:
            return text.replace(match.group(), replace_value) == replace_value
        return False

    def search_value_contains_replaced_words(
        self, search_value: re.Pattern[str], replace_value: str
    ) -> bool:
        """Check whether a replacement would touch a token an earlier replacement produced.

        Args:
            search_value: Pattern to search.
            replace_value: Replacement text.

        Returns:
            bool: True when a produced token would be replaced.
        """
        return any(self.selector(text, search_value, replace_value) for text in self.replaced_words)

    def _commit(self, replacing_word: str, replaced_words: list[str]) -> "Word":
        """Store a replacement result when it changed the token.

        Args:
            replacing_word: New token text.
            replaced_words: Tokens produced by the replacement.

        Returns:
            Word: This word.
        """
        if replacing_word != self.word:
            for word in replaced_words:
                self.replaced_words.add(word)
            self.word = replacing_word
        return self

    def replace(
        self,
        search_value: re.Pattern[str],
        replace_value: str,
        replace_replaced_words: bool = False,
    ) -> "Word":
        """Replace every match of a pattern.

        Args:
            search_value: Pattern to search.
            replace_value: Replacement, may reference groups.
            replace_replaced_words: Also replace inside tokens produced earlier.

        Returns:
            Word: This word.
        """
        if not replace_replaced_words and self.search_value_contains_replaced_words(
            search_value, replace_value
        ):
            return self
        replacing_word = self.word
        if search_value.search(self.word) is not None:
            replacing_word = search_value.sub(replace_value, self.word)
        collection = search_value.findall(self.word)
        replaced_words = [replace_value for _ in collection] if len(collection) > 1 else []
        return self._commit(replacing_word, replaced_words)

    def replace_with_func_single(
        self,
        search_value: re.Pattern[str],
        func: Callable[[], str],
        replace_replaced_words: bool = False,
    ) -> "Word":
        """Replace the text of the first match with a generated value everywhere it occurs.

        Args:
            search_value: Pattern to search.
            func: Produces the replacement.
            replace_replaced_words: Also replace inside tokens produced earlier.

        Returns:
            Word: This word.
        """
        replace_value = func()
        if not replace_replaced_words and self.search_value_contains_replaced_words(
            search_value, replace_value
        ):
            return self
        replacing_word = self.word
        match = search_value.search(self.word)
        if match is not None:
            replacing_word = self.word.replace(match.group(), replace_value)
        collection = search_value.findall(self.word)
        replaced_words = [replace_value for _ in collection] if len(collection) > 1 else []
        return self._commit(replacing_word, replaced_words)

    def replace_with_func_multiple(
        self,
        search_value: re.Pattern[str],
        func: Callable[[str, str], str],
        replace_replaced_words: bool = False,
    ) -> "Word":
        """Replace the first match using its two groups.

        Args:
            search_value: Pattern with two groups.
            func: Builds the replacement from both groups.
            replace_replaced_words: Also replace inside tokens produced earlier.

        Returns:
            Word: This word.
        """
        captures = search_value.search(self.word)
        if captures is None:
            return self
        replace_value = func(captures.group(1), captures.group(2))
        if not replace_replaced_words and self.search_value_contains_replaced_words(
            search_value, replace_value
        ):
            return self
        replacing_word = self.word.replace(captures.group(0), replace_value)
        collection = list(flatten(search_value.findall(self.word)))
        replaced_words = [replace_value for _ in collection] if len(collection) > 1 else []
        return self._commit(replacing_word, replaced_words)


O_TO_OWO = re.compile(r"o")
EW_TO_UWU = re.compile(r"ew")
HEY_TO_HAY = re.compile(r"([Hh])ey")
DEAD_TO_DED_UPPER = re.compile(r"Dead")
DEAD_TO_DED_LOWER = re.compile(r"dead")
N_VOWEL_T_TO_ND = re.compile(r"n[aeiou]*t")
READ_TO_WEAD_UPPER = re.compile(r"Read")
READ_TO_WEAD_LOWER = re.compile(r"read")
BRACKETS_TO_STARTRAILS_FORE = re.compile(r"[({<]")
BRACKETS_TO_STARTRAILS_REAR = re.compile(r"[)}>]")
PERIOD_COMMA_EXCLAMATION_SEMICOLON_TO_KAOMOJIS_FIRST = re.compile(r"[.,](?![0-9])")
PERIOD_COMMA_EXCLAMATION_SEMICOLON_TO_KAOMOJIS_SECOND = re.compile(r"[!;]+")
THAT_TO_DAT_UPPER = re.compile(r"That")
THAT_TO_DAT_LOWER = re.compile(r"that")
TH_TO_F_UPPER = re.compile(r"TH(?!E)")
TH_TO_F_LOWER = re.compile(r"[Tt]h(?![Ee])")
LE_TO_WAL = re.compile(r"le$")
VE_TO_WE_UPPER = re.compile(r"Ve")
VE_TO_WE_LOWER = re.compile(r"ve")
RY_TO_WWY = re.compile(r"ry")
RORL_TO_W_UPPER = re.compile(r"(?:R|L)")
RORL_TO_W_LOWER = re.compile(r"(?:r|l)")
LL_TO_WW = re.compile(r"ll")
VOWEL_OR_R_EXCEPT_O_L_TO_WL_UPPER = re.compile(r"[AEIUR]([lL])$")
VOWEL_OR_R_EXCEPT_O_L_TO_WL_LOWER = re.compile(r"[aeiur]l$")
OLD_TO_OWLD_UPPER = re.compile(r"OLD")
OLD_TO_OWLD_LOWER = re.compile(r"([Oo])ld")
OL_TO_OWL_UPPER = re.compile(r"OL")
OL_TO_OWL_LOWER = re.compile(r"([Oo])l")
LORR_O_TO_WO_UPPER = re.compile(r"[LR]([oO])")
LORR_O_TO_WO_LOWER = re.compile(r"[lr]o")
SPECIFIC_CONSONANTS_O_TO_LETTER_AND_WO_UPPER = re.compile(r"([BCDFGHJKMNPQSTXYZ])([oO])")
SPECIFIC_CONSONANTS_O_TO_LETTER_AND_WO_LOWER = re.compile(r"([bcdfghjkmnpqstxyz])o")
VORW_LE_TO_WAL = re.compile(r"[vw]le")
FI_TO_FWI_UPPER = re.compile(r"FI")
FI_TO_FWI_LOWER = re.compile(r"([Ff])i")
VER_TO_WER = re.compile(r"([Vv])er")
POI_TO_PWOI = re.compile(r"([Pp])oi")
SPECIFIC_CONSONANTS_LE_TO_LETTER_AND_WAL = re.compile(r"([DdFfGgHhJjPpQqRrSsTtXxYyZz])le$")
CONSONANT_R_TO_CONSONANT_W = re.compile(r"([BbCcDdFfGgKkPpQqSsTtWwXxZz])r")
LY_TO_WY_UPPER = re.compile(r"Ly")
LY_TO_WY_LOWER = re.compile(r"ly")
PLE_TO_PWE = re.compile(r"([Pp])le")
NR_TO_NW_UPPER = re.compile(r"NR")
NR_TO_NW_LOWER = re.compile(r"([Nn])r")
MEM_TO_MWEM_UPPER = re.compile(r"Mem")
MEM_TO_MWEM_LOWER = re.compile(r"mem")
NYWO_TO_NYO = re.compile(r"([Nn])ywo")
FUC_TO_FWUC = re.compile(r"([Ff])uc")
MOM_TO_MWOM = re.compile(r"([Mm])om")
ME_TO_MWE_UPPER = re.compile(r"^Me$")
ME_TO_MWE_LOWER = re.compile(r"^me$")
N_VOWEL_TO_NY_FIRST = re.compile(r"n([aeiou])")
N_VOWEL_TO_NY_SECOND = re.compile(r"N([aeiou])")
N_VOWEL_TO_NY_THIRD = re.compile(r"N([AEIOU])")
OVE_TO_UV_UPPER = re.compile(r"OVE")
OVE_TO_UV_LOWER = re.compile(r"ove")
HAHA_TO_HEHE_XD = re.compile(r"\b(ha|hah|heh|hehe)+\b")
THE_TO_TEH = re.compile(r"\b([Tt])he\b")
YOU_TO_U_UPPER = re.compile(r"\bYou\b")
YOU_TO_U_LOWER = re.compile(r"\byou\b")
TIME_TO_TIM = re.compile(r"\b([Tt])ime\b")
OVER_TO_OWOR = re.compile(r"([Oo])ver")
WORSE_TO_WOSE = re.compile(r"([Ww])orse")
GREAT_TO_GWATE = re.compile(r"([Gg])reat")
AVIAT_TO_AWIAT = re.compile(r"([Aa])viat")
DEDICAT_TO_DEDITAT = re.compile(r"([Dd])edicat")
REMEMBER_TO_REMBER = re.compile(r"([Rr])emember")
WHEN_TO_WEN = re.compile(r"([Ww])hen")
FRIGHTENED_TO_FRIGTEN = re.compile(r"([Ff])righten(ed)*")
MEME_TO_MEM_FIRST = re.compile(r"Meme")
MEME_TO_MEM_SECOND = re.compile(r"Mem")
FEEL_TO_FELL = re.compile(r"^([Ff])eel$")

STUTTER_WORD = re.compile(r"^([A-Za-z])")
S_TO_SH = re.compile(r"([Ss])(?=[aeiou])")
WORD_FINAL_Y_TO_YW = re.compile(r"y$")
WORD_FINAL_E_TO_EW = re.compile(r"([^w])e$")
ING_TO_IN = re.compile(r"([A-Za-z])ing\b")
AND_TO_AN = re.compile(r"\b([Aa])nd\b")
FOR_TO_FWO = re.compile(r"\b([Ff])or\b")
WITH_TO_WIF = re.compile(r"\b([Ww])ith\b")
JUST_TO_JUWST = re.compile(r"\b([Jj])ust\b")
HAVE_TO_HAB = re.compile(r"\b([Hh])ave\b")

FACES = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    "(* ^ ω ^)",
    "(⌒ω⌒)",
    "ヽ(*・ω・)ﾉ",
    "(o´∀`o)",
    "(o･ω･o)",
    "＼(＾▽＾)／",
    "(*^ω^)",
    "(◕‿◕✿)",
    "(◕ᴥ◕)",
    "ʕ•ᴥ•ʔ",
    "ʕ￫ᴥ￩ʔ",
    "(*^.^*)",
    "(｡♥‿♥｡)",
    "OwO",
    "uwu",
    "uvu",
    "UvU",
    "(*￣з￣)",
    "(つ✧ω✧)つ",
    "(/ =ω=)/",
    "(╯°□°）╯︵ ┻━┻",
    "┬─┬ ノ( ゜-゜ノ)",
    "¯\\_(ツ)_/¯",
]

WORD_REGEX = re.compile(r"[^\s]+")
SPACE_REGEX = re.compile(r"\s+")
URL_REGEX = re.compile(r"https?://\S+|www\.\S+")


def _replacer(*steps: tuple[re.Pattern[str], str]) -> Mapper:
    """Build a mapper applying replacements in order.

    Args:
        *steps: Pattern and replacement pairs.

    Returns:
        Mapper: The mapper.
    """

    def mapper(word: Word) -> Word:
        """Apply every replacement step to a word.

        Args:
            word: Word to change.

        Returns:
            Word: The same word.
        """
        for pattern, replacement in steps:
            word = word.replace(pattern, replacement)
        return word

    return mapper


def map_o_to_owo(word: Word) -> Word:
    """Turn ``o`` into ``owo`` two times out of three.

    Args:
        word: Word to change.

    Returns:
        Word: The same word.
    """
    replacement = "owo" if random.randint(0, 2) > 0 else "o"
    return word.replace(O_TO_OWO, replacement)


def _random_face() -> str:
    """Pick a kaomoji with a leading space.

    Returns:
        str: The kaomoji.
    """
    return f" {FACES[random.randint(0, len(FACES) - 1)]}"


def map_brackets_to_star_trails_pre(symbols: bool) -> Mapper:
    """Build the bracket to star trail mapper.

    Args:
        symbols: Whether symbols may be replaced.

    Returns:
        Mapper: The mapper.
    """

    def map_brackets_to_star_trails(word: Word) -> Word:
        """Replace brackets with star trails.

        Args:
            word: Word to change.

        Returns:
            Word: The same word.
        """
        if symbols:
            return word.replace(BRACKETS_TO_STARTRAILS_FORE, "｡･:*:･ﾟ★,｡･:*:･ﾟ☆").replace(
                BRACKETS_TO_STARTRAILS_REAR, "☆ﾟ･:*:･｡,★ﾟ･:*:･｡"
            )
        return word

    return map_brackets_to_star_trails


def map_period_comma_exclamation_semicolon_to_kaomojis_pre(symbols: bool) -> Mapper:
    """Build the punctuation to kaomoji mapper.

    Args:
        symbols: Whether symbols may be replaced.

    Returns:
        Mapper: The mapper.
    """

    def map_period_comma_exclamation_semicolon_to_kaomojis(word: Word) -> Word:
        """Replace punctuation with kaomojis.

        Args:
            word: Word to change.

        Returns:
            Word: The same word.
        """
        if symbols:
            return word.replace_with_func_single(
                PERIOD_COMMA_EXCLAMATION_SEMICOLON_TO_KAOMOJIS_FIRST, _random_face
            ).replace_with_func_single(
                PERIOD_COMMA_EXCLAMATION_SEMICOLON_TO_KAOMOJIS_SECOND, _random_face
            )
        return word

    return map_period_comma_exclamation_semicolon_to_kaomojis


def mapping_function_1(s1: str, s2: str) -> str:
    """Insert a ``w`` between a consonant and an ``o`` matching the ``o`` case.

    Args:
        s1: Consonant.
        s2: The ``o``.

    Returns:
        str: The replacement.
    """
    return s1 + ("W" if s2.upper() == s2 else "w") + s2


def map_specific_consonants_o_to_letter_and_wo(word: Word) -> Word:
    """Insert ``w`` between specific consonants and ``o``.

    Args:
        word: Word to change.

    Returns:
        Word: The same word.
    """
    return word.replace(
        SPECIFIC_CONSONANTS_O_TO_LETTER_AND_WO_LOWER, "\\1wo"
    ).replace_with_func_multiple(SPECIFIC_CONSONANTS_O_TO_LETTER_AND_WO_UPPER, mapping_function_1)


def map_stutter(word: Word) -> Word:
    """Stutter the first letter one time out of three.

    Args:
        word: Word to change.

    Returns:
        Word: The same word.
    """
    text = str(word)
    if len(text) < 2:
        return word
    match = STUTTER_WORD.match(text)
    if match and random.randint(0, 2) == 0:
        word.word = f"{match.group(1)}-{text}"
    return word


def map_add_tilde(word: Word) -> Word:
    """Append ``~`` one time out of four.

    Args:
        word: Word to change.

    Returns:
        Word: The same word.
    """
    if random.randint(0, 3) == 0:
        word.word = str(word) + "~"
    return word


map_ew_to_uwu = _replacer((EW_TO_UWU, "uwu"))
map_hey_to_hay = _replacer((HEY_TO_HAY, "\\1ay"))
map_dead_to_ded = _replacer((DEAD_TO_DED_UPPER, "Ded"), (DEAD_TO_DED_LOWER, "ded"))
map_n_vowel_t_to_nd = _replacer((N_VOWEL_T_TO_ND, "nd"))
map_read_to_wead = _replacer((READ_TO_WEAD_UPPER, "Wead"), (READ_TO_WEAD_LOWER, "wead"))
map_that_to_dat = _replacer((THAT_TO_DAT_LOWER, "dat"), (THAT_TO_DAT_UPPER, "Dat"))
map_th_to_f = _replacer((TH_TO_F_LOWER, "f"), (TH_TO_F_UPPER, "F"))
map_le_to_wal = _replacer((LE_TO_WAL, "wal"))
map_ve_to_we = _replacer((VE_TO_WE_LOWER, "we"), (VE_TO_WE_UPPER, "We"))
map_ry_to_wwy = _replacer((RY_TO_WWY, "wwy"))
map_r_or_l_to_w = _replacer((RORL_TO_W_LOWER, "w"), (RORL_TO_W_UPPER, "W"))
map_ll_to_ww = _replacer((LL_TO_WW, "ww"))
map_vowel_or_r_except_o_l_to_wl = _replacer(
    (VOWEL_OR_R_EXCEPT_O_L_TO_WL_LOWER, "wl"),
    (VOWEL_OR_R_EXCEPT_O_L_TO_WL_UPPER, "W\\1"),
)
map_old_to_owld = _replacer((OLD_TO_OWLD_LOWER, "\\1wld"), (OLD_TO_OWLD_UPPER, "OWLD"))
map_ol_to_owl = _replacer((OL_TO_OWL_LOWER, "\\1wl"), (OL_TO_OWL_UPPER, "OWL"))
map_l_or_r_o_to_wo = _replacer((LORR_O_TO_WO_LOWER, "wo"), (LORR_O_TO_WO_UPPER, "W\\1"))
map_v_or_w_le_to_wal = _replacer((VORW_LE_TO_WAL, "wal"))
map_fi_to_fwi = _replacer((FI_TO_FWI_LOWER, "\\1wi"), (FI_TO_FWI_UPPER, "FWI"))
map_ver_to_wer = _replacer((VER_TO_WER, "wer"))
map_poi_to_pwoi = _replacer((POI_TO_PWOI, "\\1woi"))
map_specific_consonants_le_to_letter_and_wal = _replacer(
    (SPECIFIC_CONSONANTS_LE_TO_LETTER_AND_WAL, "\\1wal")
)
map_consonant_r_to_consonant_w = _replacer((CONSONANT_R_TO_CONSONANT_W, "\\1w"))
map_ly_to_wy = _replacer((LY_TO_WY_LOWER, "wy"), (LY_TO_WY_UPPER, "Wy"))
map_ple_to_pwe = _replacer((PLE_TO_PWE, "\\1we"))
map_nr_to_nw = _replacer((NR_TO_NW_LOWER, "\\1w"), (NR_TO_NW_UPPER, "NW"))
map_mem_to_mwem = _replacer((MEM_TO_MWEM_UPPER, "mwem"), (MEM_TO_MWEM_LOWER, "Mwem"))
unmap_nywo_to_nyo = _replacer((NYWO_TO_NYO, "\\1yo"))
map_fuc_to_fwuc = _replacer((FUC_TO_FWUC, "\\1wuc"))
map_mom_to_mwom = _replacer((MOM_TO_MWOM, "\\1wom"))
map_me_to_mwe = _replacer((ME_TO_MWE_UPPER, "Mwe"), (ME_TO_MWE_LOWER, "mwe"))
map_n_vowel_to_ny = _replacer(
    (N_VOWEL_TO_NY_FIRST, "ny\\1"),
    (N_VOWEL_TO_NY_SECOND, "Ny\\1"),
    (N_VOWEL_TO_NY_THIRD, "NY\\1"),
)
map_ove_to_uv = _replacer((OVE_TO_UV_LOWER, "uv"), (OVE_TO_UV_UPPER, "UV"))
map_haha_to_hehe_xd = _replacer((HAHA_TO_HEHE_XD, "hehe xD"))
map_the_to_teh = _replacer((THE_TO_TEH, "\\1eh"))
map_you_to_u = _replacer((YOU_TO_U_UPPER, "U"), (YOU_TO_U_LOWER, "u"))
map_time_to_tim = _replacer((TIME_TO_TIM, "\\1im"))
map_over_to_owor = _replacer((OVER_TO_OWOR, "\\1wor"))
map_worse_to_wose = _replacer((WORSE_TO_WOSE, "\\1ose"))
map_great_to_gwate = _replacer((GREAT_TO_GWATE, "\\1wate"))
map_aviat_to_awiat = _replacer((AVIAT_TO_AWIAT, "\\1wiat"))
map_dedicat_to_deditat = _replacer((DEDICAT_TO_DEDITAT, "\\1editat"))
map_remember_to_rember = _replacer((REMEMBER_TO_REMBER, "\\1ember"))
map_when_to_wen = _replacer((WHEN_TO_WEN, "\\1en"))
map_frightened_to_frigten = _replacer((FRIGHTENED_TO_FRIGTEN, "\\1rigten"))
map_meme_to_mem = _replacer((MEME_TO_MEM_FIRST, "mem"), (MEME_TO_MEM_SECOND, "Mem"))
map_feel_to_fell = _replacer((FEEL_TO_FELL, "\\1ell"))
map_s_to_sh = _replacer((S_TO_SH, "\\1h"))
map_word_final_y_to_yw = _replacer((WORD_FINAL_Y_TO_YW, "yw"))
map_word_final_e_to_ew = _replacer((WORD_FINAL_E_TO_EW, "\\1ew"))
map_ing_to_in = _replacer((ING_TO_IN, "\\1in"))
map_and_to_an = _replacer((AND_TO_AN, "\\1n"))
map_for_to_fwo = _replacer((FOR_TO_FWO, "\\1wo"))
map_with_to_wif = _replacer((WITH_TO_WIF, "\\1if"))
map_just_to_juwst = _replacer((JUST_TO_JUWST, "\\1uwst"))
map_have_to_hab = _replacer((HAVE_TO_HAB, "\\1ab"))


def interleave_arrays(first: list[Word], second: list[Word]) -> list[Word]:
    """Interleave two lists starting with the first, appending what remains.

    Args:
        first: List taken from first.
        second: List taken from second.

    Returns:
        list[Word]: The interleaved list.
    """
    result: list[Word] = []
    observed = first
    other = second
    while len(observed) > 0:
        result.append(observed.pop(0))
        observed, other = other, observed
    if len(other) > 0:
        result += other
    return result


def _mapping_lists(
    locale: str, symbols: bool
) -> tuple[list[Mapper], list[Mapper], list[Mapper], list[Mapper], list[Mapper]]:
    """Return the specific, uvu, uwu, owo and max mapper lists of a locale.

    Args:
        locale: ``en`` or ``tr``.
        symbols: Whether symbols may be replaced.

    Returns:
        tuple[list[Mapper], list[Mapper], list[Mapper], list[Mapper], list[Mapper]]: The lists.
    """
    if locale == "en":
        return (
            [
                map_fuc_to_fwuc,
                map_mom_to_mwom,
                map_time_to_tim,
                map_me_to_mwe,
                map_over_to_owor,
                map_ove_to_uv,
                map_haha_to_hehe_xd,
                map_the_to_teh,
                map_you_to_u,
                map_read_to_wead,
                map_worse_to_wose,
                map_great_to_gwate,
                map_aviat_to_awiat,
                map_dedicat_to_deditat,
                map_remember_to_rember,
                map_when_to_wen,
                map_frightened_to_frigten,
                map_meme_to_mem,
                map_feel_to_fell,
            ],
            [
                map_o_to_owo,
                map_ew_to_uwu,
                map_hey_to_hay,
                map_dead_to_ded,
                map_n_vowel_t_to_nd,
            ],
            [
                map_brackets_to_star_trails_pre(symbols),
                map_period_comma_exclamation_semicolon_to_kaomojis_pre(symbols),
                map_that_to_dat,
                map_th_to_f,
                map_le_to_wal,
                map_ve_to_we,
                map_ry_to_wwy,
                map_r_or_l_to_w,
            ],
            [
                map_n_vowel_to_ny,
                map_ll_to_ww,
                map_vowel_or_r_except_o_l_to_wl,
                map_old_to_owld,
                map_ol_to_owl,
                map_l_or_r_o_to_wo,
                map_specific_consonants_o_to_letter_and_wo,
                map_v_or_w_le_to_wal,
                map_fi_to_fwi,
                map_ver_to_wer,
                map_poi_to_pwoi,
                map_specific_consonants_le_to_letter_and_wal,
                map_consonant_r_to_consonant_w,
                map_ly_to_wy,
                map_ple_to_pwe,
                map_nr_to_nw,
                map_mem_to_mwem,
                unmap_nywo_to_nyo,
            ],
            [
                map_stutter,
                map_s_to_sh,
                map_word_final_y_to_yw,
                map_word_final_e_to_ew,
                map_ing_to_in,
                map_and_to_an,
                map_for_to_fwo,
                map_with_to_wif,
                map_just_to_juwst,
                map_have_to_hab,
                map_add_tilde,
            ],
        )
    if locale == "tr":
        return (
            [],
            [
                map_brackets_to_star_trails_pre(symbols),
                map_period_comma_exclamation_semicolon_to_kaomojis_pre(symbols),
                map_o_to_owo,
            ],
            [map_ll_to_ww, map_ry_to_wwy],
            [map_ly_to_wy, map_nr_to_nw, map_ple_to_pwe, map_r_or_l_to_w],
            [map_stutter, map_s_to_sh, map_ing_to_in, map_add_tilde],
        )
    raise ValueError(f"Unsupported locale {locale}")


def owoify(source: str, level: int = 0, locale: str = "en", symbols: bool = True) -> str:
    """Owoify a text.

    Args:
        source: Text to change.
        level: Strength from 0 (owo) to 3 (max).
        locale: ``en`` or ``tr``.
        symbols: Whether brackets and punctuation may be replaced.

    Returns:
        str: The owoified text.
    """
    word_matches = WORD_REGEX.findall(source)
    space_matches = SPACE_REGEX.findall(source)
    specific, uvu, uwu, owo, maximum = _mapping_lists(locale, symbols)
    stages = {0: [owo], 1: [uwu, owo], 2: [uvu, uwu, owo], 3: [maximum, uvu, uwu, owo]}

    def map_owoify_levels(word: Word) -> Word:
        """Apply every mapper of the chosen level to one word.

        Args:
            word: Word to change.

        Returns:
            Word: The changed word.
        """
        if URL_REGEX.fullmatch(str(word)):
            return word
        for mapper in specific:
            word = mapper(word)
        if level not in stages:
            raise RuntimeError("The specified owoify level is not supported.")
        for mappers in stages[level]:
            for mapper in mappers:
                word = mapper(word)
        return word

    words = [map_owoify_levels(Word(text)) for text in word_matches]
    spaces = [Word(text) for text in space_matches]
    return "".join(str(item) for item in interleave_arrays(words, spaces))


UWU_LEVELS = {"owo": 0, "uwu": 1, "uvu": 2, "max": 3}


def handle_uwu(source: str, locale: str, uwu_level: str, symbols: bool = True) -> str:
    """Owoify a text at the player's configured level.

    Args:
        source: Text to change.
        locale: Player locale.
        uwu_level: ``off``, ``owo``, ``uwu``, ``uvu`` or ``max``.
        symbols: Whether brackets and punctuation may be replaced.

    Returns:
        str: The text, unchanged when the level is off.
    """
    level = UWU_LEVELS.get(uwu_level)
    if level is None:
        return source
    return owoify(source, level=level, locale=locale, symbols=symbols)
