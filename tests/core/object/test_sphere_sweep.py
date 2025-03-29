import pytest

from fdray.core.color import Color
from fdray.core.object import Curve, Polyline, SphereSweep


@pytest.fixture(scope="module", params=["linear_spline", "b_spline", "cubic_spline"])
def kind(request: pytest.FixtureRequest):
    return request.param


def test_iter(kind):
    s = SphereSweep(kind, [(0, 0, 0), (1, 0, 0)], 1, Color("red"))
    it = iter(s)
    assert next(it) == f"{kind}, 2"
    assert next(it) == "<0, 0, 0>, 1, <1, 0, 0>, 1"
    assert next(it) == "pigment { rgb <1, 0, 0> }"


def test_str(kind):
    s = SphereSweep(kind, [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)], 1)
    assert str(s).startswith(f"sphere_sweep {{ {kind}, 4")


def test_str_none():
    s = SphereSweep("linear_spline", [], 1)
    assert str(s) == ""


def test_str_one():
    s = SphereSweep("linear_spline", [(0, 0, 0)], 1)
    assert str(s) == "sphere { <0, 0, 0>, 1 }"


def test_str_two(kind):
    s = SphereSweep(kind, [(0, 0, 0), (1, 0, 0)], 1)
    assert str(s).startswith("sphere_sweep { linear_spline, 2")


def test_polyline():
    s = Polyline([(0, 0, 0), (1, 0, 0)], 1)
    assert str(s).startswith("sphere_sweep { linear_spline, 2")


def test_polyline_from_coordinates():
    s = Polyline.from_coordinates([0, 1], [0, 2], [0, 3], [1, 2])
    s = str(s)
    assert s.startswith("sphere_sweep { linear_spline, 2")
    assert s.endswith(" <0, 0, 0>, 1, <1, 2, 3>, 2 }")


def test_curve():
    s = Curve.from_coordinates([0, 1, 2, 3], [0, 2, 0, 2], [5, 4, 3, 2], [1, 2, 3, 4])
    s = str(s)
    assert s.startswith("sphere_sweep { cubic_spline, 6")
    assert s.endswith(" <3, 2, 2>, 4, <4, 4, 1>, 4 }")


def test_curve_one():
    s = Curve([(1, 1, 1)], 1)
    assert str(s) == "sphere { <1, 1, 1>, 1 }"


def test_curve_rotate():
    s = Curve.from_coordinates([0, 1], [0, 2], [0, 3], 1)
    s = str(s.rotate(10, 20, 30))
    assert s.endswith("<2, 4, 6>, 1 rotate <10, 20, 30> }")
