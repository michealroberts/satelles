# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos, radians, sin

from .common import CartesianCoordinate
from .orbit import get_orbital_radius
from .vector import rotate

# **************************************************************************************


def get_perifocal_coordinate(
    semi_major_axis: float,
    mean_anomaly: float,
    true_anomaly: float,
    eccentricity: float,
) -> CartesianCoordinate:
    """
    Calculate the position in the perifocal coordinate system for a satellite.

    The perifocal coordinate system is a coordinate system that is centered on the
    focal point of the orbit, with the x-axis aligned with the periapsis direction.
    The y-axis is perpendicular to the x-axis in the orbital plane, and the z-axis
    is perpendicular to the orbital plane.

    Args:
        semi_major_axis: The semi-major axis (a) (in meters).
        mean_anomaly: The mean anomaly (M) (in degrees).
        true_anomaly: The true anomaly (ν) (in degrees).
        eccentricity: The orbital eccentricity (e), (unitless).

    Returns:
        CartesianCoordinate: The position in the perifocal coordinate system (x, y, z).
    """
    # Calculate the orbital radius (r) for the body:
    r = get_orbital_radius(
        semi_major_axis=semi_major_axis,
        mean_anomaly=mean_anomaly,
        eccentricity=eccentricity,
    )

    x_perifocal = r * cos(radians(true_anomaly))
    y_perifocal = r * sin(radians(true_anomaly))

    # The z-coordinate is always zero in the perifocal frame:
    return CartesianCoordinate(x=x_perifocal, y=y_perifocal, z=0.0)


# **************************************************************************************


def convert_perifocal_to_eci(
    perifocal: CartesianCoordinate,
    argument_of_perigee: float,
    inclination: float,
    raan: float,
) -> CartesianCoordinate:
    """
    Convert perifocal coordinates to Earth-Centered Inertial (ECI) coordinates.

    Args:
        perifocal (CartesianCoordinate): The perifocal coordinates (x, y, z).
        argument_of_perigee (float): The argument of perigee (ω) (in degrees).
        inclination (float): The inclination (i) (in degrees).
        raan (float): The right ascension of ascending node (Ω) (in degrees).

    Returns:
        CartesianCoordinate: The ECI coordinates (x, y, z).
    """
    # Rotate by argument of perigee around the z-axis:
    rotated_z = rotate(perifocal, argument_of_perigee, "z")

    # Rotate by inclination around the x-axis:
    rotated_x = rotate(rotated_z, inclination, "x")

    # Rotate by Right Ascension of Ascending Node (RAAN) around the z-axis:
    eci = rotate(rotated_x, raan, "z")

    # The ECI coordinates are now in the rotated frame:
    return eci


# **************************************************************************************
