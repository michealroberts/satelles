# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos, radians, sin
from typing import Tuple

# **************************************************************************************

Matrix3x3 = Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]

# **************************************************************************************


def get_rotation_matrix_x(angle: float) -> Matrix3x3:
    """
    Create a right-handed active rotation matrix about the X-axis.

    Args:
        angle (float): The rotation angle, (in degrees).

    Returns:
        Matrix3x3: The rotation matrix about the X-axis.
    """
    θ = radians(angle)

    return (
        (1.0, 0.0, 0.0),
        (0.0, cos(θ), -sin(θ)),
        (0.0, sin(θ), cos(θ)),
    )


# **************************************************************************************


def get_rotation_matrix_y(angle: float) -> Matrix3x3:
    """
    Create a right-handed active rotation matrix about the Y-axis.

    Args:
        angle (float): The rotation angle, (in degrees).

    Returns:
        Matrix3x3: The rotation matrix about the Y-axis.
    """
    θ = radians(angle)

    return (
        (cos(θ), 0.0, sin(θ)),
        (0.0, 1.0, 0.0),
        (-sin(θ), 0.0, cos(θ)),
    )


# **************************************************************************************


def get_rotation_matrix_z(angle: float) -> Matrix3x3:
    """
    Create a right-handed active rotation matrix about the Z-axis.

    Args:
        angle (float): The rotation angle, (in degrees).

    Returns:
        Matrix3x3: The rotation matrix about the Z-axis.
    """
    θ = radians(angle)

    return (
        (cos(θ), -sin(θ), 0.0),
        (sin(θ), cos(θ), 0.0),
        (0.0, 0.0, 1.0),
    )


# **************************************************************************************


def multiply(i: Matrix3x3, j: Matrix3x3) -> Matrix3x3:
    """
    Multiply two 3x3 matrices.

    Args:
        i (Matrix3x3): The left-hand matrix.
        j (Matrix3x3): The right-hand matrix.

    Returns:
        Matrix3x3: The product of the two matrices.
    """
    return (
        (
            i[0][0] * j[0][0] + i[0][1] * j[1][0] + i[0][2] * j[2][0],
            i[0][0] * j[0][1] + i[0][1] * j[1][1] + i[0][2] * j[2][1],
            i[0][0] * j[0][2] + i[0][1] * j[1][2] + i[0][2] * j[2][2],
        ),
        (
            i[1][0] * j[0][0] + i[1][1] * j[1][0] + i[1][2] * j[2][0],
            i[1][0] * j[0][1] + i[1][1] * j[1][1] + i[1][2] * j[2][1],
            i[1][0] * j[0][2] + i[1][1] * j[1][2] + i[1][2] * j[2][2],
        ),
        (
            i[2][0] * j[0][0] + i[2][1] * j[1][0] + i[2][2] * j[2][0],
            i[2][0] * j[0][1] + i[2][1] * j[1][1] + i[2][2] * j[2][1],
            i[2][0] * j[0][2] + i[2][1] * j[1][2] + i[2][2] * j[2][2],
        ),
    )


# **************************************************************************************
