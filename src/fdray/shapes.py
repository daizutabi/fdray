"""3D shape primitives and operations for ray tracing.

This module provides a collection of 3D shape classes for ray tracing with POV-Ray.
Shapes can be combined using CSG operations (union, intersection, difference)
and can be transformed (scale, rotate, translate). Each shape can also have
attributes like color, texture, or other POV-Ray specific properties.

The module structure follows these principles:

1. All shapes inherit from the abstract base class Shape
2. CSG operations are implemented as special shape classes
3. Convenience methods are provided for common transformations
4. String representation of shapes matches POV-Ray SDL syntax
"""

from __future__ import annotations

import textwrap
from abc import ABC
from collections.abc import Sequence
from itertools import repeat
from typing import TYPE_CHECKING, ClassVar, Literal, overload

from .attributes import Pigment, Transform
from .color import Color
from .utils import convert, reflect_point, to_snake_case

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Self

    import numpy as np
    from numpy.typing import NDArray

    from .typing import Point


class Shape(ABC):
    """Abstract base class for all 3D shapes.

    This class defines common behavior for all shapes including:

    - String serialization to POV-Ray SDL format
    - CSG operations (union, intersection, difference, merge)
    - Transformations (scale, rotate, translate)
    - Attribute handling

    Attributes:
        nargs: Number of required arguments for this shape.
        args: List of positional arguments passed to the shape.
        attrs: List of shape attributes (color, texture, etc.).
    """

    nargs: ClassVar[int] = 0
    args: list[Any]
    attrs: list[Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = list(args[: self.nargs])
        attrs = [convert_attribute(attr) for attr in args[self.nargs :]]
        kw_attrs = [k for k, v in kwargs.items() if v]
        self.attrs = [*kw_attrs, *attrs]

    @property
    def name(self) -> str:
        """Get the POV-Ray SDL name for this shape."""
        return to_snake_case(self.__class__.__name__)

    def __iter__(self) -> Iterator[str]:
        """Yield string components for POV-Ray SDL representation.

        Each yielded string represents a line in the SDL output.
        First comes the args, then the attributes.
        """
        if self.args:
            yield ", ".join(convert(arg) for arg in self.args)

        yield from (str(attr) for attr in self.attrs)

    def __str__(self) -> str:
        """Convert the shape to POV-Ray SDL format."""
        args = list(self)
        if len(args) == 1:
            return f"{self.name} {{ {args[0]} }}"

        arg = textwrap.indent("\n".join(args), "  ")
        return f"{self.name} {{\n{arg}\n}}"

    @overload
    def __add__(self, other: Shape) -> Union: ...

    @overload
    def __add__(self, other: Any) -> Self: ...

    def __add__(self, other: Shape | Any) -> Union | Self:
        """Create a union. For attributes, adds them to this shape.

        Args:
            other: Another shape or an attribute.

        Returns:
            Union of shapes if other is a Shape, or a new shape with
            the added attribute.
        """
        if isinstance(other, Shape):
            return Union(self, other)

        return self.__class__(*self.args, *self.attrs, other)

    def __sub__(self, other: Shape) -> Difference:
        """Subtract another shape from this shape.

        Args:
            other: Shape to subtract.

        Returns:
            Difference of this shape and other.
        """
        return Difference(self, other)

    def __mul__(self, other: Shape) -> Intersection:
        """Create an intersection.

        Args:
            other: Shape to intersect with.

        Returns:
            Intersection of this shape and other.
        """
        return Intersection(self, other)

    def __or__(self, other: Shape) -> Merge:
        """Create a merge.

        Args:
            other: Shape to merge with.

        Returns:
            Merge of this shape and other.
        """
        return Merge(self, other)

    def add(self, *others: Any) -> Self:
        """Add multiple attributes to this shape.

        Args:
            *others: Attributes to add. Lists or tuples will be flattened.

        Returns:
            New shape with the added attributes.
        """
        attrs = []
        for other in others:
            if isinstance(other, list | tuple):
                attrs.extend(other)
            else:
                attrs.append(other)

        return self.__class__(*self.args, *self.attrs, *attrs)

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Scale the shape uniformly or non-uniformly.

        Args:
            x: Scale factor. If y and z are None, scales uniformly.
            y: Scale factor for y-axis. If None, uses x for uniform scaling.
            z: Scale factor for z-axis. If None, uses x for uniform scaling.

        Returns:
            New shape with the scaling transformation applied.
        """
        if y is None or z is None:
            return self.__class__(*self.args, *self.attrs, Transform(scale=x))

        return self.__class__(*self.args, *self.attrs, Transform(scale=(x, y, z)))

    def rotate(self, x: float, y: float, z: float) -> Self:
        """Rotate the shape around the x, y, and z axes.

        Args:
            x: Rotation angle in degrees around the x-axis.
            y: Rotation angle in degrees around the y-axis.
            z: Rotation angle in degrees around the z-axis.

        Returns:
            New shape with the rotation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(rotate=(x, y, z)))

    def translate(self, x: float, y: float, z: float) -> Self:
        """Translate the shape along the x, y, and z axes.

        Args:
            x: Translation distance along the x-axis.
            y: Translation distance along the y-axis.
            z: Translation distance along the z-axis.

        Returns:
            New shape with the translation transformation applied.
        """
        return self.__class__(*self.args, *self.attrs, Transform(translate=(x, y, z)))


SHAPE_KEYWORDS = ["open"]


def convert_attribute(attr: Any) -> Any:
    """Convert an attribute to the appropriate type.

    Handles:
    - Keywords like "open"
    - Colors specified as strings or tuples
    - Other attributes

    Args:
        attr: The attribute to convert.

    Returns:
        Converted attribute.
    """
    if attr in SHAPE_KEYWORDS:
        return attr

    if isinstance(attr, Color):
        return Pigment(color=attr)

    return attr


class Csg(Shape):
    """Base class for Constructive Solid Geometry (CSG) operations.

    CSG operations combine shapes using boolean operations.

    Attributes:
        attrs: List of shapes to combine with the CSG operation.
    """

    attrs: list[Any]

    def __add__(self, other: Any) -> Self:
        """Add another shape to this CSG operation.

        Args:
            other: Shape to add to the CSG operation.

        Returns:
            New CSG object with the added shape.
        """
        return self.__class__(*self.attrs, other)


class Union(Csg):
    """Union of shapes - points inside any of the shapes are inside the union.

    A union represents the boolean OR operation on shapes.
    """


class Intersection(Csg):
    """Intersection of shapes - points inside all shapes are inside the intersection.

    An intersection represents the boolean AND operation on shapes.
    """

    def __mul__(self, other: Shape) -> Self:
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

    def __sub__(self, other: Shape) -> Self:
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

    def __or__(self, other: Shape) -> Self:
        """Add another shape to this merge using the | operator.

        Args:
            other: Shape to add to the merge.

        Returns:
            New merge with the added shape.
        """
        return super().__add__(other)


class ShapeGroup:
    """A group of shapes combined as a union with utility methods.

    This is a convenience class that combines multiple shapes and provides
    transformation methods that apply to all shapes in the group.

    Attributes:
        union: The Union object containing all shapes in the group.

    Args:
        *shapes: Shapes to include in the group.
    """

    union: Union

    def __init__(self, *shapes: Shape) -> None:
        self.union = Union(*shapes)

    def __str__(self) -> str:
        """Convert the shape group to POV-Ray SDL format."""
        return str(self.union)

    def __add__(self, other: Any) -> Self:
        """Add a shape or attribute to all shapes in this group.

        Args:
            other: Shape or attribute to add.

        Returns:
            New shape group with the addition applied.
        """
        group = self.__class__.__new__(self.__class__)
        group.union = self.union + other
        return group

    def add(self, *others: Any) -> Self:
        """Add multiple attributes to all shapes in this group.

        Args:
            *others: Attributes to add. Lists or tuples will be flattened.

        Returns:
            New shape group with the additions applied.
        """
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.add(*others)
        return group

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Scale all shapes in this group.

        Args:
            x: Scale factor. If y and z are None, scales uniformly.
            y: Scale factor for y-axis. If None, uses x for uniform scaling.
            z: Scale factor for z-axis. If None, uses x for uniform scaling.

        Returns:
            New shape group with scaling applied to all shapes.
        """
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.scale(x, y, z)
        return group

    def rotate(self, x: float, y: float, z: float) -> Self:
        """Rotate all shapes in this group.

        Args:
            x: Rotation angle in degrees around the x-axis.
            y: Rotation angle in degrees around the y-axis.
            z: Rotation angle in degrees around the z-axis.

        Returns:
            New shape group with rotation applied to all shapes.
        """
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.rotate(x, y, z)
        return group

    def translate(self, x: float, y: float, z: float) -> Self:
        """Translate all shapes in this group.

        Args:
            x: Translation distance along the x-axis.
            y: Translation distance along the y-axis.
            z: Translation distance along the z-axis.

        Returns:
            New shape group with translation applied to all shapes.
        """
        group = self.__class__.__new__(self.__class__)
        group.union = self.union.translate(x, y, z)
        return group


class Box(Shape):
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


class Cuboid(Shape):
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
        center: Point,
        size: tuple[float, float, float],
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        """Convert the cuboid to a POV-Ray box definition."""
        center, size = self.args
        half_x, half_y, half_z = size[0] / 2, size[1] / 2, size[2] / 2
        corner1 = (center[0] - half_x, center[1] - half_y, center[2] - half_z)
        corner2 = (center[0] + half_x, center[1] + half_y, center[2] + half_z)
        return str(Box(corner1, corner2, *self.attrs))


class Cube(Shape):
    """A cube defined by a center point and edge length.

    This is a convenience class that creates a Box representing a cube.

    Args:
        center: Center point of the cube.
        size: Edge length of the cube.
        *attrs: Additional attributes.
        **kwargs: Additional keyword attributes.
    """

    nargs: ClassVar[int] = 2

    def __init__(self, center: Point, size: float, *attrs: Any, **kwargs: Any) -> None:
        super().__init__(center, size, *attrs, **kwargs)

    def __str__(self) -> str:
        """Convert the cube to a POV-Ray box definition."""
        center, size = self.args
        half = size / 2
        corner1 = (center[0] - half, center[1] - half, center[2] - half)
        corner2 = (center[0] + half, center[1] + half, center[2] + half)
        return str(Box(corner1, corner2, *self.attrs))


class Cone(Shape):
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


class Cylinder(Shape):
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


class Plane(Shape):
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


class Sphere(Shape):
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
        center: Point,
        radius: float,
        *attrs: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(center, radius, *attrs, **kwargs)


class SphereSweep(Shape):
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


class Polyline(Shape):
    """A polyline (broken line) represented as a linear sphere sweep.

    This is a convenience class that creates a sphere sweep with linear_spline
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

        ghost_first = reflect_point(centers[1], centers[0])
        ghost_last = reflect_point(centers[-2], centers[-1])
        centers = [ghost_first, *centers, ghost_last]

        if isinstance(radius, Sequence):
            radius = [radius[0], *radius, radius[-1]]

        return str(SphereSweep(self.kind, centers, radius, *self.attrs))
