def test_light_source_color_color():
    from fdray.colors import Color
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), Color("red"))
    assert str(x) == "light_source { <1, 2, 3> color rgb <1, 0, 0> }"


def test_light_source_color_str():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), "blue")
    assert str(x) == "light_source { <1, 2, 3> color rgb <0, 0, 1> }"


def test_light_source_color_rgba():
    from fdray.scene import LightSource

    x = LightSource((1, 2, 3), (0.1, 0.2, 0.3, 0.4))
    assert "rgbt <0.1, 0.2, 0.3, 0.6>" in str(x)


def test_global_settings():
    from fdray.scene import GlobalSettings

    x = GlobalSettings()
    assert str(x) == "global_settings { assumed_gamma 1 }"


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


def test_scene_str():
    from fdray.scene import Scene

    x = str(Scene("a", ["b", "c"]))
    assert x.startswith("#version 3.7;\n")
    assert "global_settings { assumed_gamma 1 }" in x
    assert x.endswith("\na\nb\nc")


def test_scene_render_without_camera():
    from fdray.scene import Scene

    x = Scene("a", ["b", "c"])
    assert "a\nb\nc" in x.render(100, 100)
