import re

import pytest

from fdray.core.texture import Pigment
from fdray.utils.format import format_code


@pytest.mark.parametrize("text", ["Hello, world!", "Hello,\nworld!"])
def test_format_code_no_break(text: str):
    assert format_code(text) == text


def test_format_code_delete_newline():
    assert format_code("Hello, world!\n") == "Hello, world!"


def test_format_code_bracket():
    assert format_code("Hello, { world }!") == "Hello, {\n  world\n}\n!"


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("", []),
        ("[a] [b]", ["[a]", "[b]"]),
        ("abc", ["abc"]),
        ("a}{bc", ["a}{bc"]),
        ("{abc}", ["{", "  abc", "}"]),
        ("a {b} c", ["a {", "  b", "}", "c"]),
        ("a b { c } d", ["a", "b {", "  c", "}", "d"]),
        ("a b { c };", ["a", "b {", "  c", "};"]),
    ],
)
def test_iter_lines(line: str, expected):
    from fdray.utils.format import iter_lines

    assert list(iter_lines(line)) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("a b { c d } e", ("a b", "c d", "e")),
        ("a { b } { c d } e", ("a", "b", "{ c d } e")),
        ("a { b { c d } } e", ("a", "b { c d }", "e")),
        ("a { b ", ("a { b", "", "")),
        ("a b ", ("a b", "", "")),
    ],
)
def test_split_line(line: str, expected):
    from fdray.utils.format import split_line

    assert split_line(line) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("[a] [b]", ["[a]", "[b]"]),
        ("[a[b]] [c]", ["[a[b]]", "[c]"]),
        (" [a]  [b] ", ["[a]", "[b]"]),
        (" [a  b ", []),
        ("x [a] y [b] z", ["[a]", "[b]"]),
    ],
)
def test_iter_maps(line: str, expected):
    from fdray.utils.format import iter_maps

    assert list(iter_maps(line)) == expected


@pytest.fixture
def pigment():
    from fdray.core.color import ColorMap

    a = Pigment("granite", ColorMap((0, "red { d }"), (0.9, "white")))
    b = Pigment("granite", ColorMap((0, "blue"), (0.9, "white")))
    return Pigment("checker", a, b).scale(0.5)


def test_pigment_map(pigment: Pigment):
    x = f"{pigment}"
    assert "      [0 red { d }]\n      [0.9 white]\n" in x


def test_pigment_compare(pigment: Pigment):
    assert re.sub(r"[ \n]+", " ", f"{pigment}") == str(pigment)
