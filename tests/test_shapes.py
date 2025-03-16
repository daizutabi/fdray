import textwrap


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

    x = Sphere((0, 0, 0), 1) | Sphere((1, 0, 0), 2, "red") | Sphere((0, 1, 0), 3)
    assert isinstance(x, Merge)
    s = "merge {\n  sphere { <0, 0, 0>, 1 }\n"
    s += "  sphere {\n    <1, 0, 0>, 2\n    pigment { rgb <1, 0, 0> }\n  }\n"
    s += "  sphere { <0, 1, 0>, 3 }\n}"
    assert str(x) == s


def test_add():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).add("abc")
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  abc\n}"


def test_add_list():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).add(["abc", "def"])
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  abc\n  def\n}"


def test_add_varargs():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).add("abc", ["def", "ghi"])
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  abc\n  def\n  ghi\n}"


def test_scale():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).scale(2)
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  scale 2\n}"


def test_scale_vector():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).scale(2, 3, 4)
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  scale <2, 3, 4>\n}"


def test_rotate():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).rotate(1, 2, 3)
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  rotate <1, 2, 3>\n}"


def test_translate():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1).translate(1, 2, 3)
    assert str(x) == "sphere {\n  <0, 0, 0>, 1\n  translate <1, 2, 3>\n}"


def test_csg_transform():
    from fdray.shapes import Sphere

    x = Sphere((0, 0, 0), 1) + Sphere((1, 0, 0), 2)
    x = x.scale(1, 2, 3).rotate(2, 3, 4).translate(1, 2, 3)
    y = textwrap.dedent("""\
    union {
      sphere { <0, 0, 0>, 1 }
      sphere { <1, 0, 0>, 2 }
      scale <1, 2, 3>
      rotate <2, 3, 4>
      translate <1, 2, 3>
    }""")
    assert str(x) == y


def test_box():
    from fdray.shapes import Box

    x = Box((0, 0, 0), (1, 1, 1))
    assert str(x) == "box { <0, 0, 0>, <1, 1, 1> }"


def test_cone():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2)
    assert str(x) == "cone { <0, 0, 0>, 1, <1, 0, 0>, 2 }"


def test_cone_open_kwarg():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, open=True)
    assert str(x) == "cone {\n  <0, 0, 0>, 1, <1, 0, 0>, 2\n  open\n}"


def test_cone_open_arg():
    from fdray.shapes import Cone

    x = Cone((0, 0, 0), 1, (1, 0, 0), 2, "open")
    assert str(x) == "cone {\n  <0, 0, 0>, 1, <1, 0, 0>, 2\n  open\n}"


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
    assert str(x) == "box { <0.5, 1.0, 1.5>, <1.5, 3.0, 4.5> }"


def test_cuboid_add_str():
    from fdray.shapes import Cuboid

    x = Cuboid((1, 2, 3), (1, 2, 3)) + "abc"
    assert str(x) == "box {\n  <0.5, 1.0, 1.5>, <1.5, 3.0, 4.5>\n  abc\n}"


def test_cube():
    from fdray.shapes import Cube

    x = Cube((1, 2, 3), 1)
    assert str(x) == "box { <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5> }"


def test_cube_add_str():
    from fdray.shapes import Cube

    x = Cube((1, 2, 3), 1) + "abc"
    assert str(x) == "box {\n  <0.5, 1.5, 2.5>, <1.5, 2.5, 3.5>\n  abc\n}"


def test_shape_group():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 1))
    assert str(x) == "union {\n  sphere { <1, 2, 3>, 1 }\n  sphere { <1, 2, 3>, 1 }\n}"


def test_shape_group_add_shape():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x + Sphere((1, 2, 3), 3)
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  sphere { <1, 2, 3>, 2 }\n"
    s += "  sphere { <1, 2, 3>, 3 }\n}"
    assert str(x) == s


def test_shape_group_add_str():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x + "abc"
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  sphere { <1, 2, 3>, 2 }\n  abc\n}"
    assert str(x) == s


def test_shape_group_add_method():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1), Sphere((1, 2, 3), 2))
    x = x.add("abc", "def")
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  sphere { <1, 2, 3>, 2 }\n  abc\n  def\n}"
    assert str(x) == s


def test_shape_group_scale():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.scale(2, 3, 4)
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  scale <2, 3, 4>\n}"
    assert str(x) == s


def test_shape_group_rotate():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.rotate(1, 2, 3)
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  rotate <1, 2, 3>\n}"
    assert str(x) == s


def test_shape_group_translate():
    from fdray.shapes import ShapeGroup, Sphere

    x = ShapeGroup(Sphere((1, 2, 3), 1))
    x = x.translate(1, 2, 3)
    s = "union {\n  sphere { <1, 2, 3>, 1 }\n  translate <1, 2, 3>\n}"
    assert str(x) == s
