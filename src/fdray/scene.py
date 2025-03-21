from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .attributes import Attribute
from .camera import Camera
from .color import Color

if TYPE_CHECKING:
    from typing import Any

    from .typing import ColorLike, Point


@dataclass
class LightSource(Attribute):
    location: Point
    color: ColorLike
    shadowless: bool = False
    fade_distance: float | None = None
    fade_power: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.color, Color):
            self.color = Color(self.color)

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


class Include:
    filenames: list[str]

    def __init__(self, *filenames: str) -> None:
        self.filenames = list(filenames)

    def __str__(self) -> str:
        return "\n".join(f'#include "{filename}"' for filename in self.filenames)


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

    @property
    def camera(self) -> Camera | None:
        """Get the camera from the scene."""
        for attr in self.attrs:
            if isinstance(attr, Camera):
                return attr

        return None

    def render(self, width: int, height: int) -> str:
        """Render the scene with the given image dimensions."""
        if (camera := self.camera) is None:
            return str(self)

        with camera.set(aspect_ratio=width / height):
            return str(self)
