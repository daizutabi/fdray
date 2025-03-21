from __future__ import annotations

import atexit
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile, mkdtemp
from typing import TYPE_CHECKING, overload

import numpy as np
from PIL import Image

from .scene import Scene

if TYPE_CHECKING:
    from typing import Any

    from numpy.typing import NDArray


class RenderError(Exception):
    """Rendering error"""

    def __init__(self, stderr: str) -> None:
        lines = []
        for line in stderr.splitlines():
            if "[Parsing" in line:
                lines.clear()
            lines.append(line)

        message = "POV-Ray rendering failed:"
        super().__init__("\n".join([message, *lines]))


class Renderer:
    width: int = 800
    height: int = 600
    output_alpha: bool = True
    quality: int = 9
    antialias: bool = True
    threads: int | None = None
    display: bool = False
    executable: str = "povray"
    stdout: str = ""
    stderr: str = ""

    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        output_alpha: bool | None = None,
        quality: int | None = None,
        antialias: bool | None = None,
        threads: int | None = None,
        display: bool | None = None,
    ) -> None:
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        else:
            self.height = self.width * 3 // 4
        if output_alpha is not None:
            self.output_alpha = output_alpha
        if quality is not None:
            self.quality = quality
        if antialias is not None:
            self.antialias = antialias
        if threads is not None:
            self.threads = threads
        if display is not None:
            self.display = display

    def build(
        self,
        scene: str,
        output_file: str | Path | None = None,
    ) -> list[str]:
        input_file = create_input_file(scene)
        args = [
            self.executable,
            f"Width={self.width}",
            f"Height={self.height}",
            f"Output_Alpha={to_switch(self.output_alpha)}",
            f"Quality={self.quality}",
            f"Antialias={to_switch(self.antialias)}",
            f"Display={to_switch(self.display)}",
            f"Input_File_Name={input_file}",
        ]

        if self.threads is not None:
            args.append(f"Work_Threads={self.threads}")
        if output_file is not None:
            args.append(f"Output_File_Name={output_file}")

        return args

    @overload
    def render(self, scene: Any) -> NDArray[np.uint8]: ...

    @overload
    def render(self, scene: Any, output_file: str | Path) -> None: ...

    def render(
        self,
        scene: Any,
        output_file: str | Path | None = None,
    ) -> NDArray[np.uint8] | None:
        """Render a POV-Ray scene.

        Args:
            scene: POV-Ray scene description
            output_file: Output image file path.
                If None, returns a numpy array instead of saving to file.

        Returns:
            NDArray[np.uint8] | None: RGB(A) image array if output_file is None
        """
        if output_file is None:
            with NamedTemporaryFile(suffix=".png") as file:
                output_file = Path(file.name)
                self.render(scene, output_file)
                return np.array(Image.open(output_file))

        if isinstance(scene, Scene):
            scene = scene.render(self.width, self.height)
        else:
            scene = str(scene)

        command = self.build(scene, output_file)
        cp = subprocess.run(command, check=False, capture_output=True, text=True)
        self.stdout = cp.stdout
        self.stderr = remove_progress(cp.stderr)

        if cp.returncode != 0:
            raise RenderError(self.stderr)

        return None


def to_switch(value: bool) -> str:
    """Convert a boolean value to a string 'on' or 'off'."""
    return "on" if value else "off"


def create_input_file(scene: str) -> Path:
    """Create a temporary file containing the POV-Ray scene.

    Args:
        scene (str): POV-Ray scene description

    Returns:
        Path: Path to the created scene file

    Note:
        The temporary directory and its contents will be automatically
        deleted when the program exits.
    """
    tmp_dir = Path(mkdtemp())
    file = tmp_dir / "scene.pov"
    file.write_text(scene)
    atexit.register(lambda: shutil.rmtree(tmp_dir))
    return file


def remove_progress(stderr: str) -> str:
    return re.sub(r"^=+ \[Rendering.*?---$", "", stderr, flags=re.MULTILINE | re.DOTALL)
