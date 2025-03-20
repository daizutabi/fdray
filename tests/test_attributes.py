def test_attribute_str():
    from fdray.attributes import Transform

    x = Transform(scale=0.5, rotate=(1, 2, 3))
    assert str(x) == "transform { scale 0.5 rotate <1, 2, 3> }"


def test_attribute_none():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3))
    assert str(x) == "light_source { <1, 2, 3> }"


def test_attribute_bool():
    from fdray.scene import Spotlight

    x = Spotlight((1, 2, 3), shadowless=True)
    assert str(x) == "light_source { <1, 2, 3> shadowless spotlight }"


def test_transform_scale():
    from fdray.attributes import Transform

    x = Transform(scale=(1, 2, 3))
    assert str(x) == "scale <1, 2, 3>"


def test_transform_rotate():
    from fdray.attributes import Transform

    x = Transform(rotate=(1, 2, 3))
    assert str(x) == "rotate <1, 2, 3>"


def test_transform_translate():
    from fdray.attributes import Transform

    x = Transform(translate=(1, 2, 3))
    assert str(x) == "translate <1, 2, 3>"
