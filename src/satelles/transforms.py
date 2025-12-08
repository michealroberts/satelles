# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime


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
