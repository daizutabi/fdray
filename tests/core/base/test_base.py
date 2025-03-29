from fdray.core.base import Attribute, Element


def test_attribute_str():
    x = Attribute("x", 1)
    assert str(x) == "x 1"


def test_attribute_none():
    x = Attribute("x", None)
    assert str(x) == ""


def test_attribute_false():
    x = Attribute("x", False)
    assert str(x) == ""


def test_attribute_true():
    x = Attribute("x", True)
    assert str(x) == "x"


def test_element_str():
    x = Element("x")
    assert str(x) == "element { x }"


def test_element_kwargs():
    x = Element(x=1, y=[1, 2, 3])
    assert str(x) == "element { x 1 y <1, 2, 3> }"


def test_element_repr_html():
    x = Element(x=1, y=[1, 2, 3])
    assert '<div class="highlight-ipynb">' in x._repr_html_()


class ElementArgs(Element):
    nargs = 2


def test_element_kwargs_nargs():
    x = ElementArgs("a", "b", "c", "d", x=1, y=[1, 2, 3])
    assert str(x) == "element_args { a, b c d x 1 y <1, 2, 3> }"


def test_element_add():
    x = ElementArgs("a", "b", "c").add("d", x=1, y=[1, 2, 3])
    assert str(x) == "element_args { a, b c d x 1 y <1, 2, 3> }"


def test_element_add_list():
    x = ElementArgs("a", "b", "c", x=False).add(["d", "e"])
    assert str(x) == "element_args { a, b c d e }"


def test_element_add_override():
    x = ElementArgs("a", "b", x=1, y=2).add(x=3)
    assert str(x) == "element_args { a, b y 2 x 3 }"
