from math import asin, degrees, sqrt

import numpy as np
import pytest

from fdray.core.camera import Camera


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
    np.testing.assert_allclose(v.x, 1.299743850654924)
    np.testing.assert_allclose(v.y, 0.6366710503823082)
    np.testing.assert_allclose(v.z, 1.371312682810898)


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


def test_camera_orbital_location_zero():
    camera = Camera(30, 40)
    assert camera.orbital_location() == camera.location


@pytest.fixture(params=[3, 4, 5])
def distance(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(params=[(0, 0, 0), (1, 2, 3), (-2, -4, -8)])
def look_at(request: pytest.FixtureRequest):
    return request.param


def test_camera_orbital_location(distance: float, look_at: tuple[float, float, float]):
    camera = Camera(0, 0, view_scale=2, distance=distance, look_at=look_at)

    n = sqrt(distance**2 + 4)
    forward = n / distance
    p = camera.orbital_location(forward, degrees(asin(2 / n)), 0)
    np.testing.assert_allclose(p.x, look_at[0], atol=1e-5)
    np.testing.assert_allclose(p.y, look_at[1], atol=1e-5)
    np.testing.assert_allclose(p.z, look_at[2] + 2, atol=1e-5)


def test_camera_orbital_location_left(
    distance: float,
    look_at: tuple[float, float, float],
):
    camera = Camera(0, 0, view_scale=2, distance=distance, look_at=look_at)

    n = sqrt(distance**2 + 4)
    forward = n / distance
    p = camera.orbital_location(forward, degrees(asin(2 / n)), 90)
    np.testing.assert_allclose(p.x, look_at[0], atol=1e-5)
    np.testing.assert_allclose(p.y, look_at[1] - 2, atol=1e-5)
    np.testing.assert_allclose(p.z, look_at[2], atol=1e-5)


def test_camera_orbital_location_down(distance):
    camera = Camera(0, 0, view_scale=2, distance=distance)

    n = sqrt(distance**2 + 4)
    forward = n / distance
    p = camera.orbital_location(forward, degrees(asin(2 / n)), 180)
    np.testing.assert_allclose(p.x, 0, atol=1e-5)
    np.testing.assert_allclose(p.y, 0, atol=1e-5)
    np.testing.assert_allclose(p.z, -2, atol=1e-5)


def test_camera_orbital_location_right(distance):
    camera = Camera(0, 0, view_scale=2, distance=distance)

    n = sqrt(distance**2 + 4)
    forward = n / distance
    p = camera.orbital_location(forward, degrees(asin(2 / n)), 270)
    np.testing.assert_allclose(p.x, 0, atol=1e-5)
    np.testing.assert_allclose(p.y, 2, atol=1e-5)
    np.testing.assert_allclose(p.z, 0, atol=1e-5)


def test_camera_orbital_location_behind(distance):
    camera = Camera(0, 0, view_scale=2, distance=distance)

    n = sqrt((distance / 2) ** 2 + 1)
    forward = -n / distance
    p = camera.orbital_location(forward, degrees(asin(1 / n)), 0)
    np.testing.assert_allclose(p.x, 3 * distance / 2, atol=1e-5)
    np.testing.assert_allclose(p.y, 0, atol=1e-5)
    np.testing.assert_allclose(p.z, -1, atol=1e-5)
