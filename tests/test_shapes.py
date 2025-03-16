def test_sphere():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1)
    assert str(x) == "sphere { <0, 0, 0>, 1 }"


def test_sphere_color_color():
    from fdray.colors import Color
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1, Color("red"))
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  pigment { rgb <1, 0, 0> }\n}"


def test_sphere_color_str():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1, "blue")
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  pigment { rgb <0, 0, 1> }\n}"


def test_sphere_color_rgba():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1, (0.1, 0.2, 0.3, 0.4))
    assert "rgbt <0.1, 0.2, 0.3, 0.6>" in str(x)


def test_sphere_attr_str():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1, "abc")
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  abc\n}"


def test_shape_add_str():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1) + "abc"
    assert isinstance(x, Sphere)
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  abc\n}"


def test_shape_add_shape():
    from fdray.shapes import Sphere, Union

    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2)
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 2
    s = "union {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n}"
    assert str(x) == s


def test_shape_sub():
    from fdray.shapes import Difference, Sphere

    x = Sphere((0, 0, 0), 1) - Sphere((1, 0, 0), 2)
    assert isinstance(x, Difference)
    assert not x.args
    assert len(x.attrs) == 2
    s = "difference {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n}"
    assert str(x) == s


def test_shape_mul():
    from fdray.shapes import Intersection, Sphere

    x = Sphere((0, 0, 0), 1) * Sphere((1, 0, 0), 2)
    assert isinstance(x, Intersection)
    assert not x.args
    assert len(x.attrs) == 2
    s = "intersection {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n}"
    assert str(x) == s


def test_shape_or():
    from fdray.shapes import Merge, Sphere

    x = Sphere((0, 0, 0), 1) | Sphere((1, 0, 0), 2)
    assert isinstance(x, Merge)
    assert not x.args
    assert len(x.attrs) == 2
    s = "merge {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n}"
    assert str(x) == s


def test_union_add_str():
    from fdray.shapes import Sphere, Union

    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2) + "abc"
    assert isinstance(x, Union)
    s = "union {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n  abc\n}"
    assert str(x) == s


def test_union_add_shape():
    from fdray.shapes import Sphere, Union

    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2) + Sphere((0, 1, 0), 3)
    assert isinstance(x, Union)
    s = "union {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n"
    s += "  sphere { <0, 1, 0>, 3 }\n}"
    assert str(x) == s


def test_intersection_mul_shape():
    from fdray.shapes import Intersection, Sphere

    x = Sphere((0, 0, 0), 1) * Sphere((1, 0, 0), 2) * Sphere((0, 1, 0), 3)
    assert isinstance(x, Intersection)
    s = "intersection {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n"
    s += "  sphere { <0, 1, 0>, 3 }\n}"
    assert str(x) == s


def test_difference_sub_shape():
    from fdray.shapes import Difference, Sphere

    x = Sphere((0, 0, 0), 1) - Sphere((1, 0, 0), 2) - Sphere((0, 1, 0), 3)
    assert isinstance(x, Difference)
    s = "difference {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n"
    s += "  sphere { <0, 1, 0>, 3 }\n}"
    assert str(x) == s


def test_merge_or_shape():
    from fdray.shapes import Merge, Sphere

    x = Sphere((0, 0, 0), 1) | Sphere((1, 0, 0), 2) | Sphere((0, 1, 0), 3)
    assert isinstance(x, Merge)
    s = "merge {\n  sphere { <0, 0, 0>, 1 }\n  sphere { <1, 0, 0>, 2 }\n"
    s += "  sphere { <0, 1, 0>, 3 }\n}"
    assert str(x) == s
