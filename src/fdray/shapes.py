from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .utils import convert

if TYPE_CHECKING:
    from typing import Any

    from .attributes import Point


class Shape(ABC):
    args: list[Any]
    attrs: list[Any] | None = None

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __str__(self) -> str:
        args = ", ".join(convert(arg) for arg in self.args)

        if self.attrs:
            attrs = "\n".join(f"  {attr}" for attr in self.attrs)
            return f"{self.name} {{\n  {args}\n{attrs}\n}}"

        return f"{self.name} {{ {args} }}"


class Sphere(Shape):
    def __init__(self, center: Point, radius: float, *attrs: Any) -> None:
        self.args = [center, radius]
        if attrs:
            self.attrs = list(attrs)
