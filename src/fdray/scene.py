from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .attributes import Attribute
from .colors import Color

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

    from .typing import RGB, RGBA, Point, Vector


@dataclass
class Camera(Attribute):
    location: Point = (0, 0, 0)
    look_at: Point = (0, 0, 0)
    angle: float = 45
    up: Vector | None = None
    right: Vector | None = None
    orthographic: bool = True

    def set_aspect_ratio(self, width: float, height: float) -> None:
        if self.up is None and self.right is None:
            aspect_ratio = width / height
            up = self.get_view_height()
            right = up * aspect_ratio
            self.up = (0, float(f"{up:.5g}"), 0)
            self.right = (float(f"{right:.5g}"), 0, 0)

    def get_view_height(self) -> float:
        it = zip(self.location, self.look_at, strict=True)
        distance = sum((a - b) ** 2 for a, b in it) ** 0.5
        scale = 0.7071 / math.tan(math.radians(65.5 / 2))
        return 2 * distance * scale * math.tan(math.radians(self.angle / 2))

    def __iter__(self) -> Iterator[str]:
        if self.orthographic:
            yield "orthographic"

        # with self.none("orthographic", self.orthographic and "angle"):
        with self.none("orthographic"):
            yield from super().__iter__()


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
