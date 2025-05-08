import numpy as np
import pytest

from fdray.core.color import Color
from fdray.core.texture import Pigment, PigmentMap


def test_pigment():
    pigment = Pigment(Color("red"))
    assert str(pigment) == "pigment { rgb <1, 0, 0> }"


def test_pigment_pattern():
    pigment = Pigment("checker", Color("red"), Color("blue"))
    x = "pigment { checker rgb <1, 0, 0> rgb <0, 0, 1> }"
    assert str(pigment) == x


def test_pigment_map_tuple():
    pigment = PigmentMap((0, Pigment("Red")), (0.5, Color("blue")), (1, "Green"))
    assert str(pigment) == "pigment_map { [0 Red] [0.5 rgb <0, 0, 1>] [1 Green] }"


def test_pigment_map_dict():
    pigment = PigmentMap({0: Pigment("Red"), 0.5: Color("blue"), 1: "Green"})
    assert str(pigment) == "pigment_map { [0 Red] [0.5 rgb <0, 0, 1>] [1 Green] }"


def test_pigment_uv_mapping_str():
    data = "a.png"
    x = str(Pigment.uv_mapping(data))
    assert x.startswith("pigment { uv_mapping image_map { png ")
    assert x.endswith('"a.png" interpolate 2 } }')


def test_pigment_uv_mapping_array():
    data = np.array([[0, 0], [255, 255]], dtype=np.uint8)
    x = str(Pigment.uv_mapping(data))
    assert x.startswith("pigment { uv_mapping image_map { png ")
    assert x.endswith('.png" interpolate 2 } }')


def test_pigment_uv_mapping_error():
    with pytest.raises(ValueError, match="interpolate must be between 2 and 4"):
        Pigment.uv_mapping("a.png", interpolate=1)
