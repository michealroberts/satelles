# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .checksum import perform_checksum_compute
from .common import Acceleration, CartesianCoordinate, Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .coordinates import (
    convert_ecef_to_eci,
    convert_ecef_to_enu,
    convert_eci_to_ecef,
    convert_eci_to_equatorial,
    convert_lla_to_ecef,
    convert_perifocal_to_eci,
    get_perifocal_coordinate,
)
from .covariance import Covariance
from .earth import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_FLATTENING_FACTOR,
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
from .runge_kutta import (
    RungeKuttaPropagationParameters,
    propagate_rk4,
)
from .satellite import Satellite
from .symplectic import (
    VerletPropagationParameters,
    propagate_verlet,
)
from .tle import TLE
from .vector import rotate
from .velocity import get_perifocal_velocity
from .visibility import is_visible

# **************************************************************************************

__version__ = "0.8.0"

# **************************************************************************************

__license__ = "MIT"

# **************************************************************************************

__all__: list[str] = [
    "__version__",
    "__license__",
    "EARTH_EQUATORIAL_RADIUS",
    "EARTH_FLATTENING_FACTOR",
    "EARTH_MASS",
    "EARTH_POLAR_RADIUS",
    "EARTH_MEAN_RADIUS",
    "GRAVITATIONAL_CONSTANT",
    "convert_ecef_to_eci",
    "convert_ecef_to_enu",
    "convert_eci_to_ecef",
    "convert_eci_to_equatorial",
    "convert_lla_to_ecef",
    "convert_perifocal_to_eci",
    "get_eccentric_anomaly",
    "get_orbital_radius",
    "get_perifocal_coordinate",
    "get_perifocal_velocity",
    "get_semi_latus_rectum",
    "get_semi_major_axis",
    "get_true_anomaly",
    "get_gravitational_acceleration",
    "is_visible",
    "perform_checksum_compute",
    "propagate_rk4",
    "propagate_verlet",
    "rotate",
    "Acceleration",
    "CartesianCoordinate",
    "Covariance",
    "RungeKuttaPropagationParameters",
    "Satellite",
    "TLE",
    "Velocity",
    "VerletPropagationParameters",
]

# **************************************************************************************
