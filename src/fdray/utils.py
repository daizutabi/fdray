from __future__ import annotations

from typing import Any


def convert(arg: Any) -> str:
    if isinstance(arg, dict):
        return " ".join(f"{k} {convert(v)}" for k, v in arg.items())

    if isinstance(arg, list | tuple):
        arg = ", ".join(str(x) for x in arg)
        return f"<{arg}>"

    return str(arg)
