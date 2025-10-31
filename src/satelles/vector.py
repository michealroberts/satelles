# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from dataclasses import dataclass
from math import acos, cos, degrees, isclose, radians, sin, sqrt
from sys import float_info
from typing import Literal

from .common import CartesianCoordinate

# **************************************************************************************

TOLERANCE = float_info.epsilon

# **************************************************************************************


def add(vector: CartesianCoordinate, delta: CartesianCoordinate) -> CartesianCoordinate:
    """
    Add two 3D vectors (x, y, z) component-wise.

    Args:
        vector (CartesianCoordinate): The original vector.
        delta (CartesianCoordinate): The vector to add.

    Returns:
        CartesianCoordinate: The resulting vector after addition.
    """
    return CartesianCoordinate(
        x=vector["x"] + delta["x"],
        y=vector["y"] + delta["y"],
        z=vector["z"] + delta["z"],
    )


# **************************************************************************************


def subtract(
    vector: CartesianCoordinate, delta: CartesianCoordinate
) -> CartesianCoordinate:
    """
    Subtract one 3D vector (x, y, z) from another component-wise.

    Args:
        vector (CartesianCoordinate): The original vector.
        delta (CartesianCoordinate): The vector to subtract.

    Returns:
        CartesianCoordinate: The resulting vector after subtraction.
    """
    return CartesianCoordinate(
        x=vector["x"] - delta["x"],
        y=vector["y"] - delta["y"],
        z=vector["z"] - delta["z"],
    )


# **************************************************************************************


def dilate(vector: CartesianCoordinate, scale: float) -> CartesianCoordinate:
    """
    Scale a 3D vector (x, y, z) by a given scale.

    Args:
        vector (CartesianCoordinate): The vector to scale.
        scale (float): The scaling factor.

    Returns:
        CartesianCoordinate: The scaled vector.
    """
    return CartesianCoordinate(
        x=vector["x"] * scale,
        y=vector["y"] * scale,
        z=vector["z"] * scale,
    )


# **************************************************************************************


def normalise(
    vector: CartesianCoordinate,
) -> CartesianCoordinate:
    """
    Normalise a 3D vector (x, y, z) to a unit vector.

    Args:
        vector (CartesianCoordinate): The input vector.

    Returns:
        CartesianCoordinate: The unit vector in the same direction as the input vector.

    Raises:
        ValueError: If the input vector's magnitude is zero.
    """
    # Compute the vector's magnitude (length):
    r = magnitude(vector)

    if isclose(r, 0.0, abs_tol=TOLERANCE):
        raise ValueError("Cannot convert a zero-length vector to a unit vector.")

    return CartesianCoordinate(
        x=vector["x"] / r,
        y=vector["y"] / r,
        z=vector["z"] / r,
    )


# **************************************************************************************


def magnitude(vector: CartesianCoordinate) -> float:
    """
    Compute the magnitude (length) of a 3D vector.

    Args:
        vector (CartesianCoordinate): The input vector.

    Returns:
        float: The magnitude of the vector.
    """
    x, y, z = vector["x"], vector["y"], vector["z"]

    return sqrt(x**2 + y**2 + z**2)


# **************************************************************************************


def distance(i: CartesianCoordinate, j: CartesianCoordinate) -> float:
    """
    Compute the distance between two points in 3D space.

    Args:
        i (CartesianCoordinate): The first point.
        j (CartesianCoordinate): The second point.

    Returns:
        float: The distance between the two points.
    """
    return magnitude(subtract(j, i))


# **************************************************************************************


def dot(i: CartesianCoordinate, j: CartesianCoordinate) -> float:
    """
    Compute the dot product of two 3D vectors.

    Args:
        i (CartesianCoordinate): The first vector.
        j (CartesianCoordinate): The second vector.

    Returns:
        float: The dot product of the two vectors.
    """
    return i["x"] * j["x"] + i["y"] * j["y"] + i["z"] * j["z"]


# **************************************************************************************


def cross(i: CartesianCoordinate, j: CartesianCoordinate) -> CartesianCoordinate:
    """
    Compute the cross product of two 3D vectors.

    Args:
        i (CartesianCoordinate): The first vector.
        j (CartesianCoordinate): The second vector.

    Returns:
        CartesianCoordinate: The cross product of the two vectors.
    """
    return CartesianCoordinate(
        x=i["y"] * j["z"] - i["z"] * j["y"],
        y=i["z"] * j["x"] - i["x"] * j["z"],
        z=i["x"] * j["y"] - i["y"] * j["x"],
    )


# **************************************************************************************


def angle(i: CartesianCoordinate, j: CartesianCoordinate) -> float:
    """
    Compute the angle in degrees between two 3D vectors.

    Args:
        i (CartesianCoordinate): The first vector.
        j (CartesianCoordinate): The second vector.

    Returns:
        float: The angle between the two vectors in degrees.
    """
    # Compute the magnitude of vector i:
    im = magnitude(i)

    # Compute the magnitude of vector j:
    jm = magnitude(j)

    # Check for zero-length vectors to avoid division by zero:
    if isclose(im, 0.0, abs_tol=TOLERANCE) or isclose(jm, 0.0, abs_tol=TOLERANCE):
        raise ValueError("Cannot compute the angle with a zero-length vector.")

    # Compute the cosine of the angle using the dot product formula:
    angle = dot(i, j) / (im * jm)

    # Clamp the cosine value to the valid range [-1, 1] to avoid numerical issues:
    angle = max(-1.0, min(1.0, angle))

    # Compute the angle in radians and then convert to degrees:
    return degrees(acos(angle))


# **************************************************************************************


def rotate(
    vector: CartesianCoordinate, angle: float, axis: Literal["x", "y", "z"]
) -> CartesianCoordinate:
    """
    Rotate a 3D vector (x, y, z) by a given angle (in degrees) around the specified axis.

    Args:
        vector (CartesianCoordinate): The vector to rotate.
        angle (float): The rotation angle (in degrees).
        axis (Literal['x', 'y', 'z']): The axis to rotate around ('x', 'y', or 'z').

    Returns:
        CartesianCoordinate: The rotated vector as a CartesianCoordinate object.

    Raises:
        ValueError: If the provided axis is not one of 'x', 'y', or 'z'.
    """
    x, y, z = vector["x"], vector["y"], vector["z"]

    A = radians(angle)

    # Rotate the vector around the z-axis:
    if axis == "z":
        return CartesianCoordinate(
            x=x * cos(A) - y * sin(A),
            y=x * sin(A) + y * cos(A),
            z=z,
        )

    # Rotate the vector around the x-axis:
    if axis == "x":
        return CartesianCoordinate(
            x=x,
            y=y * cos(A) - z * sin(A),
            z=y * sin(A) + z * cos(A),
        )

    # Rotate the vector around the y-axis:
    if axis == "y":
        return CartesianCoordinate(
            x=x * cos(A) + z * sin(A),
            y=y,
            z=-x * sin(A) + z * cos(A),
        )

    raise ValueError("Axis must be 'x', 'y', or 'z'.")


# **************************************************************************************


def project(
    vector: CartesianCoordinate, onto: CartesianCoordinate
) -> CartesianCoordinate:
    """
    Project one 3D vector onto another.

    Args:
        vector (CartesianCoordinate): The vector to be projected.
        onto (CartesianCoordinate): The vector to project onto.

    Returns:
        CartesianCoordinate: The projected vector.
    """
    # Compute the dot product of 'onto' with itself:
    oo = dot(onto, onto)

    # Check for zero-length 'onto' vector to avoid division by zero:
    if isclose(oo, 0.0, abs_tol=TOLERANCE):
        raise ValueError("Cannot project onto a zero-length vector.")

    # Compute the scaling factor for the projection:
    scale = dot(vector, onto) / oo

    # Return the projected vector:
    return dilate(onto, scale)


# **************************************************************************************


def reject(
    vector: CartesianCoordinate, base: CartesianCoordinate
) -> CartesianCoordinate:
    """
    Compute the rejection of one 3D vector from another.

    Args:
        vector (CartesianCoordinate): The vector to be rejected.
        base (CartesianCoordinate): The vector to reject from.

    Returns:
        CartesianCoordinate: The rejection vector.
    """
    # Compute the rejection by subtracting the projection from the original vector:
    return subtract(vector, project(vector, base))


# **************************************************************************************


@dataclass(frozen=True)
class Vector:
    """
    A class representing a 3D vector with x, y, z components.
    """

    x: float
    y: float
    z: float

    def add(self, delta: "Vector") -> "Vector":
        """
        Add another Vector to this Vector.

        Args:
            delta (Vector): The vector to add.

        Returns:
            Vector: The resulting vector after addition.
        """
        return Vector(
            x=self.x + delta.x,
            y=self.y + delta.y,
            z=self.z + delta.z,
        )

    def subtract(self, delta: "Vector") -> "Vector":
        """
        Subtract another Vector from this Vector.

        Args:
            delta (Vector): The vector to subtract.

        Returns:
            Vector: The resulting vector after subtraction.
        """
        return Vector(
            x=self.x - delta.x,
            y=self.y - delta.y,
            z=self.z - delta.z,
        )

    def dilate(self, scale: float) -> "Vector":
        """
        Scale this Vector by a given scale.

        Args:
            scale (float): The scaling factor.

        Returns:
            Vector: The scaled vector.
        """
        return Vector(
            x=self.x * scale,
            y=self.y * scale,
            z=self.z * scale,
        )

    def normalise(self) -> "Vector":
        """
        Normalise this Vector to a unit vector.

        Returns:
            Vector: The unit vector in the same direction as this vector.

        Raises:
            ValueError: If the vector's magnitude is zero.
        """
        r = self.magnitude()

        if isclose(r, 0.0, abs_tol=TOLERANCE):
            raise ValueError("Cannot convert a zero-length vector to a unit vector.")

        return Vector(
            x=self.x / r,
            y=self.y / r,
            z=self.z / r,
        )

    def magnitude(self) -> float:
        """
        Compute the magnitude (length) of this Vector.

        Returns:
            float: The magnitude of the vector.
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def distance(self, other: "Vector") -> float:
        """
        Compute the distance between this Vector and another Vector.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The distance between the two vectors.
        """
        return self.subtract(other).magnitude()

    def dot(self, other: "Vector") -> float:
        """
        Compute the dot product of this Vector with another Vector.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The dot product of the two vectors.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector") -> "Vector":
        """
        Compute the cross product of this Vector with another Vector.

        Args:
            other (Vector): The other vector.

        Returns:
            Vector: The cross product of the two vectors.
        """
        return Vector(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x,
        )

    def angle(self, other: "Vector") -> float:
        """
        Compute the angle in degrees between this Vector and another Vector.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The angle between the two vectors in degrees.
        """
        return angle(
            i=CartesianCoordinate(x=self.x, y=self.y, z=self.z),
            j=CartesianCoordinate(x=other.x, y=other.y, z=other.z),
        )

    def rotate(self, angle: float, axis: Literal["x", "y", "z"]) -> "Vector":
        """
        Rotate this Vector by a given angle (in degrees) around the specified axis.

        Args:
            angle (float): The rotation angle (in degrees).
            axis (Literal['x', 'y', 'z']): The axis to rotate around ('x', 'y', or 'z').

        Returns:
            Vector: The rotated vector.
        """
        rotated = rotate(
            vector=CartesianCoordinate(x=self.x, y=self.y, z=self.z),
            angle=angle,
            axis=axis,
        )

        return Vector(x=rotated["x"], y=rotated["y"], z=rotated["z"])

    def project(self, onto: "Vector") -> "Vector":
        """
        Project this Vector onto another Vector.

        Args:
            onto (Vector): The vector to project onto.

        Returns:
            Vector: The projected vector.
        """
        projected = project(
            vector=CartesianCoordinate(x=self.x, y=self.y, z=self.z),
            onto=CartesianCoordinate(x=onto.x, y=onto.y, z=onto.z),
        )

        return Vector(x=projected["x"], y=projected["y"], z=projected["z"])

    def reject(self, base: "Vector") -> "Vector":
        """
        Compute the rejection of this Vector from another Vector.

        Args:
            base (Vector): The vector to reject from.

        Returns:
            Vector: The rejection vector.
        """
        rejected = reject(
            vector=CartesianCoordinate(x=self.x, y=self.y, z=self.z),
            base=CartesianCoordinate(x=base.x, y=base.y, z=base.z),
        )

        return Vector(x=rejected["x"], y=rejected["y"], z=rejected["z"])

    def __add__(self, other: "Vector") -> "Vector":
        return self.add(other)

    def __sub__(self, other: "Vector") -> "Vector":
        return self.subtract(other)

    def __neg__(self) -> "Vector":
        """
        Negate the vector using the unary - operator.

        Returns:
            Vector: The negated vector.
        """
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: float) -> "Vector":
        """
        Scale the vector using the * operator.

        Args:
            scalar (float): The scaling factor.

        Returns:
            Vector: The scaled vector.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Vector can only be multiplied by a scalar.")

        return self.dilate(scalar)

    def __rmul__(self, other: float) -> "Vector":
        """
        Multiply the vector by a scalar using the * operator with reversed operands.

        Args:
            other (float): The scalar factor.

        Returns:
            Vector: The scaled vector.
        """
        return self.__mul__(other)

    def __truediv__(self, scalar: float) -> "Vector":
        """
        Divide the vector by a scalar using the / operator.

        Args:
            scalar (float): The scalar divisor.

        Returns:
            Vector: The scaled vector.
        """
        # Check for valid scalar type:
        if not isinstance(scalar, (int, float)):
            raise TypeError("Vector can only be divided by a scalar.")

        # Check for division by zero with tolerance:
        if isclose(scalar, 0.0, abs_tol=TOLERANCE):
            raise ZeroDivisionError("Cannot divide a vector by zero.")

        # Perform the division by dilating with the reciprocal of the scalar:
        return self.dilate(1.0 / float(scalar))

    def to_cartesian(self) -> CartesianCoordinate:
        """
        Convert the Vector instance to a CartesianCoordinate typed dictionary.

        Returns:
            CartesianCoordinate: The CartesianCoordinate representation of the vector.
        """
        return CartesianCoordinate(x=self.x, y=self.y, z=self.z)

    @staticmethod
    def from_cartesian(coordinate: CartesianCoordinate) -> "Vector":
        """
        Create a Vector from a CartesianCoordinate typed dictionary.

        Args:
            coordinate (CartesianCoordinate): The input coordinate.

        Returns:
            Vector: The constructed vector.
        """
        return Vector(x=coordinate["x"], y=coordinate["y"], z=coordinate["z"])


# **************************************************************************************
