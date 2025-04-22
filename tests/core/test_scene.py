def test_global_settings():
    from fdray.core.scene import GlobalSettings

    x = GlobalSettings(assumed_gamma=0.2)
    assert str(x) == "global_settings { assumed_gamma 0.2 }"


def test_include():
    from fdray.core.scene import Include

    x = Include("a", "b", "c")
    assert str(x) == '#include "a"\n#include "b"\n#include "c"'


def test_scene_attrs():
    from fdray.core.scene import Scene

    x = Scene("abc", ["def", "ghi"])
    assert x.attrs == ["abc", "def", "ghi"]


def test_scene_global_settings():
    from fdray.core.scene import GlobalSettings, Scene

    x = Scene(GlobalSettings(assumed_gamma=0.2), "a", ["b", "c"])
    assert x.attrs == ["a", "b", "c"]
    assert x.global_settings
    assert x.global_settings.assumed_gamma == 0.2


def test_scene_include():
    from fdray.core.scene import Include, Scene

    x = Scene(Include("a", "b", "c"))
    assert x.includes[0].filenames == ["a", "b", "c"]


def test_scene_str():
    from fdray.core.scene import Scene

    x = str(Scene("a", ["b", "c"]))
    assert x.startswith("#version 3.7;\n")
    assert "global_settings { assumed_gamma " in x
    assert x.endswith("\na\nb\nc")


def test_scene_to_str_without_camera():
    from fdray.core.scene import Scene

    x = Scene("a", ["b", "c"])
    assert "a\nb\nc" in x.to_str(100, 100)


def test_scene_format():
    from fdray.core.base import Declare
    from fdray.core.object import Object, Sphere
    from fdray.core.scene import Scene

    x = Scene(Object(Declare(Sphere(1, 1))).scale(1))
    x = f"{x}"
    assert "#declare SPHERE =\nsphere {\n  1, 1\n};\n" in x
    assert "object {\n  SPHERE scale 1\n}" in x


def test_scene_html():
    from fdray.core.scene import Scene

    x = Scene("a", ["b", "c"])._repr_html_()
    assert x.startswith("<div>")
    assert '<span class="n">a</span>' in x
    assert '<span class="n">b</span>' in x
    assert '<span class="n">c</span>' in x
    assert x.endswith("</div>")


def test_scene_render():
    from fdray.core.base import Declare
    from fdray.core.object import Object, Sphere
    from fdray.core.scene import Scene

    s = Scene(Object(Declare(Sphere(1, 1))).scale(1))
    assert s.render(100, 100)


def test_scene_render_trim():
    from fdray.core.camera import Camera
    from fdray.core.color import Color
    from fdray.core.object import Sphere
    from fdray.core.scene import Scene

    s = Scene(Camera(30, 20, view_scale=3), Sphere(0, 1, Color("red")))
    x = s.render(100, 100, trim=True)
    assert x.size == (34, 34)


def test_scene_add():
    from fdray.core.scene import Scene

    x = Scene("abc", ["def", "ghi"])
    y = x.add("xyz")
    assert x.attrs == ["abc", "def", "ghi"]
    assert y.attrs == ["abc", "def", "ghi", "xyz"]
