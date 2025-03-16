from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

import numpy as np

from .colors import COLOR_PALETTE
from .shapes import Cube, ShapeGroup

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from numpy.typing import NDArray

    from .shapes import Shape


class Region(ShapeGroup):
    def __init__(
        self,
        region: NDArray[np.integer[Any]],
        shape: Shape | None = None,
        spacing: float | tuple[float, ...] = 1,
        attrs: Mapping[int, Any] | None = None,
    ) -> None:
        shape = shape or get_default_shape()
        attrs = attrs or get_default_attrs(region)
        shapes = {k: shape.add(v) for k, v in attrs.items()}

        if isinstance(spacing, (int, float)):
            spacing = (spacing,) * region.ndim
        elif len(spacing) != region.ndim:
            msg = f"Spacing must have {region.ndim} components"
            raise ValueError(msg)

        cells = []

        for idx in np.ndindex(region.shape):
            index = region[idx]
            if index not in shapes:
                continue

            position = (i * s for i, s in zip(idx, spacing, strict=True))
            position = (*position, 0, 0)[:3]

            cell = shapes[index].translate(*position)
            cells.append(cell)

        super().__init__(*cells)


def get_default_shape(size: float = 0.8) -> Shape:
    return Cube((0, 0, 0), size)


def get_default_attrs(region: NDArray[np.integer[Any]]) -> dict[int, Any]:
    return dict(zip(np.unique(region), cycle(COLOR_PALETTE), strict=False))
