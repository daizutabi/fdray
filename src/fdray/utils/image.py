from __future__ import annotations

import atexit
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import NDArray

# pyright: reportMissingTypeArgument=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false


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
        (left - margin, top - margin, right + margin + 1, bottom + margin + 1),  # pyright: ignore[reportArgumentType]
    )


def save(data: NDArray | Image.Image) -> Path:
    """Save the image data to a temporary file.

    The file will be deleted when the program exits.

    Args:
        data (NDArray | Image.Image): The image data to save.

    Returns:
        Path: The path to the saved file.
    """
    image = Image.fromarray(data) if isinstance(data, np.ndarray) else data

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        path = Path(tmp.name)
        image.save(path)

    def unlink(path: Path = path) -> None:
        path.unlink(missing_ok=True)  # no cov

    atexit.register(unlink)

    return path
