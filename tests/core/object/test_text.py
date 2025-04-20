from pathlib import Path

from fdray import Text


def test_text_font_file():
    x = Text.set_font_file("a.ttf")
    assert x == "a.ttf"


def test_text_font_file_not_found():
    assert Text.set_font_file("a.otf") is None


def test_text_font_file_by_name():
    from matplotlib import font_manager

    font_files = [Path(f) for f in font_manager.findSystemFonts()]
    font_files = [f for f in font_files if f.suffix == ".ttf"]
    font_spec = font_files[0].stem

    x = Text.set_font_file(font_spec)
    assert x
    assert Path(x).stem == font_spec

    x = Text.set_font_file(font_spec.upper()[:5])
    assert x
    assert Path(x).stem == font_spec
