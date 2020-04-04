"""Code for sentence tokenization: Greek.

Sentence tokenization for Ancient Greek is available using a regular-expression based tokenizer.

>>> from cltkv1.sentence.grc import GreekRegexSentenceTokenizer
>>> from cltkv1.utils.example_texts import get_example_text
>>> splitter = GreekRegexSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("grc"))
>>> sentences[:2]
['ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν καὶ αὐτὸς ὑπ᾽ αὐτῶν ὀλίγου ἐμαυτοῦ ἐπελαθόμην, οὕτω πιθανῶς ἔλεγον.', 'καίτοι ἀληθές γε ὡς ἔπος εἰπεῖν οὐδὲν εἰρήκασιν.']
>>> len(sentences)
9
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]


from cltkv1.sentence.sentence import BaseRegexSentenceTokenizer
from cltkv1.tokenizers.grc import GreekLanguageVars


class GreekRegexSentenceTokenizer(BaseRegexSentenceTokenizer):
    """``RegexSentenceTokenizer`` for Ancient Greek."""

    def __init__(self: object):
        super().__init__(
            language="greek", sent_end_chars=GreekLanguageVars.sent_end_chars
        )
