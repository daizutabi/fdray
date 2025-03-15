from fdray.colors import Color


def test_color_str():
    color = Color("red", pigment=False)
    assert str(color) == "rgb <1, 0, 0>"


def test_color_str_pigment():
    color = Color("red", pigment=True)
    assert str(color) == "pigment { rgb <1, 0, 0> }"


def test_color_str_alpha():
    color = Color("green", 0.7, pigment=False)
    assert str(color) == "rgbt <0, 0.502, 0, 0.3>"


def test_color_float():
    color = Color([0.2, 0.3, 0.4], pigment=False)
    assert str(color) == "rgb <0.2, 0.3, 0.4>"


def test_color_float_alpha():
    color = Color([0.2, 0.3, 0.4], 0.2, pigment=False)
    assert str(color) == "rgbt <0.2, 0.3, 0.4, 0.8>"
