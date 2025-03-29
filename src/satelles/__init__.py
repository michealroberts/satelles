# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .constants import GRAVITATIONAL_CONSTANT
from .earth import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_MASS,
    EARTH_MEAN_RADIUS,
    EARTH_POLAR_RADIUS,
)
from .kepler import (
    get_eccentric_anomaly,
    get_semi_major_axis,
    get_true_anomaly,
)
from .satellite import Satellite
from .tle import TLE

# **************************************************************************************

__version__ = "0.0.0"

# **************************************************************************************

__license__ = "MIT"

# **************************************************************************************

__all__: list[str] = [
    "EARTH_EQUATORIAL_RADIUS",
    "EARTH_MASS",
    "EARTH_POLAR_RADIUS",
    "EARTH_MEAN_RADIUS",
    "GRAVITATIONAL_CONSTANT",
    "get_eccentric_anomaly",
    "get_semi_major_axis",
    "get_true_anomaly",
    "Satellite",
    "TLE",
]

# **************************************************************************************
