from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from fdray.utils.format import format_code, to_html

from .base import Declare, Descriptor
from .camera import Camera
from .light_source import LightSource

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

    from PIL import Image

    from fdray.typing import ColorLike


@dataclass
class GlobalSettings(Descriptor):
    ambient_light: ColorLike | None = None
    assumed_gamma: float = 1


class Include:
    filenames: list[str]

    def __init__(self, *filenames: str) -> None:
        self.filenames = list(filenames)

    def __str__(self) -> str:
        return "\n".join(f'#include "{filename}"' for filename in self.filenames)


class Scene:
    """A scene is a collection of elements."""

    camera: Camera | None
    includes: list[Include]
    light_sources: list[LightSource]
    global_settings: GlobalSettings
    attrs: list[Any]
    version: str = "3.7"

    def __init__(self, *attrs: Any) -> None:
        self.camera = None
        self.includes = []
        self.light_sources = []
        self.global_settings = GlobalSettings()
        self.attrs = []

        for attr in attrs:
            if isinstance(attr, Camera):
                self.camera = attr
            elif isinstance(attr, Include):
                self.includes.append(attr)
            elif isinstance(attr, LightSource):
                self.light_sources.append(attr)
            elif isinstance(attr, GlobalSettings):
                self.global_settings = attr
            elif not isinstance(attr, str) and isinstance(attr, Sequence):
                self.attrs.extend(attr)
            else:
                self.attrs.append(attr)

    def __iter__(self) -> Iterator[str]:
        Declare.clear()
        yield f"#version {self.version};"
        yield from (str(include) for include in self.includes)
        yield str(self.global_settings)
        if self.camera:
            yield str(self.camera)
        yield from (light.to_str(self.camera) for light in self.light_sources)
        attrs = [str(attr) for attr in self.attrs]  # must list to consume Declare
        yield from Declare.iter_strs()  # must be before attrs
        yield from attrs  # finally, yield the attrs

    def __str__(self) -> str:
        return "\n".join(self)

    def __format__(self, format_spec: str) -> str:
        return format_code(str(self))

    def _repr_html_(self) -> str:
        return to_html(str(self))

    def to_str(self, width: int, height: int) -> str:
        """Create a string representation of the scene with the given image dimensions.

        Args:
            width: The width of the image.
            height: The height of the image.

        Returns:
            str: A string representation of the scene.
        """
        if (camera := self.camera) is None:
            return str(self)

        with camera.set(aspect_ratio=width / height):
            return str(self)

    def render(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> Image.Image:
        """Render the scene with the given image dimensions.

        Args:
            width: The width of the image.
            height: The height of the image.

        Returns:
            Image.Image: The rendered image.
        """
        from .renderer import Renderer

        return Renderer(width, height).render(self, return_image=True)
