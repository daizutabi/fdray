from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .core import Descriptor, Element
from .utils import convert

if TYPE_CHECKING:
    from typing import Self

    from fdray.typing import Vector


@dataclass
class Transform(Descriptor):
    """POV-Ray transformation attributes."""

    scale: Vector | float | None = None
    rotate: Vector | None = None
    translate: Vector | None = None

    def __str__(self) -> str:
        if self.scale is not None and self.rotate is None and self.translate is None:
            return f"scale {convert(self.scale)}"

        if self.scale is None and self.rotate is not None and self.translate is None:
            return f"rotate {convert(self.rotate)}"

        if self.scale is None and self.rotate is None and self.translate is not None:
            return f"translate {convert(self.translate)}"

        return super().__str__()


class Transformable(Element):
    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Scale the object uniformly or non-uniformly.

        Args:
            x: Scale factor. If y and z are None, scales uniformly.
            y: Scale factor for y-axis. If None, uses x for uniform scaling.
            z: Scale factor for z-axis. If None, uses x for uniform scaling.

        Returns:
            New object with the scaling transformation applied.
        """
        if y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(self, x: float, y: float, z: float) -> Self:
        """Rotate the object around the x, y, and z axes.

        Args:
            x: Rotation angle in degrees around the x-axis.
            y: Rotation angle in degrees around the y-axis.
            z: Rotation angle in degrees around the z-axis.

        Returns:
            New object with the rotation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(self, x: float, y: float, z: float) -> Self:
        """Translate the object along the x, y, and z axes.

        Args:
            x: Translation distance along the x-axis.
            y: Translation distance along the y-axis.
            z: Translation distance along the z-axis.

        Returns:
            New object with the translation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))
