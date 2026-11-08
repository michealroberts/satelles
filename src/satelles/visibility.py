# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from math import cos, radians, sin
from warnings import warn

from celerity import sun
from celerity.astrometry import get_obliquity_of_the_ecliptic
from celerity.common import GeographicCoordinate
from celerity.nutation import get_nutation_in_longitude, get_nutation_in_obliquity
from celerity.temporal import get_julian_date

from .common import CartesianCoordinate
from .coordinates import convert_eci_to_topocentric
from .earth import EARTH_EQUATORIAL_RADIUS
from .satellite import Satellite
from .transforms import eme2000_to_eci_transform_provider
from .vector import dot, magnitude, normalise, reject

# **************************************************************************************


def is_visible(
    when: datetime,
    satellite: Satellite,
    observer: GeographicCoordinate,
    horizon: float = 0.0,
) -> bool:
    """
    Check if the satellite is above the horizon for the given observer.

    The check uses the observer's topocentric altitude of the satellite, i.e., it
    accounts for the parallax between the observer and the Earth's centre, which is
    significant for satellites (e.g., up to ~70° for a satellite in low Earth orbit).

    Args:
        when (datetime): The time of the observation (a naive datetime is treated
            as UTC).
        satellite (Satellite): The satellite to check.
        observer (GeographicCoordinate): The observer's location.
        horizon (float): The minimum altitude above the horizon that the satellite must
            be above to be considered visible (in degrees). Default is 0.0 degrees.

    Raises:
        ValueError: If the horizon is not between 0 and 90 degrees.
        Warning: If the horizon is set to 30 degrees or more, a warning is issued
            because this may result in a significant reduction in the number of visible
            satellites.
        Warning: If the satellite's position is not accurate (more than +/- 1 day from
            the epoch), a warning is issued.

    Returns:
        bool: True if the satellite is visible, False otherwise.
    """
    # The horizon is the minimum altitude above the horizon that the satellite must be
    # above to be considered visible. The default is 0 degrees, which means that the
    # satellite must be above the horizon to be visible. The maximum is 90 degrees,
    # which means that the satellite must be directly overhead to be visible.
    if horizon < 0.0 or horizon >= 90.0:
        raise ValueError(
            "Horizon must be between 0 (inclusive) and 90 (exclusive) degrees."
        )

    # If the user has set the horizon to 30 degrees or more, we should throw a warning
    # because this may result in a significant reduction in the number of visible
    # satellites.
    if horizon >= 30.0:
        warn(
            """
            Horizon is set to 30 degrees or more; this may significantly reduce 
            the number of visible satellites.
            """,
            stacklevel=2,
        )

    # Treat a naive datetime as UTC, otherwise convert an aware datetime to UTC:
    when = (
        when.replace(tzinfo=timezone.utc)
        if when.tzinfo is None
        else when.astimezone(tz=timezone.utc)
    )

    # Get the Julian date at the epoch:
    JD = get_julian_date(date=when)

    # If we are more than +/- 1 days from the epoch, we need to throw a warning that
    # the satellite's position is not accurate:
    if abs(JD - satellite.jd) >= 1.0:
        warn(
            f"""
            The satellite's position is not accurate. The current date is more 
            than +/- 1 day from the epoch. Please refine the satellite's position 
            by using the latest orbital elements, e.g., TLE or OMM.

            The satellite's epoch is {satellite.jd} and the current date is {JD}.
            
            The difference is {abs(JD - satellite.jd)} days.
            """
        )

    # Propagate a copy of the satellite, so the caller's satellite is left untouched:
    target = satellite.model_copy()

    # Set the epoch of the observation to the specified time:
    target.at(when=when)

    # Convert the satellite's position to the observer's topocentric coordinates:
    topocentric = convert_eci_to_topocentric(
        eci=target.eci_coordinate,
        when=when,
        observer=observer,
    )

    # If the satellite is above the horizon, it is visible:
    return topocentric["altitude"] > horizon


# **************************************************************************************


def is_illuminated(when: datetime, satellite: Satellite) -> bool:
    """
    Check if the satellite is in sunlight, i.e., outside of the Earth's shadow.

    The check uses the cylindrical umbra model (e.g., Vallado, Fundamentals of
    Astrodynamics and Applications, "SIGHT" and "LIGHT" algorithms): the Earth's shadow
    is a cylinder of the Earth's equatorial radius extending from the Earth along the
    Sun–Earth line, away from the Sun. The satellite is in shadow if it is on the
    anti-Sun side of the Earth (r · ŝ < 0) and its perpendicular distance from the
    Sun–Earth line is less than the Earth's equatorial radius.

    The test is made in the library's true-of-date (TOD) ECI frame. A TEME satellite's
    eci_coordinate is already in that frame. An EME2000 or ICRF satellite's position is
    rotated into it by precession and nutation (the ICRF is treated as EME2000, as the
    two differ only by the ~23 mas frame bias). The Sun's geocentric position follows a
    low-precision solar theory (accurate to ~0.01°), corrected for nutation so that it
    is referred to the true equator and equinox of date.

    The model has the following limits:

    - There is no penumbra: the Sun is treated as a point source at infinity, so the
      shadow boundary is sharp (in reality the umbra narrows and a penumbra widens with
      distance from the Earth, by ~0.27° either side of the cylinder).
    - The Earth is a sphere of its equatorial radius (the shadow is not flattened
      towards the poles).
    - There is no atmospheric refraction or absorption, which in reality spreads the
      shadow boundary over several seconds for a satellite in low Earth orbit.

    Args:
        when (datetime): The time of the observation (a naive datetime is treated
            as UTC).
        satellite (Satellite): The satellite to check.

    Raises:
        ValueError: If the satellite's reference frame is not TEME, EME2000 or ICRF
            (e.g., it is unspecified), as its position cannot then be placed in the
            true-of-date ECI frame.

    Returns:
        bool: True if the satellite is illuminated by the Sun, False otherwise.
    """
    # The reference frame validator stores the long name, but also accept the code in
    # case the validator is changed to store codes:
    is_teme = satellite.reference_frame in ("TEME", "True Equator, Mean Equinox")

    is_eme2000 = satellite.reference_frame in (
        "EME2000",
        "Epoch Mean Equinox 2000",
        "ICRF",
        "International Celestial Reference Frame",
    )

    # For any other (or an unspecified) reference frame, eci_coordinate is in the
    # unknown frame of the orbital elements, so it cannot be compared with the Sun:
    if not is_teme and not is_eme2000:
        raise ValueError(
            "The satellite's reference frame must be one of TEME, EME2000 or ICRF, "
            f"but it is {satellite.reference_frame!r}."
        )

    # Treat a naive datetime as UTC, otherwise convert an aware datetime to UTC:
    when = (
        when.replace(tzinfo=timezone.utc)
        if when.tzinfo is None
        else when.astimezone(tz=timezone.utc)
    )

    # Propagate a copy of the satellite, so the caller's satellite is left untouched:
    target = satellite.model_copy()

    # Set the epoch of the observation to the specified time:
    target.at(when=when)

    # Get the satellite's Earth-centred position (in metres), which is in the
    # true-of-date ECI frame for TEME, but in the frame of the elements otherwise:
    r = target.eci_coordinate

    # Rotate an EME2000 (or ICRF) position into the true-of-date ECI frame:
    if is_eme2000:
        r = eme2000_to_eci_transform_provider(when).apply_to_position(r)

    # Get the Sun's true geometric longitude, referred to the mean equinox of date, and
    # correct it for the nutation in longitude, so that it is referred to the true
    # equinox of date (in degrees). N.B. sun.get_equatorial_coordinate is not used here,
    # because it holds the Sun's longitude of perigee fixed, so its right ascension
    # drifts away from the equinox of date (by ~0.46° by 2026):
    λ = radians(
        sun.get_true_geometric_longitude(date=when)
        + get_nutation_in_longitude(date=when)
    )

    # Get the true obliquity of the ecliptic of date, i.e., the mean obliquity corrected
    # for the nutation in obliquity (in degrees):
    ε = radians(
        get_obliquity_of_the_ecliptic(date=when) + get_nutation_in_obliquity(date=when)
    )

    # Get the Sun's geocentric distance (in metres):
    d = sun.get_distance(date=when)

    # Get the Sun's geocentric position on the true equator of date (in metres), from
    # its ecliptic longitude (the Sun's ecliptic latitude is always less than ~1″):
    s = CartesianCoordinate(
        x=d * cos(λ),
        y=d * sin(λ) * cos(ε),
        z=d * sin(λ) * sin(ε),
    )

    # Get the unit vector from the Earth's centre towards the Sun:
    ŝ = normalise(s)

    # If the satellite is on the sunward side of the Earth, it is illuminated:
    if dot(r, ŝ) >= 0.0:
        return True

    # Otherwise, the satellite is illuminated only if it is outside the shadow
    # cylinder, i.e., its distance from the Sun–Earth line is at least the Earth's
    # equatorial radius:
    return magnitude(reject(r, ŝ)) >= EARTH_EQUATORIAL_RADIUS


# **************************************************************************************
