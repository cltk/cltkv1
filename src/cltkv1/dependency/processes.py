"""``Process`` classes for accessing the StanfordNLP project."""

from dataclasses import dataclass
from typing import Dict, List, Tuple

import stanfordnlp
from boltons.cacheutils import cachedproperty

from cltkv1.core.data_types import Doc, Process, Word
from cltkv1.dependency.stanford import StanfordNLPWrapper
from cltkv1.dependency.tree import DependencyTree


@dataclass
class StanfordNLPProcess(Process):
    """A ``Process`` type to capture everything
    that the ``stanfordnlp`` project can do for a
    given language.


    .. note::
        ``stanfordnlp`` has only partial functionality available for some languages.


    >>> from cltkv1.dependency.processes import StanfordNLPProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> process_stanford = StanfordNLPProcess(input_doc=Doc(raw=get_example_text("lat")), language="lat")
    >>> isinstance(process_stanford, StanfordNLPProcess)
    True
    >>> from stanfordnlp.pipeline.doc import Document
    >>> process_stanford.run()
    >>> isinstance(process_stanford.output_doc.stanfordnlp_doc, Document)
    True
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return StanfordNLPWrapper.get_nlp(language=self.language)

    def run(self):
        tmp_doc = self.input_doc
        stanfordnlp_wrapper = self.algorithm
        stanfordnlp_doc = stanfordnlp_wrapper.parse(tmp_doc.raw)
        cltk_words = self.stanfordnlp_to_cltk_word_type(stanfordnlp_doc)
        tmp_doc.words = cltk_words
        tmp_doc.stanfordnlp_doc = stanfordnlp_doc
        self.output_doc = tmp_doc

    @staticmethod
    def stanfordnlp_to_cltk_word_type(stanfordnlp_doc):

        """Take an entire ``stanfordnlp`` document, extract
        each word, and encode it in the way expected by
        the CLTK's ``Word`` type.

        >>> from cltkv1.dependency.processes import StanfordNLPProcess
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> process_stanford = StanfordNLPProcess(input_doc=Doc(raw=get_example_text("lat")), language="lat")
        >>> process_stanford.run()
        >>> cltk_words = process_stanford.output_doc.words
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=3, parent=None, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=None, stop=None)
        """
        words_list = list()  # type: List[Word]

        for sentence_index, sentence in enumerate(stanfordnlp_doc.sentences):
            sent_words = dict()  # type: Dict[int, Word]
            indices = list()  # type: List[Tuple[int, int]]

            for token_index, token in enumerate(sentence.tokens):
                stanfordnlp_word = token.words[0]  # type: stanfordnlp.pipeline.doc.Word
                cltk_word = Word(
                    index_token=int(stanfordnlp_word.index)
                    - 1,  # subtract 1 from index b/c snpl starts their index at 1
                    index_sentence=sentence_index,
                    string=stanfordnlp_word.text,  # same as ``token.text``
                    pos=stanfordnlp_word.pos,
                    xpos=stanfordnlp_word.xpos,
                    upos=stanfordnlp_word.upos,
                    lemma=stanfordnlp_word.lemma,
                    dependency_relation=stanfordnlp_word.dependency_relation,
                    features={}
                    if stanfordnlp_word.feats == "_"
                    else dict(
                        [f.split("=") for f in stanfordnlp_word.feats.split("|")]
                    ),
                )  # type: Word
                sent_words[cltk_word.index_token] = cltk_word
                indices.append(
                    (
                        int(stanfordnlp_word.governor)
                        - 1,  # -1 to match CLTK Word.index_token
                        int(stanfordnlp_word.parent_token.index)
                        - 1,  # -1 to match CLTK Word.index_token
                    )
                )
                words_list.append(cltk_word)

            # JS's original version put entire ``Word`` into ``Word.governor`` and ``Word.parent``
            # for idx, cltk_word in enumerate(sent_words.values()):
            #     governor_index, parent_index = indices[idx]  # type: int, int
            #     cltk_word.governor = (
            #         sent_words[governor_index] if governor_index > 0 else None
            #     )
            #     if cltk_word.index_token != sent_words[parent_index].index_token:
            #         cltk_word.parent = sent_words[parent_index]

            # Instead, put only the index # of the governor and parent
            # TODO: Confirm that cltk_word.parent is ever getting filled out. Only for some lang models?
            for idx, cltk_word in enumerate(sent_words.values()):
                governor_index, parent_index = indices[idx]  # type: int, int
                cltk_word.governor = governor_index if governor_index >= 0 else None
                if cltk_word.index_token != sent_words[parent_index].index_token:
                    cltk_word.parent = parent_index

        return words_list


@dataclass
class GreekStanfordNLPProcess(StanfordNLPProcess):
    language: str = "grc"
    description: str = "Default process for StanfordNLP for the Ancient Greek language."


@dataclass
class LatinStanfordNLPProcess(StanfordNLPProcess):
    language: str = "lat"
    description: str = "Default process for StanfordNLP for the Latin language."


@dataclass
class OCSStanfordNLPProcess(StanfordNLPProcess):
    language: str = "chu"
    description: str = "Default process for StanfordNLP for the Old Church Slavonic language."


@dataclass
class OldFrenchStanfordNLPProcess(StanfordNLPProcess):
    language: str = "fro"
    description: str = "Default process for StanfordNLP for the Old French language."


@dataclass
class GothicStanfordNLPProcess(StanfordNLPProcess):
    language: str = "got"
    description: str = "Default process for StanfordNLP for the Gothic language."


class TreeBuilderProcess(Process):
    """A ``Process`` that takes a doc containing sentences of CLTK words
    and returns a dependency tree for each sentences.

    TODO: JS help to make this work, illustrate better.

    >>> from cltkv1 import NLP
    >>> nlp = NLP(language="got")
    >>> from cltkv1.dependency.processes import TreeBuilderProcess

    # >>> nlp.pipeline.add_process(TreeBuilderProcess)
    # >>> from cltkv1.utils.example_texts import get_example_text
    # >>> doc = nlp.analyze(text=get_example_text("got"))
    # >>> len(doc.trees)
    # 4
    """

    def algorithm(self, doc):
        doc.trees = [DependencyTree.to_tree(sentence) for sentence in doc.sentences]
        return doc
