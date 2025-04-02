# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import List, Tuple, TypedDict

from .common import Acceleration, CartesianCoordinate, Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS
from .gravity import get_gravitational_acceleration

# **************************************************************************************


class VerletPropagationParameters(TypedDict):
    # The time step (in seconds) for the propagation:
    timestep: float
    # The number of steps to propagate the satellite's state for:
    number_of_steps: int


# **************************************************************************************


def propagate_verlet(
    position: CartesianCoordinate,
    velocity: Velocity,
    params: VerletPropagationParameters,
    μ: float = EARTH_MASS * GRAVITATIONAL_CONSTANT,
) -> Tuple[List[CartesianCoordinate], List[Velocity]]:
    """
    Propagate the satellite's state using the Velocity Verlet method in a single function.

    Args:
        position: Initial position vector with keys "x", "y", "z" (in meters).
        velocity: Initial velocity vector with keys "vx", "vy", "vz" (in m/s).
        params: VerletPropagationParameters
        μ (float): Gravitational parameter (m^3/s^2), defaults to Earth's μ.

    Returns:
        Tuple[CartesianCoordinate, Velocity]: Final position and velocity vectors after propagation.
    """
    # Initialize state variables for position and velocity:
    r = position
    v = velocity

    positions: List[CartesianCoordinate] = []
    velocities: List[Velocity] = []

    # Initialize time step (and default to 1 second if not provided):
    dt = params.get("timestep", 1.0)

    for _ in range(params.get("number_of_steps", 1)):
        # Compute acceleration at current position:
        a: Acceleration = get_gravitational_acceleration(r, μ)

        # Update the position using the current velocity and acceleration:
        r_next: CartesianCoordinate = {
            "x": r["x"] + v["vx"] * dt + 0.5 * a["ax"] * dt * dt,
            "y": r["y"] + v["vy"] * dt + 0.5 * a["ay"] * dt * dt,
            "z": r["z"] + v["vz"] * dt + 0.5 * a["az"] * dt * dt,
        }

        positions.append(r_next)

        # Compute acceleration at new position:
        a_next: Acceleration = get_gravitational_acceleration(r_next, μ)

        # Update velocity using average of current and next acceleration:
        v_next: Velocity = {
            "vx": v["vx"] + 0.5 * (a["ax"] + a_next["ax"]) * dt,
            "vy": v["vy"] + 0.5 * (a["ay"] + a_next["ay"]) * dt,
            "vz": v["vz"] + 0.5 * (a["az"] + a_next["az"]) * dt,
        }

        velocities.append(v_next)

        # Set the current state to the next state for the next iteration:
        r, v = r_next, v_next

    return positions, velocities


# **************************************************************************************
