# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

EARTH_MASS = 5.972168e24  # kg

# **************************************************************************************

EARTH_EQUATORIAL_RADIUS = 6_378_137  # m

# **************************************************************************************

EARTH_POLAR_RADIUS = 6_356_752  # m

# **************************************************************************************

EARTH_MEAN_RADIUS = 6_371_008.7714  # m

# **************************************************************************************

"""
The flattening of the Earth is defined as the difference between the equatorial and polar
radii divided by the equatorial radius. This is a measure of how much the Earth deviates
from being a perfect sphere.
"""
EARTH_FLATTENING_FACTOR = (
    EARTH_EQUATORIAL_RADIUS - EARTH_POLAR_RADIUS
) / EARTH_EQUATORIAL_RADIUS

# **************************************************************************************
