from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .camera import Camera
from .color import Color
from .core import Declare, Descriptor

if TYPE_CHECKING:
    from typing import Any

    from PIL import Image

    from .typing import ColorLike, Point
    from .vector import Vector


@dataclass
class LightSource(Descriptor):
    location: Point | Vector | str
    color: ColorLike | Color | None = None
    shadowless: bool = False
    fade_distance: float | None = None
    fade_power: float | None = None

    def __post_init__(self) -> None:
        if self.color and not isinstance(self.color, Color):
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
class GlobalSettings(Descriptor):
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
    includes: list[Include]
    global_settings: GlobalSettings | None = None

    def __init__(self, *attrs: Any) -> None:
        self.attrs = []
        self.includes = []

        for attr in attrs:
            if isinstance(attr, GlobalSettings):
                self.global_settings = attr
            elif isinstance(attr, Include):
                self.includes.append(attr)
            elif isinstance(attr, Sequence):
                self.attrs.extend(attr)
            else:
                self.attrs.append(attr)

        if self.global_settings is None:
            self.global_settings = GlobalSettings()

    def __str__(self) -> str:
        Declare.clear()
        version = f"#version {self.version};"
        includes = (str(include) for include in self.includes)
        attrs = [str(attr) for attr in (self.global_settings, *self.attrs)]  # must list
        attrs = (version, *includes, *Declare.iter_strs(), *attrs)
        return "\n".join(attr for attr in attrs)

    @property
    def camera(self) -> Camera | None:
        """Get the camera from the scene."""
        for attr in self.attrs:
            if isinstance(attr, Camera):
                return attr

        return None

    def to_str(self, width: int, height: int) -> str:
        """Render the scene with the given image dimensions."""
        if (camera := self.camera) is None:
            return str(self)

        with camera.set(aspect_ratio=width / height):
            return str(self)

    def render(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> Image.Image:
        """Render the scene with the given image dimensions."""
        from .renderer import Renderer

        return Renderer(width, height).render(self, return_image=True)
