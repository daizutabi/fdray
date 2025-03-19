from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .attributes import Attribute
from .colors import Color

if TYPE_CHECKING:
    from typing import Any

    from .typing import RGB, RGBA, Point, Vector


@dataclass
class Camera(Attribute):
    location: Point = (0, 0, 0)
    look_at: Point = (0, 0, 0)
    angle: float | None = None
    up: Vector | None = None
    right: Vector | None = None
    orthographic: bool = True

    def set_aspect_ratio(self, width: int, height: int) -> None:
        if self.up is None and self.right is None:
            aspect_ratio = float(f"{width / height:.5g}")
            self.up = (0, 1, 0)
            self.right = (aspect_ratio, 0, 0)


@dataclass
class LightSource(Attribute):
    location: Point
    color: Color | str | RGB | RGBA | None = None
    shadowless: bool = False
    fade_distance: float | None = None
    fade_power: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.color, Color):
            c = self.color
            self.color = Color((c.red, c.green, c.blue), alpha=c.alpha, pigment=False)
        elif self.color is not None:
            self.color = Color(self.color, pigment=False)

    @property
    def name(self) -> str:
        return "light_source"


@dataclass
class Spotlight(LightSource):
    spotlight: bool = True
    radius: float | None = None
    falloff: float | None = None
    tightness: float | None = None
    point_at: Point | None = None


@dataclass
class GlobalSettings(Attribute):
    assumed_gamma: float = 1

    @property
    def name(self) -> str:
        return "global_settings"


class Scene:
    """A scene is a collection of elements."""

    attrs: list[Any]
    version: str = "3.7"
    global_settings: GlobalSettings | None = None

    def __init__(self, *attrs: Any) -> None:
        self.attrs = []

        for attr in attrs:
            if isinstance(attr, GlobalSettings):
                self.global_settings = attr
            elif isinstance(attr, list | tuple):
                self.attrs.extend(attr)
            else:
                self.attrs.append(attr)

        if self.global_settings is None:
            self.global_settings = GlobalSettings()

    def __str__(self) -> str:
        version = f"#version {self.version};"
        attrs = [version, self.global_settings, *self.attrs]
        return "\n".join(str(attr) for attr in attrs if attr is not None)

    def set_aspect_ratio(self, width: int, height: int) -> None:
        for attr in self.attrs:
            if isinstance(attr, Camera):
                attr.set_aspect_ratio(width, height)
                break
