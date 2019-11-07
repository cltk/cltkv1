"""Init for `cltkv1.tokenize`."""

from dataclasses import dataclass, field
import re
from typing import Any, Callable, List

from cltk.tokenize.word import WordTokenizer as LatinWordTokenizer

from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.utils.data_types import Operation, Language

from .word import *

latin_word_tok = LatinWordTokenizer(language='latin')


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
    return re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", input_str)


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
    def output(self):
        return self.algorithm(self.operation_input)


