from dataclasses import dataclass

import pytest

from fdray.core.base import Descriptor


def test_descriptor_missing():
    @dataclass
    class C(Descriptor):
        x: int
        y: int

    x = C(1, 2)
    assert str(x) == "c { 1 2 }"


def test_descriptor_default():
    @dataclass
    class C(Descriptor):
        x: int = 2
        y: int = 3

    x = C(0)
    assert str(x) == "c { x 0 y 3 }"


@pytest.mark.parametrize(
    ("y", "expected"),
    [(True, "c { x 0 y }"), (False, "c { x 0 }")],
)
def test_descriptor_bool(y: bool, expected: str):
    @dataclass
    class C(Descriptor):
        x: int = 2
        y: bool = False

    x = C(0, y=y)
    assert str(x) == expected


def test_descriptor_set():
    @dataclass
    class C(Descriptor):
        x: int = 2

    x = C(0)
    with x.set(x=1):
        assert str(x) == "c { x 1 }"
    assert str(x) == "c { x 0 }"
