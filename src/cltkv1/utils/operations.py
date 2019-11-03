"""Operations are distinct NLP algorithms that perform particular
processing for particular languages. Each ``Operation`` is to be used
in the ``Pipeline`` data type. For each ``Operation`` data type,
the two most important attributes are:

1. the particular function which it implements
2. data type required of input
3. data type produced

Inheritance example: ``Operation`` -> ``TokenizationOperation`` -> ``LatinTokenizationOperation``
"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, List

from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.tokenizers.sentence import DefaultSplitter, LatinSplitter
from cltkv1.tokenizers.word import DefaultTokenizer, LatinTokenizer, dummy_get_token
from cltkv1.utils.data_types import Operation, TokenizationOperation, Word


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default Latin tokenization algorithm"""

    name = "CLTK Dummy Latin Tokenizer"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]
    algorithm = LatinTokenizer.dummy_get_token_indices
    language = LANGUAGES["lat"]


if __name__ == "__main__":
    lto = LatinTokenizationOperation
    print(lto.__dict__.keys())
    print(lto.name)
    print(lto.description)
    print(lto.language)
    print(lto.language.name)
    print(lto.language.latitude)
    print(lto.language.glottocode)
