"""The camera implementation.

This camera implementation is based on the following Qiita article:
Title: Efficient Camera Settings in POV-Ray
Author: @Hyrodium (Yuto Horikawa)
URL: https://qiita.com/Hyrodium/items/af91b1ddb8ea2c4359c2
Date: 2017-12-07

We adopt the spherical coordinate system for camera positioning
and the calculation methods for direction, right, and up vectors
as proposed in the article.
The sky parameter is also included as it's essential for proper
orientation.

The following code is to reproduce the image in the article.

```python
from PIL import Image

from fdray import Background, Camera, Color, Cylinder, LightSource, Renderer, Scene

camera = Camera(longitude=30, latitude=30, zoom=1, perspective=0.1)
scene = Scene(
    camera,
    Background("white"),
    LightSource(camera.location, "white"),
    Cylinder((0, 0, 0), (1, 0, 0), 0.1, Color("red")),
    Cylinder((0, 0, 0), (0, 1, 0), 0.1, Color("green")),
    Cylinder((0, 0, 0), (0, 0, 1), 0.1, Color("blue")),
)
renderer = Renderer(width=300, height=300)
array = renderer.render(scene)
Image.fromarray(array)
```
"""

from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from math import cos, radians, sin, sqrt
from typing import TYPE_CHECKING

from .attributes import Attribute
from .utils import convert
from .vector import Vector

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .typing import Point


@dataclass
class Camera(Attribute):
    """A camera."""

    longitude: InitVar[float] = 0
    """The longitude of the camera in degrees (0 on x-axis, 90 on y-axis)."""

    latitude: InitVar[float] = 0
    """The latitude of the camera in degrees (0 at equator, 90 at north pole,
    -90 at south pole)."""

    zoom: float = 1
    """The zoom of the camera."""

    perspective: float = 1
    """The perspective of the camera."""

    tilt: float = 0
    """The tilt angle of the camera in degrees (-180 to 180)."""

    look_at: Point = (0, 0, 0)
    """The point the camera is looking at."""

    aspect_ratio: float = 4 / 3
    """The aspect ratio of the camera."""

    phi: float = field(init=False)
    theta: float = field(init=False)

    def __post_init__(self, longitude: float, latitude: float) -> None:
        self.phi = radians(longitude)
        self.theta = radians(latitude)

    @property
    def z(self) -> Vector:
        return Vector.from_spherical(self.phi, self.theta)

    @property
    def x(self) -> Vector:
        tilt = radians(self.tilt)
        return Vector(-sin(self.phi), cos(self.phi), 0).rotate(self.z, tilt)

    @property
    def y(self) -> Vector:
        return self.z.cross(self.x)

    @property
    def direction(self) -> Vector:
        return self.z / (self.zoom * self.perspective)

    @property
    def location(self) -> Point:
        x, y, z = self.direction
        return x + self.look_at[0], y + self.look_at[1], z + self.look_at[2]

    @property
    def right(self) -> Vector:
        return -2 * self.x * sqrt(self.aspect_ratio) / self.zoom

    @property
    def up(self) -> Vector:
        return 2 * self.y / sqrt(self.aspect_ratio) / self.zoom

    @property
    def sky(self) -> Vector:
        return self.y

    def __iter__(self) -> Iterator[str]:
        for name in ["location", "look_at", "direction", "right", "up", "sky"]:
            yield name
            yield convert(getattr(self, name))
