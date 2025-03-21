from __future__ import annotations

import textwrap
from abc import ABC
from collections.abc import Sequence
from itertools import repeat
from typing import TYPE_CHECKING, ClassVar, Literal, overload

from .attributes import Transform
from .colors import Color
from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self

    import numpy as np
    from numpy.typing import NDArray

    from .typing import Point


class Shape(ABC):
    nargs: ClassVar[int] = 0
    args: list[Any]
    attrs: list[Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = list(args[: self.nargs])
        attrs = [convert_attribute(attr) for attr in args[self.nargs :]]
        kw_attrs = [k for k, v in kwargs.items() if v]
        self.attrs = [*kw_attrs, *attrs]

    @property
    def name(self) -> str:
        return to_snake_case(self.__class__.__name__)

    def __iter__(self) -> Iterator[str]:
        if self.args:
            yield ", ".join(convert(arg) for arg in self.args)

        yield from (str(attr) for attr in self.attrs)

    def __str__(self) -> str:
        args = list(self)
        if len(args) == 1:
            return f"{self.name} {{ {args[0]} }}"

        arg = textwrap.indent("\n".join(args), "  ")
        return f"{self.name} {{\n{arg}\n}}"

    @overload
    def __add__(self, other: Shape) -> Union: ...

    @overload
    def __add__(self, other: Any) -> Self: ...

    def __add__(self, other: Shape | Any) -> Union | Self:
        if isinstance(other, Shape):
            return Union(self, other)

        return self.__class__(*self.args, *self.attrs, other)

    def __sub__(self, other: Shape) -> Difference:
        return Difference(self, other)

    def __mul__(self, other: Shape) -> Intersection:
        return Intersection(self, other)

    def __or__(self, other: Shape) -> Merge:
        return Merge(self, other)

    def add(self, *others: Any) -> Self:
        attrs = []
        for other in others:
            if isinstance(other, list | tuple):
                attrs.extend(other)
            else:
                attrs.append(other)

        return self.__class__(*self.args, *self.attrs, *attrs)

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        if y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(self, x: float, y: float, z: float) -> Self:
        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(self, x: float, y: float, z: float) -> Self:
        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))


SHAPE_KEYWORDS = ["open"]


def convert_attribute(attr: Any) -> Any:
    if attr in SHAPE_KEYWORDS:
        return attr

    if isinstance(attr, str | tuple):
        try:
            return Color(attr)
        except ValueError:
            return attr

    return attr


class Csg(Shape):
    attrs: list[Any]

    def __add__(self, other: Any) -> Self:
        return self.__class__(*self.attrs, other)


class Union(Csg):
    pass


class Intersection(Csg):
    def __mul__(self, other: Shape) -> Self:
        return super().__add__(other)


class Difference(Csg):
    def __sub__(self, other: Shape) -> Self:
        return super().__add__(other)


class Merge(Csg):
    def __or__(self, other: Shape) -> Self:
        return super().__add__(other)


class ShapeGroup:
    union: Union

    def __init__(self, *shapes: Shape) -> None:
        self.union = Union(*shapes)

    def __str__(self) -> str:
        return str(self.union)

    def __add__(self, other: Any) -> Self:
        group = self.__class__.__new__(self.__class__)
        group.union = self.union + other
        return group

    def add(self, *others: Any) -> Self:
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.add(*others)
        return group

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.scale(x, y, z)
        return group

    def rotate(self, x: float, y: float, z: float) -> Self:
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.rotate(x, y, z)
        return group

    def translate(self, x: float, y: float, z: float) -> Self:
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.translate(x, y, z)
        return group


class Box(Shape):
    nargs: ClassVar[int] = 2

    def __init__(
        self,
        corner1: Point,
        corner2: Point,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(corner1, corner2, *attrs, **kwargs)


class Cone(Shape):
    nargs: ClassVar[int] = 4

    def __init__(
        self,
        center1: Point,
        radius1: float,
        center2: Point,
        radius2: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center1, radius1, center2, radius2, *attrs, **kwargs)


class Cylinder(Shape):
    nargs: ClassVar[int] = 3

    def __init__(
        self,
        center1: Point,
        center2: Point,
        radius: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center1, center2, radius, *attrs, **kwargs)


class Plane(Shape):
    nargs: ClassVar[int] = 2

    def __init__(
        self,
        normal: Point,
        distance: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(normal, distance, *attrs, **kwargs)


class Sphere(Shape):
    nargs: ClassVar[int] = 2

    def __init__(
        self,
        center: Point,
        radius: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, radius, *attrs, **kwargs)


class SphereSweep(Shape):
    nargs: ClassVar[int] = 3

    def __init__(
        self,
        kind: Literal["linear_spline", "b_spline", "cubic_spline"],
        centers: Sequence[Point],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        if kind in ["b_spline", "cubic_spline"] and len(centers) < 4:
            msg = f"At least 4 points are required for {kind}"
            raise ValueError(msg)

        if kind == "linear_spline" and len(centers) < 2:
            msg = "At least 2 points are required for linear spline"
            raise ValueError(msg)

        super().__init__(kind, centers, radius, *attrs, **kwargs)

    def __iter__(self) -> Iterator[str]:
        kind, centers, radius = self.args
        yield f"{kind}, {len(centers)}"
        radii = radius if isinstance(radius, Sequence) else repeat(radius)
        it = zip(centers, radii, strict=False)
        yield ", ".join(f"{convert(c)}, {convert(r)}" for c, r in it)
        yield from (str(attr) for attr in self.attrs)


class Polyline(Shape):
    """A polyline (broken line) represented as a linear sphere sweep.

    This is a convenience class that creates a sphere sweep with linear_spline
    interpolation, providing a simpler interface for creating polylines.
    """

    nargs: ClassVar[int] = 2
    kind: ClassVar[Literal["linear_spline"]] = "linear_spline"

    def __init__(
        self,
        centers: Sequence[Point] | NDArray[np.number],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize a polyline.

        Args:
            centers (Sequence[Point] | NDArray[np.number]): Sequence of 3D
                points or NumPy array with shape (n, 3) where n is the number
                of points.
            radius (float | Sequence[float]): Constant radius or sequence
                of radii for each point.
            *attrs: Additional attributes.
            **kwargs: Additional keyword attributes.
        """
        super().__init__(centers, radius, *attrs, **kwargs)

    def __str__(self) -> str:
        return str(SphereSweep(self.kind, *self.args, *self.attrs))

    @classmethod
    def from_coordinates(
        cls,
        x: Sequence[float],
        y: Sequence[float],
        z: Sequence[float],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> Self:
        """Create a polyline from separate x, y, z coordinate sequences."""
        return cls(list(zip(x, y, z, strict=True)), radius, *attrs, **kwargs)


class Curve(Polyline):
    """A smooth curve that passes through all specified points.

    Create a cubic spline sphere sweep that is guaranteed to pass
    through all given points, including the start and end points. It uses ghost
    points to ensure proper curve behavior at the endpoints.

    Unlike standard cubic splines which may not pass through the endpoints,
    this implementation ensures the curve follows all specified points exactly.
    """

    nargs: ClassVar[int] = 2
    kind: ClassVar[Literal["cubic_spline"]] = "cubic_spline"

    def __init__(
        self,
        centers: Sequence[Point] | NDArray[np.number],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        if len(centers) < 2:
            msg = "At least 2 points are required"
            raise ValueError(msg)

        first, second = centers[0], centers[1]
        ghost_first = (
            2 * first[0] - second[0],
            2 * first[1] - second[1],
            2 * first[2] - second[2],
        )

        last, second_last = centers[-1], centers[-2]
        ghost_last = (
            2 * last[0] - second_last[0],
            2 * last[1] - second_last[1],
            2 * last[2] - second_last[2],
        )

        centers = [ghost_first, *centers, ghost_last]

        if isinstance(radius, Sequence):
            radius = [radius[0], *radius, radius[-1]]

        super().__init__(centers, radius, *attrs, **kwargs)


class Cuboid(Shape):
    nargs: ClassVar[int] = 2

    def __init__(
        self,
        center: Point,
        size: tuple[float, float, float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        center, size = self.args
        half_x, half_y, half_z = size[0] / 2, size[1] / 2, size[2] / 2
        corner1 = (center[0] - half_x, center[1] - half_y, center[2] - half_z)
        corner2 = (center[0] + half_x, center[1] + half_y, center[2] + half_z)
        return str(Box(corner1, corner2, *self.attrs))


class Cube(Shape):
    nargs: ClassVar[int] = 2

    def __init__(self, center: Point, size: float, *attrs: Any, **kwargs: Any) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        center, size = self.args
        half = size / 2
        corner1 = (center[0] - half, center[1] - half, center[2] - half)
        corner2 = (center[0] + half, center[1] + half, center[2] + half)
        return str(Box(corner1, corner2, *self.attrs))
