# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .common import CartesianCoordinate
from .constants import GRAVITATIONAL_CONSTANT
from .coordinates import get_perifocal_coordinate
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
from .orbit import get_orbital_radius
from .satellite import Satellite
from .tle import TLE
from .vector import rotate

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
    "get_orbital_radius",
    "get_perifocal_coordinate",
    "get_semi_major_axis",
    "get_true_anomaly",
    "rotate",
    "Satellite",
    "CartesianCoordinate",
    "TLE",
]

# **************************************************************************************
