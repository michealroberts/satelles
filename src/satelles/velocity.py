# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos, radians, sin, sqrt

from .common import Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS
from .kepler import get_semi_latus_rectum

# **************************************************************************************


def get_perifocal_velocity(
    semi_major_axis: float,
    true_anomaly: float,
    eccentricity: float,
    μ: float = EARTH_MASS * GRAVITATIONAL_CONSTANT,
) -> Velocity:
    """
    Calculate the velocity in the perifocal coordinate system.

    Args:
        semi_major_axis: Semi-major axis (in meters).
        true_anomaly: True anomaly (in degrees).
        eccentricity: Orbital eccentricity.
        μ: Gravitational parameter (m^3/s^2); defaults to Earth's μ.

    Returns:
        Velocity: A TypedDict with keys 'vx', 'vy', 'vz' representing the velocity in m/s.
    """
    # Compute the semi-latus rectum using the semi-major axis and eccentricity:
    p = get_semi_latus_rectum(semi_major_axis, eccentricity)

    # Ensure p is positive to avoid complex numbers:
    if p <= 0:
        raise ValueError("Semi-latus rectum must be positive.")

    # Compute perifocal velocity components:
    v_x = -sqrt(μ / p) * sin(radians(true_anomaly))
    v_y = sqrt(μ / p) * (eccentricity + cos(radians(true_anomaly)))
    v_z = 0.0

    return Velocity(vx=v_x, vy=v_y, vz=v_z)


# **************************************************************************************
