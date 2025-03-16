from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .colors import Color
from .utils import convert

if TYPE_CHECKING:
    from typing import Any

    from .typing import Point


class Shape(ABC):
    args: list[Any]
    attrs: list[Any] | None = None

    def __init__(self, args: list[Any], *attrs: Any) -> None:
        self.args = args
        if attrs:
            self.attrs = [convert_attribute(attr) for attr in attrs]

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __str__(self) -> str:
        args = ", ".join(convert(arg) for arg in self.args)

        if self.attrs:
            attrs = "\n".join(f"  {attr}" for attr in self.attrs)
            return f"{self.name} {{\n  {args}\n{attrs}\n}}"

        return f"{self.name} {{ {args} }}"


def convert_attribute(attr: Any) -> Any:
    if isinstance(attr, str | tuple):
        try:
            return Color(attr)
        except ValueError:
            return attr
    return attr


class Sphere(Shape):
    def __init__(self, center: Point, radius: float, *attrs: Any) -> None:
        super().__init__([center, radius], *attrs)
