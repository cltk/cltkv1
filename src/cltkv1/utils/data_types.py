"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.

>>> from cltkv1.utils.data_types import Word
>>> from cltkv1.utils.data_types import Operation
>>> from cltkv1.utils.data_types import Doc
>>> from cltkv1.utils.data_types import Language
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, List, Type

from cltkv1.utils import example_texts


@dataclass
class Language:
    """For holding information about any given language. Used to
    encode data from ISO 639-3 and Glottolog at
    ``cltkv1.lagnuages.glottolog.LANGUAGES`` May be extended by
    user for dialects or languages not documented by ISO 639-3.

    >>> from cltkv1.utils.data_types import Language
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> latin = LANGUAGES["lat"]
    >>> isinstance(latin, Language)
    True
    >>> latin
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso639P3code='lat', type='a')
    """

    name: str  # Glottolog description
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
class Word:
    """Contains attributes of each processed word in a list of
    tokens. To be used most often in the ``Doc.tokens`` dataclass.

    >>> from cltkv1.utils.data_types import Word
    >>> from cltkv1.utils.example_texts import LATIN
    >>> LATIN[:25]
    'Gallia est omnis divisa i'
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> latin = LANGUAGES["lat"]
    >>> Word(index_char_start=0, index_char_stop=6, index_token=0, string=LATIN[0:6], pos="nom")
    Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos='nom', scansion=None)
    """

    index_char_start: int = None
    index_char_stop: int = None
    index_token: int = None
    index_sentence: int = None
    string: str = None
    pos: str = None
    scansion: str = None


@dataclass
class Operation:
    """For each type of NLP operation there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field within ``Word`` it will populate.
    This base class is intended to be inherited by NLP operation
    types (e.g., ``TokenizationOperation`` or ``DependencyOperation``).

    >>> an_operation = Operation(data_input="input words here")
    """

    data_input: Any
    algorithm = None
    language = None

    @property
    def data_output(self):
        """Attribute for subclassed ``Operation`` objects to return
        ``data_input`` that has been processed by the ``algorithm``.
        """
        if self.algorithm:
            return self.algorithm(self.data_input)
        else:
            raise NotImplementedError


@dataclass
class MultiOperation(Operation):
    """A class to be called directly or inherited from when
    a particular NLP algo does more than one process, such
    as tokenization and tagging together.

    >>> def multi_fn(_str: str) -> List[str]:    return _str.upper().split()
    >>> a_multi_operation = MultiOperation(data_input="Some words for processing.", algorithm=multi_fn)
    >>> a_multi_operation.data_output
    ['SOME', 'WORDS', 'FOR', 'PROCESSING.']
    """
    algorithm: Callable


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``tokens``,
    being a list of ``Word`` types.
    """

    indices_sentences: List[List[int]] = None
    indices_tokens: List[List[int]] = None
    language: str = None
    tokens: List[Word] = None
    pipeline: List[Operation] = None
    raw: str = None


@dataclass
class Pipeline:
    """Abstract ``Pipeline`` class to be inherited.

    # TODO: Consider adding a Unicode normalization as a default first Operation

    >>> from cltkv1.utils.data_types import Operation, Pipeline
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> from cltkv1.tokenizers import LatinTokenizationOperation
    >>> a_pipeline = Pipeline(description="an abstract pipeline", execution_order=[LatinTokenizationOperation], language=LANGUAGES["lat"])
    >>> a_pipeline.description
    'an abstract pipeline'
    >>> issubclass(a_pipeline.execution_order[0], Operation)
    True
    """

    description: str
    execution_order: List[Type[Operation]]
    language: Language
