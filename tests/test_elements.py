import textwrap


def test_element_init():
    from fdray.elements import Element

    e = Element("a", [1, 2, 3], b=4, c=[5, 6, 7])
    assert e.args == ["a", [1, 2, 3], {"b": 4, "c": [5, 6, 7]}]


def test_camera_render():
    from fdray.elements import Camera

    e = Camera(location=[0, 2, -3], look_at=(0, 1, 2))
    x = "camera { location <0, 2, -3> look_at <0, 1, 2> }"
    assert str(e) == x


def test_sphere_render():
    from fdray.elements import Pigment, Sphere, Texture

    e = Sphere([0, 1, 2], 2, Texture(Pigment(color="Yellow")))
    x = """\
    sphere { <0, 1, 2>
    2
    texture { pigment { color Yellow } } }"""
    assert str(e) == textwrap.dedent(x)
