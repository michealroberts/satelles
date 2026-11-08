# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

EARTH_MASS = 5.972168e24  # kg

# **************************************************************************************

EARTH_EQUATORIAL_RADIUS = 6_378_137  # m

# **************************************************************************************

"""
The flattening of the Earth is defined as the difference between the equatorial and polar
radii divided by the equatorial radius. This is a measure of how much the Earth deviates
from being a perfect sphere. In the WGS-84 ellipsoid model the flattening is a defining
constant, 1/f = 298.257223563 exactly, alongside the equatorial radius.
"""
EARTH_FLATTENING_FACTOR = 1 / 298.257223563

# **************************************************************************************

"""
The polar radius (semi-minor axis) of the WGS-84 ellipsoid is not a defining constant;
it is derived from the equatorial radius and the flattening as b = a * (1 - f).
"""
EARTH_POLAR_RADIUS = EARTH_EQUATORIAL_RADIUS * (1 - EARTH_FLATTENING_FACTOR)  # m

# **************************************************************************************

EARTH_MEAN_RADIUS = 6_371_008.7714  # m

# **************************************************************************************
