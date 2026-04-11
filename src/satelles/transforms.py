# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime

from celerity.astrometry import get_obliquity_of_the_ecliptic
from celerity.ecliptic import get_true_obliquity_of_the_ecliptic
from celerity.equinox import get_equation_of_the_equinoxes
from celerity.nutation import get_nutation_in_longitude
from celerity.temporal import get_greenwich_sidereal_time, get_julian_date

from .common import CartesianCoordinate
from .frame import Transform
from .matrix import (
    get_rotation_matrix_x,
    get_rotation_matrix_y,
    get_rotation_matrix_z,
    multiply,
)
from .quaternion import Quaternion

# **************************************************************************************


def identity_transform_provider(_: datetime) -> Transform:
    """
    Identity transform (no rotation, no translation).

    Returns:
        Transform: An identity transform with no rotation and zero translation.
    """
    return Transform(
        rotation=Quaternion.identity(),
        translation=CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        ),
    )


# **************************************************************************************


def ecef_to_eci_transform_provider(when: datetime) -> Transform:
    """
    Transform from ECEF frame to ECI frame at a given time.

    Args:
        when (datetime): The time at which to compute the transform.

    Returns:
        Transform: The transform from ECEF to ECI frame.
    """
    # Get the Greenwich Mean Sidereal Time (GMST) for the given date (and convert to
    # degrees):
    GMST = get_greenwich_sidereal_time(date=when) * 15

    # Create the rotation coordinate axis (Z-axis):
    axis = CartesianCoordinate(
        x=0.0,
        y=0.0,
        z=1.0,
    )

    # Create the rotation quaternion for the GMST angle about the Z-axis:
    rotation = Quaternion.from_axis_angle(
        axis=axis,
        angle=GMST,
    )

    # No translation between ECEF and ECI origins:
    translation = CartesianCoordinate(
        x=0.0,
        y=0.0,
        z=0.0,
    )

    # Return the transform:
    return Transform(
        rotation=rotation,
        translation=translation,
    )


# **************************************************************************************


def eci_to_ecef_transform_provider(when: datetime) -> Transform:
    """
    Transform from ECI frame to ECEF frame at a given time.

    Args:
        when (datetime): The time at which to compute the transform.

    Returns:
        Transform: The transform from ECI to ECEF frame.
    """
    # Get the Greenwich Mean Sidereal Time (GMST) for the given date (and convert to
    # degrees):
    GMST = get_greenwich_sidereal_time(date=when) * 15

    # Create the rotation coordinate axis (Z-axis):
    axis = CartesianCoordinate(
        x=0.0,
        y=0.0,
        z=1.0,
    )

    # Create the rotation quaternion for the negative GMST angle about the Z-axis:
    rotation = Quaternion.from_axis_angle(
        axis=axis,
        angle=-GMST,
    )

    # No translation between ECEF and ECI origins:
    translation = CartesianCoordinate(
        x=0.0,
        y=0.0,
        z=0.0,
    )

    # Return the transform:
    return Transform(
        rotation=rotation,
        translation=translation,
    )


# **************************************************************************************


def eme2000_to_eci_transform_provider(when: datetime) -> Transform:
    """
    Transform from EME2000 to ECI frame at a given time.

    Args:
        when (datetime): The time at which to compute the transform.

    Returns:
        Transform: The transform from EME2000 to ECI frame at the given time.
    """
    T = (get_julian_date(when) - 2451545.0) / 36525.0

    ζ = (2306.2181 * T + 0.30188 * T * T + 0.017998 * T * T * T) / 3600.0

    θ = (2004.3109 * T - 0.42665 * T * T - 0.041833 * T * T * T) / 3600.0

    z = (2306.2181 * T + 1.09468 * T * T + 0.018203 * T * T * T) / 3600.0

    precession = multiply(
        get_rotation_matrix_z(-z),
        multiply(
            get_rotation_matrix_y(θ),
            get_rotation_matrix_z(-ζ),
        ),
    )

    ε = get_obliquity_of_the_ecliptic(when)

    e = get_true_obliquity_of_the_ecliptic(when)

    Δψ = get_nutation_in_longitude(
        date=when,
    )

    nutation = multiply(
        get_rotation_matrix_x(-e),
        multiply(
            get_rotation_matrix_z(-Δψ),
            get_rotation_matrix_x(ε),
        ),
    )

    rotation = Quaternion.from_rotation_matrix(
        multiply(nutation, precession),
    )

    return Transform(
        rotation=rotation,
        translation=CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        ),
    )


# **************************************************************************************


def teme_to_eci_transform_provider(when: datetime) -> Transform:
    """
    Transform from TEME to ECI using the equation of the equinoxes.

    Args:
        when (datetime): The time at which to compute the transform.

    Returns:
        Transform: The transform from TEME to ECI.
    """
    axis = CartesianCoordinate(
        x=0.0,
        y=0.0,
        z=1.0,
    )

    rotation = Quaternion.from_axis_angle(
        axis=axis,
        angle=get_equation_of_the_equinoxes(
            date=when,
        ),
    )

    return Transform(
        rotation=rotation,
        translation=CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        ),
    )


# **************************************************************************************
