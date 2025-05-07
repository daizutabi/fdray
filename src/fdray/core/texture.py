from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import fdray.utils.image

from .base import Descriptor, Map, Transformable

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from typing import Self

    from numpy.typing import NDArray
    from PIL.Image import Image

    from fdray.typing import ColorLike


class Texture(Transformable):
    pass


class InteriorTexture(Transformable):
    pass


class TextureMap(Map):
    cls = Texture


class Pigment(Transformable):
    @classmethod
    def uv_mapping(
        cls,
        data: str | Path | NDArray | Image,
        interpolate: int = 2,
    ) -> Self:
        if isinstance(data, str | Path):
            path = Path(data).as_posix()
        else:
            path = fdray.utils.image.save(data).as_posix()

        return cls(f'uv_mapping image_map {{ png "{path}" interpolate {interpolate} }}')


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

    ambient: float | ColorLike | None = None
    emission: float | ColorLike | None = None
    diffuse: float | None = None
    brilliance: float | None = None
    phong: float | None = None
    phong_size: float | None = None
    specular: float | None = None
    roughness: float | None = None
    metallic: float | None = None
    reflection: float | ColorLike | None = None
