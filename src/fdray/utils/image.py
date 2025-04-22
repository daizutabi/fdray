from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from PIL import Image


def trim(image: Image.Image, margin: int = 0) -> Image.Image:
    """Trim the output image to the non-transparent region.

    Args:
        image (Image.Image): The output image.
        margin (int): The margin to trim.

    Returns:
        Image.Image: The trimmed image.
    """
    array = np.array(image)
    alpha = array[:, :, 3]
    y, x = np.where(alpha > 0)
    top, bottom = np.min(y), np.max(y)
    left, right = np.min(x), np.max(x)
    return image.crop(
        (left - margin, top - margin, right + margin + 1, bottom + margin + 1),  # type: ignore
    )
