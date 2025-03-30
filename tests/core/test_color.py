import numpy as np

from fdray.core.color import Background, Color, ColorMap


def test_color_name():
    color = Color("Red")
    assert str(color) == "Red"


def test_color_name_filter():
    color = Color("Red", filter=0.3)
    assert str(color) == "Red filter 0.3"


def test_color_name_transmit():
    color = Color("Red", transmit=0.3)
    assert str(color) == "Red transmit 0.3"


def test_color_name_filter_transmit():
    color = Color("Red", filter=0.3, transmit=0.4)
    assert str(color) == "Red filter 0.3 transmit 0.4"


def test_color_str_include_color_false():
    color = Color("red")
    assert str(color) == "rgb <1, 0, 0>"


def test_color_str_alpha():
    color = Color("green", 0.7)
    assert str(color) == "rgbt <0, 0.502, 0, 0.3>"


def test_color_str_rgba():
    color = Color("#10203040", transmit=0.7)
    assert str(color) == "rgbt <0.0627, 0.125, 0.188, 0.749>"


def test_color_str_transmit():
    color = Color("#102030", transmit=0.7)
    assert str(color) == "rgbt <0.0627, 0.125, 0.188, 0.7>"


def test_color_str_filter_transmit():
    color = Color("#102030", filter=0.2, transmit=0.8)
    assert str(color) == "rgbft <0.0627, 0.125, 0.188, 0.2, 0.8>"


def test_color_tuple():
    color = Color((0.2, 0.3, 0.4))
    assert str(color) == "rgb <0.2, 0.3, 0.4>"


def test_color_tuple_alpha():
    color = Color((0.2, 0.3, 0.4), alpha=0.2)
    assert str(color) == "rgbt <0.2, 0.3, 0.4, 0.8>"


def test_color_tuple_filter():
    color = Color((0.2, 0.3, 0.4), filter=0.2)
    assert str(color) == "rgbf <0.2, 0.3, 0.4, 0.2>"


def test_color_tuple_rgba():
    color = Color((0.2, 0.3, 0.4, 0.2))
    assert str(color) == "rgbt <0.2, 0.3, 0.4, 0.8>"


def test_color_color():
    color = Color((0.2, 0.3, 0.4), filter=0.2, transmit=0.8)
    color = Color(color, filter=0.3, transmit=0.1)
    assert str(color) == "rgbft <0.2, 0.3, 0.4, 0.3, 0.1>"


def test_background_str():
    background = Background("blue")
    assert str(background) == "background { rgb <0, 0, 1> }"


def test_color_map_str():
    color_map = ColorMap((0, Color("red")), (1, "Blue"))
    assert str(color_map) == "color_map { [0 rgb <1, 0, 0>] [1 Blue] }"


def test_from_direction():
    c = Color.from_direction([1, 2, 3])
    np.testing.assert_allclose(
        (c.red, c.green, c.blue),
        (0.9699322, 0.99017757, 0.63654272),
    )
