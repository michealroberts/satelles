# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from enum import Enum
from math import cos, radians

from .earth import EARTH_EQUATORIAL_RADIUS
from .kepler import get_eccentric_anomaly

# **************************************************************************************

# The semi-major axis of a geostationary orbit (in meters):
GEO_SEMI_MAJOR_AXIS = 42_164_200.0

# The bandwidth (tolerance) around the GEO semi-major axis for classification (in meters):
GEO_BANDWIDTH = 500_000.0

# The upper semi-major axis limit for Low Earth Orbit (in meters):
# LEO extends up to an altitude of 2,000 km above Earth's equatorial surface.
LEO_SEMI_MAJOR_AXIS_LIMIT = EARTH_EQUATORIAL_RADIUS + 2_000_000.0

# The eccentricity threshold above which an orbit is classified as Highly Elliptical:
HEO_ECCENTRICITY_THRESHOLD = 0.25

# **************************************************************************************


class OrbitClassification(Enum):
    """
    Classification of satellite orbits by orbital regime.
    """

    # Low Earth Orbit: altitude from ~160 km to ~2,000 km.
    LEO = "LEO"

    # Medium Earth Orbit: altitude from ~2,000 km to ~35,286 km.
    MEO = "MEO"

    # Geostationary/Geosynchronous Earth Orbit: altitude ~35,786 km.
    GEO = "GEO"

    # Highly Elliptical Orbit: eccentricity greater than 0.25 (e.g., Molniya orbits).
    HEO = "HEO"


# **************************************************************************************


def classify_orbit(
    semi_major_axis: float,
    eccentricity: float,
) -> OrbitClassification:
    """
    Classify the orbital regime of a satellite based on its semi-major axis and
    eccentricity.

    The classification follows conventional orbital regime definitions:

    - HEO (Highly Elliptical Orbit): eccentricity > 0.25 (e.g., Molniya orbits).
    - LEO (Low Earth Orbit): semi-major axis below 2,000 km above Earth's equatorial
      radius (altitude < 2,000 km).
    - GEO (Geostationary Earth Orbit): semi-major axis within ±500 km of the
      geostationary orbit radius (~42,164 km).
    - MEO (Medium Earth Orbit): all other orbits (including those beyond GEO).

    Args:
        semi_major_axis: The semi-major axis of the orbit (in meters).
        eccentricity: The orbital eccentricity (unitless, in the range [0, 1)).

    Returns:
        The orbital regime classification as an OrbitClassification enum value.
    """
    # HEO: Highly Elliptical Orbit takes precedence over all other criteria:
    if eccentricity > HEO_ECCENTRICITY_THRESHOLD:
        return OrbitClassification.HEO

    # LEO: Low Earth Orbit — semi-major axis below 2,000 km altitude:
    if semi_major_axis < LEO_SEMI_MAJOR_AXIS_LIMIT:
        return OrbitClassification.LEO

    # GEO: Geostationary Earth Orbit — semi-major axis within ±500 km of GEO:
    if abs(semi_major_axis - GEO_SEMI_MAJOR_AXIS) <= GEO_BANDWIDTH:
        return OrbitClassification.GEO

    # MEO: Medium Earth Orbit — all remaining orbits:
    return OrbitClassification.MEO


# **************************************************************************************


def get_orbital_radius(
    semi_major_axis: float,
    mean_anomaly: float,
    eccentricity: float,
) -> float:
    """
    Calculate the orbital radius (r) given the semi-major axis (a), eccentricity (e),
    and eccentric anomaly (E).

    Args:
        semi_major_axis: The semi-major axis (a) (in meters).
        mean_anomaly: The mean anomaly (M) (in degrees).
        eccentricity: The orbital eccentricity (e), (unitless).

    Returns:
        float: The orbital radius (r) in meters.
    """
    E = radians(get_eccentric_anomaly(mean_anomaly, eccentricity))

    # Calculate the orbital radius (r) (in meters):
    return semi_major_axis * (1 - eccentricity * cos(E))


# **************************************************************************************
