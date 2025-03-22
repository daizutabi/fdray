import textwrap

from fdray.color import Color
from fdray.shapes import Difference, Intersection, Merge, Sphere, Union


def test_args():
    x = Sphere((0, 0, 0), 1)
    assert x.args == [(0, 0, 0), 1]
    assert x.attrs == []


def test_attrs():
    x = Sphere((0, 0, 0), 1, "a", "b")
    assert x.args == [(0, 0, 0), 1]
    assert x.attrs == ["a", "b"]


def test_shape_add_shape():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a + b
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_shape_sub():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a - b
    assert isinstance(x, Difference)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_shape_mul():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a * b
    assert isinstance(x, Intersection)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_shape_or():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a | b
    assert isinstance(x, Merge)
    assert not x.args
    assert len(x.attrs) == 2
    assert x.attrs[0] is a
    assert x.attrs[1] is b


def test_union_add_str():
    a, b = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2)
    x = a + b + "abc"
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] == "abc"


def test_union_add_shape():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a + b + c
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_intersection_mul_shape():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a * b * c
    assert isinstance(x, Intersection)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_difference_sub_shape():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a - b - c
    assert isinstance(x, Difference)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_merge_or_shape():
    a, b, c = Sphere((0, 0, 0), 1), Sphere((1, 0, 0), 2), Sphere((0, 1, 0), 3)
    x = a | b | c
    assert isinstance(x, Merge)
    assert not x.args
    assert len(x.attrs) == 3
    assert x.attrs[0] is a
    assert x.attrs[1] is b
    assert x.attrs[2] is c


def test_csg_transform():
    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2)
    x = x.scale(1, 2, 3).rotate(2, 3, 4).translate(3, 4, 5)
    assert isinstance(x, Union)
    assert not x.args
    assert len(x.attrs) == 5
    assert x.attrs[2].scale == (1, 2, 3)
    assert x.attrs[3].rotate == (2, 3, 4)
    assert x.attrs[4].translate == (3, 4, 5)


def test_box():
    from fdray.shapes import Box

    x = Box((0, 0, 0), (1, 1, 1), "a")
    assert str(x) == "box { <0, 0, 0>, <1, 1, 1> a }"


def test_cone():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2)
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 }"


def test_cone_open_kwarg():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, open=True)
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 open }"


def test_cone_open_arg():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, "open")
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 open }"


def test_cylinder():
    from fdray.shapes import Cylinder

    x = Cylinder((0, 0, 0), (1, 0, 0), 1)
    assert str(x) == "cylinder { <0, 0, 0>, <1, 0, 0>, 1 }"


def test_plane():
    from fdray.shapes import Plane

    x = Plane((0, 0, 1), 1)
    assert str(x) == "plane { <0, 0, 1>, 1 }"


def test_cuboid():
    from fdray.shapes import Cuboid

    x = Cuboid((1, 2, 3), (1, 2, 3))
    assert str(x) == "box { <0.5, 1, 1.5>, <1.5, 3, 4.5> }"


def test_cuboid_add_str():
    from fdray.shapes import Cuboid

    x = Cuboid((1, 2, 3), (1, 2, 3)) + "abc"
    assert str(x) == "box { <0.5, 1, 1.5>, <1.5, 3, 4.5> abc }"


def test_cube():
    from fdray.shapes import Cube

    x = Cube((1, 2, 3), 1)
    assert str(x) == "box { <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5> }"


def test_cube_add_str():
    from fdray.shapes import Cube

    x = Cube((1, 2, 3), 1) + "abc"
    assert str(x) == "box { <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5> abc }"


def test_shape_group():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 1))
    assert str(x) == "union { sphere { <1, 2, 3>, 1 } sphere { <1, 2, 3>, 1 } }"


def test_shape_group_add_shape():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x + Sphere((1, 2, 3), 3)
    s = "union { sphere { <1, 2, 3>, 1 } sphere { <1, 2, 3>, 2 } "
    s += "sphere { <1, 2, 3>, 3 } }"
    assert str(x) == s


def test_shape_group_add_str():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x + "abc"
    s = "union { sphere { <1, 2, 3>, 1 } sphere { <1, 2, 3>, 2 } abc }"
    assert str(x) == s


def test_shape_group_add_method():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x.add("abc", "def")
    s = "union { sphere { <1, 2, 3>, 1 } sphere { <1, 2, 3>, 2 } abc def }"
    assert str(x) == s


def test_shape_group_scale():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.scale(2, 3, 4)
    s = "union { sphere { <1, 2, 3>, 1 } scale <2, 3, 4> }"
    assert str(x) == s


def test_shape_group_rotate():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.rotate(1, 2, 3)
    s = "union { sphere { <1, 2, 3>, 1 } rotate <1, 2, 3> }"
    assert str(x) == s


def test_shape_group_translate():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.translate(1, 2, 3)
    s = "union { sphere { <1, 2, 3>, 1 } translate <1, 2, 3> }"
    assert str(x) == s
