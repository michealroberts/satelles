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


# **************************************************************************************
