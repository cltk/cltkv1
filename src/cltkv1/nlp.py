"""Primary module for CLTK pipeline."""

from typing import List

from cltkv1.languages.glottolog import get_lang
from cltkv1.utils.data_types import Doc, Language, Pipeline
from cltkv1.utils.exceptions import UnknownLanguageError
from cltkv1.utils.pipelines import DefaultPipeline, LatinPipeline


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
            raise UnknownLanguageError(
                f"Unknown language '{language}'. Use ISO 639-3 languages."
            )
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
        >>> cltk_obj = cltk_nlp.analyze(text=LATIN)
        >>> isinstance(cltk_obj, Doc)
        True
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=4, parent_token=<Token index=1;words=[<Word index=1;text=Gallia;lemma=aallius;upos=NOUN;xpos=A1|grn1|casA|gen2|stAM;feats=Case=Nom|Degree=Pos|Gender=Fem|Number=Sing;governor=4;dependency_relation=nsubj>]>, feats='Case=Nom|Degree=Pos|Gender=Fem|Number=Sing')
        """
        # print(self.pipeline)  # <class 'cltkv1.utils.pipelines.LatinPipeline'>
        # print(dir(self.pipeline))  # 'description', 'language'
        a_pipeline = self.pipeline()
        # print(a_pipeline.description)
        # print(a_pipeline.language)
        # print(a_pipeline.language.name)  # Latin
        # print(type(a_pipeline.processes))  # <class 'list'>
        # print(a_pipeline.processes[0])  # <class 'cltkv1.wrappers.StanfordNLPProcess'>
        # print("")
        for process in a_pipeline.processes:
            # print(type(process))  # <class 'type'>
            # print(dir(process))  # ['algorithm', 'data_output', 'language', 'stanfordnlp_to_cltk_word_type']
            # print(process)  # <class 'cltkv1.wrappers.StanfordNLPProcess'>
            # print("")
            process_stanford = process(
                data_input=text, language=self.language.iso_639_3_code
            )
            cltk_words = process_stanford.words

            doc = Doc(language=self.language.iso_639_3_code, words=cltk_words)

            return doc
