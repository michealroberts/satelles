# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

from math import degrees, pi, sqrt
from typing import Annotated

from pydantic import BaseModel, Field

from .constants import GRAVITATIONAL_CONSTANT
from .earth import EARTH_MASS

# **************************************************************************************


class HohmannTransferParameters(BaseModel):
    """
    Represents the computed parameters of a Hohmann transfer between two circular orbits.
    """

    # Initial orbit radius (in meters):
    r1: Annotated[
        float,
        Field(
            gt=0,
            description="Initial circular orbit radius in meters",
        ),
    ]

    # Final orbit radius (in meters):
    r2: Annotated[
        float,
        Field(
            gt=0,
            description="Final circular orbit radius in meters",
        ),
    ]

    # Transfer orbit semi-major axis (in meters):
    a: Annotated[
        float,
        Field(
            gt=0,
            description="Semi-major axis of the transfer ellipse in meters",
        ),
    ]

    # Transfer orbit eccentricity (dimensionless):
    e: Annotated[
        float,
        Field(
            ge=0,
            lt=1,
            description="Eccentricity of the transfer ellipse",
        ),
    ]

    # Delta-v for the first burn at periapsis (in meters per second)
    Δv1: Annotated[
        float,
        Field(
            description="Delta-v for departure burn in meters per second",
        ),
    ]

    # Delta-v for the second burn at apoapsis (in meters per second)
    Δv2: Annotated[
        float,
        Field(
            description="Delta-v for arrival/circularization burn in meters per second"
        ),
    ]

    # Total delta-v (in meters per second)
    Δv: Annotated[
        float,
        Field(
            ge=0,
            description="Total delta-v required in meters per second",
        ),
    ]
    # Transfer time (in seconds)
    T: Annotated[
        float,
        Field(
            gt=0,
            description="Time of flight for the transfer in seconds",
        ),
    ]

    # Phase angle required for rendezvous (in degrees)
    φ: Annotated[
        float,
        Field(
            ge=-180,
            le=180,
            description="Required phase angle for rendezvous in degrees",
        ),
    ]


# **************************************************************************************


def get_hohmann_transfer_semi_major_axis(
    r1: float,
    r2: float,
) -> float:
    """
    Calculate the semi-major axis (a) of the Hohmann transfer ellipse.

    The transfer ellipse has its periapsis at r1 and apoapsis at r2 (or vice versa), so
    the semi-major axis is simply the average of the two radii.

    Args:
        r1: Radius of the initial circular orbit (in meters).
        r2: Radius of the final circular orbit (in meters).

    Returns:
        The semi-major axis (a) of the transfer orbit (in meters).
    """
    return (r1 + r2) / 2


# **************************************************************************************


def get_hohmann_transfer_eccentricity(
    r1: float,
    r2: float,
) -> float:
    """
    Calculate the eccentricity (e) of the Hohmann transfer ellipse.

    The eccentricity is calculated based on the periapsis and apoapsis radii of the
    transfer orbit.

    Args:
        r1: Radius of the initial circular orbit (in meters).
        r2: Radius of the final circular orbit (in meters).

    Returns:
        The eccentricity (e) of the transfer orbit (dimensionless).
    """
    # Guard against identical orbit radii which would lead to 0 eccentricity:
    if r1 == r2:
        return 0.0

    # Guard against invalid inputs that would lead to division by zero:
    if r1 + r2 == 0:
        raise ValueError(
            "The sum of r1 and r2 must be greater than zero to calculate eccentricity."
        )

    return abs(r2 - r1) / (r1 + r2)


# **************************************************************************************


def get_hohmann_transfer_phase_angle(
    r1: float,
    r2: float,
) -> float:
    """
    Calculate the required phase angle (φ) for a Hohmann transfer rendezvous.

    The phase angle is the angular separation between the target and the spacecraft at
    the time of the departure burn, measured in the direction of orbital motion.

    Args:
        r1: Radius of the initial circular orbit (in meters).
        r2: Radius of the final circular orbit (in meters).

    Returns:
        The required phase angle φ (in degrees).
    """
    # Guard against non-positive orbit radii for the initial orbit:
    if r1 <= 0:
        raise ValueError("Initial orbit radius r1 must be positive.")

    # Guard against non-positive orbit radii for the final orbit:
    if r2 <= 0:
        raise ValueError("Final orbit radius r2 must be positive.")

    # Guard against identical orbit radii which would make a transfer meaningless:
    if r1 == r2:
        raise ValueError("Initial and final orbit radii must be different.")

    # Ratio of radii (always express as outer/inner for the formula):
    if r2 > r1:
        # Transfer to higher orbit: therefore the target must be ahead:
        ratio = r1 / r2

        # Angular travel of target during transfer:
        α = pi * sqrt(((1 + ratio) / 2) ** 3)

        # Phase angle for ascent phase:
        φ = pi - α
    else:
        # Transfer to lower orbit: therefore the target must be behind:
        ratio = r2 / r1

        # Angular travel of target during transfer:
        α = pi * sqrt(((1 + ratio) / 2) ** 3)

        # Phase angle for descent phase:
        φ = α - pi

    # Convert to degrees (result is already in range [-180, 180] due to the formula):
    return degrees(φ)


# **************************************************************************************


def get_hohmann_transfer_parameters(
    r1: float,
    r2: float,
    *,
    μ: float = GRAVITATIONAL_CONSTANT * EARTH_MASS,
) -> HohmannTransferParameters:
    """
    Calculate the parameters for a Hohmann transfer between two circular orbits.

    This function computes the properties of the elliptical transfer orbit and the
    associated velocity changes (Δv) required to move from an initial circular
    orbit of radius r1 to a final circular orbit of radius r2 under a
    central gravitational field with parameter μ.

    Args:
        r1: Radius of the initial circular orbit (in meters).
        r2: Radius of the final circular orbit (in meters).
        μ: Gravitational parameter (GM) in m³/s². Defaults to Earth's μ.

    Returns:
        HohmannTransferParameters: The computed transfer parameters, including
        the transfer-orbit semi-major axis, eccentricity, burn Δv values,
        total Δv, transfer time and the phase angle.

    Raises:
        ValueError: If r1 is not positive, if r2 is not positive, or if r1 equals r2.
    """
    # Guard against non-positive orbit radii for the initial orbit:
    if r1 <= 0:
        raise ValueError("Initial orbit radius r1 must be positive.")

    # Guard against non-positive orbit radii for the final orbit:
    if r2 <= 0:
        raise ValueError("Final orbit radius r2 must be positive.")

    # Guard against identical orbit radii which would make a transfer meaningless:
    if r1 == r2:
        raise ValueError("Initial and final orbit radii must be different.")

    # Calculate the semi-major axis of the transfer orbit:
    a = get_hohmann_transfer_semi_major_axis(r1=r1, r2=r2)

    # Calculate the eccentricity of the transfer orbit:
    e = get_hohmann_transfer_eccentricity(
        r1=r1,
        r2=r2,
    )

    # Calculate the Δv for the first burn (at periapsis / apoapsis):
    Δv1 = sqrt(μ / r1) - sqrt(μ * (2 / r1 - 1 / a))

    # Calculate the Δv for the second burn (at apoapsis / periapsis):
    Δv2 = sqrt(μ / r2) - sqrt(μ * (2 / r2 - 1 / a))

    # Calculate the total Δv required:
    Δv = abs(Δv1) + abs(Δv2)

    # Calculate the transfer time (half the orbital period of the ellipse):
    T = pi * sqrt(a**3 / μ)

    # Calculate the required phase angle for rendezvous:
    φ = get_hohmann_transfer_phase_angle(r1=r1, r2=r2)

    return HohmannTransferParameters(
        r1=r1,
        r2=r2,
        a=a,
        e=e,
        Δv1=Δv1,
        Δv2=Δv2,
        Δv=Δv,
        T=T,
        φ=φ,
    )


# **************************************************************************************
