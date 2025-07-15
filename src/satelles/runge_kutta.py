# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from copy import deepcopy
from typing import List, Tuple, TypedDict

from .common import Acceleration, CartesianCoordinate, Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS
from .gravity import get_gravitational_acceleration

# **************************************************************************************


class RungeKuttaPropagationParameters(TypedDict):
    # The time step (in seconds) for the propagation:
    timestep: float
    # The number of steps to propagate the satellite's state for:
    number_of_steps: int


# **************************************************************************************


def propagate_rk4(
    position: CartesianCoordinate,
    velocity: Velocity,
    params: RungeKuttaPropagationParameters,
    μ: float = EARTH_MASS * GRAVITATIONAL_CONSTANT,
) -> Tuple[List[CartesianCoordinate], List[Velocity]]:
    """
    Propagate the satellite's state using a 4th-order Runge–Kutta method.

    This integrator advances the state (position and velocity) by computing four
    intermediate slopes (k1, k2, k3, k4) at each step. Although it is not symplectic,
    the method is highly accurate for a fixed time step and is often used when high
    precision is required.

    Args:
        position: Initial position vector with keys "x", "y", "z" (in meters).
        velocity: Initial velocity vector with keys "vx", "vy", "vz" (in m/s).
        params: RungeKuttaPropagationParameters
        μ (float): Gravitational parameter (m^3/s^2), defaults to Earth's μ.

    Returns:
        Tuple[List[CartesianCoordinate], List[Velocity]]: Final position and velocity vectors after propagation.
    """
    # Initialize state variables for position and velocity:
    r = deepcopy(position)
    v = deepcopy(velocity)

    positions: List[CartesianCoordinate] = []
    velocities: List[Velocity] = []

    # Initialize time step (and default to 1 second if not provided):
    dt = params.get("timestep", 1.0)

    for _ in range(params.get("number_of_steps", 1)):
        # k1: at the beginning of the interval
        a1: Acceleration = get_gravitational_acceleration(r, μ)
        k1_r = v  # derivative of position is current velocity
        k1_v = a1  # derivative of velocity is acceleration

        # k2: evaluate at the midpoint using k1
        r2: CartesianCoordinate = {
            "x": r["x"] + 0.5 * dt * k1_r["vx"],
            "y": r["y"] + 0.5 * dt * k1_r["vy"],
            "z": r["z"] + 0.5 * dt * k1_r["vz"],
        }
        v2: Velocity = {
            "vx": v["vx"] + 0.5 * dt * k1_v["ax"],
            "vy": v["vy"] + 0.5 * dt * k1_v["ay"],
            "vz": v["vz"] + 0.5 * dt * k1_v["az"],
        }
        a2: Acceleration = get_gravitational_acceleration(r2, μ)
        k2_r = v2
        k2_v = a2

        # k3: evaluate at the midpoint using k2
        r3: CartesianCoordinate = {
            "x": r["x"] + 0.5 * dt * k2_r["vx"],
            "y": r["y"] + 0.5 * dt * k2_r["vy"],
            "z": r["z"] + 0.5 * dt * k2_r["vz"],
        }
        v3: Velocity = {
            "vx": v["vx"] + 0.5 * dt * k2_v["ax"],
            "vy": v["vy"] + 0.5 * dt * k2_v["ay"],
            "vz": v["vz"] + 0.5 * dt * k2_v["az"],
        }
        a3: Acceleration = get_gravitational_acceleration(r3, μ)
        k3_r = v3
        k3_v = a3

        # k4: evaluate at the end of the interval using k3
        r4: CartesianCoordinate = {
            "x": r["x"] + dt * k3_r["vx"],
            "y": r["y"] + dt * k3_r["vy"],
            "z": r["z"] + dt * k3_r["vz"],
        }
        v4: Velocity = {
            "vx": v["vx"] + dt * k3_v["ax"],
            "vy": v["vy"] + dt * k3_v["ay"],
            "vz": v["vz"] + dt * k3_v["az"],
        }
        a4: Acceleration = get_gravitational_acceleration(r4, μ)
        k4_r = v4
        k4_v = a4

        # Update the position using the current velocity and acceleration:
        r_next: CartesianCoordinate = {
            "x": r["x"]
            + (dt / 6.0)
            * (k1_r["vx"] + 2.0 * k2_r["vx"] + 2.0 * k3_r["vx"] + k4_r["vx"]),
            "y": r["y"]
            + (dt / 6.0)
            * (k1_r["vy"] + 2.0 * k2_r["vy"] + 2.0 * k3_r["vy"] + k4_r["vy"]),
            "z": r["z"]
            + (dt / 6.0)
            * (k1_r["vz"] + 2.0 * k2_r["vz"] + 2.0 * k3_r["vz"] + k4_r["vz"]),
        }

        positions.append(r_next)

        # Update velocity using average of current and next acceleration:
        v_next: Velocity = {
            "vx": v["vx"]
            + (dt / 6.0)
            * (k1_v["ax"] + 2.0 * k2_v["ax"] + 2.0 * k3_v["ax"] + k4_v["ax"]),
            "vy": v["vy"]
            + (dt / 6.0)
            * (k1_v["ay"] + 2.0 * k2_v["ay"] + 2.0 * k3_v["ay"] + k4_v["ay"]),
            "vz": v["vz"]
            + (dt / 6.0)
            * (k1_v["az"] + 2.0 * k2_v["az"] + 2.0 * k3_v["az"] + k4_v["az"]),
        }

        velocities.append(v_next)

        # Set the current state to the next state for the next iteration:
        r, v = r_next, v_next

    return positions, velocities


# **************************************************************************************
