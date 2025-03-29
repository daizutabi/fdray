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
) -> NDArray[np.float64]:
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
    norm = np.linalg.norm(vector)
    field = [[x / norm for x in vector]]
    color = encode_direction_field(field, axis)
    return Color(color[0])
