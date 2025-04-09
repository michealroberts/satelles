# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from warnings import warn

from celerity.common import GeographicCoordinate
from celerity.coordinates import convert_equatorial_to_horizontal
from celerity.temporal import get_julian_date

from .satellite import Satellite

# **************************************************************************************


def is_visible(
    when: datetime,
    satellite: Satellite,
    observer: GeographicCoordinate,
    horizon: float = 0.0,
):
    """
    Check if the satellite is visible from the given location.

    Args:
        when (datetime): The time of the observation.
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

    # Set the epoch of the observation to the specified time:
    satellite.at(when=when.astimezone(tz=timezone.utc))

    # Convert the equatorial coordinate of the satellite to horizontal (observed topocentric)
    # coordinates:
    horizontal = convert_equatorial_to_horizontal(
        date=when,
        observer=observer,
        target=satellite.equatorial_coordinate,
    )

    # If the satellite is above the horizon, it is visible:
    return horizontal["alt"] > horizon


# **************************************************************************************
