import numpy as np
import pytest


def test_colormap():
    from fdray.data.color import get_colormap

    colormap = get_colormap("viridis")
    assert len(colormap) == 256
    assert isinstance(colormap[0], tuple)
    np.testing.assert_allclose(colormap[0], (0.267004, 0.004874, 0.329415))


def test_colormap_num_colors():
    from fdray.data.color import get_colormap

    colormap = get_colormap("viridis", num_colors=10)
    assert len(colormap) == 10


@pytest.fixture(scope="module")
def color_field():
    from fdray.data.color import colorize_direction_field

    field = [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [-1, 1, 0],
        [-1, 0, 0],
        [-1, -1, 0],
        [0, -1, 0],
        [1, -1, 0],
        [0, 0, 1],
        [0, 0, -1],
    ]
    return colorize_direction_field(field)


@pytest.mark.parametrize(
    ("k", "r", "g", "b"),
    [
        (0, 0.75, 0, 0),
        (1, 0.75, 0.5625, 0),
        (2, 0.375, 0.75, 0),
        (3, 0, 0.75, 0.1875),
        (4, 0, 0.75, 0.75),
        (5, 0, 0.1875, 0.75),
        (6, 0.375, 0, 0.75),
        (7, 0.75, 0, 0.5625),
        (8, 1, 1, 1),
        (9, 0, 0, 0),
    ],
)
def test_colorize_direction_field(color_field, k, r, g, b):
    assert color_field[k][0] == r
    assert color_field[k][1] == g
    assert color_field[k][2] == b


def test_colorize_direction():
    from fdray.data.color import colorize_direction

    c = colorize_direction([1, 2, 3])
    np.testing.assert_allclose(c, (0.9699322, 0.99017757, 0.63654272))


def test_import_error():
    from fdray.data.color import raise_import_error

    with pytest.raises(ImportError):
        raise_import_error("test")
