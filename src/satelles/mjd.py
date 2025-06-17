# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from math import floor
from typing import Tuple

from celerity.temporal import get_modified_julian_date

# **************************************************************************************

MJD_EPOCH_AS_DATETIME = datetime(1858, 11, 17, 0, 0, 0, tzinfo=timezone.utc)

# **************************************************************************************


def convert_mjd_to_datetime(mjd: float) -> datetime:
    """
    Convert Modified Julian Date (MJD) to a UTC datetime object.

    Args:
        mjd (float): The Modified Julian Date to convert (e.g., 60000.0).

    Returns:
        datetime: The corresponding UTC datetime object.
    """
    return MJD_EPOCH_AS_DATETIME + timedelta(days=mjd)


# **************************************************************************************


def get_modified_julian_date_from_parts(mjd: Tuple[int, float]) -> datetime:
    """
    Convert a tuple of (days, seconds) representing Modified Julian Date (MJD)
    to a UTC datetime object.

    Args:
        mjd (Tuple[int, float]): The Modified Julian Date parts to convert (e.g., 60000, 23500.0).

    Returns:
        datetime: The corresponding UTC datetime object.
    """
    days, seconds = mjd

    return MJD_EPOCH_AS_DATETIME + timedelta(days=days, seconds=seconds)


# **************************************************************************************


def get_modified_julian_date_as_parts(when: datetime) -> Tuple[int, float]:
    """
    Convert a UTC datetime object to Modified Julian Date (MJD) and its
    corresponding seconds of the day (e.g., 0.0 to 86400.0).

    Args:
        when (datetime): The UTC datetime to convert.

    Returns:
        Tuple[int, float]: (integer MJD, seconds since UTC midnight)
    """
    # If the datetime does not have a timezone (e.g., a naive datetime), assume UTC;
    # otherwise, convert it to UTC:
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    else:
        when = when.astimezone(tz=timezone.utc)

    # Get the Modified Julian Date for the given datetime:
    MJD = get_modified_julian_date(when)

    # Get the UTC date at midnight for the given datetime:
    midnight = when.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Calculate the seconds of the day since midnight for the currrent datetime:
    seconds_of_day = (when - midnight).total_seconds()

    return floor(MJD), seconds_of_day


# **************************************************************************************
