import pytest


def test_from_spherical_coordinates():
    from fdray.data.frame import from_spherical_coordinates

    df = from_spherical_coordinates(step_phi=20, step_theta=20)
    assert df.shape == (163, 3)


def test_from_spherical_coordinates_error_step_phi():
    from fdray.data.frame import from_spherical_coordinates

    m = r"step_phi \(11\) must be a divisor of 360"
    with pytest.raises(ValueError, match=m):
        from_spherical_coordinates(step_phi=11)


def test_from_spherical_coordinates_error_step_theta():
    from fdray.data.frame import from_spherical_coordinates

    m = r"step_theta \(11\) must be a divisor of 180"
    with pytest.raises(ValueError, match=m):
        from_spherical_coordinates(step_theta=11)
