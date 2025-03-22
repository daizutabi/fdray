from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fdray.attribute import Attribute
from fdray.transformable import Transformable

if TYPE_CHECKING:
    from collections.abc import Iterator


class Pigment(Transformable):
    pass


class PigmentMap:
    pigments: list[tuple[float, Pigment | str]]

    def __init__(self, *pigments: tuple[float, Pigment | str]) -> None:
        self.pigments = list(pigments)

    def __iter__(self) -> Iterator[str]:
        for k, pigment in self.pigments:
            if isinstance(pigment, Pigment):
                yield f"[{k} {' '.join(pigment)}]"
            else:
                yield f"[{k} {pigment}]"

    def __str__(self) -> str:
        return f"pigment_map {{ {' '.join(self)} }}"


@dataclass
class Finish(Attribute):
    """POV-Ray finish attributes."""

    ambient: float | None = None
    diffuse: float | None = None
    phong: float | None = None
    phong_size: float | None = None
    reflection: float | None = None
    specular: float | None = None
    roughness: float | None = None


@dataclass
class Interior(Attribute):
    """POV-Ray interior attributes."""

    ior: float | None = None  # Index of Refraction
    caustics: float | None = None
    fade_distance: float | None = None
    fade_power: float | None = None
