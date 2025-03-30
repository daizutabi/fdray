import pytest

from fdray.core.color import Color
from fdray.core.object import Sphere
from fdray.data.field import Union


@pytest.fixture(scope="module")
def region_1d():
    region = [0, 1, 1, 2, 2]
    return Union.from_region(region)


def test_region_1d(region_1d: Union):
    x = str(region_1d)
    assert "rgb <0.122, 0.467, 0.706> } translate <-2, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> } translate <-1, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> } translate <0, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> } translate <1, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> } translate <2, 0, 0>" in x


@pytest.fixture(scope="module")
def region_2d():
    region = [[0, 0], [1, 1], [1, 2], [2, 2]]
    obj = Sphere((0, 0, 0), 1)
    attrs = {1: Color("red"), 2: Color("blue")}
    return Union.from_region(region, obj, spacing=2, mapping=attrs)


def test_region_2d(region_2d: Union):
    x = str(region_2d)
    assert "pigment { rgb <1, 0, 0> } translate <-1, -1, 0>" in x
    assert "pigment { rgb <1, 0, 0> } translate <-1, 1, 0>" in x
    assert "pigment { rgb <1, 0, 0> } translate <1, -1, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <1, 1, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <3, -1, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <3, 1, 0>" in x


@pytest.fixture(scope="module")
def region_3d():
    region = [[[0, 0], [1, 2]], [[1, 0], [0, 1]]]
    obj = Sphere((0, 0, 0), 1)
    attrs = {1: Color("red"), 2: Color("blue")}
    return Union.from_region(region, obj, spacing=(2, 3, 4), mapping=attrs)


def test_region_3d(region_3d: Union):
    x = str(region_3d)
    assert "pigment { rgb <1, 0, 0> } translate <-1, 1.5, -2>" in x
    assert "pigment { rgb <1, 0, 0> } translate <1, -1.5, -2>" in x
    assert "pigment { rgb <1, 0, 0> } translate <1, 1.5, 2>" in x
    assert "pigment { rgb <0, 0, 1> } translate <-1, 1.5, 2>" in x
