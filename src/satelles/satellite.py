# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Annotated

from pydantic import BaseModel, Field, field_validator

# **************************************************************************************


class ID(BaseModel):
    id: Annotated[
        int,
        Field(
            ge=0,
            description="The satellite catalog number, e.g., NORAD ID",
        ),
    ]

    name: Annotated[
        str,
        Field(
            description="The designated name of the satellite",
        ),
    ]

    classification: Annotated[
        str,
        Field(
            description="The classification of the satellite, e.g., 'U' for unclassified, 'C' for classified, 'S' for secret",
        ),
    ]

    designator: Annotated[
        str,
        Field(
            description="The international designator of the satellite",
        ),
    ]

    year: Annotated[
        int,
        Field(
            ge=1900,
            le=2100,
            description="The Epoch year of the TLE (full four-digit year)",
        ),
    ]

    day: Annotated[
        float,
        Field(
            ge=1,
            le=367,
            description="Epoch day of the year with fractional portion included, e.g., 123.456789",
        ),
    ]

    jd: Annotated[
        float,
        Field(
            description="The Julian date of the Epoch",
        ),
    ]

    ephemeris: Annotated[
        int,
        Field(
            description="Ephemeris type (always zero; only used in undistributed TLE data)",
        ),
    ]

    set: Annotated[
        int,
        Field(
            ge=0,
            description="The element set number, incremented when a new TLE is generated for this object",
        ),
    ]

    @field_validator("classification")
    def validate_classification(cls, value: str) -> str:
        allowed = {"U", "C", "S"}
        if value not in allowed:
            raise ValueError(f"Classification must be one of {allowed}, got '{value}'")
        return value


# **************************************************************************************
