# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

from typing import Annotated

from pydantic import BaseModel, Field

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
