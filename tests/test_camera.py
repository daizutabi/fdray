import numpy as np
import pytest

from fdray.camera import Camera


@pytest.fixture(scope="module")
def camera():
    return Camera(
        longitude=20,
        latitude=40,
        view_scale=0.5,
        distance=1.6666667,
        tilt=10,
        look_at=(0.1, 0.2, 0.3),
        aspect_ratio=16 / 9,
    )


def test_camera_phi(camera: Camera):
    assert camera.phi == np.radians(20)


def test_camera_theta(camera: Camera):
    assert camera.theta == np.radians(40)


def test_camera_z(camera: Camera):
    v = camera.z
    np.testing.assert_allclose(v.x, 0.719846310392954)
    np.testing.assert_allclose(v.y, 0.262002630229384)
    np.testing.assert_allclose(v.z, 0.6427876096865393)


def test_camera_x(camera: Camera):
    v = camera.x
    np.testing.assert_allclose(v.x, -0.44171154273062)
    np.testing.assert_allclose(v.y, 0.88724066723178)
    np.testing.assert_allclose(v.z, 0.13302222155948)


def test_camera_y(camera: Camera):
    v = camera.y
    np.testing.assert_allclose(v.x, -0.53545513577906)
    np.testing.assert_allclose(v.y, -0.37968226211264)
    np.testing.assert_allclose(v.z, 0.7544065067354)


def test_camera_direction(camera: Camera):
    v = camera.direction
    np.testing.assert_allclose(v.x, 1.199743850654923)
    np.testing.assert_allclose(v.y, 0.43667105038230)
    np.testing.assert_allclose(v.z, 1.071312682810898)


def test_camera_location(camera: Camera):
    v = camera.location
    np.testing.assert_allclose(v[0], 1.299743850654924)
    np.testing.assert_allclose(v[1], 0.6366710503823082)
    np.testing.assert_allclose(v[2], 1.371312682810898)


def test_camera_right(camera: Camera):
    v = camera.right
    np.testing.assert_allclose(v.x, 0.5889487236408335)
    np.testing.assert_allclose(v.y, -1.1829875563090513)
    np.testing.assert_allclose(v.z, -0.1773629620793187)


def test_camera_up(camera: Camera):
    v = camera.up
    np.testing.assert_allclose(v.x, -0.40159135183430)
    np.testing.assert_allclose(v.y, -0.2847616965844833)
    np.testing.assert_allclose(v.z, 0.56580488005161)


def test_camera_sky(camera: Camera):
    v = camera.sky
    np.testing.assert_allclose(v.x, -0.53545513577906)
    np.testing.assert_allclose(v.y, -0.37968226211264)
    np.testing.assert_allclose(v.z, 0.7544065067354)


def test_camera_iter(camera: Camera):
    x = list(camera)
    assert len(x) == 12
    assert x[0] == "location"
    assert x[1] == "<1.2997, 0.63667, 1.3713>"
    assert x[-2] == "sky"
    assert x[-1] == "<-0.53546, -0.37968, 0.75441>"
