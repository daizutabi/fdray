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
