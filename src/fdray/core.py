from __future__ import annotations

from contextlib import contextmanager
from dataclasses import MISSING, dataclass, fields
from typing import TYPE_CHECKING, ClassVar

from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self

    from fdray.typing import Vector


class Base:
    @property
    def name(self) -> str:
        return to_snake_case(self.__class__.__name__)

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name} {{ {' '.join(self)} }}"


@dataclass
class Attribute:
    name: str
    value: Any

    def __str__(self) -> str:
        if self.value is None or self.value is False:
            return ""

        if self.value is True:
            return self.name

        return f"{self.name} {convert(self.value)}"


class Element(Base):
    nargs: ClassVar[int] = 0
    args: list[Any]
    attrs: list[Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = list(args[: self.nargs])
        attrs = (Attribute(k, v) for k, v in kwargs.items() if v)
        self.attrs = [*args[self.nargs :], *attrs]

    def __iter__(self) -> Iterator[str]:
        if self.args:
            yield ", ".join(convert(arg) for arg in self.args)

        attrs = (str(attr) for attr in self.attrs)
        yield from (attr for attr in attrs if attr)

    def add(self, *args: Any, **kwargs: Any) -> Self:
        attrs = self.attrs[:]

        for other in args:
            if isinstance(other, list | tuple):
                attrs.extend(other)
            else:
                attrs.append(other)

        def predicate(attr: Any) -> bool:
            if not isinstance(attr, Attribute):
                return True

            return attr.name not in kwargs

        attrs = (attr for attr in attrs if predicate(attr))
        return self.__class__(*self.args, *attrs, **kwargs)


@dataclass
class Descriptor(Base):
    def __iter__(self) -> Iterator[str]:
        """Iterate over the attribute."""
        for field in fields(self):
            value = getattr(self, field.name)
            if value is True:
                yield field.name
            elif value is not None and value is not False:
                if field.default != MISSING or field.default_factory != MISSING:
                    yield field.name
                yield convert(value)

    @contextmanager
    def set(self, **kwargs: Any) -> Iterator[None]:
        """A context manager to set attributes."""
        values = [getattr(self, name) for name in kwargs]
        for name, value in kwargs.items():
            setattr(self, name, value)
        try:
            yield
        finally:
            for name, value in zip(kwargs, values, strict=True):
                setattr(self, name, value)


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
