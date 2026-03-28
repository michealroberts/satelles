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
