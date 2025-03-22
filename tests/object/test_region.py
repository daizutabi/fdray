import numpy as np
import pytest

from fdray.color import Color
from fdray.object import Sphere, Union


@pytest.fixture(scope="module")
def region_1d():
    region = np.array([0, 1, 1, 2, 2])
    return Union.from_region(region)


def test_region_1d(region_1d: Union):
    x = str(region_1d)
    assert "rgb <0.122, 0.467, 0.706> } translate <0, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> } translate <1, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> } translate <2, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> } translate <3, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> } translate <4, 0, 0>" in x


@pytest.fixture(scope="module")
def region_2d():
    region = np.array([[0, 0], [1, 1], [1, 2], [2, 2]])
    shape = Sphere((0, 0, 0), 1)
    attrs = {1: Color("red"), 2: Color("blue")}
    return Union.from_region(region, shape, spacing=2, attrs=attrs)


def test_region_2d(region_2d: Union):
    x = str(region_2d)
    assert "pigment { rgb <1, 0, 0> } translate <2, 0, 0>" in x
    assert "pigment { rgb <1, 0, 0> } translate <2, 2, 0>" in x
    assert "pigment { rgb <1, 0, 0> } translate <4, 0, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <4, 2, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <6, 0, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <6, 2, 0>" in x


@pytest.fixture(scope="module")
def region_3d():
    region = np.array([[[0, 0], [1, 2]], [[1, 0], [0, 1]]])
    shape = Sphere((0, 0, 0), 1)
    attrs = {1: Color("red"), 2: Color("blue")}
    return Union.from_region(region, shape, spacing=(2, 3, 4), attrs=attrs)


def test_region_3d(region_3d: Union):
    x = str(region_3d)
    assert "pigment { rgb <1, 0, 0> } translate <0, 3, 0>" in x
    assert "pigment { rgb <0, 0, 1> } translate <0, 3, 4>" in x
    assert "pigment { rgb <1, 0, 0> } translate <2, 0, 0>" in x
    assert "pigment { rgb <1, 0, 0> } translate <2, 3, 4>" in x


def test_region_error():
    with pytest.raises(ValueError, match="Spacing must have 1 components"):
        Union.from_region([1, 2, 3], spacing=(1, 2))
