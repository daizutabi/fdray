import pytest

from fdray.core.camera import Camera
from fdray.core.color import Color
from fdray.core.light_source import LightSource, Spotlight


def test_light_source_color_color():
    x = LightSource((1, 2, 3), Color("red"), from_camera=False)
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> }"


def test_light_source_color_str():
    x = LightSource((1, 2, 3), "blue", from_camera=False)
    assert str(x) == "light_source { <1, 2, 3> color rgb <0, 0, 1> }"


def test_light_source_color_tuple():
    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3), from_camera=False)
    assert "rgb <0.1, 0.2, 0.3>" in str(x)


def test_light_source_camera_error():
    x = LightSource(0, (0.1, 0.2, 0.3))
    with pytest.raises(ValueError, match="Cannot convert"):
        str(x)


def test_light_source_to_str_camera():
    camera = Camera(10, 20, distance=10)
    x = LightSource(0, (0.1, 0.2, 0.3))
    assert x.to_str(camera).startswith("light_source { <9.2542, 1.6318, 3.4202>")


def test_light_source_to_str_camera_iterable():
    camera = Camera(10, 20, distance=10)
    x = LightSource((0.4, 10, 20), (0.1, 0.2, 0.3))
    assert x.to_str(camera).startswith("light_source { <5.4301, 0.71625, 2.6862>")


def test_light_source_to_str_without_camera():
    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3), from_camera=False)
    assert x.to_str(None) == "light_source { <1, 2, 3> color rgb <0.1, 0.2, 0.3> }"


def test_light_source_to_str_absolute():
    camera = Camera(10, 20, distance=10)
    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3), from_camera=False)
    assert x.to_str(camera) == "light_source { <1, 2, 3> color rgb <0.1, 0.2, 0.3> }"


def test_light_source_to_str_str():
    camera = Camera(10, 20, distance=10)
    x = LightSource("abc", (0.1, 0.2, 0.3))
    assert x.to_str(camera) == "light_source { abc color rgb <0.1, 0.2, 0.3> }"


def test_light_source_to_str_camera_error():
    x = LightSource(0, (0.1, 0.2, 0.3))
    with pytest.raises(ValueError, match="Camera is required"):
        x.to_str(None)


def test_spotlight():
    x = Spotlight((1, 2, 3), "red", from_camera=False)
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> spotlight }"
