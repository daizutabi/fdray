from fdray.color import Color
from fdray.transformable import Pigment


def test_pigment():
    x = Pigment(Color("red"))
    assert str(x) == "pigment { rgb <1, 0, 0> }"


def test_add():
    x = Pigment("abc").add("def")
    assert str(x) == "pigment {\n  abc\n  def\n}"


def test_add_list():
    x = Pigment("abc").add(["def", "ghi"])
    assert str(x) == "pigment {\n  abc\n  def\n  ghi\n}"


def test_add_varargs():
    x = Pigment("abc").add("def", ["ghi", "jkl"])
    assert str(x) == "pigment {\n  abc\n  def\n  ghi\n  jkl\n}"


def test_scale():
    x = Pigment("abc").scale(2)
    assert str(x) == "pigment {\n  abc\n  scale 2\n}"


def test_scale_vector():
    x = Pigment("abc").scale(2, 3, 4)
    assert str(x) == "pigment {\n  abc\n  scale <2, 3, 4>\n}"


def test_rotate():
    x = Pigment("abc").rotate(1, 2, 3)
    assert str(x) == "pigment {\n  abc\n  rotate <1, 2, 3>\n}"


def test_translate():
    x = Pigment("abc").translate(1, 2, 3)
    assert str(x) == "pigment {\n  abc\n  translate <1, 2, 3>\n}"
