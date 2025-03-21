from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


def convert(arg: Any) -> str:
    if isinstance(arg, tuple):
        if len(arg) == 2:
            return f"{to_str(arg[0])} {to_str(arg[1])}"

        arg = ", ".join(to_str(x) for x in arg)
        return f"<{arg}>"

    return str(arg)


def to_str(arg: Any) -> str:
    if isinstance(arg, float):
        return f"{arg:.5g}"

    return str(arg)
