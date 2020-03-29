""" Code for sentence tokenization: Latin

>>> from cltkv1.sentence.lat import LatinPunktSentenceTokenizer
>>> from cltkv1.utils.example_texts import get_example_text
>>> splitter = LatinPunktSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("lat"))
>>> sentences[:2]

>>> len(sentences)
9
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."

import os.path

import nltk
from cltk.tokenize.latin.params import (
    PUNCTUATION,
    STRICT_PUNCTUATION,
    LatinLanguageVars,
)
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars

from cltkv1.sentence.sentence import (
    BasePunktSentenceTokenizer,
    BaseRegexSentenceTokenizer,
)
from cltkv1.tokenizers.lat import PUNCTUATION, STRICT_PUNCTUATION, LatinLanguageVars
from cltkv1.utils import get_cltk_data_dir

# def SentenceTokenizer(tokenizer: str = "punkt", strict: bool = False):
#     if tokenizer == "punkt":
#         return LatinPunktSentenceTokenizer(strict=strict)


class LatinPunktSentenceTokenizer(BasePunktSentenceTokenizer):
    """ PunktSentenceTokenizer trained on Latin
    """

    models_path = os.path.normpath(
        get_cltk_data_dir() + "/lat/model/latin_models_cltk/tokenizers/sentence"
    )

    def __init__(self: object, strict: bool = False):
        """
        :param strict : allow for stricter puctuation for sentence tokenization
        :type strict: bool
        """
        self.lang_vars = LatinLanguageVars()
        self.strict = strict
        super().__init__(language="lat", lang_vars=self.lang_vars)
        self.models_path = LatinPunktSentenceTokenizer.models_path

        try:
            self.model = open_pickle(
                os.path.join(self.models_path, "latin_punkt.pickle")
            )
        except FileNotFoundError as err:
            missing_models_message = "``LatinPunktSentenceTokenizer`` requires the ``latin_models_cltk`` repo to be in cltk_data. Please download this corpus."
            raise type(err)(LatinPunktSentenceTokenizer.missing_models_message)

        if self.strict:
            PunktLanguageVars.sent_end_chars = STRICT_PUNCTUATION
        else:
            PunktLanguageVars.sent_end_chars = PUNCTUATION
