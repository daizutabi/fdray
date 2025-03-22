from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

Point: TypeAlias = tuple[float, float, float] | float | str | Sequence[float]
Vector: TypeAlias = Point
RGB: TypeAlias = tuple[float, float, float]
RGBA: TypeAlias = tuple[float, float, float, float]
ColorLike: TypeAlias = str | RGB | RGBA | Sequence[float]
