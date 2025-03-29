from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Any


def to_snake_case(name: str) -> str:
    result = ""

    for i, char in enumerate(name):
        if i > 0 and char.isupper():
            result += "_"
        result += char.lower()

    return result


def to_str(arg: Any) -> str:
    if isinstance(arg, float):
        if abs(arg) < 1e-5:
            return "0"

        return f"{arg:.5g}"

    return str(arg)


def convert(arg: Any) -> str:
    if isinstance(arg, list | tuple | np.ndarray):
        if len(arg) == 2:
            return f"{to_str(arg[0])} {to_str(arg[1])}"

        arg = ", ".join(to_str(x) for x in arg)
        return f"<{arg}>"

    return str(arg)
