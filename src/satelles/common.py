# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import TypedDict

# **************************************************************************************


class CartesianCoordinate(TypedDict):
    """
    Typed dictionary for a Cartesian coordinate.
    """

    x: float
    y: float
    z: float


# **************************************************************************************


class Velocity(TypedDict):
    """
    Typed dictionary for a velocity vector.
    """

    vx: float
    vy: float
    vz: float


# **************************************************************************************


class Acceleration(TypedDict):
    """
    Typed dictionary for a gravitational acceleration vector.
    """

    ax: float
    ay: float
    az: float


# **************************************************************************************
