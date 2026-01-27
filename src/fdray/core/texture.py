from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import fdray.utils.image

from .base import Descriptor, Map, Transformable

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from numpy.typing import NDArray
    from PIL.Image import Image

    from fdray.typing import ColorLike


class Texture(Transformable):
    pass


class InteriorTexture(Transformable):
    pass


class TextureMap(Map):
    cls: type = Texture


class Pigment(Transformable):
    @classmethod
    def uv_mapping(
        cls,
        data: str | Path | NDArray[Any] | Image,
        interpolate: int = 2,
    ) -> Self:
        """Create a UV mapping pigment from image data.

        Args:
            data (str | Path | NDArray | Image): The image data. Can be a file path,
                NumPy array, or PIL Image.
            interpolate (int, optional): The interpolation method. Defaults to 2.
                0: none, 1: linear, 2: bilinear, 3: trilinear, 4: bicubic.

        Returns:
            Self: A Pigment instance with UV mapping.

        Raises:
            FileNotFoundError: If the image file does not exist.
            ValueError: If the interpolation value is invalid.
        """
        if not 2 <= interpolate <= 4:
            msg = "interpolate must be between 2 and 4"
            raise ValueError(msg)

        if isinstance(data, str | Path):
            path = Path(data).as_posix()
        else:
            path = fdray.utils.image.save(data).as_posix()  # pyright: ignore[reportUnknownMemberType]

        attr = f'uv_mapping image_map {{ png "{path}" interpolate {interpolate} }}'
        return cls(attr)


class PigmentMap(Map):
    cls: type = Pigment


class Normal(Transformable):
    pass


class NormalMap(Map):
    cls: type = Normal


class SlopeMap(Map):
    def __init__(self, *args: tuple[float, Sequence[float]]) -> None:  # pyright: ignore[reportMissingSuperCall]
        self.args = list(args)  # pyright: ignore[reportUnannotatedClassAttribute]

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
