from __future__ import annotations

from typing import TypeAlias

Point: TypeAlias = tuple[float, float, float]
Vector: TypeAlias = tuple[float, float, float]
RGB: TypeAlias = tuple[float, float, float]
RGBA: TypeAlias = tuple[float, float, float, float]
ColorLike: TypeAlias = str | RGB | RGBA
