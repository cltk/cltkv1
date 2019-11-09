"""Module for tokenizers."""

import re
from dataclasses import dataclass, field
from typing import Callable, List, Tuple

from cltk.tokenize.word import WordTokenizer as WordTokenizer

from cltkv1.utils.data_types import Word, Operation


akkadian_word_tok = WordTokenizer(language="akkadian")
arabic_word_tok = WordTokenizer(language="arabic")
greek_word_tok = WordTokenizer(language="greek")
latin_word_tok = WordTokenizer(language="latin")
middle_english_word_tok = WordTokenizer(language="middle_english")
middle_french_word_tok = WordTokenizer(language="middle_french")
middle_high_german_word_tok = WordTokenizer(language="middle_high_german")
old_french_word_tok = WordTokenizer(language="old_french")
old_norse_word_tok = WordTokenizer(language="old_norse")
sanskrit_word_tok = WordTokenizer(language="sanskrit")
# multilingual_word_tok = WordTokenizer(language="multilingual")



@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declarations.

    Example: ``TokenizationOperation`` -> ``LatinTokenizationOperation``

    >>> from cltkv1.tokenizers.word import TokenizationOperation
    >>> from cltkv1.utils.data_types import Operation
    >>> issubclass(TokenizationOperation, Operation)
    True
    >>> def a_function():    pass
    >>> TokenizationOperation(description="some description", algorithm=a_function())
    TokenizationOperation(description='some description', algorithm=None)
    """

def simple_regexp_tok(input_str: str) -> List[str]:
    """Simple regexp tokenizer for illustration.

    >>> from cltkv1.tokenizers.word import simple_regexp_tok
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> simple_regexp_tok(input_str=OLD_NORSE[:29])
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """
    return re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|['\w\-]+", input_str)


@dataclass
class DefaultTokenizationOperation(TokenizationOperation):
    """The default tokenization algorithm.

    >>> from cltkv1.tokenizers.word import DefaultTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = DefaultTokenizationOperation(operation_input=OLD_NORSE[:29])
    >>> tok.output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    >>> tok.description
    'A basic whitespace tokenizer'
    """

    operation_input: str = None
    description: str = field(default="A basic whitespace tokenizer")
    algorithm: Callable = field(default=simple_regexp_tok)

    @property
    def output(self):
        return self.algorithm(self.operation_input)


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm.

    >>> from cltkv1.tokenizers import LatinTokenizationOperation
    >>> from cltkv1.utils.example_texts import LATIN
    >>> tok = LatinTokenizationOperation(operation_input=LATIN[:23])
    >>> tok.output
    ['Gallia', 'est', 'omnis', 'divisa']
    """

    operation_input: str = None
    description: str = field(default="The default Latin tokenizer")
    algorithm: Callable = field(default=latin_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class GreekTokenizationOperation(TokenizationOperation):
    """The default Greek tokenization algorithm.

    >>> from cltkv1.tokenizers import GreekTokenizationOperation
    >>> from cltkv1.utils.example_texts import GREEK
    >>> tok = GreekTokenizationOperation(operation_input=GREEK[:23])
    >>> tok.output
    ['ὅτι', 'μὲν', 'ὑμεῖς', ',', 'ὦ', 'ἄνδρες']
    """

    operation_input: str = None
    description: str = field(default="The default Greek tokenizer")
    algorithm: Callable = field(default=greek_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class AkkadianTokenizationOperation(TokenizationOperation):
    """The default Akkadian tokenization algorithm.

    >>> from cltkv1.tokenizers import AkkadianTokenizationOperation
    >>> from cltkv1.utils.example_texts import AKKADIAN
    >>> tok = AkkadianTokenizationOperation(operation_input=AKKADIAN)
    >>> tok.output
    [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'), ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'), ('wu-e-er', 'akkadian')]
    """

    operation_input: str = None
    description: str = field(default="The default Akkadian tokenizer")
    algorithm: Callable = field(default=akkadian_word_tok.tokenize)

    @property
    def output(self) -> List[Tuple[str, str]]:
        return self.algorithm(self.operation_input)


@dataclass
class OldNorseTokenizationOperation(TokenizationOperation):
    """The default OldNorse tokenization algorithm.

    >>> from cltkv1.tokenizers import OldNorseTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_NORSE
    >>> tok = OldNorseTokenizationOperation(operation_input=OLD_NORSE[:29])
    >>> tok.output
    ['Gylfi', 'konungr', 'réð', 'þar', 'löndum']
    """

    operation_input: str = None
    description: str = field(default="The default Old Norse tokenizer")
    algorithm: Callable = field(default=old_norse_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class MHGTokenizationOperation(TokenizationOperation):
    """The default Middle High German tokenization algorithm.

    >>> from cltkv1.tokenizers import MHGTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_HIGH_GERMAN
    >>> tok = MHGTokenizationOperation(operation_input=MIDDLE_HIGH_GERMAN[:29])
    >>> tok.output
    ['Ik', 'gihorta', 'ðat', 'seggen', 'ðat', 'sih']
    """

    operation_input: str = None
    description: str = field(default="The default Middle High German tokenizer")
    algorithm: Callable = field(default=middle_high_german_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class ArabicTokenizationOperation(TokenizationOperation):
    """The default Arabic tokenization algorithm.

    >>> from cltkv1.tokenizers import ArabicTokenizationOperation
    >>> from cltkv1.utils.example_texts import ARABIC
    >>> tok = ArabicTokenizationOperation(operation_input=ARABIC[:34])
    >>> tok.output
    ['كهيعص', '﴿', '١', '﴾', 'ذِكْرُ', 'رَحْمَتِ', 'رَبِّكَ']
    """

    operation_input: str = None
    description: str = field(default="The default Arabic tokenizer")
    algorithm: Callable = field(default=arabic_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class OldFrenchTokenizationOperation(TokenizationOperation):
    """The default Old French tokenization algorithm.

    >>> from cltkv1.tokenizers import OldFrenchTokenizationOperation
    >>> from cltkv1.utils.example_texts import OLD_FRENCH
    >>> tok = OldFrenchTokenizationOperation(operation_input=OLD_FRENCH[:37])
    >>> tok.output
    ['Une', 'aventure', 'vos', 'voil', 'dire', 'Molt', 'bien']
    """

    operation_input: str = None
    description: str = field(default="The default Old French tokenizer")
    algorithm: Callable = field(default=old_french_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class MiddleFrenchTokenizationOperation(TokenizationOperation):
    """The default Middle French tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleFrenchTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_FRENCH
    >>> tok = MiddleFrenchTokenizationOperation(operation_input=MIDDLE_FRENCH[:37])
    >>> tok.output
    ['Attilius', 'Regulus', ',', 'general', 'de', "l'", 'armée']
    """

    operation_input: str = None
    description: str = field(default="The default Middle French tokenizer")
    algorithm: Callable = field(default=middle_french_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class MiddleEnglishTokenizationOperation(TokenizationOperation):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import MiddleEnglishTokenizationOperation
    >>> from cltkv1.utils.example_texts import MIDDLE_ENGLISH
    >>> tok = MiddleEnglishTokenizationOperation(operation_input=MIDDLE_ENGLISH[:31])
    >>> tok.output
    ['Whilom', ',', 'as', 'olde', 'stories', 'tellen']
    """

    operation_input: str = None
    description: str = field(default="The default Middle English tokenizer")
    algorithm: Callable = field(default=middle_english_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


@dataclass
class SanskritTokenizationOperation(TokenizationOperation):
    """The default Middle English tokenization algorithm.

    >>> from cltkv1.tokenizers import SanskritTokenizationOperation
    >>> from cltkv1.utils.example_texts import SANSKRIT
    >>> tok = SanskritTokenizationOperation(operation_input=SANSKRIT[:31])
    >>> tok.output
    ['ईशा', 'वास्यम्', 'इदं', 'सर्वं', 'यत्', 'किञ्च']
    """

    operation_input: str = None
    description: str = field(default="The default Middle English tokenizer")
    algorithm: Callable = field(default=sanskrit_word_tok.tokenize)

    @property
    def output(self) -> List[str]:
        return self.algorithm(self.operation_input)


class Tokenizer:
    def __init__(self):
        pass

    def tokenize_str(self, text: str) -> List[str]:
        """Tokenize inputs and return list of str."""
        return text.split(" ")

    @staticmethod
    def dummy_get_token_indices(text: str) -> List[List[int]]:
        """Get the start/stop char indices of word boundaries.

        >>> from cltkv1.tokenizers import Tokenizer
        >>> generic_toker = Tokenizer()
        >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας"
        >>> indices_words = generic_toker.dummy_get_token_indices(text=john_damascus_corinth)
        >>> indices_words[0:3]
        [[0, 5], [6, 11], [13, 20]]
        """
        indices_words = list()
        pattern_word = re.compile(r"\w+")
        for word_match in pattern_word.finditer(string=text):
            idx_word_start, idx_word_stop = word_match.span()
            indices_words.append([idx_word_start, idx_word_stop])
        return indices_words


class DefaultTokenizer(Tokenizer):
    """This tokenizer is for language for which there is no specially word tokenizer."""

    def __init__(self):
        super().__init__()


class LatinTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()


def dummy_get_token(indices_tokens: List[List[int]], text: str) -> List[Word]:
    """Take indices and raw string text, then return populated Word object.

    >>> from cltkv1 import NLP
    >>> cltk_nlp = NLP(language='greek')
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> toker = Tokenizer()
    >>> indices_words = toker.dummy_get_token_indices(text=john_damascus_corinth)
    >>> tokens = dummy_get_token(indices_words, john_damascus_corinth)
    >>> tokens[0]
    Word(index_char_start=0, index_char_stop=5, index_token=0, index_sentence=None, string='Τοῦτο', pos=None, scansion=None)
    """
    tokens = list()
    for count, indices in enumerate(indices_tokens):
        start, end = indices[0], indices[1]
        token_str = text[start:end]
        word = Word(
            index_char_start=start,
            index_char_stop=end,
            index_token=count,
            string=token_str,
        )
        tokens.append(word)
    return tokens


if __name__ == "__main__":
    def_tok = DefaultTokenizer()
    def_tokens = def_tok.tokenize("here ye here ye")
    print(def_tokens)

    lat_tok = LatinTokenizer()
    lat_tokens = lat_tok.tokenize("amo amas amat")
    print(lat_tokens)
