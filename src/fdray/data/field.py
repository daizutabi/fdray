from __future__ import annotations

from collections.abc import Iterable
from itertools import cycle
from typing import TYPE_CHECKING, Literal, overload

import numpy as np

from fdray.core.color import COLOR_PALETTE, Color
from fdray.core.object import Cube, Object
from fdray.core.object import Union as BaseUnion

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping, Sequence
    from typing import Any, Self

    from numpy.typing import NDArray


class Union(BaseUnion):
    @overload
    @classmethod
    def from_field(
        cls,
        field: Sequence | NDArray,
        obj: Callable[[Any], Object | Iterable[Object] | None],
        spacing: float | tuple[float, ...] = 1,
        ndim: int = 1,
        mask: Sequence | NDArray | None = None,
        *,
        as_union: Literal[True] = True,
    ) -> Self: ...

    @overload
    @classmethod
    def from_field(
        cls,
        field: Sequence | NDArray,
        obj: Callable[[Any], Object | Iterable[Object] | None],
        spacing: float | tuple[float, ...] = 1,
        ndim: int = 1,
        mask: Sequence | NDArray | None = None,
        *,
        as_union: Literal[False],
    ) -> list[Object]: ...

    @overload
    @classmethod
    def from_field(
        cls,
        field: Sequence | NDArray,
        obj: Callable[[Any], Object | Iterable[Object] | None],
        spacing: float | tuple[float, ...] = 1,
        ndim: int = 1,
        mask: Sequence | NDArray | None = None,
        *,
        as_union: bool,
    ) -> Self | list[Object]: ...

    @classmethod
    def from_field(
        cls,
        field: Sequence | NDArray,
        obj: Callable[[Any], Object | Iterable[Object] | None],
        spacing: float | tuple[float, ...] = 1,
        ndim: int = 1,
        mask: Sequence | NDArray | None = None,
        *,
        as_union: bool = True,
    ) -> Self | list[Object]:
        """Create objects from scalar, vector or tensor fields.

        This function generates 3D objects from field data.
        The last `ndim` dimensions of the input array are considered
        as field components.

        Args:
            field (Sequence | NDArray): Array containing field data
            obj (Callable[[Any], Object | Iterable[Object] | None]): Function
                that takes field data at a position and returns an Object
                (or None to skip)
            spacing (float | tuple[float, ...]): Distance between objects
                (scalar or per-dimension)
            ndim (int): Number of dimensions to treat as field
                components:

                - ndim=0: Scalar field (all dimensions used for positioning)
                - ndim=1: Vector field (last dimension contains vector components)
                - ndim=2: Tensor field (last two dimensions contain tensor components)
            mask (Sequence | NDArray | None): Boolean mask to filter field data
            as_union (bool): Whether to return a Union object or a list of objects

        Returns:
            Union object or list of objects representing the field
        """
        it = iter_objects_from_callable(obj, field, spacing, ndim, mask)
        return cls(*it) if as_union else list(it)

    @overload
    @classmethod
    def from_region(
        cls,
        region: Sequence | NDArray,
        obj: Object | Callable[[Any], Object | Iterable[Object] | None] | None = None,
        spacing: float | tuple[float, ...] = 1,
        mapping: Mapping[Any, Any] | None = None,
        *,
        as_union: Literal[True] = True,
    ) -> Self: ...

    @overload
    @classmethod
    def from_region(
        cls,
        region: Sequence | NDArray,
        obj: Object | Callable[[Any], Object | Iterable[Object] | None] | None = None,
        spacing: float | tuple[float, ...] = 1,
        mapping: Mapping[Any, Any] | None = None,
        *,
        as_union: Literal[False],
    ) -> list[Object]: ...

    @overload
    @classmethod
    def from_region(
        cls,
        region: Sequence | NDArray,
        obj: Object | Callable[[Any], Object | Iterable[Object] | None] | None = None,
        spacing: float | tuple[float, ...] = 1,
        mapping: Mapping[Any, Any] | None = None,
        *,
        as_union: bool,
    ) -> Self | list[Object]: ...

    @classmethod
    def from_region(
        cls,
        region: Sequence | NDArray,
        obj: Object | Callable[[Any], Object | Iterable[Object] | None] | None = None,
        spacing: float | tuple[float, ...] = 1,
        mapping: Mapping[Any, Any] | None = None,
        *,
        as_union: bool = True,
    ) -> Self | list[Object]:
        """Create objects from a discrete region.

        This function generates 3D objects from a discrete region,
        where each unique value in the region corresponds to an
        object with specific attributes.

        The function supports two modes:

        1. Base object + attribute mapping: Provide an Object instance
        and a mapping of region values to attributes (e.g., colors).
        2. Custom object generation: Provide a callback function that
        takes a region value and returns an Object (similar to from_field).

        Args:
            region (Sequence | NDArray): Array containing region data
                (discrete values)
            obj (Object | Callable[[Any], Object | Iterable[Object] | None] | None):
                Either an Object instance to be used as base, or a function that
                takes a region value and returns an Object, or None to use
                a default Cube
            spacing (float | tuple[float, ...]): Distance between objects
                (scalar or per-dimension)
            mapping: Mapping from region values to attributes (used only
                when obj is an Object)
            as_union: Whether to return a Union object or a list of objects

        Returns:
            Union object or list of objects representing the region
        """
        if callable(obj):
            return cls.from_field(region, obj, spacing, ndim=0, as_union=as_union)

        if obj is None:
            obj = Cube((0, 0, 0), 0.85)

        mapping = mapping or get_default_mapping(region)
        objects = {k: obj.add(v) for k, v in mapping.items()}
        it = iter_objects_from_dict(objects, region, spacing)

        return cls(*it) if as_union else list(it)


def iter_objects_from_callable(
    obj: Callable[[Any], Object | Iterable[Object] | None],
    field: Sequence | NDArray,
    spacing: float | tuple[float, ...] = 1,
    ndim: int = 1,
    mask: Sequence | NDArray | None = None,
) -> Iterator[Object]:
    if not isinstance(field, np.ndarray):
        field = np.array(field)

    if mask is not None and not isinstance(mask, np.ndarray):
        mask = np.array(mask)

    shape = field.shape[: field.ndim - ndim]
    offset = [(i - 1) / 2 for i in shape]

    for idx in np.ndindex(shape):
        if mask is not None and not mask[idx]:
            continue

        if o := obj(field[idx]):
            if not isinstance(o, Object):
                o = Union(*o)
            yield from translate(o, [idx], spacing, offset)


def iter_objects_from_dict(
    objects: dict[Any, Object],
    region: Sequence | NDArray,
    spacing: float | tuple[float, ...] = 1,
) -> Iterator[Object]:
    indices = get_indices(region)
    offset = [(i - 1) / 2 for i in np.shape(region)]

    for index, obj in objects.items():
        if index in indices:
            yield from translate(obj, indices[index], spacing, offset)


def get_indices(region: Sequence | NDArray) -> dict[Any, list[tuple[int, ...]]]:
    if not isinstance(region, np.ndarray):
        region = np.array(region)

    indices: dict[Any, list[tuple[int, ...]]] = {}

    for idx in np.ndindex(region.shape):
        index = region[idx]
        indices.setdefault(index, []).append(idx)

    return indices


def get_default_mapping(region: Sequence | NDArray) -> dict[Any, Any]:
    colors = [Color(c) for c in COLOR_PALETTE]
    return dict(zip(np.unique(region), cycle(colors), strict=False))


def translate(
    obj: Object,
    indices: Iterable[Iterable[float]],
    spacing: float | Iterable[float] = 1,
    offset: float | Iterable[float] = 0,
) -> Iterator[Object]:
    spacing = list(spacing) if isinstance(spacing, Iterable) else [spacing]
    offset = list(offset) if isinstance(offset, Iterable) else [offset]

    for index in indices:
        it = zip(index, cycle(spacing), cycle(offset), strict=False)
        position = ((i - o) * s for i, s, o in it)
        position = (*position, 0, 0)[:3]  # for 1D or 2D regions

        yield obj.translate(*position)
