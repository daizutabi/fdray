from __future__ import annotations

from collections.abc import Iterable
from itertools import cycle
from typing import TYPE_CHECKING, Literal, overload

import numpy as np

from fdray.core.color import COLOR_PALETTE, Color
from fdray.core.object import Cube, Object, Union

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence
    from typing import Any

    from numpy.typing import NDArray


def translate(
    obj: Object,
    indices: Iterable[Iterable[float]],
    spacing: float | Iterable[float] = 1,
) -> Iterator[Object]:
    spacing = list(spacing) if isinstance(spacing, Iterable) else [spacing]

    for index in indices:
        position = (i * s for i, s in zip(index, cycle(spacing), strict=False))
        position = (*position, 0, 0)[:3]  # for 1D or 2D regions

        yield obj.translate(*position)


def get_indices(region: Sequence | NDArray) -> dict[Any, list[tuple[int, ...]]]:
    if not isinstance(region, np.ndarray):
        region = np.array(region)

    indices: dict[Any, list[tuple[int, ...]]] = {}

    for idx in np.ndindex(region.shape):
        index = region[idx]
        indices.setdefault(index, []).append(idx)

    return indices


def iter_objects(
    objects: dict[Any, Object],
    region: Sequence | NDArray,
    spacing: float | tuple[float, ...] = 1,
) -> Iterator[Object]:
    indices = get_indices(region)

    for index, obj in objects.items():
        if index in indices:
            yield from translate(obj, indices[index], spacing)


@overload
def from_region(
    region: Sequence | NDArray,
    obj: Object | None = None,
    spacing: float | tuple[float, ...] = 1,
    mapping: Mapping[Any, Any] | None = None,
    *,
    as_union: Literal[True] = True,
) -> Union: ...


@overload
def from_region(
    region: Sequence | NDArray,
    obj: Object | None = None,
    spacing: float | tuple[float, ...] = 1,
    mapping: Mapping[Any, Any] | None = None,
    *,
    as_union: Literal[False] = False,
) -> list[Object]: ...


@overload
def from_region(
    region: Sequence | NDArray,
    obj: Object | None = None,
    spacing: float | tuple[float, ...] = 1,
    mapping: Mapping[Any, Any] | None = None,
    *,
    as_union: Literal[False] = False,
) -> list[Object]: ...


def from_region(
    region: Sequence | NDArray,
    obj: Object | None = None,
    spacing: float | tuple[float, ...] = 1,
    mapping: Mapping[Any, Any] | None = None,
    *,
    as_union: bool = True,
) -> Union | list[Object]:
    def get_default_attrs() -> dict[Any, Any]:
        colors = [Color(c) for c in COLOR_PALETTE]
        return dict(zip(np.unique(region), cycle(colors), strict=False))

    obj = obj or Cube((0, 0, 0), 0.85)
    mapping = mapping or get_default_attrs()
    objects = {k: obj.add(v) for k, v in mapping.items()}

    it = iter_objects(objects, region, spacing)

    return Union(*it) if as_union else list(it)
