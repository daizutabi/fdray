from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, sqrt
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        return f"<{self.x:.5g}, {self.y:.5g}, {self.z:.5g}>"

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: Vector) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Self:
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
        length = self.norm()
        return self.__class__(self.x / length, self.y / length, self.z / length)

    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __matmul__(self, other: Vector) -> float:
        return self.dot(other)

    def cross(self, other: Vector) -> Self:
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def rotate(self, axis: Vector, theta: float) -> Self:
        """Rotate a vector around an axis by an angle (Rodrigues' rotation formula).

        Args:
            axis (Vector): The axis of rotation (will be normalized).
            theta (float): The angle of rotation in radians.

        Returns:
            Vector: The rotated vector.
        """
        cos_t = cos(theta)
        sin_t = sin(theta)
        a = axis.normalize()

        return self * cos_t + a.cross(self) * sin_t + a * (a @ self) * (1 - cos_t)

    @classmethod
    def from_spherical(cls, phi: float, theta: float) -> Self:
        """Create a vector from spherical coordinates.

        Args:
            phi: azimuthal angle in radians (-π to π or 0 to 2π)
                0 on x-axis, π/2 on y-axis
            theta: polar angle in radians (-π/2 to π/2)
                0 at equator, π/2 at north pole, -π/2 at south pole

        Returns:
            Vector: unit vector (x, y, z) where:
                x = cos(θ)cos(φ)
                y = cos(θ)sin(φ)
                z = sin(θ)
        """
        return cls(cos(theta) * cos(phi), cos(theta) * sin(phi), sin(theta))
