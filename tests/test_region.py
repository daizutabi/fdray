import numpy as np
import pytest

from fdray.region import Region


@pytest.fixture(scope="module")
def region_1d():
    region = np.array([0, 1, 1, 2, 2])
    return Region(region)


def test_region_1d(region_1d: Region):
    x = str(region_1d)
    assert "rgb <0.122, 0.467, 0.706> }\n    translate <0, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> }\n    translate <1, 0, 0>" in x
    assert "rgb <1, 0.498, 0.0549> }\n    translate <2, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> }\n    translate <3, 0, 0>" in x
    assert "rgb <0.173, 0.627, 0.173> }\n    translate <4, 0, 0>" in x
