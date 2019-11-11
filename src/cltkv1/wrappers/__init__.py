"""Init for `cltkv1.wrappers`."""

from .stanford import *

from cltkv1.utils.data_types import Doc, Word


class StanfordNLPProcess(MultiProcess):
    """An ``Process`` type to capture everything
    that the ``stanfordnlp`` project can do for a
    given language.

    .. note::
       Note that ``stanfordnlp` has
       only partial functionality available for
       some languages.

    >>> from cltkv1.wrappers import StanfordNLPProcess
    >>> from cltkv1.utils.example_texts import LATIN
    >>> process_stanford = StanfordNLPProcess(data_input=LATIN, language="lat")
    >>> from cltkv1.wrappers import StanfordNLPProcess
    >>> isinstance(process_stanford, StanfordNLPProcess)
    True
    >>> stanford_nlp_doc = process_stanford.nlp_doc_stanford
    >>> from stanfordnlp.pipeline.doc import Document
    >>> isinstance(stanford_nlp_doc, Document)
    True
    """

    def __init__(self, data_input, language):
        """Constructor."""
        self.data_input = data_input
        self.language = language
        self.nlp_doc_stanford = self._get_stanford_nlp_obj()
        self.words = self.stanfordnlp_to_cltk_word_type()

    def _get_stanford_nlp_obj(self):
        """Call ``stanfordnlp`` and return original document object."""
        nlp_obj_stanford = StanfordNLPWrapper(language=self.language)
        return nlp_obj_stanford.parse(text=self.data_input)

    def stanfordnlp_to_cltk_word_type(self):
        """Take an entire ``stanfordnlp`` object, extract
        each word, and encode it in the way expected in
        the CLTK's ``Word`` type.

        >>> from cltkv1.wrappers import StanfordNLPProcess
        >>> from cltkv1.utils.example_texts import LATIN
        >>> process_stanford = StanfordNLPProcess(data_input=LATIN, language="lat")
        >>> cltk_words = process_stanford.words
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None)
        """
        words_list = list()
        # print('* * * ', dir(self.nlp_doc_stanford))  # .sentences, .text, .conll_file, .load_annotations, .write_conll_to_file
        # .text is the raw str
        # .sentences is list
        for sentence_index, sentence in enumerate(self.nlp_doc_stanford.sentences):
            # print(type(sentence))  # <class 'stanfordnlp.pipeline.doc.Sentence'>
            # print(dir(sentence))  # 'build_dependencies', 'dependencies', 'dependencies_string', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'tokens_string', 'words', 'words_string'
            for token in sentence.tokens:
                # print("%%%", type(token), token)  # stanfordnlp.pipeline.doc.Token
                # print("999", dir(token))  # 'index', 'text', 'words'
                # print(type(token.text))  # str
                # print(token.index, type(token.index))  # str; is the word index per sentence

                # print("$$$", type(token.words))  # type: list
                # print("!!!", type(token.words[0]), dir(token.words[0]), token.words[0])  # type: 'stanfordnlp.pipeline.doc.Word'; 'dependency_relation', 'feats', 'governor', 'index', 'lemma', 'parent_token', 'pos', 'text', 'upos', 'xpos'
                # print(token.words)  # [<Word index=7;text=.;lemma=.;upos=PUNCT;xpos=Punc;feats=_;governor=1;dependency_relation=punct>]
                # print(len(token.words))  # 1
                stanfordnlp_word = token.words[0]
                # print(dir(stanfordnlp_word))  # 'dependency_relation', 'feats', 'governor', 'index', 'lemma', 'parent_token', 'pos', 'text', 'upos', 'xpos

                cltk_word = Word(index_token=int(token.index), index_sentence=sentence_index, string=token.text, pos=stanfordnlp_word.pos, lemma=stanfordnlp_word.lemma)
                words_list.append(cltk_word)

        return words_list

