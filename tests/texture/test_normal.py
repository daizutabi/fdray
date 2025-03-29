from fdray.core.texture import SlopeMap


def test_slope_map():
    x = SlopeMap((0, (0, 0)), (0.5, (1, 1)), (0.5, (1, -1)), (1, (0, -1)))
    assert str(x) == "slope_map { [0 <0, 0>] [0.5 <1, 1>] [0.5 <1, -1>] [1 <0, -1>] }"
