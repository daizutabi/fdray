from __future__ import annotations

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
    location: Point | str
    color: ColorLike | None = None
    shadowless: bool = False
    fade_distance: float | None = None
    fade_power: float | None = None

    def __post_init__(self) -> None:
        if self.color and not isinstance(self.color, Color):
            self.color = Color(self.color)

    @property
    def name(self) -> str:
        return "light_source"

    def to_str(self, camera: Camera | None) -> str:
        return str(self)


@dataclass
class Spotlight(LightSource):
    spotlight: bool = True
    radius: float | None = None
    falloff: float | None = None
    tightness: float | None = None
    point_at: Point | None = None
