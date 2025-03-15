from __future__ import annotations

from typing import TYPE_CHECKING

from fdray.elements import Camera, Element

if TYPE_CHECKING:
    from collections.abc import Iterable


class Scene:
    """A scene is a collection of elements."""

    camera: Camera
    elements: list[Element]

    def __init__(self, camera: Camera, *elements: Element | Iterable[Element]) -> None:
        self.camera = camera
        self.elements = []

        for element in elements:
            if isinstance(element, Element):
                self.elements.append(element)
            else:
                self.elements.extend(element)

    def __str__(self) -> str:
        return "\n".join(str(e) for e in [self.camera, *self.elements])
