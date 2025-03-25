from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .camera import Camera
from .color import Color
from .core import Descriptor

if TYPE_CHECKING:
    from .camera import Camera
    from .typing import ColorLike, Point


@dataclass
class LightSource(Descriptor):
    location: Point
    color: ColorLike | None = None
    from_camera: bool = True
    shadowless: bool = False
    fade_distance: float | None = None
    fade_power: float | None = None

    def __post_init__(self) -> None:
        if self.color and not isinstance(self.color, Color):
            self.color = Color(self.color)

    @property
    def name(self) -> str:
        return "light_source"

    def __str__(self) -> str:
        with self.set(from_camera=False):
            return super().__str__()

    def to_str(self, camera: Camera | None) -> str:
        if camera is None:
            return str(self)

        if not self.from_camera or isinstance(self.location, str):
            return str(self)

        if not isinstance(self.location, Iterable):
            loc = camera.orbital_location(self.location)
        else:
            loc = camera.orbital_location(*self.location)

        with self.set(location=loc):
            return str(self)


@dataclass
class Spotlight(LightSource):
    spotlight: bool = True
    radius: float | None = None
    falloff: float | None = None
    tightness: float | None = None
    point_at: Point | None = None
