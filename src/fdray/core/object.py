"""3D objects and operations for ray tracing.

This module provides a collection of 3D object classes for ray tracing with POV-Ray.
Objects can be combined using CSG operations (union, intersection, difference)
and can be transformed (scale, rotate, translate). Each object can also have
attributes like color, texture, or other POV-Ray specific properties.

The module structure follows these principles:

1. All objects inherit from the base class Object
2. CSG operations are implemented as special object classes
3. Convenience methods are provided for common transformations
4. String representation of objects matches POV-Ray SDL syntax
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import repeat
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Literal, overload

from fdray.utils.string import convert
from fdray.utils.vector import Vector

from .base import Transformable
from .color import Color
from .media import Interior
from .texture import Finish, Normal, Pigment, Texture

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self

    import numpy as np
    from numpy.typing import NDArray

    from fdray.typing import ColorLike, Point


class Object(Transformable):
    """Base class for all 3D objects.

    This class defines common behavior for all objects including:

    - String serialization to POV-Ray SDL format
    - CSG operations (union, intersection, difference, merge)
    - Transformations (scale, rotate, translate)
    - Attribute handling

    Attributes:
        nargs: Number of required arguments for this object.
        args: List of positional arguments passed to the object.
        attrs: List of object attributes (pigment, texture, etc.).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        args_ = (Pigment(arg) if isinstance(arg, Color) else arg for arg in args)
        super().__init__(*args_, **kwargs)

    @overload
    def __add__(self, other: Object) -> Union: ...

    @overload
    def __add__(self, other: Any) -> Self: ...

    def __add__(self, other: Object | Any) -> Union | Self:
        """Create a union. For attributes, adds them to this shape.

        Args:
            other: Another shape or an attribute.

        Returns:
            Union of shapes if other is a Shape, or a new shape with
            the added attribute.
        """
        if isinstance(other, Object):
            return Union(self, other)

        return self.__class__(*self.args, *self.attrs, other)

    def __sub__(self, other: Object) -> Difference:
        """Subtract another shape from this shape.

        Args:
            other: Shape to subtract.

        Returns:
            Difference of this shape and other.
        """
        return Difference(self, other)

    def __mul__(self, other: Object) -> Intersection:
        """Create an intersection.

        Args:
            other: Shape to intersect with.

        Returns:
            Intersection of this shape and other.
        """
        return Intersection(self, other)

    def __or__(self, other: Object) -> Merge:
        """Create a merge.

        Args:
            other: Shape to merge with.

        Returns:
            Merge of this shape and other.
        """
        return Merge(self, other)

    def texture(self, *args: Any, **kwargs: Any) -> Self:
        """Add a texture to the object."""
        return self.add(Texture(*args, **kwargs))

    def pigment(self, *args: Any, **kwargs: Any) -> Self:
        """Add a pigment to the object."""
        return self.add(Pigment(*args, **kwargs))

    def normal(self, *args: Any, **kwargs: Any) -> Self:
        """Add a normal to the object."""
        return self.add(Normal(*args, **kwargs))

    def finish(
        self,
        ambient: float | ColorLike | None = None,
        emission: float | ColorLike | None = None,
        diffuse: float | None = None,
        brilliance: float | None = None,
        phong: float | None = None,
        phong_size: float | None = None,
        specular: float | None = None,
        roughness: float | None = None,
        metallic: float | None = None,
        reflection: float | ColorLike | None = None,
    ) -> Self:
        """Add a finish to the object."""
        return self.add(
            Finish(
                ambient=ambient,
                emission=emission,
                diffuse=diffuse,
                brilliance=brilliance,
                phong=phong,
                phong_size=phong_size,
                specular=specular,
                roughness=roughness,
                metallic=metallic,
                reflection=reflection,
            ),
        )

    def interior(
        self,
        ior: float | None = None,
        caustics: float | None = None,
        dispersion: float | None = None,
        dispersion_samples: int | None = None,
        fade_distance: float | None = None,
        fade_power: float | None = None,
        fade_color: ColorLike | None = None,
    ) -> Self:
        """Add an interior to the object."""
        return self.add(
            Interior(
                ior=ior,
                caustics=caustics,
                dispersion=dispersion,
                dispersion_samples=dispersion_samples,
                fade_distance=fade_distance,
                fade_power=fade_power,
                fade_color=fade_color,
            ),
        )

    def material(self, *args: Any, **kwargs: Any) -> Self:
        """Add a material to the object."""
        return self.add(Material(*args, **kwargs))


class Material(Transformable):
    """Materials define the appearance of objects in the scene."""


def has_attributes(obj: Any) -> bool:
    """Check if the object has attributes."""
    if isinstance(obj, Object):
        return any(not isinstance(attr, Object) for attr in obj.attrs)

    return False


class Csg(Object):
    """Base class for Constructive Solid Geometry (CSG) operations."""

    def __add__(self, other: Any) -> Self:
        """Add another shape to this CSG operation.

        Args:
            other: Shape to add to the union.

        Returns:
            New CSG operation with the added shape.
        """
        if has_attributes(self) or has_attributes(other):
            return self.__class__(self, other)

        return self.__class__(*self.attrs, other)


class Union(Csg):
    """Union of shapes - points inside any of the shapes are inside the union.

    A union represents the boolean OR operation on shapes.
    """

    def __add__(self, other: Any) -> Self:
        """Add another shape to this union using the + operator.

        Args:
            other: Shape to add to the union.

        Returns:
            New union with the added shape.
        """
        return super().__add__(other)


class Intersection(Csg):
    """Intersection of shapes - points inside all shapes are inside the intersection.

    An intersection represents the boolean AND operation on shapes.
    """

    def __mul__(self, other: Object) -> Self:
        """Add another shape to this intersection using the * operator.

        Args:
            other: Shape to add to the intersection.

        Returns:
            New intersection with the added shape.
        """
        return super().__add__(other)


class Difference(Csg):
    """Difference of shapes - points inside the first shape and outside all others.

    A difference represents the boolean subtraction operation on shapes.
    """

    def __sub__(self, other: Object) -> Self:
        """Subtract another shape from this difference using the - operator.

        Args:
            other: Shape to subtract.

        Returns:
            New difference with the subtracted shape.
        """
        return super().__add__(other)


class Merge(Csg):
    """Merge of shapes - similar to union but with different surface calculations.

    A merge represents a union where internal surfaces are removed.
    """

    def __or__(self, other: Object) -> Self:
        """Add another shape to this merge using the | operator.

        Args:
            other: Shape to add to the merge.

        Returns:
            New merge with the added shape.
        """
        return super().__add__(other)


class Box(Object):
    """A box defined by two corner points.

    A box is an axis-aligned rectangular prism defined by two opposite corners.

    Args:
        corner1: First corner point.
        corner2: Second corner point (diagonally opposite to corner1).
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        corner1: Point,
        corner2: Point,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(corner1, corner2, *attrs, **kwargs)


class Cuboid(Object):
    """A rectangular prism defined by a center point and dimensions.

    This is a convenience class that creates a Box centered at a specified point.

    Args:
        center: Center point of the cuboid.
        size: Dimensions (width, height, depth) of the cuboid.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        center: float | Sequence[float] | Vector,
        size: float | Sequence[float] | Vector,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        """Convert the cuboid to a POV-Ray box definition."""
        center, size = self.args
        if not isinstance(center, Sequence):
            center = (center,) * 3
        if not isinstance(size, Sequence):
            size = (size,) * 3
        half_x, half_y, half_z = size[0] / 2, size[1] / 2, size[2] / 2
        corner1 = (center[0] - half_x, center[1] - half_y, center[2] - half_z)
        corner2 = (center[0] + half_x, center[1] + half_y, center[2] + half_z)
        return str(Box(corner1, corner2, *self.attrs))


class Cube(Object):
    """A cube defined by a center point and edge length.

    This is a convenience class that creates a Box representing a cube.

    Args:
        center: Center point of the cube.
        size: Edge length of the cube.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        center: float | Sequence[float] | Vector = 0,
        size: float = 1,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        """Convert the cube to a POV-Ray box definition."""
        center, size = self.args
        if not isinstance(center, Sequence):
            center = (center,) * 3
        half = size / 2
        corner1 = (center[0] - half, center[1] - half, center[2] - half)
        corner2 = (center[0] + half, center[1] + half, center[2] + half)
        return str(Box(corner1, corner2, *self.attrs))


class Cone(Object):
    """A cone or truncated cone between two points with specified radii.

    Args:
        center1: Center of the first end.
        radius1: Radius of the first end.
        center2: Center of the second end.
        radius2: Radius of the second end.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 4

    def __init__(
        self,
        center1: Point,
        radius1: float,
        center2: Point,
        radius2: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center1, radius1, center2, radius2, *attrs, **kwargs)


class Cylinder(Object):
    """A cylinder defined by two points and a radius.

    Args:
        center1: Center of the first end.
        center2: Center of the second end.
        radius: Radius of the cylinder.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 3

    def __init__(
        self,
        center1: Point,
        center2: Point,
        radius: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center1, center2, radius, *attrs, **kwargs)


class Plane(Object):
    """A plane defined by a normal vector and distance from origin.

    Args:
        normal: Normal vector of the plane.
        distance: Distance from the origin along the normal.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        normal: Point,
        distance: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(normal, distance, *attrs, **kwargs)


class SkySphere(Object):
    """A sky sphere that defines the background color of the scene."""


class Sphere(Object):
    """A sphere defined by a center point and radius.

    Args:
        center: Center point of the sphere.
        radius: Radius of the sphere.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        center: Point = 0,
        radius: float = 1,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, radius, *attrs, **kwargs)


class SphereSweep(Object):
    """A sweep of spheres along a path with specified interpolation.

    SphereSweep creates a smooth shape passing through a series of spheres
    using different interpolation methods.

    Args:
        kind: Interpolation method for the sweep.
        centers: Sequence of center points for the spheres.
        radius: Constant radius or sequence of radii for each sphere.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 3

    def __init__(
        self,
        kind: Literal["linear_spline", "b_spline", "cubic_spline"],
        centers: Sequence[Point],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(kind, centers, radius, *attrs, **kwargs)

    def __iter__(self) -> Iterator[str]:
        """Yield string components for POV-Ray SDL representation."""
        kind, centers, radius = self.args

        yield f"{kind}, {len(centers)}"
        radii = radius if isinstance(radius, Sequence) else repeat(radius)
        it = zip(centers, radii, strict=False)
        yield ", ".join(f"{convert(c)}, {convert(r)}" for c, r in it)
        yield from (str(attr) for attr in self.attrs)

    def __str__(self) -> str:
        """Convert the sphere sweep to POV-Ray SDL format.

        Special cases are handled:

        - Empty centers list: returns empty string
        - Single point: returns a sphere
        - Too few points for cubic or b-spline: falls back to linear spline
        """
        kind, centers, radius = self.args

        if len(centers) == 0:
            return ""

        if len(centers) == 1:
            radius = radius[0] if isinstance(radius, Sequence) else radius
            return str(Sphere(centers[0], radius, *self.attrs))

        if kind in ["b_spline", "cubic_spline"] and len(centers) < 4:
            return str(SphereSweep("linear_spline", centers, radius, *self.attrs))

        return super().__str__()


class Polyline(Object):
    """A polyline (broken line) represented as a linear sphere sweep.

    This is a convenience class that creates a sphere sweep with `linear_spline`
    interpolation, providing a simpler interface for creating polylines.

    Args:
        centers (Sequence[Point] | NDArray[np.number]): Sequence of 3D
            points or NumPy array with shape (n, 3) where n is the number
            of points.
        radius (float | Sequence[float]): Constant radius or sequence
            of radii for each point.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2
    kind: ClassVar[Literal["linear_spline"]] = "linear_spline"

    def __init__(
        self,
        centers: Sequence[Point] | NDArray[np.number],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(centers, radius, *attrs, **kwargs)

    def __str__(self) -> str:
        """Convert the polyline to a POV-Ray sphere_sweep with linear_spline."""
        return str(SphereSweep(self.kind, *self.args, *self.attrs))

    @classmethod
    def from_coordinates(
        cls,
        x: Sequence[float],
        y: Sequence[float],
        z: Sequence[float],
        radius: float | Sequence[float],
        *attrs: Any,
        **kwargs: Any,
    ) -> Self:
        """Create a polyline from separate x, y, z coordinate sequences.

        Args:
            x: Sequence of x-coordinates.
            y: Sequence of y-coordinates.
            z: Sequence of z-coordinates.
            radius: Constant radius or sequence of radii for each point.
            *attrs: Additional attributes.
            **kwargs: Additional keyword attributes.

        Returns:
            New Polyline instance.
        """
        return cls(list(zip(x, y, z, strict=True)), radius, *attrs, **kwargs)


class Curve(Polyline):
    """A smooth curve that passes through all specified points.

    Create a cubic spline sphere sweep that is guaranteed to pass
    through all given points, including the start and end points. It uses ghost
    points to ensure proper curve behavior at the endpoints.

    Unlike standard cubic splines which may not pass through the endpoints,
    this implementation ensures the curve follows all specified points exactly.

    Args:
        centers (Sequence[Point] | NDArray[np.number]): Sequence of 3D
            points or NumPy array with shape (n, 3) where n is the number
            of points.
        radius (float | Sequence[float]): Constant radius or sequence
            of radii for each point.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2
    kind: ClassVar[Literal["cubic_spline"]] = "cubic_spline"

    def __str__(self) -> str:
        """Convert the curve to POV-Ray sphere_sweep with cubic_spline.

        For curves with fewer than 2 points, falls back to linear_spline.
        For valid curves, adds ghost points at the ends to ensure the curve
        passes through all input points.
        """
        centers, radius = self.args

        if len(centers) < 2:
            return str(Polyline(centers, radius, *self.attrs))

        ghost_first = Vector(*centers[1]).reflect(centers[0])
        ghost_last = Vector(*centers[-2]).reflect(centers[-1])
        centers = [ghost_first, *centers, ghost_last]

        if isinstance(radius, Sequence):
            radius = [radius[0], *radius, radius[-1]]

        return str(SphereSweep(self.kind, centers, radius, *self.attrs))


class Text(Object):
    """A text object defined by a string and a font.

    Args:
        text: The text string to display.
        font: The font to use for the text.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2
    font_file: ClassVar[str] = "cyrvetic.ttf"

    def __init__(
        self,
        text: str,
        thickness: float = 0,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(text, thickness, *attrs, **kwargs)

    def __iter__(self) -> Iterator[str]:
        text, thickness = self.args
        font_file = self.__class__.font_file
        yield f'ttf "{font_file}", "{text}", {thickness}, 0'
        attrs = (str(attr) for attr in self.attrs)
        yield from (attr for attr in attrs if attr)

    def align(self, longitude: float = 0, latitude: float = 0) -> Self:
        """Align the text with the given longitude and latitude.

        Args:
            longitude: The longitude of the text.
            latitude: The latitude of the text.
        """
        text = self.rotate("90*y").rotate("90*x")

        if longitude == 0 and latitude == 0:
            return text

        return text.rotate(0, -latitude, longitude)

    @classmethod
    def set_font(cls, font_spec: str | Path) -> str | None:
        """Set the font file for the text object.

        This method determines how to handle the font specification
        based on its format:

        - If `font_spec` ends with '.ttf', it's treated as a direct file path.
        - Otherwise, it's treated as a font name to search in system fonts.

        Args:
            font_spec (str | Path): Font specification, either a path to a TTF file
                or a font name. If it's a font name, the method will search for
                matching fonts in the system fonts directory.

        Returns:
            str: Path to the font file if found, None otherwise.

        Raises:
            ImportError: If matplotlib is not installed and a font name search
                is attempted.

        """
        font_path = Path(font_spec)

        if font_path.suffix == ".ttf":
            cls.font_file = font_path.as_posix()
            return cls.font_file

        try:
            from matplotlib import font_manager
        except ImportError:  # no cov
            msg = "Warning: matplotlib is not installed."
            msg += " Font search by name is not available."
            raise ImportError(msg) from None

        search_name = font_path.name.lower()

        font_files = [Path(f) for f in font_manager.findSystemFonts()]
        font_files = [f for f in font_files if f.suffix == ".ttf"]

        for font_file in font_files:
            if font_file.stem.lower() == search_name:
                cls.font_file = font_file.as_posix()
                return cls.font_file

        for font_file in font_files:
            if search_name in font_file.stem.lower():
                cls.font_file = font_file.as_posix()
                return cls.font_file

        return None


class Torus(Object):
    """A torus defined by a center point and a radius.

    Args:
        major_radius: Major radius of the torus.
        minor_radius: Minor radius of the torus.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(
        self,
        major_radius: float,
        minor_radius: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(major_radius, minor_radius, *attrs, **kwargs)
