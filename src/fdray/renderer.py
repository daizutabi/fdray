from __future__ import annotations

import atexit
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import NamedTemporaryFile, mkdtemp
from typing import TYPE_CHECKING, overload

import numpy as np
from PIL import Image

if TYPE_CHECKING:
    from numpy.typing import NDArray


class Renderer:
    width: int = 800
    height: int = 600
    output_alpha: bool = True
    quality: int = 9
    threads: int | None = None
    display: bool = False
    executable: str = "povray"

    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        output_alpha: bool | None = None,
        quality: int | None = None,
        display: bool | None = None,
    ) -> None:
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if output_alpha is not None:
            self.output_alpha = output_alpha
        if quality is not None:
            self.quality = quality
        if display is not None:
            self.display = display

    def get_command(
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
            f"Display={to_switch(self.display)}",
            f"Input_File_Name={input_file}",
        ]

        if self.threads is not None:
            args.append(f"Work_Threads={self.threads}")
        if output_file is not None:
            args.append(f"Output_File_Name={output_file}")

        return args

    @overload
    def render(self, scene: str) -> NDArray[np.uint8]: ...

    @overload
    def render(self, scene: str, output_file: str | Path) -> CompletedProcess: ...

    def render(
        self,
        scene: str,
        output_file: str | Path | None = None,
    ) -> NDArray[np.uint8] | CompletedProcess:
        """Render POV-Ray scene.

        Args:
            scene (str): POV-Ray scene description
            output_file (str | Path | None): Output image file path.
                If None, returns numpy array

        Returns:
            np.ndarray: RGB(A) image array if output_file is None
            CompletedProcess: Process information if output_file is specified

        """
        if output_file:
            command = self.get_command(scene, output_file)
            return subprocess.run(command, check=False, capture_output=True)

        with NamedTemporaryFile(suffix=".png") as file:
            output_file = Path(file.name)
            cp = self.render(scene, output_file)

            if cp.returncode != 0:
                raise RuntimeError(cp.stderr)

            return np.array(Image.open(output_file))


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
