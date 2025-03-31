# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Annotated, Optional

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
        mapping = {"U": "Unclassified", "C": "Classified", "S": "Secret"}
        if value not in mapping.keys():
            raise ValueError(f"Classification must be one of {list(mapping.keys())}")
        return mapping[value]


# **************************************************************************************


class OrbitalElements(BaseModel):
    drag: Annotated[
        float,
        Field(
            description="The B*, the drag term, or radiation pressure coefficient (decimal point assumed)",
        ),
    ]

    raan: Annotated[
        float,
        Field(
            description="Right Ascension of the ascending node (in degrees)",
        ),
    ]

    inclination: Annotated[
        float,
        Field(
            description="The orbital inclination of the satellite (in degrees)",
        ),
    ]

    eccentricity: Annotated[
        float,
        Field(
            description="The orbital eccentricity of the satellite (dimensionless)",
        ),
    ]

    argument_of_perigee: Annotated[
        float,
        Field(
            description="The argument of perigee of the satellite (in degrees)",
        ),
    ]

    mean_anomaly: Annotated[
        float,
        Field(
            description="The mean anomaly of the satellite (in degrees)",
        ),
    ]

    mean_motion: Annotated[
        float,
        Field(
            gt=0,
            description="The mean motion (revolutions per day) of the satellite",
        ),
    ]

    first_derivative_of_mean_motion: Annotated[
        float,
        Field(
            description="The first derivative of mean motion (decimal point assumed) of the satellite 'the ballistic coefficient'",
        ),
    ]

    second_derivative_of_mean_motion: Annotated[
        float,
        Field(
            description="Second derivative of mean motion (decimal point assumed) of the satellite",
        ),
    ]

    number_of_revolutions: Annotated[
        int,
        Field(
            ge=0,
            description="The number of complete revolutions the satellite has made around the Earth at the Epoch time",
        ),
    ]


# **************************************************************************************


class Satellite(ID, OrbitalElements):
    reference_frame: Annotated[
        Optional[str],
        Field(
            description="Reference frame used for orbit propagation",
            default=None,
        ),
    ]

    center: Annotated[
        Optional[str],
        Field(
            description="The center name of the satellite, e.g., 'Earth', 'Moon', 'Mars', 'Sun', etc.",
            default=None,
        ),
    ]

    @field_validator("reference_frame")
    def validate_reference_frame(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        mapping = {
            "TEME": "True Equator, Mean Equinox",
            "ICRF": "International Celestial Reference Frame",
            "EME2000": "Epoch Mean Equinox 2000",
        }

        if value is not None and value.upper() not in mapping.keys():
            raise ValueError(f"Reference frame must be one of {list(mapping.keys())}")

        return mapping.get(value.upper()) if value else None

    @field_validator("center")
    def validate_center(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        mapping = {
            "EARTH": "Earth",
            "MOON": "Moon",
            "SUN": "Sun",
            "MERCURY": "Mercury",
            "VENUS": "Venus",
            "MARS": "Mars",
            "JUPITER": "Jupiter",
            "SATURN": "Saturn",
            "URANUS": "Uranus",
            "NEPTUNE": "Neptune",
            "PLUTO": "Pluto",
            "CERES": "Ceres",
        }

        if value is not None and value.upper() not in mapping.keys():
            raise ValueError(f"Center must be one of {list(mapping.keys())}")

        return mapping.get(value.upper()) if value else None


# **************************************************************************************
