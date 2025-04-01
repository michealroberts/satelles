# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import sqrt

from .common import Acceleration, CartesianCoordinate
from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS

# **************************************************************************************


def get_gravitational_acceleration(
    r: CartesianCoordinate, μ: float = EARTH_MASS * GRAVITATIONAL_CONSTANT
) -> Acceleration:
    """
    Compute gravitational acceleration given position vector r in SI units.

    Args:
        r (CartesianCoordinate): Position vector [x, y, z] in meters.
        μ (float): Gravitational parameter (m^3/s^2), default is for Earth.

    Returns:
        Acceleration: Gravitational acceleration vector [ax, ay, az] in m/s^2.
    """
    # Calculate the magnitude of the position vector:
    r_magnitude = sqrt(r["x"] ** 2 + r["y"] ** 2 + r["z"] ** 2)

    if r_magnitude == 0:
        raise ValueError("Position vector cannot be zero.")

    # Calculate the gravitational acceleration, which is directed towards the
    # center of the Earth:
    f = -μ / (r_magnitude**3)

    # Calculate the acceleration vector components:
    return Acceleration(
        ax=f * r["x"],
        ay=f * r["y"],
        az=f * r["z"],
    )


# **************************************************************************************
