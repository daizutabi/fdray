from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from fdray.core.color import Color

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import NDArray


def raise_import_error(msg: str) -> None:
    msg = f"{msg} Install with: pip install matplotlib."
    raise ImportError(msg) from None


def get_colormap(name: str, num_colors: int = 256) -> list[Color]:
    """Get a list of colors from a named colormap.

    Args:
        name (str): Name of the colormap (e.g., 'viridis', 'plasma', etc.)
        num_colors (int): Number of colors to include in the colormap

    Returns:
        list[Color]: List of Color objects representing the colormap
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # no cov
        raise_import_error(f"Colormap '{name}' requires matplotlib.")

    cmap = plt.get_cmap(name)
    return [Color(cmap(i)[:3]) for i in np.linspace(0, 1, num_colors)]


def encode_direction_field(
    field: Sequence | NDArray,
    axis: int = 2,
) -> NDArray:
    """Encode a vector field as colors based on vector directions.

    This function maps direction vectors to colors using a spherical
    color mapping:

    - Azimuthal angle (XY plane) determines the hue
    - Polar angle (Z component) affects saturation and value

    Note:
        Input vectors must be normalized (unit length). No normalization is
        performed by this function. Use `encode_direction` for automatic
        normalization of single vectors.

    Args:
        field (Sequence | NDArray): Array of direction vectors to
            encode as colors. Last dimension should contain vector
            components.
        axis (int): Principal axis index (0=X, 1=Y, 2=Z).
            Default is 2 (Z-axis).

    Returns:
        Array of RGB colors corresponding to the input vector directions.

    Requires:
        matplotlib for HSV to RGB conversion.
    """
    try:
        from matplotlib.colors import hsv_to_rgb
    except ImportError:  # no cov
        raise_import_error("HSV to RGB conversion requires matplotlib.")

    if not isinstance(field, np.ndarray):
        field = np.array(field, dtype=np.float64)

    i, j = [[1, 2], [0, 2], [0, 1]][axis]
    x = field[..., i]
    y = field[..., j]
    z = field[..., axis]
    geom = np.linalg.norm(field, axis=-1) != 0

    hsv = np.empty_like(field)
    hsv[..., 0] = (np.arctan2(-y, -x) + np.pi) / (2 * np.pi)
    hsv[..., 1] = np.where(geom, 1 - z**2, 0)
    hsv[..., 2] = 1 - (1 - z) ** 2 / 4

    return hsv_to_rgb(hsv)


def encode_direction(vector: Sequence, axis: int = 2) -> Color:
    """Encode a single direction vector as a color.

    This function converts a direction vector to a color based
    on its orientation. The vector is automatically normalized
    to unit length before encoding.

    Args:
        vector (Sequence | NDArray): Direction vector to encode as a color
        axis (int): Principal axis index (0=X, 1=Y, 2=Z).
            Default is 2 (Z-axis).

    Returns:
        A Color object representing the encoded direction.

    Requires:
        matplotlib for HSV to RGB conversion.
    """
    norm = np.linalg.norm(vector)
    field = [[x / norm for x in vector]]
    color = encode_direction_field(field, axis)
    return Color(color[0])
