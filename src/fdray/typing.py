from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

from .core.color import Color
from .utils.vector import Vector

Point: TypeAlias = float | str | Sequence[float] | Vector
RGB: TypeAlias = tuple[float, float, float]
RGBA: TypeAlias = tuple[float, float, float, float]
ColorLike: TypeAlias = str | RGB | RGBA | Sequence[float] | Color
