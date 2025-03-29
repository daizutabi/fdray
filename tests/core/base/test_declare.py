import pytest

from fdray.core.base import Declare, IdGenerator
from fdray.core.object import Sphere


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
    assert IdGenerator.generate(x) == "SPHERE"
    assert IdGenerator.generate(x) == "SPHERE_1"
    assert IdGenerator.generate(x) == "SPHERE_2"


def test_declare():
    x = Declare(Sphere(1, 1))
    y = Declare(Sphere(0, 2))
    assert str(x) == "SPHERE"
    assert str(y) == "SPHERE_1"
    assert Declare.declarations["SPHERE"] == x
    assert Declare.declarations["SPHERE_1"] == y
    assert x.to_str() == "#declare SPHERE = sphere { 1, 1 };"
    assert y.to_str() == "#declare SPHERE_1 = sphere { 0, 2 };"
    assert list(Declare.iter_strs()) == [x.to_str(), y.to_str()]
