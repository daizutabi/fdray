from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from .color import Color

Point: TypeAlias = tuple[float, float, float]
Vector: TypeAlias = tuple[float, float, float]
RGB: TypeAlias = tuple[float, float, float]
RGBA: TypeAlias = tuple[float, float, float, float]
ColorLike: TypeAlias = "str | RGB | RGBA | Color"
