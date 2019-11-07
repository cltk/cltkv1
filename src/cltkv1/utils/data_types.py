"""Custom data types for the CLTK. These types form the building blocks
of the NLP pipeline.

>>> from cltkv1.utils.data_types import Word
>>> from cltkv1.utils.data_types import Operation
>>> from cltkv1.utils.data_types import Doc
>>> from cltkv1.utils.data_types import Language
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, List

# from cltkv1.tokenizers.word import DefaultTokenizer
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

    >>> def a_function():    pass
    >>> Operation(description="abstract operation", algorithm=a_function())
    Operation(description='abstract operation', algorithm=None)
    """

    description: str
    algorithm: Callable


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class.
    Contains overall attributes of submitted texts, plus most
    importantly the processed tokenized text ``tokens``,
    being a list of ``Word`` types.

    >>> from cltkv1.utils.data_types import Doc
    >>> from cltkv1.languages.glottolog import LANGUAGES
    >>> latin_lang = LANGUAGES["lat"]
    >>> from cltkv1.utils.example_texts import LATIN
    >>> latin_text = LATIN[:275]  # first three sentences
    >>> from cltkv1 import NLP
    >>> cltk_nlp = NLP(language="latin")
    >>> analyzed_doc = cltk_nlp.analyze(latin_text)
    >>> isinstance(analyzed_doc, Doc)
    True
    >>> analyzed_doc.indices_sentences
    [[144, 145], [201, 202], [274, 275]]
    >>> analyzed_doc.indices_tokens
    [[0, 6], [7, 10], [11, 16], [17, 23], [24, 26], [27, 33], [34, 38], [40, 46], [47, 51], [52, 60], [61, 67], [69, 74], [75, 83], [85, 92], [93, 96], [97, 104], [105, 111], [112, 118], [120, 126], [127, 132], [133, 144], [146, 148], [149, 154], [155, 161], [163, 173], [175, 182], [183, 188], [189, 191], [192, 201], [203, 209], [210, 212], [213, 222], [223, 230], [231, 237], [239, 240], [241, 247], [248, 255], [256, 258], [259, 266], [267, 274]]
    >>> analyzed_doc.language
    'latin'
    >>> analyzed_doc.tokens
    [Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos=None, scansion=None), Word(index_char_start=7, index_char_stop=10, index_token=1, index_sentence=None, string='est', pos=None, scansion=None), Word(index_char_start=11, index_char_stop=16, index_token=2, index_sentence=None, string='omnis', pos=None, scansion=None), Word(index_char_start=17, index_char_stop=23, index_token=3, index_sentence=None, string='divisa', pos=None, scansion=None), Word(index_char_start=24, index_char_stop=26, index_token=4, index_sentence=None, string='in', pos=None, scansion=None), Word(index_char_start=27, index_char_stop=33, index_token=5, index_sentence=None, string='partes', pos=None, scansion=None), Word(index_char_start=34, index_char_stop=38, index_token=6, index_sentence=None, string='tres', pos=None, scansion=None), Word(index_char_start=40, index_char_stop=46, index_token=7, index_sentence=None, string='quarum', pos=None, scansion=None), Word(index_char_start=47, index_char_stop=51, index_token=8, index_sentence=None, string='unam', pos=None, scansion=None), Word(index_char_start=52, index_char_stop=60, index_token=9, index_sentence=None, string='incolunt', pos=None, scansion=None), Word(index_char_start=61, index_char_stop=67, index_token=10, index_sentence=None, string='Belgae', pos=None, scansion=None), Word(index_char_start=69, index_char_stop=74, index_token=11, index_sentence=None, string='aliam', pos=None, scansion=None), Word(index_char_start=75, index_char_stop=83, index_token=12, index_sentence=None, string='Aquitani', pos=None, scansion=None), Word(index_char_start=85, index_char_stop=92, index_token=13, index_sentence=None, string='tertiam', pos=None, scansion=None), Word(index_char_start=93, index_char_stop=96, index_token=14, index_sentence=None, string='qui', pos=None, scansion=None), Word(index_char_start=97, index_char_stop=104, index_token=15, index_sentence=None, string='ipsorum', pos=None, scansion=None), Word(index_char_start=105, index_char_stop=111, index_token=16, index_sentence=None, string='lingua', pos=None, scansion=None), Word(index_char_start=112, index_char_stop=118, index_token=17, index_sentence=None, string='Celtae', pos=None, scansion=None), Word(index_char_start=120, index_char_stop=126, index_token=18, index_sentence=None, string='nostra', pos=None, scansion=None), Word(index_char_start=127, index_char_stop=132, index_token=19, index_sentence=None, string='Galli', pos=None, scansion=None), Word(index_char_start=133, index_char_stop=144, index_token=20, index_sentence=None, string='appellantur', pos=None, scansion=None), Word(index_char_start=146, index_char_stop=148, index_token=21, index_sentence=None, string='Hi', pos=None, scansion=None), Word(index_char_start=149, index_char_stop=154, index_token=22, index_sentence=None, string='omnes', pos=None, scansion=None), Word(index_char_start=155, index_char_stop=161, index_token=23, index_sentence=None, string='lingua', pos=None, scansion=None), Word(index_char_start=163, index_char_stop=173, index_token=24, index_sentence=None, string='institutis', pos=None, scansion=None), Word(index_char_start=175, index_char_stop=182, index_token=25, index_sentence=None, string='legibus', pos=None, scansion=None), Word(index_char_start=183, index_char_stop=188, index_token=26, index_sentence=None, string='inter', pos=None, scansion=None), Word(index_char_start=189, index_char_stop=191, index_token=27, index_sentence=None, string='se', pos=None, scansion=None), Word(index_char_start=192, index_char_stop=201, index_token=28, index_sentence=None, string='differunt', pos=None, scansion=None), Word(index_char_start=203, index_char_stop=209, index_token=29, index_sentence=None, string='Gallos', pos=None, scansion=None), Word(index_char_start=210, index_char_stop=212, index_token=30, index_sentence=None, string='ab', pos=None, scansion=None), Word(index_char_start=213, index_char_stop=222, index_token=31, index_sentence=None, string='Aquitanis', pos=None, scansion=None), Word(index_char_start=223, index_char_stop=230, index_token=32, index_sentence=None, string='Garumna', pos=None, scansion=None), Word(index_char_start=231, index_char_stop=237, index_token=33, index_sentence=None, string='flumen', pos=None, scansion=None), Word(index_char_start=239, index_char_stop=240, index_token=34, index_sentence=None, string='a', pos=None, scansion=None), Word(index_char_start=241, index_char_stop=247, index_token=35, index_sentence=None, string='Belgis', pos=None, scansion=None), Word(index_char_start=248, index_char_stop=255, index_token=36, index_sentence=None, string='Matrona', pos=None, scansion=None), Word(index_char_start=256, index_char_stop=258, index_token=37, index_sentence=None, string='et', pos=None, scansion=None), Word(index_char_start=259, index_char_stop=266, index_token=38, index_sentence=None, string='Sequana', pos=None, scansion=None), Word(index_char_start=267, index_char_stop=274, index_token=39, index_sentence=None, string='dividit', pos=None, scansion=None)]
    >>> analyzed_doc.pipeline
    >>> analyzed_doc.raw
    'Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit.'
    """

    indices_sentences: List[List[int]] = None
    indices_tokens: List[List[int]] = None
    language: str = None
    tokens: List[Word] = None
    pipeline: List[Operation] = None
    raw: str = None
