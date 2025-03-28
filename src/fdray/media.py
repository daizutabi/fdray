from __future__ import annotations

from dataclasses import dataclass

from .core import Descriptor


@dataclass
class Interior(Descriptor):
    """POV-Ray interior attributes."""

    ior: float | None = None  # Index of Refraction
    caustics: float | None = None
    fade_distance: float | None = None
    fade_power: float | None = None
