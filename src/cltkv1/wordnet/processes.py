"""``Process`` to wrap WordNet."""


from dataclasses import dataclass
from typing import Dict, List, Tuple

from boltons.cacheutils import cachedproperty

from cltkv1.core.data_types import Doc, Process, Word
from cltkv1.wordnet.wordnet import WordNetCorpusReader, WordNetICCorpusReader


@dataclass
class WordNetProcess(Process):
    """A ``Process`` type to capture what the
    ``wordnet`` module can do for a
    given language.
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        """The method to be executed coming out of the

        TODO: @Bill we need to decide upon what the most generally useful method call to your class will be.

        For example, let's say .synsets() is best. The we would loop through Doc.words. Within that list are many Word objects. You
        would look at word.lemma (say) and then in .run() (below) you would create a new key-value pair within Word. So
        if Word.lemma = "adversarius" you could add something like Word.synset = [inimicus, perduellis].
        """

        #
        pass

    def run(self):
        pass
