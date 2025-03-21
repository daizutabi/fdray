from __future__ import annotations

import textwrap
from abc import ABC
from typing import TYPE_CHECKING, ClassVar, overload

from .attributes import Transform
from .colors import Color
from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self

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

    def __str__(self) -> str:
        attrs = "\n".join(str(attr) for attr in self.attrs)
        attrs = textwrap.indent(attrs, "  ")
        return f"{self.name} {{\n{attrs}\n}}"


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
