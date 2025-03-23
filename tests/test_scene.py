def test_light_source_color_color():
    from fdray.color import Color
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), Color("red"))
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> }"


def test_light_source_color_str():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), "blue")
    assert str(x) == "light_source { <1, 2, 3> color rgb <0, 0, 1> }"


def test_light_source_color_tuple():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3))
    assert "rgb <0.1, 0.2, 0.3>" in str(x)


def test_spotlight():
    from fdray.scene import Spotlight

    x = Spotlight((1, 2, 3), "red")
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> spotlight }"


def test_global_settings():
    from fdray.scene import GlobalSettings

    x = GlobalSettings(assumed_gamma=0.2)
    assert str(x) == "global_settings { assumed_gamma 0.2 }"


def test_include():
    from fdray.scene import Include

    x = Include("a", "b", "c")
    assert str(x) == '#include "a"\n#include "b"\n#include "c"'


def test_scene_attrs():
    from fdray.scene import Scene

    x = Scene("a", ["b", "c"])
    assert x.attrs == ["a", "b", "c"]


def test_scene_global_settings():
    from fdray.scene import GlobalSettings, Scene

    x = Scene(GlobalSettings(assumed_gamma=0.2), "a", ["b", "c"])
    assert x.attrs == ["a", "b", "c"]
    assert x.global_settings
    assert x.global_settings.assumed_gamma == 0.2


def test_scene_include():
    from fdray.scene import Include, Scene

    x = Scene(Include("a", "b", "c"))
    assert x.includes[0].filenames == ["a", "b", "c"]


def test_scene_str():
    from fdray.scene import Scene

    x = str(Scene("a", ["b", "c"]))
    assert x.startswith("#version 3.7;\n")
    assert "global_settings { assumed_gamma " in x
    assert x.endswith("\na\nb\nc")


def test_scene_to_str_without_camera():
    from fdray.scene import Scene

    x = Scene("a", ["b", "c"])
    assert "a\nb\nc" in x.to_str(100, 100)


def test_scene_format():
    from fdray.core import Declare
    from fdray.object import Object, Sphere
    from fdray.scene import Scene

    x = Scene(Object(Declare(Sphere(1, 1))).scale(1))
    x = f"{x}"
    assert "#declare SPHERE =\nsphere {\n  1, 1\n};\n" in x
    assert "object {\n  SPHERE scale 1\n}" in x


def test_scene_render():
    from fdray.core import Declare
    from fdray.object import Object, Sphere
    from fdray.scene import Scene

    s = Scene(Object(Declare(Sphere(1, 1))).scale(1))
    assert s.render(100, 100)
