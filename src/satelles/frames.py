# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .body import Body
from .frame import Frame, Reference
from .transforms import (
    ecef_to_eci_transform_provider,
    identity_transform_provider,
)

# **************************************************************************************

ECI = Frame(
    reference=Reference.ECI,
    origin=Body.EARTH,
    is_inertial=True,
    parent=None,
    transform_to_parent=identity_transform_provider,
    name="Earth Centered Inertial",
)

# **************************************************************************************

ECEF = Frame(
    reference=Reference.ECEF,
    origin=Body.EARTH,
    is_inertial=False,
    parent=ECI,
    transform_to_parent=ecef_to_eci_transform_provider,
    name="Earth Centered Earth Fixed",
)

# **************************************************************************************
