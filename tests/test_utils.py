from fdray.utils.string import convert


def test_convert_tuple_2():
    assert convert((1, 2)) == "1 2"


def test_convert_tuple_3():
    assert convert((1, 2, 3)) == "<1, 2, 3>"


def test_convert_tuple_zero():
    assert convert((1e-6, 1.2345678e-5, 0)) == "<0, 1.2346e-05, 0>"


def test_convert_str():
    assert convert("test") == "test"
