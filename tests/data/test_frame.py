import pytest
from PIL import Image


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


def test_to_spherical_coordinates():
    from fdray.data.frame import from_spherical_coordinates, to_spherical_coordinates

    df = from_spherical_coordinates(step_phi=20, step_theta=20)
    df = to_spherical_coordinates(df)
    assert df.shape == (190, 5)


@pytest.mark.parametrize("scale", [1, 3])
def test_visualize_spherical_data(scale: int):
    from fdray.data.frame import (
        from_spherical_coordinates,
        to_spherical_coordinates,
        visualize_spherical_data,
    )

    df = from_spherical_coordinates(step_phi=20, step_theta=20)
    df = to_spherical_coordinates(df)
    image = visualize_spherical_data(df, "z", scale=scale)
    assert isinstance(image, Image.Image)
    assert image.width == 19 * scale
    assert image.height == 10 * scale
