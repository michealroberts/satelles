# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import pi
from typing import Optional

from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS

# **************************************************************************************


def get_semi_major_axis(mean_motion: float, mass: Optional[float] = 0.0) -> float:
    """
    Calculate the semi-major axis of the satellite's orbit in meters.

    The semi-major axis is calculated using the mean motion and the gravitational
    constant of the Earth.

    Args:
        mean_motion: The mean motion of the satellite in revolutions per day.
        mass: The mass of the satellite in kilograms. Default is 0.0 (for a point mass).

    Returns:
        The semi-major axis (in SI meters).
    """
    if mass is None:
        mass = 0.0

    # Calculate the standard gravitational parameter (μ) using the gravitational constant
    # and the mass of the Earth, and the mass of the satellite (if provided):
    μ = GRAVITATIONAL_CONSTANT * (EARTH_MASS + mass)  # μ ≈ GM

    # Convert the mean motion from revolutions per day to radians per second:
    n = (mean_motion * 2 * pi) / 86400

    # Calculate the semi-major axis using the formula (in meters):
    return (μ / n**2) ** (1 / 3)


# **************************************************************************************
