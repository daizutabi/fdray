from __future__ import annotations

import numpy as np

from fdray.core.color import Color


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

        cmap = plt.get_cmap(name)
        return [Color(cmap(i)[:3]) for i in np.linspace(0, 1, num_colors)]

    except ImportError:  # no cov
        msg = (
            f"Colormap '{name}' requires matplotlib. "
            "Install with: pip install matplotlib."
        )
        raise ImportError(msg) from None
