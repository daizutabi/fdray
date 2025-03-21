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

This camera model features:

- Intuitive camera positioning using spherical coordinates
  (`longitude`, `latitude`).
- Independent control of view range (`view_scale`) and perspective
  effect (`distance`).
- Rotation control via camera tilt (`tilt`).
- Proper handling of aspect ratio.

The following code is to reproduce the image in the article.

```python
from PIL import Image

from fdray import Background, Camera, Color, Cylinder, LightSource, Renderer, Scene

camera = Camera(longitude=30, latitude=30)
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
    """A camera for viewing 3D scenes.

    Define the viewpoint and projection for a 3D scene.
    The camera position is specified using spherical coordinates,
    and various parameters allow adjusting the field of view
    and perspective effects.
    """

    longitude: InitVar[float] = 0
    """The longitude of the camera in degrees.

    Specify the horizontal angle around the vertical axis,
    with 0 pointing along the x-axis and 90 pointing along the y-axis.
    """

    latitude: InitVar[float] = 0
    """The latitude of the camera in degrees.

    Specify the angle from the equator, with 0 at the equator,
    90 at the north pole, and -90 at the south pole.
    """

    view_scale: float = 1
    """The scale of the view frustum, controlling how much of the scene is visible.

    Determine the coordinate range that will be rendered, from -view_scale to
    +view_scale. Larger values show more of the scene (zoom out), smaller
    values show less (zoom in). This directly affects the apparent size of
    objects in the rendered image."""

    distance: float = 10
    """The distance of the camera from the look_at point.

    Affect the perspective effect (depth perception) of the scene.
    Larger values reduce perspective distortion. The apparent size of objects
    is controlled by view_scale, not distance."""

    tilt: float = 0
    """The tilt angle of the camera in degrees (-180 to 180).

    Control the rotation of the camera around its viewing direction.
    A value of 0 keeps the camera upright, while other values rotate it
    clockwise (positive) or counterclockwise (negative).
    """

    look_at: Point = (0, 0, 0)
    """The point the camera is looking at.

    Define the center of the view and the point the camera is oriented
    towards. The camera will always point at this location regardless
    of its position.
    """

    aspect_ratio: float = 4 / 3
    """The aspect ratio of the camera.

    The ratio of width to height of the viewing plane. This affects
    how the scene is projected onto the image, with common values
    being 4/3, 16/9, etc.
    """

    phi: float = field(init=False)
    """Internal storage for longitude in radians."""

    theta: float = field(init=False)
    """Internal storage for latitude in radians."""

    def __post_init__(self, longitude: float, latitude: float) -> None:
        """Initialize derived fields after the dataclass initialization.

        Converts longitude and latitude from degrees to radians.

        Args:
            longitude: Camera longitude in degrees
            latitude: Camera latitude in degrees
        """
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
        return self.z * self.distance

    @property
    def location(self) -> Point:
        x, y, z = self.direction
        return x + self.look_at[0], y + self.look_at[1], z + self.look_at[2]

    @property
    def right(self) -> Vector:
        return -2 * self.x * sqrt(self.aspect_ratio) * self.view_scale

    @property
    def up(self) -> Vector:
        return 2 * self.y / sqrt(self.aspect_ratio) * self.view_scale

    @property
    def sky(self) -> Vector:
        return self.y

    def __iter__(self) -> Iterator[str]:
        for name in ["location", "look_at", "direction", "right", "up", "sky"]:
            yield name
            yield convert(getattr(self, name))
