import pytest

from fdray.colors import Background, Color


def test_color_str():
    color = Color("red", pigment=False)
    assert str(color) == "rgb <1, 0, 0>"


def test_color_str_pigment():
    color = Color("red", pigment=True)
    assert str(color) == "pigment { rgb <1, 0, 0> }"


def test_color_str_alpha():
    color = Color("green", 0.7, pigment=False)
    assert str(color) == "rgbt <0, 0.502, 0, 0.3>"


def test_color_str_rgba():
    color = Color("#10203040", pigment=False)
    assert str(color) == "rgbt <0.0627, 0.125, 0.188, 0.749>"


def test_color_float():
    color = Color((0.2, 0.3, 0.4), pigment=True)
    assert str(color) == "pigment { rgb <0.2, 0.3, 0.4> }"


def test_color_float_alpha():
    color = Color((0.2, 0.3, 0.4), 0.2, pigment=False)
    assert str(color) == "rgbt <0.2, 0.3, 0.4, 0.8>"


def test_color_float_rgba():
    color = Color((0.2, 0.3, 0.4, 0.6), pigment=True)
    assert str(color) == "pigment { rgbt <0.2, 0.3, 0.4, 0.4> }"


def test_color_str_error():
    with pytest.raises(ValueError):
        Color("invalid")


def test_color_float_error():
    with pytest.raises(ValueError):
        Color((0.2, 0.3, 0.4, 0.6, 0.8), pigment=True)  # type: ignore


def test_background_str():
    background = Background("blue")
    assert str(background) == "background { rgb <0, 0, 1> }"


@pytest.mark.parametrize(
    "color",
    [
        (1.1, 0, 0),
        (0, 0, 0, 1.1),
        (0, 0, 0, 1.1, 1.1),
        (0, 0, 0, 1.1, 1.1, 1.1),
    ],
)
def test_color_validate(color):
    with pytest.raises(ValueError):
        Color(color)
