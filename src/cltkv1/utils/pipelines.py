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
from cltkv1.utils.data_types import Language, Pipeline, Process
from cltkv1.wrappers import StanfordNLPProcess


@dataclass
class DefaultPipeline(Pipeline):
    """Default ``Pipeline`` object to be run when language is unknown
    or of which CLTK coverage is not know.

    >>> from cltkv1.utils.pipelines import DefaultPipeline
    >>> a_pipeline = DefaultPipeline(description="Pipeline for some language", processes=[DefaultTokenizationProcess], language=LANGUAGES["ett"])
    >>> a_pipeline.description
    'Pipeline for some language'
    >>> etruscan = "laris velkasnas mini muluvanice menervas"
    >>> for process in a_pipeline.processes:    print(process.algorithm(etruscan))
    ['laris', 'velkasnas', 'mini', 'muluvanice', 'menervas']
    """


def upp(_str: str) -> str:
    return _str.upper()


def apnd(_str: str) -> str:
    return _str + " YYY"


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    >>> from cltkv1.utils.pipelines import DefaultPipeline
    >>> a_pipeline = LatinPipeline()
    >>> a_pipeline.description
    'Pipeline for the Latin language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
    >>> a_pipeline.language.name
    'Latin'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Latin language"
    language: Language = LANGUAGES["lat"]
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])
