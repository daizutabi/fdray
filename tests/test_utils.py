from fdray.utils import convert


def test_convert_tuple_2():
    assert convert((1, 2)) == "1 2"


def test_convert_tuple_3():
    assert convert((1, 2, 3)) == "<1, 2, 3>"


def test_convert_str():
    assert convert("test") == "test"
