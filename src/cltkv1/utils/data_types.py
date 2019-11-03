"""Custom data types for the CLTK.

TODO: Fill out more attributes to these
"""

from dataclasses import dataclass, field
from typing import List
from typing import Any, Callable, Generic, List

# from cltkv1.tokenizers.word import DefaultTokenizer
from cltkv1.utils import example_texts


@dataclass
class Language:
    name: str  # Glottolog name
    glottolog_id: str
    latitude: float
    longitude: float
    dates: List[int]  # add later; not available from Glottolog or ISO list
    family_id: str  # from Glottolog
    parent_id: str  # from Glottolog
    level: str  # a language or a dialect
    iso639P3code: str
    type: str  # "an" for ancient and "h" for historical



@dataclass
class Operation:
    """For each type of NLP operation there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field withing ``Word`` it will populate.
    This base class is intended to be inherited by NLP operation
    types (e.g., ``TokenizationOperation`` or ``DependencyOperation``).
    """

    name: str
    description: str
    input: Any
    output: Any
    algorithm: Callable
    type: str



@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declaration.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``
    """

    type = "tokenization"


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm"""

    name = "CLTK Dummy Tokenizer for any language"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = None  # DefaultTokenizer.dummy_get_token_indices
    language = None


@dataclass
class Word:
    """Contains attributes of each processed word in a list of tokens. To be used most often in the ``Doc.tokens``
    dataclass. """

    index_char_start: int = None
    index_char_stop: int = None
    index_token: int = None
    index_sentence: int = None
    string: str = None
    pos: str = None
    scansion: str = None


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class. Contains overall attributes of submitted texts,
    plus most importantly the processed tokenized text ``tokens``, being a list of ``Word`` types.. """

    indices_sentences: List[List[int]] = None
    indices_tokens: List[List[int]] = None
    language: str = None
    tokens: List[Word] = None
    pipeline: List[str] = None
    raw: str = None

