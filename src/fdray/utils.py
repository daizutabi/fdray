from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


def convert(arg: Any) -> str:
    if isinstance(arg, tuple):
        if len(arg) == 2:
            return f"{arg[0]} {arg[1]}"

        arg = ", ".join(str(x) for x in arg)
        return f"<{arg}>"

    return str(arg)
