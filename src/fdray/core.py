from __future__ import annotations

from contextlib import contextmanager
from dataclasses import MISSING, dataclass, fields
from typing import TYPE_CHECKING, ClassVar

from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self


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


class Base:
    @property
    def name(self) -> str:
        return to_snake_case(self.__class__.__name__)

    def __iter__(self) -> Iterator[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name} {{ {' '.join(self)} }}"


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
