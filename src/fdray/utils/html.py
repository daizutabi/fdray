from __future__ import annotations

import base64
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from PIL.Image import Image


def encode(image: Image) -> str:
    if data := image._repr_png_():
        return base64.b64encode(data).decode()

    return ""


def to_html_horizontal(images: Iterable[Image], spacing: int = 10) -> str:
    html = f'<div style="display: flex; gap: {spacing}px;">'
    for image in images:
        html += f'<img src="data:image/png;base64,{encode(image)}">'
    html += "</div>"
    return html
