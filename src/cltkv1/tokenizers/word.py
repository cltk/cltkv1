"""Module for tokenizers.

TODO: Think about adding check somewhere if a contrib (not user) chooses an unavailable item
"""

import re
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Type

from cltk.tokenize.word import WordTokenizer as WordTokenizer

from cltkv1.languages.glottolog import get_lang, LANGUAGES
from cltkv1.utils.data_types import Process, Word
from cltkv1.utils.exceptions import UnknownLanguageError

AKKADIAN_WORD_TOK = WordTokenizer(language="akkadian")
ARABIC_WORD_TOK = WordTokenizer(language="arabic")
GREEK_WORD_TOK = WordTokenizer(language="greek")
LATIN_WORD_TOK = WordTokenizer(language="latin")
MIDDLE_ENGLISH_WORD_TOK = WordTokenizer(language="middle_english")
MIDDLE_FRENCH_WORD_TOK = WordTokenizer(language="middle_french")
MIDDLE_HIGH_GERMAN_WORD_TOK = WordTokenizer(language="middle_high_german")
MULTILINGUAL_WORD_TOK = WordTokenizer(language="multilingual")
OLD_FRENCH_WORD_TOK = WordTokenizer(language="old_french")
OLD_NORSE_WORD_TOK = WordTokenizer(language="old_norse")
SANSKRIT_WORD_TOK = WordTokenizer(language="sanskrit")


@dataclass
class TokenizationProcess(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationProcess`` -> ``LatinTokenizationProcess``

    >>> from cltkv1.tokenizers.word import TokenizationProcess
    >>> from cltkv1.utils.data_types import Process
    >>> issubclass(TokenizationProcess, Process)
    True
    >>> tok = TokenizationProcess(data_input="some input data")
    """
    language = None


@dataclass
class DefaultTokenizationProcess(TokenizationProcess):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers.word import DefaultTokenizationProcess
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = DefaultTokenizationProcess(data_input=OLD_NORSE[:29])
    >>> tok.description
    'Whitespace tokenizer inheriting from the NLTK'
    >>> tok.data_output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    data_input: str
    algorithm = MULTILINGUAL_WORD_TOK.tokenize
    description = "Whitespace tokenizer inheriting from the NLTK"
    language = None


@dataclass
class LatinTokenizationProcess(TokenizationProcess):
    """The default Latin tokenization algorithm.

    >>> from cltkv1.tokenizers import LatinTokenizationProcess
    >>> from cltkv1.utils.example_texts import LATIN
    >>> tok = LatinTokenizationProcess(data_input=LATIN[:23])
    >>> tok.data_output
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    data_input: str
    algorithm = LATIN_WORD_TOK.tokenize
    description = "Default tokenizer for Latin"
    language = "lat"


@dataclass
class GreekTokenizationProcess(TokenizationProcess):
    """The default Greek tokenization algorithm.

    >>> from cltkv1.tokenizers import GreekTokenizationProcess
    >>> from cltkv1.utils.example_texts import GREEK
    >>> tok = GreekTokenizationProcess(data_input=GREEK[:23])
    >>> tok.data_output
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    data_input: str
    algorithm = GREEK_WORD_TOK.tokenize
    description = "Default Greek tokenizer"
    language = "grc"


@dataclass
class AkkadianTokenizationProcess(TokenizationProcess):
    """The default Akkadian tokenization algorithm.

    >>> from cltkv1.tokenizers import AkkadianTokenizationProcess
    >>> from cltkv1.utils.example_texts import AKKADIAN
    >>> tok = AkkadianTokenizationProcess(data_input=AKKADIAN)
    >>> tok.data_output
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    data_input: str
    algorithm = AKKADIAN_WORD_TOK.tokenize
    description = "Default Akkadian tokenizer"
    language = "akk"


@dataclass
class OldNorseTokenizationProcess(TokenizationProcess):
    """The default OldNorse tokenization algorithm.

    >>> from cltkv1.tokenizers import OldNorseTokenizationProcess
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = OldNorseTokenizationProcess(data_input=OLD_NORSE[:29])
    >>> tok.data_output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    data_input: str
    algorithm = OLD_NORSE_WORD_TOK.tokenize
    description = "Default Old Norse tokenizer"
    language = "non"


@dataclass
class MHGTokenizationProcess(TokenizationProcess):
    """The default Middle High German tokenization algorithm.

    >>> from cltkv1.tokenizers import MHGTokenizationProcess
    >>> from cltkv1.utils.example_texts import MIDDLE_HIGH_GERMAN
    >>> tok = MHGTokenizationProcess(data_input=MIDDLE_HIGH_GERMAN[:29])
    >>> tok.data_output
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    data_input: str
    algorithm = MIDDLE_HIGH_GERMAN_WORD_TOK.tokenize
    description = "The default Middle High German tokenizer"
    language = "gmh"


@dataclass
class ArabicTokenizationProcess(TokenizationProcess):
    """The default Arabic tokenization algorithm.

    >>> from cltkv1.tokenizers import ArabicTokenizationProcess
    >>> from cltkv1.utils.example_texts import ARABIC
    >>> tok = ArabicTokenizationProcess(data_input=ARABIC[:34])
    >>> tok.data_output
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    data_input: str
    algorithm = ARABIC_WORD_TOK.tokenize
    description = "Default Arabic tokenizer"
    language = "arb"


@dataclass
class OldFrenchTokenizationProcess(TokenizationProcess):
    """The default Old French tokenization algorithm.

    >>> from cltkv1.tokenizers import OldFrenchTokenizationProcess
    >>> from cltkv1.utils.example_texts import OLD_FRENCH
    >>> tok = OldFrenchTokenizationProcess(data_input=OLD_FRENCH[:37])
    >>> tok.data_output
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    data_input: str
    algorithm = OLD_FRENCH_WORD_TOK.tokenize
    description = "Default Old French tokenizer"
    language = "fro"


@dataclass
class MiddleFrenchTokenizationProcess(TokenizationProcess):
    """The default Middle French tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleFrenchTokenizationProcess
    >>> from cltkv1.utils.example_texts import MIDDLE_FRENCH
    >>> tok = MiddleFrenchTokenizationProcess(data_input=MIDDLE_FRENCH[:37])
    >>> tok.data_output
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    data_input: str
    algorithm = MIDDLE_FRENCH_WORD_TOK.tokenize
    description = "Default Middle French tokenizer"
    language = "frm"


@dataclass
class MiddleEnglishTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleEnglishTokenizationProcess
    >>> from cltkv1.utils.example_texts import MIDDLE_ENGLISH
    >>> tok = MiddleEnglishTokenizationProcess(data_input=MIDDLE_ENGLISH[:31])
    >>> tok.data_output
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    data_input: str
    algorithm = MIDDLE_ENGLISH_WORD_TOK.tokenize
    description = "Default Middle English tokenizer"
    language = "enm"


@dataclass
class SanskritTokenizationProcess(TokenizationProcess):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import SanskritTokenizationProcess
    >>> from cltkv1.utils.example_texts import SANSKRIT
    >>> tok = SanskritTokenizationProcess(data_input=SANSKRIT[:31])
    >>> tok.data_output
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    data_input: str
    algorithm: Callable = SANSKRIT_WORD_TOK.tokenize
    description = "The default Middle English tokenizer"
    language = "san"
