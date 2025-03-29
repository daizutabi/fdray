from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .base import Descriptor

if TYPE_CHECKING:
    from fdray.typing import ColorLike


@dataclass
class Interior(Descriptor):
    """POV-Ray interior descriptor."""

    ior: float | None = None  # Index of Refraction
    caustics: float | None = None
    dispersion: float | None = None
    dispersion_samples: int | None = None
    fade_distance: float | None = None
    fade_power: float | None = None
    fade_color: ColorLike | None = None
