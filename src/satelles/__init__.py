# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .body import Body
from .checksum import perform_checksum_compute
from .common import (
    Acceleration,
    CartesianCoordinate,
    StateVector,
    TopocentricCoordinate,
)
from .constants import GRAVITATIONAL_CONSTANT
from .coordinates import (
    convert_ecef_to_eci,
    convert_ecef_to_enu,
    convert_ecef_to_lla,
    convert_eci_to_ecef,
    convert_eci_to_equatorial,
    convert_eci_to_perifocal,
    convert_eci_to_topocentric,
    convert_enu_to_horizontal,
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
from .frame import (
    Frame,
    Reference,
    Transform,
    TransformProvider,
)
from .gravity import get_gravitational_acceleration
from .hohmann import (
    HohmannTransferParameters,
    get_hohmann_transfer_semi_major_axis,
)
from .interpolation import (
    BarycentricLagrange3DPositionInterpolator,
    Base3DInterpolator,
    Hermite3DKinematicInterpolator,
    Hermite3DPositionInterpolator,
)
from .kepler import (
    get_eccentric_anomaly,
    get_semi_latus_rectum,
    get_semi_major_axis,
    get_true_anomaly,
)
from .matrix import (
    Matrix3x3,
)
from .mjd import (
    convert_mjd_as_parts_to_datetime,
    convert_mjd_to_datetime,
    get_modified_julian_date_as_parts,
    get_modified_julian_date_from_parts,
)
from .models import (
    Position,
    Velocity,
)
from .orbit import get_orbital_radius
from .origin import Origin
from .quaternion import (
    EulerRotation,
    Quaternion,
    QuaternionEulerKind,
    QuaternionEulerOrder,
)
from .runge_kutta import (
    RungeKuttaPropagationParameters,
    propagate_rk4,
)
from .satellite import Satellite
from .slr import (
    CPFEphemeris,
    CPFHeader,
)
from .symplectic import (
    VerletPropagationParameters,
    propagate_verlet,
)
from .tle import TLE
from .transforms import (
    ecef_to_eci_transform_provider,
    eci_to_ecef_transform_provider,
    identity_transform_provider,
)
from .vector import (
    Vector,
    add,
    angle,
    cross,
    dilate,
    distance,
    dot,
    magnitude,
    normalise,
    project,
    reject,
    rotate,
    subtract,
)
from .velocity import get_perifocal_velocity
from .visibility import is_visible

# **************************************************************************************

__version__ = "0.26.0"

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
    "add",
    "angle",
    "convert_ecef_to_eci",
    "convert_ecef_to_enu",
    "convert_ecef_to_lla",
    "convert_eci_to_ecef",
    "convert_eci_to_equatorial",
    "convert_eci_to_perifocal",
    "convert_eci_to_topocentric",
    "convert_enu_to_horizontal",
    "convert_lla_to_ecef",
    "convert_mjd_as_parts_to_datetime",
    "convert_mjd_to_datetime",
    "convert_perifocal_to_eci",
    "cross",
    "dilate",
    "distance",
    "dot",
    "ecef_to_eci_transform_provider",
    "eci_to_ecef_transform_provider",
    "get_eccentric_anomaly",
    "get_gravitational_acceleration",
    "get_hohmann_transfer_semi_major_axis",
    "get_modified_julian_date_as_parts",
    "get_modified_julian_date_from_parts",
    "get_orbital_radius",
    "get_perifocal_coordinate",
    "get_perifocal_velocity",
    "get_semi_latus_rectum",
    "get_semi_major_axis",
    "get_true_anomaly",
    "identity_transform_provider",
    "is_visible",
    "normalise",
    "magnitude",
    "perform_checksum_compute",
    "propagate_rk4",
    "propagate_verlet",
    "project",
    "reject",
    "rotate",
    "subtract",
    "Acceleration",
    "BarycentricLagrange3DPositionInterpolator",
    "Base3DInterpolator",
    "Body",
    "CartesianCoordinate",
    "Covariance",
    "CPFEphemeris",
    "CPFHeader",
    "EulerRotation",
    "Frame",
    "Hermite3DPositionInterpolator",
    "Hermite3DKinematicInterpolator",
    "HohmannTransferParameters",
    "Matrix3x3",
    "Origin",
    "Position",
    "Quaternion",
    "QuaternionEulerKind",
    "QuaternionEulerOrder",
    "Reference",
    "RungeKuttaPropagationParameters",
    "Satellite",
    "StateVector",
    "TLE",
    "TopocentricCoordinate",
    "Transform",
    "TransformProvider",
    "Vector",
    "Velocity",
    "VerletPropagationParameters",
]

# **************************************************************************************
