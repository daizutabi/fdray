from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import MISSING, dataclass, fields
from math import degrees
from typing import TYPE_CHECKING, Any, ClassVar

from fdray.utils.format import format_code, to_html
from fdray.utils.string import convert, to_snake_case
from fdray.utils.vector import Vector

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import Any, Self

    from fdray.typing import Point


class Base:
    @property
    def name(self) -> str:
        return to_snake_case(self.__class__.__name__)

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name} {{ {' '.join(self)} }}"

    def __format__(self, format_spec: str) -> str:
        return format_code(str(self))

    def _repr_html_(self) -> str:
        return to_html(str(self))


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


class Map(Base):
    cls: ClassVar[type]
    args: list[tuple[Any, Any]]

    def __init__(self, *args: Iterable[Any]) -> None:
        self.args = []
        for arg in args:
            if isinstance(arg, dict):
                self.args.extend(arg.items())
            else:
                self.args.append(tuple(arg))

    def __iter__(self) -> Iterator[str]:
        for k, arg in self.args:
            if isinstance(arg, self.cls):
                yield f"[{convert(k)} {' '.join(arg)}]"
            else:
                yield f"[{convert(k)} {convert(arg)}]"


class IdGenerator:
    """Generate unique identifiers for objects."""

    counters: ClassVar[dict[str, int]] = {}

    @classmethod
    def clear(cls) -> None:
        """Clear the counters."""
        cls.counters.clear()

    @classmethod
    def generate(cls, value: Any, name: str | None = None) -> str:
        """Generate a unique identifier for an object."""
        if name is None:
            name = str(value.__class__.__name__.upper())

        if name not in cls.counters:
            cls.counters[name] = 0
            return name

        cls.counters[name] += 1

        return f"{name}_{cls.counters[name]}"


class Declare:
    name: str
    value: Any
    declarations: ClassVar[dict[str, Self]] = {}

    def __init__(self, value: Any, name: str | None = None) -> None:
        self.name = IdGenerator.generate(value, name)
        self.value = value

    @classmethod
    def clear(cls) -> None:
        """Clear the members."""
        IdGenerator.clear()
        cls.declarations.clear()

    @classmethod
    def add(cls, member: Self) -> None:
        cls.declarations.setdefault(member.name, member)

    def __str__(self) -> str:
        self.__class__.add(self)
        return self.name

    def to_str(self) -> str:
        return f"#declare {self.name} = {self.value!s};"

    @classmethod
    def iter_strs(cls) -> Iterator[str]:
        yield from (m.to_str() for m in cls.declarations.values())


@dataclass
class Descriptor(Base):
    def __iter__(self) -> Iterator[str]:
        """Iterate over the descriptor."""
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
    """POV-Ray transformation descriptor."""

    scale: Point | None = None
    rotate: Point | None = None
    translate: Point | None = None

    def __str__(self) -> str:
        if self.scale is not None and self.rotate is None and self.translate is None:
            return f"scale {convert(self.scale)}"

        if self.scale is None and self.rotate is not None and self.translate is None:
            return f"rotate {convert(self.rotate)}"

        if self.scale is None and self.rotate is None and self.translate is not None:
            return f"translate {convert(self.translate)}"

        return super().__str__()


class Transformable(Element):
    def scale(
        self,
        x: float | str,
        y: float | None = None,
        z: float | None = None,
    ) -> Self:
        """Scale the object uniformly or non-uniformly.

        Args:
            x: Scale factor. If y and z are None, scales uniformly.
            y: Scale factor for y-axis. If None, uses x for uniform scaling.
            z: Scale factor for z-axis. If None, uses x for uniform scaling.

        Returns:
            New object with the scaling transformation applied.
        """
        if isinstance(x, str) or y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(
        self,
        x: float | str,
        y: float | None = None,
        z: float | None = None,
    ) -> Self:
        """Rotate the object around the x, y, and z axes.

        Args:
            x: Rotation angle in degrees around the x-axis.
            y: Rotation angle in degrees around the y-axis.
            z: Rotation angle in degrees around the z-axis.

        Returns:
            New object with the rotation transformation applied.
        """
        if isinstance(x, str) or y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(rotate=x))

        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(
        self,
        x: float | str,
        y: float | None = None,
        z: float | None = None,
    ) -> Self:
        """Translate the object along the x, y, and z axes.

        Args:
            x: Translation distance along the x-axis.
            y: Translation distance along the y-axis.
            z: Translation distance along the z-axis.

        Returns:
            New object with the translation transformation applied.
        """
        if isinstance(x, str) or y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(translate=x))

        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))

    def align(self, direction: Vector | Iterable[float]) -> Self:
        if not isinstance(direction, Vector):
            direction = Vector(*direction)

        phi, theta = direction.to_spherical()
        return self.rotate(0, -degrees(theta), degrees(phi))
