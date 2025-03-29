# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos

from .kepler import get_eccentric_anomaly

# **************************************************************************************


def get_orbital_radius(
    semi_major_axis: float,
    mean_anomaly: float,
    eccentricity: float,
) -> float:
    """
    Calculate the orbital radius (r) given the semi-major axis (a), eccentricity (e),
    and eccentric anomaly (E).

    Args:
        semi_major_axis: The semi-major axis (a) (in meters).
        mean_anomaly: The mean anomaly (M) (in degrees).
        eccentricity: The orbital eccentricity (e), (unitless).

    Returns:
        float: The orbital radius (r) in meters.
    """
    E = get_eccentric_anomaly(mean_anomaly, eccentricity)

    # Calculate the orbital radius (r) (in meters):
    return semi_major_axis * (1 - eccentricity * cos(E))


# **************************************************************************************
