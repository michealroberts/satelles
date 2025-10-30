# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

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
