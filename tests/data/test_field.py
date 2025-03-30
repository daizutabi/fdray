import pytest

from fdray.core.object import Box, Sphere
from fdray.data.field import Union


@pytest.fixture(scope="module")
def field_scalar():
    region = [0.2, 0.3, 0.4]
    return Union.from_region(region, lambda x: Sphere(0, x))


@pytest.mark.parametrize(("r", "p"), [(0.2, -1), (0.3, 0), (0.4, 1)])
def test_field_scalar(field_scalar: Union, r, p):
    x = str(field_scalar)
    assert f"{r} translate <{p}, 0, 0>" in x


@pytest.fixture(scope="module")
def field_vector():
    direction = [
        [1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 1],
        [0, 0, -1],
        [1, 1, 1],
        [1, -1, -1],
    ]
    return Union.from_field(direction, lambda x: [Box(0, 1).align(x)], ndim=1)


@pytest.mark.parametrize(
    ("ry", "rz", "p"),
    [
        (0, 0, -3),
        (0, 90, -2),
        (0, -90, -1),
        (-90, 0, 0),
        (90, 0, 1),
        (-35.264, 45, 2),
        (35.264, -45, 3),
    ],
)
def test_field_vector(field_vector: Union, ry, rz, p):
    x = str(field_vector)
    assert f"rotate <0, {ry}, {rz}> }} translate <{p}, 0, 0>" in x


def test_field_mask():
    direction = [[1, 0, 0], [0, 1, 0], [0, -1, 0]]
    mask = [True, False, True]
    objs = Union.from_field(
        direction,
        lambda x: [Box(0, 1).align(x)],
        mask=mask,
        as_union=False,
    )
    assert len(objs) == 2
