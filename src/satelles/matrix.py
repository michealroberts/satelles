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
