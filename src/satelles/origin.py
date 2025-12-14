# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from enum import Enum

# **************************************************************************************


class Origin(Enum):
    OBSERVER = "Observer"
    SOLAR_SYSTEM_BARYCENTER = "Solar System Barycenter"
    EARTH_MOON_BARYCENTER = "Earth-Moon Barycenter"
    L1 = "L1 Lagrange Point"
    L2 = "L2 Lagrange Point"
    L3 = "L3 Lagrange Point"
    L4 = "L4 Lagrange Point"
    L5 = "L5 Lagrange Point"
    # etc.


# **************************************************************************************
