from __future__ import annotations

from typing import TYPE_CHECKING

from fdray.transformable import Transformable

if TYPE_CHECKING:
    from collections.abc import Iterator


class Pigment(Transformable):
    pass


class PigmentMap:
    pigments: list[tuple[float, Pigment | str]]

    def __init__(self, *pigments: tuple[float, Pigment | str]) -> None:
        self.pigments = list(pigments)

    def __iter__(self) -> Iterator[str]:
        for k, pigment in self.pigments:
            if isinstance(pigment, Pigment):
                yield f"[{k} {' '.join(pigment)}]"
            else:
                yield f"[{k} {pigment}]"

    def __str__(self) -> str:
        return f"pigment_map {{ {' '.join(self)} }}"
