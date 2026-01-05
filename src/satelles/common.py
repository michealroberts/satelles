# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime
from typing import TypedDict

# **************************************************************************************


class CartesianCoordinate(TypedDict):
    """
    Typed dictionary for a Cartesian coordinate.
    """

    x: float
    y: float
    z: float


# **************************************************************************************


class Position(CartesianCoordinate):
    """
    Typed dictionary for a position vector.
    """

    ...


# **************************************************************************************


class Velocity(TypedDict):
    """
    Typed dictionary for a velocity vector.
    """

    vx: float
    vy: float
    vz: float


# **************************************************************************************


class Acceleration(TypedDict):
    """
    Typed dictionary for a gravitational acceleration vector.
    """

    ax: float
    ay: float
    az: float


# **************************************************************************************


class StateVector(Position, Velocity):
    """
    Typed dictionary for a state vector, combining position and velocity.
    """

    ...


# **************************************************************************************


class TopocentricCoordinate(TypedDict):
    # The date and time of the observation (in UTC):
    at: datetime
    # The altitude angle above the horizon for the observed object (in degrees):
    altitude: float
    # The azimuth angle measured clockwise from true north to the
    # direction of the observed object (in degrees):
    azimuth: float
    # The distance from the observation point to the observed object (in meters):
    range: float
    # The round-trip (two-way) light time for a signal between the observed object
    # and the observation point (in seconds):
    time_of_flight: float


# **************************************************************************************
