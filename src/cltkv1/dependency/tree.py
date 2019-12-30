"""A data structure for representing dependency tree graphs."""

__author__ = ["John Stewart <free-variation>"]

from typing import List, Union
from xml.etree.ElementTree import Element, ElementTree

from cltkv1.utils.data_types import Word


class Form(Element):
    """For the word (ie, node) of a dependency tree and its attributes. Inherits
    from the ``Element`` class of Python's ``xml.etree`` library.

    >>> desc_form = Form('described')
    >>> desc_form
    described_0
    >>> desc_form.set('Tense', 'Past')
    >>> desc_form
    described_0
    >>> desc_form / 'VBN'
    described_0/VBN
    >>> desc_form.full_str()
    'described_0 [Tense=Past,pos=VBN]'
    """

    def __init__(self, form: str, form_id: int = 0) -> None:
        """Constructor for the Form class."""
        Element.__init__(self, form, attrib={"form_id": str(form_id)})

    def __truediv__(self, pos_tag: str) -> "Form":
        """Assigns the POS feature for current form. This is
        done by overloading ``operator.truediv()`` (``a / b``) to
        perform ``.set()`` upon and ``Element`` of the xml library.

        >>> desc_form = Form('described')
        >>> desc_form / 'VBN'
        described_0/VBN
        >>> import operator
        >>> desc_form = Form('described')
        >>> operator.truediv(desc_form, 'VBN')
        described_0/VBN
        """
        self.set("pos", pos_tag)
        return self

    def __rshift__(self, other: Union["Form", str]) -> "Dependency":
        """Create a dependency between this form as governor, to
        the other as dependent. Adds the dependent to the children
        of this form. This is done by overloading ``operator.rshift()``
        (``a >> b``) to perform ``.append()`` upon ``Element`` of the xml
        library. Returns ``Dependency`` xxx

        >>> john = Form('John', 1) / 'NNP'
        >>> john
        John_1/NNP
        >>> loves = Form('loves', 2) / 'VRB'
        >>> loves
        loves_2/VRB
        >>> mary = Form('Mary', 3) / 'NNP'
        >>> mary
        Mary_3/NNP
        """
        other = Form(other) if isinstance(other, str) else other
        self.append(other)
        return Dependency(self, other)

    def get_dependencies(self, relation: str) -> List["Dependency"]:
        """Extract dependents of this form for the specified
        dependency relation.

        >>> john = Form('John', 1) / 'NNP'
        >>> john
        John_1/NNP
        >>> loves = Form('loves', 2) / 'VRB'
        >>> loves
        loves_2/VRB
        >>> mary = Form('Mary', 3) / 'NNP'
        >>> mary
        Mary_3/NNP
        """
        deps = self.findall('*[@relation="{}"]'.format(relation))
        return [Dependency(self, dep, relation) for dep in deps]

    def __str__(self) -> str:
        return (
            self.tag
            + "_"
            + self("form_id")
            + (("/" + self("pos")) if self("pos") else "")
        )

    __repr__ = __str__

    def full_str(self, include_relation=True) -> str:
        """Returns a string containing all features of the Form.
        The ID is attached to the text, and the relation is
        optionally suppressed.

        TODO: Make this test more meaningful. KJ couldn't get the ``desc_form.full_str()`` to equal the target.

        >>> f = Form
        >>> desc_form = f('described')
        >>> type(desc_form.full_str())
        <class 'str'>
        """
        excluded = ["form_id", "relation"] if not include_relation else ["form_id"]
        return "{0}_{1} [{2}]".format(
            self.tag,
            self("form_id"),
            ",".join(
                [
                    feature + "=" + self(feature)
                    for feature in self.attrib.keys()
                    if feature not in excluded
                ]
            ),
        )

    def __call__(self, feature: str) -> str:
        return self.get(feature)

    @staticmethod
    def to_form(word: Word) -> "Form":
        """Converts a ``cltk`` ``Word`` object to a ``Form``.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> cltk_nlp = NLP(language="lat")
        >>> doc = cltk_nlp.analyze(text=EXAMPLE_TEXTS["lat"])
        >>> f = Form.to_form(doc.words[0])
        >>> f.full_str()
        'Gallia_1 [lemma=aallius,pos=A1|grn1|casA|gen2|stAM,upos=NOUN,xpos=A1|grn1|casA|gen2|stAM,Case=Nom,Degree=Pos,Gender=Fem,Number=Sing]'
        """

        form = Form(word.string, form_id=word.index_token)
        form.set("lemma", word.lemma)
        form.set("pos", word.pos)
        form.set("upos", word.upos)
        form.set("xpos", word.xpos)

        if word.feats != "_":
            for f in word.feats.split("|"):
                feature = f.split("=")
                form.set(feature[0], feature[1])

        return form


class Dependency:
    """The relationship (or edge) between a hierarchical
    and subordinate Node.

    TODO: Explain this better.
    """

    def __init__(self, head: Form, dep: Form, relation: str = None) -> None:
        self.head = head
        self.dep = dep
        self.relation = relation

    def __str__(self) -> str:
        return "{0}({1}, {2})".format(
            self.relation if self.relation else "", self.head, self.dep
        )

    __repr__ = __str__

    def __or__(self, relation: str) -> "Dependency":
        self.relation = relation
        self.dep.set("relation", relation)
        return self


class DependencyTree(ElementTree):
    """The hierarchical tree representing the entirety of a parse."""

    def __init__(self, root: Form) -> None:
        root.set("relation", "root")

        ElementTree.__init__(self, root)

    def _get_deps(self, node: Form, deps: List[Dependency]) -> List[Dependency]:
        for child_node in list(node):
            deps = self._get_deps(child_node, deps)
            deps.extend(node.get_dependencies(child_node("relation")))
        return deps

    def get_dependencies(self) -> List[Dependency]:
        """Returns a list of all the dependency relations in the tree,
        generated by depth-first search.
        """
        deps = self._get_deps(self.getroot(), [])
        deps.append(Dependency(None, self.getroot(), "root"))
        return deps

    def _print_treelet(self, node: Form, indent: int, all_features: bool):
        edge = "└─ " if indent > 0 else ""
        node_str = node.full_str(False) if all_features else str(node)
        print(" " * indent + edge + node("relation") + " | " + node_str)

        for child_node in list(node):
            self._print_treelet(child_node, indent + 4, all_features)

    def print_tree(self, all_features: bool = True):
        """Prints a pretty-printed (indented) representation
        of the dependency tree. If ``all_features`` is ``True``, then
        each node is printed with its complete feature bundle.
        """
        self._print_treelet(self.getroot(), indent=0, all_features=all_features)

    @staticmethod
    def to_tree(sentence: List[Word]) -> "DependencyTree":
        """Factory method to create trees from sentence parses, i.e. lists of words.
        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> cltk_nlp = NLP(language="lat")
        >>> doc = cltk_nlp.analyze(text=EXAMPLE_TEXTS["lat"])
        >>> t = DependencyTree.to_tree(doc.words[:25])
        >>> t.findall(".")
        [divisa_4/L2]
        """

        forms = {}
        for word in sentence:
            forms[word.index_token] = Form.to_form(word)

        for word in sentence:
            if word.dependency_relation == "root":
                root = forms[word.index_token]
            else:
                gov = forms[word.governor]
                dep = forms[word.index_token]
                gov >> dep | word.dependency_relation

        return DependencyTree(root)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
