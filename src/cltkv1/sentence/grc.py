"""Code for sentence tokenization: Greek.

Sentence tokenization for Ancient Greek is available using (by default) a regular-expression based tokenizer. To tokenize a Greek text by sentences:

>>> from cltk.tokenize.greek.sentence import GreekRegexSentenceTokenizer
>>> from cltkv1.utils.example_texts import get_example_text
>>> splitter_regex = GreekRegexSentenceTokenizer()
>>> sentences = splitter_regex.tokenize(get_example_text("grc"))
>>> sentences[:2]
['ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν καὶ αὐτὸς ὑπ᾽ αὐτῶν ὀλίγου ἐμαυτοῦ ἐπελαθόμην, οὕτω πιθανῶς ἔλεγον.', 'καίτοι ἀληθές γε ὡς ἔπος εἰπεῖν οὐδὲν εἰρήκασιν.']
>>> len(sentences)
9
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]


from cltkv1.sentence.sentence import BaseRegexSentenceTokenizer
from cltkv1.tokenizers.grc import GreekLanguageVars


class GreekRegexSentenceTokenizer(BaseRegexSentenceTokenizer):
    """ RegexSentenceTokenizer for Ancient Greek
    """

    def __init__(self: object):
        super().__init__(
            language="greek", sent_end_chars=GreekLanguageVars.sent_end_chars
        )


# def splitter():
#     """Calls a regular expression-based sentence splitter."""
#     return GreekRegexSentenceTokenizer()


# TODO: KJ: I recommend deprecating this, since a statistical model isn't really necessary for Greek. And if it were, our old training set might not have been right.
# class GreekPunktSentenceTokenizer(BasePunktSentenceTokenizer):
#     """ PunktSentenceTokenizer trained on Ancient Greek
#
#     """
#
#     models_path = (
#         get_cltk_data_dir() + "/greek/model/greek_models_cltk/tokenizers/sentence"
#     )
#     missing_models_message = "GreekPunktSentenceTokenizer requires the ```greek_models_cltk``` to be in cltk_data. Please load this corpus."
#
#     def __init__(self: object, language: str = "greek"):
#         """
#         :param language : language for sentence tokenization
#         :type language: str
#         """
#         super().__init__(language="greek")
#         self.models_path = GreekPunktSentenceTokenizer.models_path
#
#         try:
#             self.model = open_pickle(
#                 os.path.join(os.path.expanduser(self.models_path), "greek_punkt.pickle")
#             )
#         except FileNotFoundError as err:
#             raise type(err)(GreekPunktSentenceTokenizer.missing_models_message)
#
#         self.lang_vars = GreekLanguageVars()
