# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .common import Acceleration, CartesianCoordinate, Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .coordinates import (
    convert_eci_to_equatorial,
    convert_perifocal_to_eci,
    get_perifocal_coordinate,
)
from .earth import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_MASS,
    EARTH_MEAN_RADIUS,
    EARTH_POLAR_RADIUS,
)
from .gravity import get_gravitational_acceleration
from .kepler import (
    get_eccentric_anomaly,
    get_semi_latus_rectum,
    get_semi_major_axis,
    get_true_anomaly,
)
from .orbit import get_orbital_radius
from .satellite import Satellite
from .symplectic import (
    VerletPropagationParameters,
    propagate_verlet,
)
from .tle import TLE
from .vector import rotate
from .velocity import get_perifocal_velocity

# **************************************************************************************

__version__ = "0.3.0"

# **************************************************************************************

__license__ = "MIT"

# **************************************************************************************

__all__: list[str] = [
    "EARTH_EQUATORIAL_RADIUS",
    "EARTH_MASS",
    "EARTH_POLAR_RADIUS",
    "EARTH_MEAN_RADIUS",
    "GRAVITATIONAL_CONSTANT",
    "convert_eci_to_equatorial",
    "convert_perifocal_to_eci",
    "get_eccentric_anomaly",
    "get_orbital_radius",
    "get_perifocal_coordinate",
    "get_perifocal_velocity",
    "get_semi_latus_rectum",
    "get_semi_major_axis",
    "get_true_anomaly",
    "get_gravitational_acceleration",
    "propagate_verlet",
    "rotate",
    "Acceleration",
    "Satellite",
    "CartesianCoordinate",
    "TLE",
    "Velocity",
    "VerletPropagationParameters",
]

# **************************************************************************************
