"""Primary module for CLTK pipeline."""

from typing import List

from cltkv1.utils.data_types import Doc, Language, Pipeline
from cltkv1.languages.glottolog import get_lang
from cltkv1.utils.pipelines import DefaultPipeline, LatinPipeline
from cltkv1.utils.exceptions import UnknownLanguageError


class NLP:
    """NLP class for default processing."""

    def __init__(self, language: str, custom_pipeline: List[str] = None) -> None:
        """Constructor for CLTK class.

        >>> from cltkv1 import NLP
        >>> cltk_nlp = NLP(language="lat")
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> NLP(language="xxx")
        Traceback (most recent call last):
          ...
        cltkv1.utils.exceptions.UnknownLanguageError: Unknown language 'xxx'. Use ISO 639-3 languages.
        """
        try:
            self.language = get_lang(language)  # type: Language
        except UnknownLanguageError:
            raise UnknownLanguageError(f"Unknown language '{language}'. Use ISO 639-3 languages.")
        if custom_pipeline:
            raise NotImplementedError("Custom pipelines not implemented yet.")
        self.pipeline = self._get_pipeline()  # type: Pipeline

    def _get_pipeline(self):
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat")
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> issubclass(cltk_nlp.pipeline, Pipeline)
        True
        >>> issubclass(lat_pipeline, Pipeline)
        True
        """
        if self.language.iso_639_3_code == "lat":
            return LatinPipeline
        return DefaultPipeline

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import LATIN
        >>> from cltkv1.utils.data_types import Doc
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=LATIN)
        >>> isinstance(cltk_doc, Doc)
        True
        >>> cltk_doc.tokens[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=4, parent_token=<Token index=1;words=[<Word index=1;text=Gallia;lemma=aallius;upos=NOUN;xpos=A1|grn1|casA|gen2|stAM;feats=Case=Nom|Degree=Pos|Gender=Fem|Number=Sing;governor=4;dependency_relation=nsubj>]>, feats='Case=Nom|Degree=Pos|Gender=Fem|Number=Sing')
        """
        # TODO: Figure out why I cannot get the .execution_order attribute when using feild(default_factory=)
        # 'language', 'process0', 'word_tokenizer'
        # print(dir(self.pipeline))  # type: Pipeline
        # 'algorithm', 'data_output', 'language', 'stanfordnlp_to_cltk_word_type
        snlpwrapper = self.pipeline.process0
        # print(dir(snlp))
        process_stanford = snlpwrapper(data_input=text, language=self.language.iso_639_3_code)
        cltk_words = process_stanford.words
        # print(cltk_words)
        doc = Doc(language=self.language.iso_639_3_code,
                  tokens=cltk_words,
                  raw=text)
        return doc

