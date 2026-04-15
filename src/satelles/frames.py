# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .body import Body
from .frame import Frame, Reference
from .transforms import (
    eci_to_ecef_transform_provider,
    eme2000_to_eci_transform_provider,
    identity_transform_provider,
    itrf_to_ecef_transform_provider,
)

# **************************************************************************************

ECEF = Frame(
    reference=Reference.ECEF,
    origin=Body.EARTH,
    is_inertial=False,
    parent=None,
    transform_to_parent=identity_transform_provider,
    name="Earth Centered Earth Fixed",
)

# **************************************************************************************

ECI = Frame(
    reference=Reference.ECI,
    origin=Body.EARTH,
    is_inertial=True,
    parent=ECEF,
    transform_to_parent=eci_to_ecef_transform_provider,
    name="Earth Centered Inertial",
)


# **************************************************************************************


EME2000 = Frame(
    reference=Reference.EME2000,
    origin=Body.EARTH,
    is_inertial=True,
    parent=ECI,
    transform_to_parent=eme2000_to_eci_transform_provider,
    name="Earth Mean Equator 2000",
)


# **************************************************************************************


ITRF = Frame(
    reference=Reference.ITRF,
    origin=Body.EARTH,
    is_inertial=False,
    parent=ECEF,
    transform_to_parent=itrf_to_ecef_transform_provider,
    name="International Terrestrial Reference Frame",
)


# **************************************************************************************
