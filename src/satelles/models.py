# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Annotated

from pydantic import BaseModel, Field

# **************************************************************************************


class Position(BaseModel):
    x: Annotated[
        float,
        Field(
            description="Geocentric X coordinate in meters; used for precise position calculations"
        ),
    ]

    y: Annotated[
        float,
        Field(
            description="Geocentric Y coordinate in meters; used for precise position calculations"
        ),
    ]

    z: Annotated[
        float,
        Field(
            description="Geocentric Z coordinate in meters; used for precise position calculations"
        ),
    ]

    at: Annotated[
        float,
        Field(
            description="Modified Julian Date (MJD) of the position; used for precise time-based calculations"
        ),
    ]


# **************************************************************************************


class Velocity(BaseModel):
    vx: Annotated[
        float,
        Field(
            description="Geocentric X velocity in meters/second; required for orbit interpolation"
        ),
    ]

    vy: Annotated[
        float,
        Field(
            description="Geocentric Y velocity in meters/second; required for orbit interpolation"
        ),
    ]

    vz: Annotated[
        float,
        Field(
            description="Geocentric Z velocity in meters/second; required for orbit interpolation"
        ),
    ]

    at: Annotated[
        float,
        Field(
            description="Modified Julian Date (MJD) of the velocity; used for precise time-based calculations"
        ),
    ]


# **************************************************************************************
