from __future__ import annotations

import textwrap
from abc import ABC
from typing import TYPE_CHECKING, ClassVar

from .attributes import Transform
from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self


class Transformable(ABC):
    nargs: ClassVar[int] = 0
    args: list[Any]
    attrs: list[Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = list(args[: self.nargs])
        attrs = (k for k, v in kwargs.items() if v)
        self.attrs = [*attrs, *args[self.nargs :]]

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

    def add(self, *others: Any) -> Self:
        attrs = []
        for other in others:
            if isinstance(other, list | tuple):
                attrs.extend(other)
            else:
                attrs.append(other)

        return self.__class__(*self.args, *self.attrs, *attrs)

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Scale the object uniformly or non-uniformly.

        Args:
            x: Scale factor. If y and z are None, scales uniformly.
            y: Scale factor for y-axis. If None, uses x for uniform scaling.
            z: Scale factor for z-axis. If None, uses x for uniform scaling.

        Returns:
            New object with the scaling transformation applied.
        """
        if y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(self, x: float, y: float, z: float) -> Self:
        """Rotate the object around the x, y, and z axes.

        Args:
            x: Rotation angle in degrees around the x-axis.
            y: Rotation angle in degrees around the y-axis.
            z: Rotation angle in degrees around the z-axis.

        Returns:
            New object with the rotation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(self, x: float, y: float, z: float) -> Self:
        """Translate the object along the x, y, and z axes.

        Args:
            x: Translation distance along the x-axis.
            y: Translation distance along the y-axis.
            z: Translation distance along the z-axis.

        Returns:
            New object with the translation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))
