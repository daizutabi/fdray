import numpy as np
import pytest

from fdray.vector import Vector


@pytest.fixture(scope="module")
def v():
    return Vector(1, 2, 3)


@pytest.fixture(scope="module")
def o():
    return Vector(4, 5, 6)


def test_vector_repr(v: Vector):
    assert repr(v) == "Vector(1, 2, 3)"


def test_vector_str(v: Vector):
    assert str(v) == "<1, 2, 3>"


def test_vector_iter(v: Vector):
    assert list(v) == [1, 2, 3]


def test_vector_add(v: Vector, o: Vector):
    assert v + o == Vector(5, 7, 9)


def test_vector_sub(v: Vector, o: Vector):
    assert v - o == Vector(-3, -3, -3)


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


def test_vector_dot(v: Vector, o: Vector):
    assert v @ o == 32


def test_vector_cross(v: Vector, o: Vector):
    assert v.cross(o) == Vector(-3, 6, -3)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_x(sign):
    x = Vector(1, 1, 1).rotate(Vector(1, 0, 0), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, 1)
    np.testing.assert_allclose(x.y, -sign)
    np.testing.assert_allclose(x.z, sign)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_y(sign):
    x = Vector(1, 1, 1).rotate(Vector(0, 1, 0), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, sign)
    np.testing.assert_allclose(x.y, 1)
    np.testing.assert_allclose(x.z, -sign)


@pytest.mark.parametrize("sign", [1, -1])
def test_rotate_z(sign):
    x = Vector(1, 1, 1).rotate(Vector(0, 0, 1), np.pi / 2 * sign)
    np.testing.assert_allclose(x.x, -sign)
    np.testing.assert_allclose(x.y, sign)
    np.testing.assert_allclose(x.z, 1)


def test_from_spherical():
    x = Vector.from_spherical(np.pi / 5, np.pi / 6)
    np.testing.assert_allclose(x.x, 0.7006292692220368)
    np.testing.assert_allclose(x.y, 0.5090369604551273)
    np.testing.assert_allclose(x.z, 0.5)
