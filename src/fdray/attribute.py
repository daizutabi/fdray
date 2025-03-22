from __future__ import annotations

from contextlib import contextmanager
from dataclasses import MISSING, dataclass, fields
from typing import TYPE_CHECKING

from .utils import convert, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any


@dataclass
class Attribute:
    """A base class for all attributes."""

    @property
    def name(self) -> str:
        """The name of the attribute."""
        return to_snake_case(self.__class__.__name__)

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

    def __str__(self) -> str:
        """Convert the attribute to a string."""
        return f"{self.name} {{ {' '.join(self)} }}"

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
