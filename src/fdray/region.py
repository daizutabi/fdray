from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

import numpy as np

from .color import COLOR_PALETTE, Color
from .shapes import Cube, ShapeGroup

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping
    from typing import Any

    from numpy.typing import NDArray

    from .shapes import Shape


class Region(ShapeGroup):
    def __init__(
        self,
        region: list[int] | NDArray[np.integer],
        shape: Shape | None = None,
        spacing: float | tuple[float, ...] = 1,
        attrs: Mapping[int, Any] | None = None,
    ) -> None:
        if isinstance(region, list):
            region = np.array(region)

        shape = shape or get_default_shape()
        attrs = attrs or get_default_attrs(region)
        shapes = {k: shape.add(v) for k, v in attrs.items()}

        if isinstance(spacing, (int, float)):
            spacing = (spacing,) * region.ndim
        elif len(spacing) != region.ndim:
            msg = f"Spacing must have {region.ndim} components"
            raise ValueError(msg)

        def iter_shapes() -> Iterator[Shape]:
            for idx in np.ndindex(region.shape):
                index = region[idx]
                if index not in shapes:
                    continue

                position = (i * s for i, s in zip(idx, spacing, strict=True))
                position = (*position, 0, 0)[:3]  # for 1D or 2D regions

                yield shapes[index].translate(*position)

        super().__init__(*iter_shapes())


def get_default_shape(size: float = 0.85) -> Shape:
    return Cube((0, 0, 0), size)


def get_default_attrs(region: NDArray[np.integer]) -> dict[int, Any]:
    colors = [Color(c) for c in COLOR_PALETTE]
    return dict(zip(np.unique(region), cycle(colors), strict=False))
