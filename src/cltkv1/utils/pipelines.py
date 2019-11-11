"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processs that the CLTK can do
2. the order in which processs are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import Callable, List, Type

from cltkv1 import DefaultTokenizationProcess, LatinTokenizationProcess
from cltkv1.languages.glottolog import LANGUAGES
from cltkv1.utils.data_types import Doc, Language, Process, Pipeline, Word


@dataclass
class DefaultPipeline(Pipeline):
    """Default ``Pipeline`` object to be run when language is unknown
    or of which CLTK coverage is not know.

    >>> from cltkv1.utils.pipelines import DefaultPipeline
    >>> a_pipeline = DefaultPipeline(description="Pipeline for some language", execution_order=[DefaultTokenizationProcess], language=LANGUAGES["ett"])
    >>> a_pipeline.description
    'Pipeline for some language'
    >>> etruscan = "laris velkasnas mini muluvanice menervas"
    >>> for process in a_pipeline.execution_order:    print(process.algorithm(etruscan))
    ['laris', 'velkasnas', 'mini', 'muluvanice', 'menervas']
    """


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    >>> from cltkv1.utils.pipelines import DefaultPipeline
    >>> a_pipeline = LatinPipeline(description="Pipeline for some language", execution_order=[DefaultTokenizationProcess])
    >>> a_pipeline.description
    'Pipeline for some language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso639P3code='lat', type='a')
    >>> a_pipeline.language.name
    'Latin'
    >>> etruscan = "laris velkasnas mini muluvanice menervas"
    >>> for process in a_pipeline.execution_order:    print(process.algorithm(etruscan))
    ['laris', 'velkasnas', 'mini', 'muluvanice', 'menervas']
    """

    word_tokenizer = LatinTokenizationProcess
    language: Language = LANGUAGES["lat"]
    execution_order: List[Type[Process]] = field(default_factory=[word_tokenizer])
