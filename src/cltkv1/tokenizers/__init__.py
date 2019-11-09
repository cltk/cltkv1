"""Init for `cltkv1.tokenize`."""

import re
from dataclasses import dataclass, field
from typing import Any, Callable, List, Tuple

from cltk.tokenize.word import WordTokenizer as WordTokenizer

from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.utils.data_types import Language, Operation

from .word import *

akkadian_word_tok = WordTokenizer(language="akkadian")
arabic_word_tok = WordTokenizer(language="arabic")
# french_word_tok = WordTokenizer(language="french")
greek_word_tok = WordTokenizer(language="greek")
latin_word_tok = WordTokenizer(language="latin")
# middle_french_word_tok = WordTokenizer(language="middle_french")
middle_high_german_word_tok = WordTokenizer(language="middle_high_german")
old_french_word_tok = WordTokenizer(language="old_french")
old_norse_word_tok = WordTokenizer(language="old_norse")

# TODO: Add these to the below

# middle_english_word_tok = WordTokenizer(language="middle_english")

#
# sanskrit_word_tok = WordTokenizer(language="sanskrit")
# multilingual_word_tok = WordTokenizer(language="multilingual")


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``

    >>> from cltkv1.tokenizers import TokenizationOperation
    >>> from cltkv1.utils.data_types import Operation
    >>> issubclass(TokenizationOperation, Operation)
    True
    >>> def a_function():    pass
    >>> TokenizationOperation(description="some description", algorithm=a_function())
    TokenizationOperation(description='some description', algorithm=None)
    """


def simple_regexp_tok(input_str: str) -> List[str]:
    """Simple regexp tokenizer for illustration.

    >>> from cltkv1.tokenizers import simple_regexp_tok
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> simple_regexp_tok(input_str=OLD_NORSE[:29])
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """
    return re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|['\w\-]+", input_str)


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers import DefaultTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = DefaultTokenizationOperation(operation_input=OLD_NORSE[:29])
    >>> tok.output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    >>> tok.description
    'A basic whitespace tokenizer'
    """

    operation_input: str = None
    description: str = field(default="A basic whitespace tokenizer")
    algorithm: Callable = field(default=simple_regexp_tok)

    @property
    def output(self):
        return self.algorithm(self.operation_input)


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm.

    >>> from cltkv1.tokenizers import LatinTokenizationOperation
    >>> from cltkv1.utils.example_texts import LATIN
    >>> tok = LatinTokenizationOperation(operation_input=LATIN[:23])
    >>> tok.output
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    operation_input: str = None
    description: str = field(default="The default Latin tokenizer")
    algorithm: Callable = field(default=latin_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class GreekTokenizationOperation(TokenizationOperation):
    """The default Greek tokenization algorithm.

    >>> from cltkv1.tokenizers import GreekTokenizationOperation
    >>> from cltkv1.utils.example_texts import GREEK
    >>> tok = GreekTokenizationOperation(operation_input=GREEK[:23])
    >>> tok.output
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    operation_input: str = None
    description: str = field(default="The default Greek tokenizer")
    algorithm: Callable = field(default=greek_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class AkkadianTokenizationOperation(TokenizationOperation):
    """The default Akkadian tokenization algorithm.

    >>> from cltkv1.tokenizers import AkkadianTokenizationOperation
    >>> from cltkv1.utils.example_texts import AKKADIAN
    >>> tok = AkkadianTokenizationOperation(operation_input=AKKADIAN)
    >>> tok.output
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    operation_input: str = None
    description: str = field(default="The default Akkadian tokenizer")
    algorithm: Callable = field(default=akkadian_word_tok.tokenize)

    @property
    def output(self) -> List[Tuple[str, str]]:
        return self.algorithm(self.operation_input)


@dataclass
class OldNorseTokenizationOperation(TokenizationOperation):
    """The default OldNorse tokenization algorithm.

    >>> from cltkv1.tokenizers import OldNorseTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = OldNorseTokenizationOperation(operation_input=OLD_NORSE[:29])
    >>> tok.output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    operation_input: str = None
    description: str = field(default="The default Old Norse tokenizer")
    algorithm: Callable = field(default=old_norse_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class MHGTokenizationOperation(TokenizationOperation):
    """The default Middle High German tokenization algorithm.

    >>> from cltkv1.tokenizers import MHGTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_HIGH_GERMAN
    >>> tok = MHGTokenizationOperation(operation_input=MIDDLE_HIGH_GERMAN[:29])
    >>> tok.output
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    operation_input: str = None
    description: str = field(default="The default Middle High German tokenizer")
    algorithm: Callable = field(default=middle_high_german_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class ArabicTokenizationOperation(TokenizationOperation):
    """The default Arabic tokenization algorithm.

    >>> from cltkv1.tokenizers import ArabicTokenizationOperation
    >>> from cltkv1.utils.example_texts import ARABIC
    >>> tok = ArabicTokenizationOperation(operation_input=ARABIC[:34])
    >>> tok.output
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    operation_input: str = None
    description: str = field(default="The default Arabic tokenizer")
    algorithm: Callable = field(default=arabic_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class OldFrenchTokenizationOperation(TokenizationOperation):
    """The default OldFrench tokenization algorithm.

    >>> from cltkv1.tokenizers import OldFrenchTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_FRENCH
    >>> tok = OldFrenchTokenizationOperation(operation_input=OLD_FRENCH[:37])
    >>> tok.output
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    operation_input: str = None
    description: str = field(default="The default OldFrench tokenizer")
    algorithm: Callable = field(default=old_french_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)
