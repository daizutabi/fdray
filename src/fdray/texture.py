from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fdray.core import Map

from .core import Descriptor, Transformable

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence


class Texture(Transformable):
    pass


class Pigment(Transformable):
    pass


class PigmentMap(Map):
    cls = Pigment


class Normal(Transformable):
    pass


class NormalMap(Map):
    cls = Normal


class SlopeMap(Map):
    def __init__(self, *args: tuple[float, Sequence[float]]) -> None:
        self.args = list(args)

    def __iter__(self) -> Iterator[str]:
        for k, arg in self.args:
            yield f"[{k} <{arg[0]:.5g}, {arg[1]:.5g}>]"


@dataclass
class Finish(Descriptor):
    """POV-Ray finish attributes."""

    ambient: float | None = None
    diffuse: float | None = None
    phong: float | None = None
    phong_size: float | None = None
    reflection: float | None = None
    specular: float | None = None
    roughness: float | None = None


@dataclass
class Interior(Descriptor):
    """POV-Ray interior attributes."""

    ior: float | None = None  # Index of Refraction
    caustics: float | None = None
    fade_distance: float | None = None
    fade_power: float | None = None
