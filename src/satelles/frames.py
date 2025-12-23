# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .body import Body
from .frame import Frame, Reference
from .transforms import (
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
