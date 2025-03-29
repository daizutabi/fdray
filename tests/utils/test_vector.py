import numpy as np
import pytest

from fdray.utils.vector import Vector


@pytest.fixture(scope="module")
def v():
    return Vector(1, 2, 3)


@pytest.fixture(scope="module", params=[Vector(4, 5, 6), (4, 5, 6)])
def o(request: pytest.FixtureRequest):
    return request.param


def test_vector_init_from_iteralbe():
    assert Vector([1, 2, 3]) == (1, 2, 3)


def test_vector_ne():
    assert Vector(1, 2, 3) != (1, 2, 4)
    assert Vector(1, 2, 3) != (1, 2)


def test_vector_init_error():
    with pytest.raises(ValueError, match="Invalid arguments"):
        Vector(1, 2)


def test_vector_repr(v: Vector):
    assert repr(v) == "Vector(1, 2, 3)"


def test_vector_str(v: Vector):
    assert str(v) == "<1, 2, 3>"


def test_vector_str_zero():
    assert str(Vector(1e-6, 1.2345678e-5, 0)) == "<0, 1.2346e-05, 0>"


def test_vector_iter(v: Vector):
    assert list(v) == [1, 2, 3]


def test_vector_add(v: Vector, o):
    assert v + o == Vector(5, 7, 9)
    assert v + list(o) == Vector(5, 7, 9)


def test_vector_sub(v: Vector, o):
    assert v - o == Vector(-3, -3, -3)
    assert v - list(o) == Vector(-3, -3, -3)


def test_vector_mul(v: Vector):
    assert v * 2 == Vector(2, 4, 6)


def test_vector_rmul(v: Vector):
    assert 2 * v == Vector(2, 4, 6)


def test_vector_truediv(v: Vector):
    assert v / 2 == Vector(0.5, 1, 1.5)


def test_vector_neg(v: Vector):
    assert -v == Vector(-1, -2, -3)


def test_vector_norm(v: Vector):
    np.testing.assert_allclose(v.norm(), 3.741657386)


def test_vector_normalize(v: Vector):
    n = v.normalize()
    np.testing.assert_allclose(n.x, 0.2672612419124244)
    np.testing.assert_allclose(n.y, 0.5345224838248488)
    np.testing.assert_allclose(n.z, 0.8017837257372732)


def test_vector_dot(v: Vector, o):
    assert v.dot(o) == 32
    assert v @ o == 32
    assert v.dot(list(o)) == 32
    assert v @ list(o) == 32


def test_vector_cross(v: Vector, o):
    assert v.cross(o) == Vector(-3, 6, -3)
    assert v.cross(list(o)) == Vector(-3, 6, -3)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_x(sign):
    x = Vector(1, 1, 1).rotate((1, 0, 0), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, 1)
    np.testing.assert_allclose(x.y, -sign)
    np.testing.assert_allclose(x.z, sign)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_y(sign):
    x = Vector(1, 1, 1).rotate((0, 1, 0), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, sign)
    np.testing.assert_allclose(x.y, 1)
    np.testing.assert_allclose(x.z, -sign)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_z(sign):
    x = Vector(1, 1, 1).rotate((0, 0, 1), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, -sign)
    np.testing.assert_allclose(x.y, sign)
    np.testing.assert_allclose(x.z, 1)


def test_angle():
    assert Vector(1, 0, 0).angle((0, 1, 0)) == np.pi / 2
    assert Vector(1, 0, 0).angle((-1, 0, 0)) == np.pi
    assert Vector(1, 0, 0).angle((1, 0, 0)) == 0
    assert Vector(1, 0, 0).angle((-1, 0, 0)) == np.pi
    assert Vector(1, 0, 0).angle((0, 1, 0)) == np.pi / 2


@pytest.mark.parametrize(
    ("phi", "theta", "expected"),
    [
        (0, 0, (1, 0, 0)),
        (np.pi / 2, 0, (0, 1, 0)),
        (np.pi, 0, (-1, 0, 0)),
        (3 * np.pi / 2, 0, (0, -1, 0)),
        (np.pi / 2, np.pi / 2, (0, 0, 1)),
        (0, -np.pi / 2, (0, 0, -1)),
        (np.pi / 4, np.pi / 4, (0.5, 0.5, 0.70711)),
    ],
)
def test_from_spherical_0_0(phi, theta, expected):
    x = Vector.from_spherical(phi, theta)
    np.testing.assert_allclose(x.x, expected[0], atol=1e-5)
    np.testing.assert_allclose(x.y, expected[1], atol=1e-5)
    np.testing.assert_allclose(x.z, expected[2], atol=1e-5)
    x = Vector.from_spherical(*x.to_spherical())
    np.testing.assert_allclose(x.x, expected[0], atol=1e-5)
    np.testing.assert_allclose(x.y, expected[1], atol=1e-5)
    np.testing.assert_allclose(x.z, expected[2], atol=1e-5)


def test_from_spherical():
    x = Vector.from_spherical(np.pi / 5, np.pi / 6)
    np.testing.assert_allclose(x.x, 0.7006292692220368)
    np.testing.assert_allclose(x.y, 0.5090369604551273)
    np.testing.assert_allclose(x.z, 0.5)
    p, t = x.to_spherical()
    np.testing.assert_allclose(p, np.pi / 5, atol=1e-5)
    np.testing.assert_allclose(t, np.pi / 6, atol=1e-5)


@pytest.mark.parametrize(
    ("x", "y", "z"),
    [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
        (1, 1, 1),
        (-1, -1, -1),
        (1, -1, 1),
        (-1, 1, -1),
        (1, 1, -1),
        (-1, -1, 1),
    ],
)
def test_to_spherical(x, y, z):
    v = Vector(x, y, z)
    p, t = v.to_spherical()
    v = Vector.from_spherical(p, t) * v.norm()
    np.testing.assert_allclose(v.x, x, atol=1e-5)
    np.testing.assert_allclose(v.y, y, atol=1e-5)
    np.testing.assert_allclose(v.z, z, atol=1e-5)


def test_to_spherical_zero():
    assert Vector(0, 0, 0).to_spherical() == (0, 0)
