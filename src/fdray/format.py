from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


def format_code(text: str) -> str:
    return "\n".join(iter_codes(text.rstrip()))


def iter_codes(text: str) -> Iterator[str]:
    for line in text.splitlines():
        yield from iter_lines(line)


def iter_lines(line: str, indent: int = 0) -> Iterator[str]:
    if not line:
        return

    ind = " " * indent

    if line.startswith("[") and line.endswith("]"):
        for map_element in iter_maps(line):
            yield ind + map_element
        return

    if "{" not in line or "}" not in line:
        yield ind + line.strip()
        return

    prefix, body, suffix = split_line(line)

    if not body:
        yield ind + prefix
        return

    if " " in prefix:
        pre, prefix = prefix.rsplit(" ", 1)
        yield ind + pre

    if prefix:
        yield ind + prefix + " {"
    else:
        yield ind + "{"

    yield from iter_lines(body, indent + 2)

    if suffix == ";":
        yield ind + "};"
    else:
        yield ind + "}"
        yield from iter_lines(suffix, indent)


def split_line(line: str) -> tuple[str, str, str]:
    start = line.find("{")
    if start == -1:
        return line.strip(), "", ""

    depth = 0
    end = -1

    for i, c in enumerate(line[start + 1 :], start + 1):
        if c == "}":
            if depth == 0:
                end = i
                break
            depth -= 1
        elif c == "{":
            depth += 1

    if end == -1:
        return line.strip(), "", ""

    return line[:start].strip(), line[start + 1 : end].strip(), line[end + 1 :].strip()


def iter_maps(line: str) -> Iterator[str]:
    start = 0
    depth = 0

    for end, c in enumerate(line):
        if c == "]":
            if depth == 1:
                yield line[start : end + 1]
            depth -= 1
        elif c == "[":
            if depth == 0:
                start = end
            depth += 1


def to_html(code: str) -> str:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import PovrayLexer

    code = highlight(
        format_code(code),
        PovrayLexer(),
        HtmlFormatter(cssclass="highlight-ipynb"),
    )

    return f"<div>{code}</div>"
