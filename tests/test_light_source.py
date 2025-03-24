def test_light_source_color_color():
    from fdray.color import Color
    from fdray.light_source import LightSource

    x = LightSource((1, 2, 3), Color("red"))
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> }"


def test_light_source_color_str():
    from fdray.light_source import LightSource

    x = LightSource((1, 2, 3), "blue")
    assert str(x) == "light_source { <1, 2, 3> color rgb <0, 0, 1> }"


def test_light_source_color_tuple():
    from fdray.light_source import LightSource

    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3))
    assert "rgb <0.1, 0.2, 0.3>" in str(x)


def test_spotlight():
    from fdray.light_source import Spotlight

    x = Spotlight((1, 2, 3), "red")
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> spotlight }"
