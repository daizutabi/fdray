import textwrap
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture(scope="module")
def scene() -> str:
    scene = """\
    #version 3.7;
    #include "colors.inc"

    global_settings {
      assumed_gamma 1.0
    }

    background { color Cyan }
    camera {
        location <0, 2, -3>
        look_at  <0, 1,  2>
    }
    sphere {
        <0, 1, 2>, 2
        texture {
          pigment { color Yellow }
        }
    }
    light_source { <2, 4, -3> color White}
    """

    return textwrap.dedent(scene)


def test_render_output_file(scene: str, tmp_path: Path):
    from fdray.renderer import Renderer

    renderer = Renderer(width=150, height=100, quality=4)
    output_file = tmp_path / "test.png"
    cp = renderer.render(scene, output_file)
    assert cp.returncode == 0
    assert output_file.exists()


@pytest.mark.parametrize(("output_alpha", "n"), [(True, 4), (False, 3)])
def test_render_array(scene: str, output_alpha: bool, n: int):
    from fdray.renderer import Renderer

    renderer = Renderer(width=150, height=100, quality=4, output_alpha=output_alpha)
    array = renderer.render(scene)
    assert array.shape == (100, 150, n)
    assert array.dtype == np.uint8
