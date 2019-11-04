"""Init for `cltkv1.tokenize`."""

from dataclasses import dataclass

from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.utils.data_types import Operation

from .word import *


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declaration.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``
    """

    type = "tokenization"


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm."""

    name = "CLTK Dummy Tokenizer for any language"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = None  # DefaultTokenizer.dummy_get_token_indices
    language = None


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm"""

    name = "CLTK Dummy Latin Tokenizer"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = LatinTokenizer.dummy_get_token_indices
    language = LANGUAGES["lat"]
