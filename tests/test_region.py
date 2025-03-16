import numpy as np
import pytest

from fdray.region import Region
from fdray.shapes import Sphere


@pytest.fixture(scope="module")
def region_1d():
    region = np.array([0, 1, 1, 2, 2])
    return Region(region)


def test_region_1d(region_1d):
    print(str(region_1d))
    assert 0
