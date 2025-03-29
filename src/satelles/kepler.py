# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import cos, pi, sin
from typing import Optional

from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS

# **************************************************************************************


def get_semi_major_axis(mean_motion: float, mass: Optional[float] = 0.0) -> float:
    """
    Calculate the semi-major axis of the satellite's orbit in meters.

    The semi-major axis is calculated using the mean motion and the gravitational
    constant of the Earth.

    Args:
        mean_motion: The mean motion of the satellite in revolutions per day.
        mass: The mass of the satellite in kilograms. Default is 0.0 (for a point mass).

    Returns:
        The semi-major axis (in SI meters).
    """
    if mass is None:
        mass = 0.0

    # Calculate the standard gravitational parameter (μ) using the gravitational constant
    # and the mass of the Earth, and the mass of the satellite (if provided):
    μ = GRAVITATIONAL_CONSTANT * (EARTH_MASS + mass)  # μ ≈ GM

    # Convert the mean motion from revolutions per day to radians per second:
    n = (mean_motion * 2 * pi) / 86400

    # Calculate the semi-major axis using the formula (in meters):
    return (μ / n**2) ** (1 / 3)


# **************************************************************************************


def get_eccentric_anomaly(
    mean_anomaly: float, eccentricity: float, tolerance: float = 1e-8
) -> float:
    """
    Solve Kepler's Equation for the eccentric anomaly using the Newton-Raphson method.

    This function computes the eccentric anomaly (E) for a given mean anomaly (M) and
    orbital eccentricity (e). It iteratively refines the estimate using Newton-Raphson until
    the update is smaller than the specified tolerance.

    Args:
        mean_anomaly: The mean anomaly (M) (in radians).
        eccentricity: The orbital eccentricity (e), (unitless).
        tolerance: Convergence tolerance. Defaults to 1e-8.

    Raises:
        ValueError: If the derivative is zero, indicating no solution found.
        ValueError: If the maximum number of iterations is reached without convergence.

    Returns:
        float: The eccentric anomaly (E) (in radians)
    """
    # Start with an initial guess for the eccentric anomaly equal to the mean anomaly:
    E = mean_anomaly

    iteration = 0

    while iteration < 1_000_000:
        # Compute the value of Kepler's function: f(E) = E - e*sin(E) - M:
        f_value = E - eccentricity * sin(E) - mean_anomaly

        # Compute the derivative: f'(E) = 1 - e*cos(E):
        f_derivative = 1 - eccentricity * cos(E)

        # Check if the derivative is close to zero to avoid division by zero:
        if abs(f_derivative) < 1e-12:
            raise ValueError("Derivative is close to zero; no solution found.")

        # Calculate the Newton-Raphson correction term:
        delta_E = -f_value / f_derivative

        # Update the estimate for the eccentric anomaly:
        E += delta_E

        # Check for convergence by comparing the absolute value of the correction
        # term to the tolerance:
        if abs(delta_E) < tolerance:
            break

        # Increment the iteration count:
        iteration += 1

    # Check if the maximum number of iterations was reached without convergence:
    else:
        raise ValueError(
            "Failed to converge to the desired tolerance after 1,000,000 iterations."
        )

    return E


# **************************************************************************************
