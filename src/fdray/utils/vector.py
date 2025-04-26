from __future__ import annotations

from collections.abc import Iterable
from math import acos, asin, atan2, cos, sin, sqrt
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Iterator


class Vector:
    x: float
    y: float
    z: float

    def __init__(
        self,
        x: float | Iterable[float],
        y: float | None = None,
        z: float | None = None,
    ) -> None:
        if isinstance(x, Iterable):
            self.x, self.y, self.z = x
        elif y is not None and z is not None:
            self.x = x
            self.y = y
            self.z = z
        else:
            msg = "Invalid arguments"
            raise ValueError(msg)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        args = ["0" if abs(arg) < 1e-5 else f"{arg:.5g}" for arg in self]
        return f"<{', '.join(args)}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        if isinstance(other, Iterable):
            o = list(other)
            if len(o) == 3:
                return self.x == o[0] and self.y == o[1] and self.z == o[2]
        return False

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: Vector | Iterable[float]) -> Self:
        if not isinstance(other, Vector):
            other = Vector(*other)

        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector | Iterable[float]) -> Self:
        if not isinstance(other, Vector):
            other = Vector(*other)

        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Self:
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Self:
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> Self:
        return self.__class__(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def norm(self) -> float:
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Self:
        """Normalize the vector to unit length.

        Returns:
            The normalized vector.
        """
        length = self.norm()
        return self.__class__(self.x / length, self.y / length, self.z / length)

    def dot(self, other: Vector | Iterable[float]) -> float:
        """Compute the dot product of two vectors.

        Args:
            other (Vector | Iterable[float]): The vector to dot with

        Returns:
            The dot product of the two vectors.
        """
        if not isinstance(other, Vector):
            other = Vector(*other)

        return self.x * other.x + self.y * other.y + self.z * other.z

    def __matmul__(self, other: Vector | Iterable[float]) -> float:
        if not isinstance(other, Vector):
            other = Vector(*other)

        return self.dot(other)

    def cross(self, other: Vector | Iterable[float]) -> Self:
        """Compute the cross product of two vectors.

        Args:
            other (Vector | Iterable[float]): The vector to cross with

        Returns:
            The cross product of the two vectors.
        """
        if not isinstance(other, Vector):
            other = Vector(*other)

        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def rotate(self, axis: Vector | Iterable[float], theta: float) -> Self:
        """Rotate a vector around an axis by an angle (Rodrigues' rotation formula).

        Args:
            axis (Vector | Iterable[float]): The axis of rotation
                (will be normalized).
            theta (float): The angle of rotation in radians.

        Returns:
            Vector: The rotated vector.
        """
        if not isinstance(axis, Vector):
            axis = Vector(*axis)

        cos_t = cos(theta)
        sin_t = sin(theta)
        a = axis.normalize()

        return self * cos_t + a.cross(self) * sin_t + a * (a @ self) * (1 - cos_t)

    def reflect(self, across: Vector | Iterable[float]) -> Self:
        """Reflect this vector across another vector.

        Args:
            across (Vector | Iterable[float]): The vector to reflect across

        Returns:
            The reflected vector
        """
        if not isinstance(across, Vector):
            across = Vector(*across)

        return -self + 2 * across

    def angle(self, other: Vector | Iterable[float]) -> float:
        """Calculate angle between two vectors in radians.

        Args:
            other (Vector | Iterable[float]): Another vector to calculate angle with

        Returns:
            Angle between vectors in radians (0-π)
        """
        if not isinstance(other, Vector):
            other = Vector(*other)

        v1 = self.normalize()
        v2 = other.normalize()
        cos_theta = max(min(v1.dot(v2), 1), -1)
        return acos(cos_theta)

    @classmethod
    def from_spherical(cls, phi: float, theta: float) -> Self:
        """Create a vector from spherical coordinates.

        Args:
            phi (float): azimuthal angle in radians (-π to π or 0 to 2π)
                0 on x-axis, π/2 on y-axis
            theta (float): polar angle in radians (-π/2 to π/2)
                0 at equator, π/2 at north pole, -π/2 at south pole

        Returns:
            Vector: unit vector (x, y, z) where:
                x = cos(θ)cos(φ)
                y = cos(θ)sin(φ)
                z = sin(θ)
        """
        return cls(cos(theta) * cos(phi), cos(theta) * sin(phi), sin(theta))

    def to_spherical(self) -> tuple[float, float]:
        """Convert vector to spherical coordinates.

        Returns:
            tuple[float, float]: A tuple of (phi, theta)
            where

            - phi: azimuthal angle in radians (-π to π),
              0 on x-axis, π/2 on y-axis
            - theta: polar angle in radians (-π/2 to π/2),
              0 at equator, π/2 at north pole, -π/2 at south pole
        """
        length = self.norm()
        if length < 1e-10:
            return 0.0, 0.0

        theta = asin(self.z / length)
        phi = atan2(self.y, self.x)

        return phi, theta
