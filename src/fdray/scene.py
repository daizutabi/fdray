from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .camera import Camera
from .core import Declare, Descriptor
from .format import format_code
from .light_source import LightSource

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

    from PIL import Image


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

    includes: list[Include]
    light_sources: list[LightSource]
    global_settings: GlobalSettings
    attrs: list[Any]
    version: str = "3.7"

    def __init__(self, *attrs: Any) -> None:
        self.includes = []
        self.light_sources = []
        self.global_settings = GlobalSettings()
        self.attrs = []

        for attr in attrs:
            if isinstance(attr, Include):
                self.includes.append(attr)
            elif isinstance(attr, LightSource):
                self.light_sources.append(attr)
            elif isinstance(attr, GlobalSettings):
                self.global_settings = attr
            elif not isinstance(attr, str) and isinstance(attr, Sequence):
                self.attrs.extend(attr)
            else:
                self.attrs.append(attr)

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

    def __iter__(self) -> Iterator[str]:
        Declare.clear()
        yield f"#version {self.version};"
        yield from (str(include) for include in self.includes)
        yield str(self.global_settings)
        attrs = [str(attr) for attr in self.attrs]  # must list to consume Declare
        yield from Declare.iter_strs()  # must be before attrs
        yield from attrs

    def __str__(self) -> str:
        return "\n".join(self)

    def __format__(self, format_spec: str) -> str:
        return format_code(str(self))

    def render(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> Image.Image:
        """Render the scene with the given image dimensions."""
        from .renderer import Renderer

        return Renderer(width, height).render(self, return_image=True)
