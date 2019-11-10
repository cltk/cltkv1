"""Module for tokenizers."""

import re
from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Type

from cltk.tokenize.word import WordTokenizer as WordTokenizer

from cltkv1.utils.data_types import Operation, Word

akkadian_word_tok = WordTokenizer(language="akkadian")
arabic_word_tok = WordTokenizer(language="arabic")
greek_word_tok = WordTokenizer(language="greek")
latin_word_tok = WordTokenizer(language="latin")
middle_english_word_tok = WordTokenizer(language="middle_english")
middle_french_word_tok = WordTokenizer(language="middle_french")
middle_high_german_word_tok = WordTokenizer(language="middle_high_german")
multilingual_word_tok = WordTokenizer(language="multilingual")
old_french_word_tok = WordTokenizer(language="old_french")
old_norse_word_tok = WordTokenizer(language="old_norse")
sanskrit_word_tok = WordTokenizer(language="sanskrit")


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``

    >>> from cltkv1.tokenizers.word import TokenizationOperation
    >>> from cltkv1.utils.data_types import Operation
    >>> issubclass(TokenizationOperation, Operation)
    True
    >>> tok = TokenizationOperation(data_input="some input data")
    """


def simple_regexp_tok(input_str: str) -> List[str]:
    """Simple regexp tokenizer for illustration.

    >>> from cltkv1.tokenizers.word import simple_regexp_tok
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> simple_regexp_tok(input_str=OLD_NORSE[:29])
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """
    return re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|['\w\-]+", input_str)


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers.word import DefaultTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = DefaultTokenizationOperation(data_input=OLD_NORSE[:29])
    >>> tok.description
    'Whitespace tokenizer inheriting from the NLTK'
    >>> tok.data_output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    data_input: str
    algorithm = multilingual_word_tok.tokenize
    description = "Whitespace tokenizer inheriting from the NLTK"
    language = None


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm.

    >>> from cltkv1.tokenizers import LatinTokenizationOperation
    >>> from cltkv1.utils.example_texts import LATIN
    >>> tok = LatinTokenizationOperation(data_input=LATIN[:23])
    >>> tok.data_output
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    data_input: str
    algorithm = latin_word_tok.tokenize
    description = "Default tokenizer for Latin"
    language = "lat"


@dataclass
class GreekTokenizationOperation(TokenizationOperation):
    """The default Greek tokenization algorithm.

    >>> from cltkv1.tokenizers import GreekTokenizationOperation
    >>> from cltkv1.utils.example_texts import GREEK
    >>> tok = GreekTokenizationOperation(data_input=GREEK[:23])
    >>> tok.data_output
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    data_input: str
    algorithm = greek_word_tok.tokenize
    description = "Default Greek tokenizer"
    language = "grc"


@dataclass
class AkkadianTokenizationOperation(TokenizationOperation):
    """The default Akkadian tokenization algorithm.

    >>> from cltkv1.tokenizers import AkkadianTokenizationOperation
    >>> from cltkv1.utils.example_texts import AKKADIAN
    >>> tok = AkkadianTokenizationOperation(data_input=AKKADIAN)
    >>> tok.data_output
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    data_input: str
    algorithm = akkadian_word_tok.tokenize
    description = "Default Akkadian tokenizer"
    language = "akk"


@dataclass
class OldNorseTokenizationOperation(TokenizationOperation):
    """The default OldNorse tokenization algorithm.

    >>> from cltkv1.tokenizers import OldNorseTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = OldNorseTokenizationOperation(data_input=OLD_NORSE[:29])
    >>> tok.data_output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    data_input: str
    algorithm = old_norse_word_tok.tokenize
    description = "Default Old Norse tokenizer"
    language = "non"


@dataclass
class MHGTokenizationOperation(TokenizationOperation):
    """The default Middle High German tokenization algorithm.

    >>> from cltkv1.tokenizers import MHGTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_HIGH_GERMAN
    >>> tok = MHGTokenizationOperation(data_input=MIDDLE_HIGH_GERMAN[:29])
    >>> tok.data_output
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    data_input: str
    algorithm = middle_high_german_word_tok.tokenize
    description = "The default Middle High German tokenizer"
    language = "gmh"


@dataclass
class ArabicTokenizationOperation(TokenizationOperation):
    """The default Arabic tokenization algorithm.

    >>> from cltkv1.tokenizers import ArabicTokenizationOperation
    >>> from cltkv1.utils.example_texts import ARABIC
    >>> tok = ArabicTokenizationOperation(data_input=ARABIC[:34])
    >>> tok.data_output
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    data_input: str
    algorithm = arabic_word_tok.tokenize
    description = "Default Arabic tokenizer"
    language = "arb"


@dataclass
class OldFrenchTokenizationOperation(TokenizationOperation):
    """The default Old French tokenization algorithm.

    >>> from cltkv1.tokenizers import OldFrenchTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_FRENCH
    >>> tok = OldFrenchTokenizationOperation(data_input=OLD_FRENCH[:37])
    >>> tok.data_output
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    data_input: str
    algorithm = old_french_word_tok.tokenize
    description = "Default Old French tokenizer"
    language = "fro"


@dataclass
class MiddleFrenchTokenizationOperation(TokenizationOperation):
    """The default Middle French tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleFrenchTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_FRENCH
    >>> tok = MiddleFrenchTokenizationOperation(data_input=MIDDLE_FRENCH[:37])
    >>> tok.data_output
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    data_input: str
    algorithm = middle_french_word_tok.tokenize
    description = "Default Middle French tokenizer"
    language = "frm"


@dataclass
class MiddleEnglishTokenizationOperation(TokenizationOperation):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleEnglishTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_ENGLISH
    >>> tok = MiddleEnglishTokenizationOperation(data_input=MIDDLE_ENGLISH[:31])
    >>> tok.data_output
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    data_input: str
    algorithm = middle_english_word_tok.tokenize
    description = "Default Middle English tokenizer"
    language = "enm"


@dataclass
class SanskritTokenizationOperation(TokenizationOperation):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import SanskritTokenizationOperation
    >>> from cltkv1.utils.example_texts import SANSKRIT
    >>> tok = SanskritTokenizationOperation(data_input=SANSKRIT[:31])
    >>> tok.data_output
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    data_input: str
    algorithm: Callable = sanskrit_word_tok.tokenize
    description = "The default Middle English tokenizer"
    language = "san"
