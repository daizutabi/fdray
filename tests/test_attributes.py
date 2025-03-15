def test_attribute_str():
    from fdray.attributes import Transform

    x = Transform(scale=0.5)
    assert str(x) == "transform { scale 0.5 }"


def test_attribute_missing():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3))
    assert str(x) == "light_source { <1, 2, 3> }"


def test_attribute_bool():
    from fdray.scene import Spotlight

    x = Spotlight((1, 2, 3), shadowless=True)
    assert str(x) == "light_source { <1, 2, 3> shadowless spotlight }"
