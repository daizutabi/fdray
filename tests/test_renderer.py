import textwrap
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture(scope="module")
def scene() -> str:
    scene = """\
    #version 3.7;
    global_settings { assumed_gamma 1 }
    background { rgb <0, 1, 1> }
    camera { location <0, 2, -3> look_at <0, 1, 2> }
    light_source { <2, 4, -3> color rgb <1, 1, 1> }
    sphere {
      <0, 1, 2>, 2
      pigment { rgb <1, 1, 0> }
    }
    """

    return textwrap.dedent(scene)


def test_render_output_file(scene: str, tmp_path: Path):
    from fdray.renderer import Renderer

    renderer = Renderer(150, 100, quality=4)
    output_file = tmp_path / "test.png"
    cp = renderer.render(scene, output_file)
    assert cp.returncode == 0
    assert output_file.exists()


@pytest.mark.parametrize(("output_alpha", "n"), [(True, 4), (False, 3)])
def test_render_array(scene: str, output_alpha: bool, n: int):
    from fdray.renderer import Renderer

    renderer = Renderer(200, quality=4, output_alpha=output_alpha)
    array = renderer.render(scene)
    assert array.shape == (150, 200, n)
    assert array.dtype == np.uint8


def test_render_options():
    from fdray.renderer import Renderer

    renderer = Renderer(display=True, threads=2)
    x = renderer.get_command("test")
    assert "Display=on" in x
    assert "Work_Threads=2" in x


def test_render_error():
    from fdray.renderer import Renderer

    renderer = Renderer(100, 200)
    with pytest.raises(RuntimeError):
        renderer.render("test")


def test_render_scene():
    from fdray import (
        Camera,
        Color,
        LightSource,
        Renderer,
        Scene,
        Sphere,
    )

    camera = Camera((1, 2, 3))

    scene = Scene(
        camera,
        LightSource((1, 2, -3), "white", shadowless=True),
        Sphere((0, 0, 0), 1, Color("white")),
    )
    renderer = Renderer(120, 240)
    renderer.render(scene)

    assert camera.up == (0, 1, 0)
    assert camera.right == (0.5, 0, 0)
