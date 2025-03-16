from __future__ import annotations

import textwrap
from abc import ABC
from typing import TYPE_CHECKING, ClassVar, overload

from .attributes import Transform
from .colors import Color
from .utils import convert

if TYPE_CHECKING:
    from typing import Any, Self

    from .typing import Point


class Shape(ABC):
    nargs: ClassVar[int] = 0
    args: list[Any]
    attrs: list[Any]

    def __init__(self, *args: Any) -> None:
        self.args = list(args[: self.nargs])
        self.attrs = [convert_attribute(attr) for attr in args[self.nargs :]]

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __str__(self) -> str:
        args = ", ".join(convert(arg) for arg in self.args)

        if self.attrs:
            attrs = "\n".join(f"  {attr}" for attr in self.attrs)
            return f"{self.name} {{\n  {args}\n{attrs}\n}}"

        return f"{self.name} {{ {args} }}"

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

    def add(self, other: Any) -> Self:
        return self.__class__(*self.args, *self.attrs, other)

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        if y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(self, x: float, y: float, z: float) -> Self:
        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(self, x: float, y: float, z: float) -> Self:
        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))


def convert_attribute(attr: Any) -> Any:
    if isinstance(attr, str | tuple):
        try:
            return Color(attr)
        except ValueError:
            return attr
    return attr


class Csg(Shape):
    attrs: list[Any]

    def __add__(self, other: Any) -> Self:
        attrs = [*self.attrs, other]
        return self.__class__(*attrs)

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


class Sphere(Shape):
    nargs: ClassVar[int] = 2

    def __init__(self, center: Point, radius: float, *attrs: Any) -> None:
        super().__init__(center, radius, *attrs)
