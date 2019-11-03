"""Custom data types for the CLTK.

TODO: Fill out more attributes to these
"""

from dataclasses import dataclass, field
from typing import List

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

    def get_raw_tokens(self):
        """Return list of string tokens.

        >>> from cltkv1 import NLP
        >>> cltk_nlp = NLP(language='greek')
        >>> john_text_analyzed = cltk_nlp.analyze(example_texts.GREEK)
        >>> str_tokens = john_text_analyzed.get_raw_tokens()
        >>> str_tokens[0:3]
        ['ὅτι', 'μὲν', 'ὑμεῖς']
        """
        return [word.string for word in self.tokens]
