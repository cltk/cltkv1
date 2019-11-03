"""Primary module for CLTK pipeline."""

import re
from typing import List

from cltkv1.tokenizers.sentence import DefaultSplitter
from cltkv1.tokenizers.word import Tokenizer, dummy_get_token
from cltkv1.utils import example_texts
from cltkv1.utils.data_types import Doc
from cltkv1.utils.pipelines import DefaultPipeline, LatinPipeline

# from cltkv1.wrappers import StanfordNLPWrapper


class NLP:
    """Primary class for NLP pipeline.

    >>> cltk_nlp = NLP(language='greek')
    >>> cltk_nlp.language
    'greek'
    >>> greek_text_analyzed = cltk_nlp.analyze(example_texts.GREEK)
    >>> greek_text_analyzed.language
    'greek'
    >>> greek_text_analyzed.indices_sentences
    [[155, 156], [204, 205], [349, 350], [641, 642], [1095, 1096], [1352, 1353], [1369, 1370], [1477, 1478], [1877, 1878]]
    >>> greek_text_analyzed.indices_tokens[0:3]
    [[0, 3], [4, 7], [8, 13]]
    """

    def __init__(self, language: str, custom_pipeline: List[str] = None) -> None:
        """Constructor for CLTK class.

        >>> cltk_nlp = NLP(language='greek')
        >>> isinstance(cltk_nlp, NLP)
        True
        """
        self.language = language
        self.toker = Tokenizer()
        self.custom_pipeline = custom_pipeline
        self.pipeline = self._get_pipeline(self.custom_pipeline)

    def _get_pipeline(self, custom_pipeline=None):
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.
        """
        if not custom_pipeline:
            # look up default pipeline for given language
            if self.language == "latin":
                self.pipeline = LatinPipeline
            self.pipeline = DefaultPipeline
        else:
            # confirm that user-defined pipeline is possible
            raise NotImplementedError("Custom pipelines not implemented yet.")

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        >>> cltk_nlp = NLP(language='latin')
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> analyzed_text = cltk_nlp.analyze(example_texts.LATIN)
        >>> analyzed_text.language
        'latin'
        >>> analyzed_text.indices_sentences
        [[144, 145], [201, 202], [274, 275], [572, 573], [768, 769], [985, 986], [1122, 1123], [1269, 1270]]
        >>> analyzed_text.indices_tokens[0:3]
        [[0, 6], [7, 10], [11, 16]]
        >>> analyzed_text.tokens[0]
        Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=None, string='Gallia', pos=None, scansion=None)
        """

        sentence_splitter = DefaultSplitter()
        indices_sentences = sentence_splitter.dummy_get_indices(text=text)
        indices_words = self.toker.dummy_get_token_indices(text=text)
        tokens = dummy_get_token(indices_words, text)
        text = Doc(
            indices_sentences=indices_sentences,
            indices_tokens=indices_words,
            language=self.language,
            raw=text,
            tokens=tokens,
        )
        return text
