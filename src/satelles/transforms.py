# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime

from celerity.temporal import get_greenwich_sidereal_time

from .common import CartesianCoordinate
from .frame import Transform
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
