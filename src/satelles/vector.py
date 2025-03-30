# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos, radians, sin
from typing import Literal

from .common import CartesianCoordinate

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
