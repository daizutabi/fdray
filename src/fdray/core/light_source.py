from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .base import Descriptor
from .color import Color

if TYPE_CHECKING:
    from fdray.typing import ColorLike, Point

    from .camera import Camera


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
        if self.from_camera:
            msg = (
                "Cannot convert camera-relative light source to string directly. "
                "Use Scene.to_str() or LightSource.to_str(camera) instead.",
            )
            raise ValueError(msg)

        return super().__str__()

    def to_str(self, camera: Camera | None) -> str:
        if camera is None:
            if self.from_camera:
                msg = (
                    "Camera is required for camera-relative light source. "
                    "Set from_camera=False to use absolute coordinates."
                )
                raise ValueError(msg)

            return super().__str__()

        if not self.from_camera or isinstance(self.location, str):
            loc = self.location
        elif not isinstance(self.location, Iterable):
            loc = camera.orbital_location(self.location)
        else:
            loc = camera.orbital_location(*self.location)

        with self.set(location=loc, from_camera=False):
            return super().__str__()


@dataclass
class Spotlight(LightSource):
    spotlight: bool = True
    radius: float | None = None
    falloff: float | None = None
    tightness: float | None = None
    point_at: Point | None = None
