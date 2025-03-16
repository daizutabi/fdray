from __future__ import annotations

from dataclasses import MISSING, dataclass, fields
from typing import TYPE_CHECKING

from .utils import convert

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .typing import Scale, Vector


@dataclass
class Attribute:
    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __iter__(self) -> Iterator[str]:
        for field in fields(self):
            value = getattr(self, field.name)
            if value is True:
                yield field.name
            elif value is not None and value is not False:
                if field.default != MISSING or field.default_factory != MISSING:
                    yield field.name
                yield convert(value)

    def __str__(self) -> str:
        return f"{self.name} {{ {' '.join(self)} }}"


@dataclass
class Transform(Attribute):
    """POV-Ray transformation attributes."""

    scale: Scale | None = None
    rotate: Vector | None = None
    translate: Vector | None = None


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
