# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime
from math import asin, atan2, cos, degrees, pi, pow, radians, sin, sqrt

from celerity.coordinates import (
    EquatorialCoordinate,
    GeographicCoordinate,
    HorizontalCoordinate,
)
from celerity.temporal import get_greenwich_sidereal_time

from .common import CartesianCoordinate
from .earth import EARTH_EQUATORIAL_RADIUS, EARTH_FLATTENING_FACTOR
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


def convert_eci_to_perifocal(
    eci: CartesianCoordinate,
    argument_of_perigee: float,
    inclination: float,
    raan: float,
) -> CartesianCoordinate:
    """
    Convert Earth-Centered Inertial (ECI) coordinates to perifocal coordinates.

    Args:
        eci (CartesianCoordinate): The ECI coordinates (x, y, z).
        argument_of_perigee (float): The argument of perigee (ω) (in degrees).
        inclination (float): The inclination (i) (in degrees).
        raan (float): The right ascension of ascending node (Ω) (in degrees).

    Returns:
        CartesianCoordinate: The perifocal coordinates (x, y, z).
    """
    # Inverse rotate by Right Ascension of Ascending Node (RAAN) around the z-axis:
    rotated_z = rotate(eci, -raan, "z")

    # Inverse rotate by inclination around the x-axis:
    rotated_x = rotate(rotated_z, -inclination, "x")

    # Inverse rotate by argument of perigee around the z-axis:
    perifocal = rotate(rotated_x, -argument_of_perigee, "z")

    # The perifocal coordinates are now in the inversely rotated frame:
    return perifocal


# **************************************************************************************


def convert_ecef_to_eci(
    ecef: CartesianCoordinate,
    when: datetime,
) -> CartesianCoordinate:
    """
    Convert Earth-Centered Earth-Fixed (ECEF) coordinates back to
    Earth-Centered Inertial (ECI) coordinates.

    Args:
        ecef (CartesianCoordinate): The ECEF coordinates (x, y, z).
        when (datetime): The date and time for the conversion.

    Returns:
        CartesianCoordinate: The ECI coordinates (x, y, z).
    """
    # Get the Greenwich Mean Sidereal Time (GMST) for the given date:
    GMST = get_greenwich_sidereal_time(date=when)

    # Rotate around Z-axis (from ECEF to ECI) using the GMST:
    return CartesianCoordinate(
        x=ecef["x"] * cos(radians(GMST * 15)) - ecef["y"] * sin(radians(GMST * 15)),
        y=ecef["x"] * sin(radians(GMST * 15)) + ecef["y"] * cos(radians(GMST * 15)),
        z=ecef["z"],
    )


# **************************************************************************************


def convert_eci_to_ecef(
    eci: CartesianCoordinate,
    when: datetime,
) -> CartesianCoordinate:
    """
    Convert Earth-Centered Inertial (ECI) coordinates to Earth-Centered Earth Fixed (ECEF)
    coordinates.

    Args:
        eci (CartesianCoordinate): The ECI coordinates (x, y, z).
        when (datetime): The date and time for the conversion.

    Returns:
        CartesianCoordinate: The ECEF coordinates (x, y, z).
    """
    # Get the Greenwich Mean Sidereal Time (GMST) for the given date:
    GMST = get_greenwich_sidereal_time(date=when)

    # Rotate around Z-axis (from ECI to ECEF) using the GMST:
    return CartesianCoordinate(
        x=(eci["x"] * cos(radians(GMST * 15))) + (eci["y"] * sin(radians(GMST * 15))),
        y=-(eci["x"] * sin(radians(GMST * 15))) + (eci["y"] * cos(radians(GMST * 15))),
        z=eci["z"],
    )


# **************************************************************************************


def convert_eci_to_equatorial(
    eci: CartesianCoordinate,
) -> EquatorialCoordinate:
    """
    Convert ECI coordinates to equatorial coordinates.

    Args:
        eci (CartesianCoordinate): The ECI coordinates (x, y, z).

    Raises:
        ValueError: If the ECI coordinates are a zero vector.

    Returns:
        EquatorialCoordinate: The equatorial coordinates (RA, Dec).
    """
    x, y, z = eci["x"], eci["y"], eci["z"]

    r = sqrt(x**2 + y**2 + z**2)

    if r == 0:
        raise ValueError("Cannot convert zero vector to equatorial coordinates.")

    ra = degrees(atan2(y, x))

    dec = degrees(asin(z / r))

    if ra < 0:
        ra += 360

    return EquatorialCoordinate(ra=ra % 360, dec=dec)


# **************************************************************************************


def convert_ecef_to_enu(
    ecef: CartesianCoordinate,
    observer: GeographicCoordinate,
) -> CartesianCoordinate:
    """
    Convert  ECEF (Earth-Centered, Earth-Fixed) coordinates into East-North-Up (ENU)
    coordinates using the observer's latitude (φ) and longitude (θ).

    Args:
        ecef (CartesianCoordinate): The ECEF coordinates (x, y, z).
        observer (GeographicCoordinate): The geographic coordinates (lat, lon, el) of the observer.

    Notes:
        The latitude (φ) and longitude (θ) are in degrees, and the height (el) is in meters above mean sea level.
        The ECEF coordinates (x, y, z) are in meters.
        The ENU coordinates (east, north, up) are in meters.

    Returns:
        CartesianCoordinate: The ENU coordinates (east, north, up).
    """

    site = convert_lla_to_ecef(lla=observer)

    # The ECEF relative coordinates are the coordinates of the observer in the ECEF frame:
    dx = ecef["x"] - site["x"]
    dy = ecef["y"] - site["y"]
    dz = ecef["z"] - site["z"]

    # Convert the latitude and longitude to radians:
    φ = radians(observer["latitude"])
    θ = radians(observer["longitude"])

    # The east coordinate is the projection of the ECEF coordinates onto the local
    # east-west plane. The negative sine is used here because the eastward direction
    # involves a rotation in the negative sense around the z-axis in the ENU
    # coordinate system:
    east = -sin(θ) * dx + cos(θ) * dy

    # The north coordinate is the projection of the ECEF coordinates onto the local
    # meridian:
    north = -sin(φ) * cos(θ) * dx - sin(φ) * sin(θ) * dy + cos(φ) * dz

    # The up coordinate is the projection of the ECEF coordinates onto the local
    # vertical:
    up = cos(φ) * cos(θ) * dx + cos(φ) * sin(θ) * dy + sin(φ) * dz

    # The East North-Up coordinates are now in the rotated frame:
    return CartesianCoordinate(x=east, y=north, z=up)


# **************************************************************************************


def convert_enu_to_horizontal(
    enu: CartesianCoordinate,
) -> HorizontalCoordinate:
    """
    Convert local East-North-Up coordinates to horizontal azimuth and altitude.

    Args:
        enu (CartesianCoordinate): Coordinates in the ENU frame (east, north, up) in meters.

    Returns:
        HorizontalCoordinate: The horizontal coordinates (altitude, azimuth) in degrees.
    """
    # Compute the azimuth along the bearing clockwise from north:
    az = degrees(atan2(enu["x"], enu["y"]))

    if az < 0:
        az += 360.0

    return HorizontalCoordinate(
        {
            "alt": degrees(atan2(enu["z"], sqrt(enu["x"] ** 2 + enu["y"] ** 2))),
            "az": az,
        }
    )


# **************************************************************************************


def convert_lla_to_ecef(
    lla: GeographicCoordinate,
) -> CartesianCoordinate:
    """
    Convert geographic coordinates (latitude, longitude, height) to ECEF coordinates.

    Args:
        lla (GeographicCoordinate): The geographic coordinates (lat, lon, el).

    Returns:
        CartesianCoordinate: The ECEF coordinates (x, y, z).

    Raises:
        ValueError: If the flattening factor is not between 0 and 1.
        ValueError: If the latitude is not between -90 and 90 degrees.
        ValueError: If the longitude is not between -180 and 180 degrees.
    """
    earth_radius = EARTH_EQUATORIAL_RADIUS

    # Convert the latitude to radians:
    φ = radians(lla["latitude"])

    # Convert the longitude to radians:
    θ = radians(lla["longitude"])

    # The height (el) is the height above the ellipsoid (e.g., the elevation):
    h = lla["elevation"]

    # The flattening factor (f) is the ratio of the difference between the equatorial
    # and polar radii to the equatorial radius, in the WGS-84 ellipsoid model:
    f = EARTH_FLATTENING_FACTOR

    # Ensure that the latitude (φ) is between -π/2 and π/2 radians:
    if abs(φ) > (pi / 2):
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    # Ensure that the longitude (θ) is between -π and π radians:
    if abs(θ) > pi:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    # Ensure that f is between 0 and 1:
    if f < 0 or f > 1:
        raise ValueError("Earth flattening factor must be between 0 and 1.")

    # The square of the flattening factor (FF) is used to calculate the radius of
    # curvature in the prime vertical (N):
    FF = f * (2 - f)

    # The radius of curvature in the prime vertical (N) is the Earth’s east–west
    # curvature radius at the given latitude, accounting for ellipsoidal flattening:
    C = 1 / sqrt(1 - (FF * pow(sin(φ), 2)))

    # The radius of curvature in the prime vertical (N):
    N = earth_radius * C

    # Compute the x coordinate in the ECEF frame:
    x = (N + h) * cos(φ) * cos(θ)

    # Compute the y coordinate in the ECEF frame:
    y = (N + h) * cos(φ) * sin(θ)

    # Compute the z coordinate in the ECEF frame:
    z = ((N * (1 - FF)) + h) * sin(φ)

    return CartesianCoordinate(
        x=x,
        y=y,
        z=z,
    )


# **************************************************************************************
