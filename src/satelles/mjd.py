# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timedelta, timezone

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
