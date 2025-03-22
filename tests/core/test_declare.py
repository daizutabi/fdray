import pytest

from fdray.core import Declare, IdGenerator
from fdray.object import Sphere


@pytest.fixture(autouse=True)
def clear():
    Declare.clear()
    yield
    Declare.clear()


def test_id_generator():
    assert IdGenerator.generate("x", "x") == "x"
    assert IdGenerator.generate("x", "x") == "x_1"
    assert IdGenerator.generate("x", "x") == "x_2"


def test_id_generator_clear():
    assert IdGenerator.generate("x", "x") == "x"
    assert IdGenerator.generate("x", "x") == "x_1"
    assert IdGenerator.generate("x", "x") == "x_2"


def test_id_generator_class():
    x = Sphere(1, 1)
    assert IdGenerator.generate("x", "x") == "x"
    assert IdGenerator.generate("x", "x") == "x_1"
    assert IdGenerator.generate("x", "x") == "x_2"
