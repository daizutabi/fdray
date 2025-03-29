"""The camera implementation.

This camera implementation is based on the following Qiita article

 - Title: Efficient Camera Settings in POV-Ray
 - Author: @Hyrodium (Yuto Horikawa)
 - URL: https://qiita.com/Hyrodium/items/af91b1ddb8ea2c4359c2
 - Date: 2017-12-07

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

scene = Scene(
    Background("white"),
    Camera(30, 30, view_scale=1),
    LightSource(0, "white"),  # at camera location
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

from fdray.utils.string import convert
from fdray.utils.vector import Vector

from .base import Descriptor

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class Camera(Descriptor):
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
    objects in the rendered image.
    """

    distance: float = 0
    """The distance of the camera from the look_at point.

    Affect the perspective effect (depth perception) of the scene.
    If set to 0, a value of 10 * view_scale will be used automatically.
    """

    tilt: float = 0
    """The tilt angle of the camera in degrees (-180 to 180).

    Control the rotation of the camera around its viewing direction.
    A value of 0 keeps the camera upright, while other values rotate it
    clockwise (positive) or counterclockwise (negative).
    """

    look_at: tuple[float, float, float] = (0, 0, 0)
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
        if self.distance == 0:
            self.distance = 10 * self.view_scale

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
    def location(self) -> Vector:
        return self.direction + self.look_at

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

    def orbital_location(
        self,
        forward: float = 0,
        angle: float = 0,
        rotation: float = 0,
    ) -> Vector:
        """Calculate a position in orbit around the camera's location.

        Imagine tilting your head up (angle) and then rotating
        counter-clockwise (rotation):

        - First, move forward along viewing direction (0=at `camera.location`,
          1=at `camera.look_at`). Negative values move behind the camera.
        - Then, tilt up from viewing direction by 'angle' degrees
        - Finally, rotate counter-clockwise from up by 'rotation' degrees
          (0=up, 90=left, 180=down, 270=right)

        Args:
            forward (float): Relative position along viewing direction
                (0=camera, 1=look_at, negative=behind camera)
            angle (float): Tilt angle from viewing direction in degrees
            rotation (float): Rotation angle from up direction in degrees
                (counter-clockwise)

        Returns:
            Position vector in absolute coordinates
        """
        if forward == 0:
            return self.location

        pos = -self.direction * forward

        if angle != 0:
            rotation_axis = self.x.rotate(self.direction, radians(rotation))
            pos = pos.rotate(rotation_axis, radians(angle))

        return pos + self.location
