"""Init for `cltkv1.tokenize`."""

from dataclasses import dataclass, field
import re
from typing import Any, Callable, List

from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.utils.data_types import Operation, Language

from .word import *


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


def splitter(input_str: str) -> List[str]:
    return input_str.split()


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
    >>> tok = DefaultTokenizationOperation(operation_input="aaa bbb ccc")
    >>> tok.output
    ['aaa', 'bbb', 'ccc']
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
    """The default Latin tokenization algorithm"""

    description = "CLTK Dummy Latin Tokenizer"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    op_input = str
    op_output = List[List[int]]
    algorithm = LatinTokenizer.dummy_get_token_indices
    language = LANGUAGES["lat"]
