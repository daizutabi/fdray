from fdray.color import Background, Color


def test_color_name():
    color = Color("Red")
    assert str(color) == "color Red"


def test_color_name_filter():
    color = Color("Red", filter=0.3)
    assert str(color) == "color Red filter 0.3"


def test_color_name_transmit():
    color = Color("Red", transmit=0.3)
    assert str(color) == "color Red transmit 0.3"


def test_color_name_filter_transmit():
    color = Color("Red", filter=0.3, transmit=0.4)
    assert str(color) == "color Red filter 0.3 transmit 0.4"


def test_color_str_include_color_false():
    color = Color("red", include_color=False)
    assert str(color) == "rgb <1, 0, 0>"


def test_color_str_filter():
    color = Color("green", 0.7)
    assert str(color) == "color rgbf <0, 0.502, 0, 0.7>"


def test_color_str_transmit():
    color = Color("#102030", transmit=0.7)
    assert str(color) == "color rgbt <0.0627, 0.125, 0.188, 0.7>"


def test_color_str_filter_transmit():
    color = Color("#102030", filter=0.2, transmit=0.8)
    assert str(color) == "color rgbft <0.0627, 0.125, 0.188, 0.2, 0.8>"


def test_color_tuple():
    color = Color((0.2, 0.3, 0.4))
    assert str(color) == "color rgb <0.2, 0.3, 0.4>"


def test_color_color():
    color = Color((0.2, 0.3, 0.4), filter=0.2, transmit=0.8)
    color = Color(color, filter=0.3, transmit=0.1)
    assert str(color) == "color rgbft <0.2, 0.3, 0.4, 0.3, 0.1>"


def test_color_tuple_alpha():
    color = Color((0.2, 0.3, 0.4), alpha=0.2)
    assert str(color) == "color rgbt <0.2, 0.3, 0.4, 0.8>"


def test_background_str():
    background = Background("blue")
    assert str(background) == "background { color rgb <0, 0, 1> }"
