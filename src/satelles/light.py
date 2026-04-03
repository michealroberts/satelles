# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

from .constants import c

# **************************************************************************************


def convert_distance_to_light_travel_time(distance: float | int) -> float:
    """
    Convert a distance in meters to the time it takes for light to travel that distance.

    Args:
        distance: The distance in meters.

    Returns:
        float: The time in seconds it takes for light to travel the given distance.

    Raises:
        ValueError: If distance is negative.
    """
    # Guard against negative distances:
    if distance < 0:
        raise ValueError("Distance must be non-negative.")

    return distance / c


# **************************************************************************************


def convert_light_travel_time_to_distance(time: float | int) -> float:
    """
    Convert a time in seconds to the distance light travels in that time.

    Args:
        time: The time in seconds.

    Returns:
        float: The distance in meters that light travels in the given time.

    Raises:
        ValueError: If time is negative.
    """
    # Guard against negative times:
    if time < 0:
        raise ValueError("Time must be non-negative.")

    return time * c


# **************************************************************************************
