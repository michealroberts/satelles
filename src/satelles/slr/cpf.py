# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict, Literal, Optional, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from ..mjd import convert_mjd_to_datetime
from ..models import Position, Velocity

# **************************************************************************************

ReferenceFrame = Literal[
    "Geocentric True Body Fixed (ECEF)",
    "Geocentric Space Fixed Inertial (ECI)",
    "Geocentric Space Fixed Mean Of Date (J2000)",
]

# **************************************************************************************

TargetClass = Literal[
    "No Retro-Reflector",
    "Passive Retro-Reflector",
    "Synchronous Transponder",
    "Asynchronous Transponder",
    "Other",
]

# **************************************************************************************

TargetLocation = Literal[
    "Other",
    "Earth",
    "Lunar Orbit",
    "Lunar Surface",
    "Mars Orbit",
    "Mars Surface",
    "Venus Orbit",
    "Mercury Orbit",
    "Asteroid Orbit",
    "Asteroid Surface",
    "Solar Orbit",
]

# **************************************************************************************

Direction = Literal["Common Epoch", "Transmit", "Receive"]

# **************************************************************************************


# @see https://ilrs.gsfc.nasa.gov/docs/2018/cpf_2.00h-1.pdf
class CPFHeader(BaseModel):
    model_config = ConfigDict(extra="ignore")

    norad_id: Annotated[
        str,
        Field(
            description="NORAD ID (1-8 digits); cross-references NORAD/USSTRATCOM catalog"
        ),
    ]

    cospar_id: Annotated[
        str,
        Field(
            description="Compressed COSPAR ID (1-8 digits); cross-references international satellite catalog"
        ),
    ]

    sic: Annotated[
        str,
        Field(
            description="Satellite Identification Code (1-4 digits); assigned by ILRS for unique identification"
        ),
    ]

    # The CPF version number is explicitly defined as 2, with no backwards compatibility
    # for earlier versions:
    version: Annotated[
        Literal[2],
        Field(
            default=2,
            description="CPF version number; currently fixed at 2 for all files",
        ),
    ]

    ephemeris_source: Annotated[
        str,
        Field(
            description="Three-character code identifying the ephemeris producer; used to track data provenance"
        ),
    ]

    year: Annotated[
        int,
        Field(
            ge=1950,
            le=3100,
            description="Production year of the CPF file; establishes data currency",
        ),
    ]

    month: Annotated[
        int,
        Field(
            ge=1,
            le=12,
            description="Production month (1-12); establishes data currency",
        ),
    ]

    day: Annotated[
        int,
        Field(
            ge=1,
            le=31,
            description="Production day of month; establishes data currency",
        ),
    ]

    hour: Annotated[
        int,
        Field(
            ge=0,
            le=23,
            description="Production hour in UTC; critical for knowing when predictions were generated",
        ),
    ]

    ephemeris_sequence_number: Annotated[
        int,
        Field(
            ge=0,
            le=366,
            description="Sequence number (often day-of-year) for this ephemeris; used to identify file order",
        ),
    ]

    sub_daily_sequence_number: Annotated[
        int,
        Field(
            ge=0,
            le=99,
            description="Sub-daily sequence number for multiple updates in one UTC day; used for versioning",
        ),
    ]

    target_name: Annotated[
        str,
        Field(
            max_length=10,
            description="ILRS-registered target name (up to 10 chars); identifies the satellite or reflector",
        ),
    ]

    target_class: Annotated[
        TargetClass,
        Field(
            description="Target class code used to apply relevant corrections",
        ),
    ]

    start: Annotated[
        datetime,
        Field(
            description="Start of prediction validity window (UTC datetime); defines when ephemeris data begin to apply"
        ),
    ]

    end: Annotated[
        datetime,
        Field(
            description="End of prediction validity window (UTC datetime); defines when ephemeris data cease to apply"
        ),
    ]

    interval: Annotated[
        int,
        Field(
            ge=1,
            description="Time between table entries in seconds; used for interpolation spacing",
        ),
    ]

    # Acceptable inputs: 0,1,2 → mapped to these string literals
    reference_frame: Annotated[
        ReferenceFrame,
        Field(
            description="Reference frame code (0=ECEF/ITRF, 1=ECI, 2=J2000); used to interpret position/velocity data"
        ),
    ]

    rotational_angle_type: Annotated[
        int,
        Field(
            ge=0,
            le=2,
            description="Rotational angle type (0=n.a., 1=first order, 2=second order); used for attitude corrections",
        ),
    ]

    center_of_mass_correction: Annotated[
        bool,
        Field(
            description="Center-of-mass correction flag (0=no, 1=yes); indicates whether to apply COM-to-reflector offset",
        ),
    ]

    center_of_mass_to_reflector_offset: Annotated[
        Optional[float],
        Field(
            ge=0,
            description="Center of mass to reflector offset in meters; applies only if center_of_mass_correction is true",
        ),
    ] = None

    tiv_compatibility: Annotated[
        bool,
        Field(
            description="Compatibility with Tuned Inter-Range Vectors (TIVs); indicates geocentric integration",
        ),
    ]

    location_dynamics: Annotated[
        TargetLocation,
        Field(
            description="Location/dynamics target used to understand orbital regime",
        ),
    ]

    notes: Annotated[
        Optional[str],
        Field(
            max_length=10,
            description="Optional free-text notes (up to 10 chars); provides additional context or flags",
        ),
    ] = None

    @field_validator("target_class", mode="before")
    def convert_target_class(cls, v: int) -> TargetClass:
        target_types: Dict[int, TargetClass] = {
            0: "No Retro-Reflector",
            1: "Passive Retro-Reflector",
            3: "Synchronous Transponder",
            4: "Asynchronous Transponder",
            5: "Other",
        }

        if isinstance(v, int) and v in target_types:
            return target_types[v]

        raise ValueError(
            "Target type must be one of 0, 1, 3, 4 or 5 for their respective types"
        )

    @field_validator("reference_frame", mode="before")
    def convert_reference_frame(cls, v: int) -> ReferenceFrame:
        frames: Dict[int, ReferenceFrame] = {
            0: "Geocentric True Body Fixed (ECEF)",
            1: "Geocentric Space Fixed Inertial (ECI)",
            2: "Geocentric Space Fixed Mean Of Date (J2000)",
        }

        if isinstance(v, int) and v in frames:
            return frames[v]

        valid_frames = ", ".join(f"{key} ({value})" for key, value in frames.items())

        raise ValueError(
            f"Invalid value for 'reference_frame'. Must be one of: {valid_frames}"
        )

    @field_validator("center_of_mass_correction", mode="before")
    def convert_center_of_mass_correction(cls, v: int) -> bool:
        if isinstance(v, int) and v in (0, 1):
            return bool(v)

        raise ValueError(
            "Center of mass correction must be either 0 (no correction) or 1 (apply correction)"
        )

    @field_validator("tiv_compatibility", mode="before")
    def convert_tiv_compatibility(cls, v: int) -> bool:
        if isinstance(v, int) and v in (0, 1):
            return bool(v)

        raise ValueError(
            "TIV compatibility must be either 0 (not compatible) or 1 (compatible)"
        )

    @field_validator("location_dynamics", mode="before")
    def convert_location_dynamics(cls, v: int) -> TargetLocation:
        locations: Dict[int, TargetLocation] = {
            0: "Other",
            1: "Earth",
            2: "Lunar Orbit",
            3: "Lunar Surface",
            4: "Mars Orbit",
            5: "Mars Surface",
            6: "Venus Orbit",
            7: "Mercury Orbit",
            8: "Asteroid Orbit",
            9: "Asteroid Surface",
            10: "Solar Orbit",
        }

        if isinstance(v, int) and v in locations:
            return locations[v]

        raise ValueError(
            "Location/dynamics must be one of 0-10 for their respective locations"
        )

    @model_validator(mode="after")
    def is_start_before_end(cls, data: Any) -> "CPFHeader":
        if not isinstance(data.start, datetime):
            raise TypeError(f"start must be a datetime, not {type(data.start)}")

        if not isinstance(data.end, datetime):
            raise TypeError(f"end must be a datetime, not {type(data.end)}")

        if data.start >= data.end:
            raise ValueError(
                f"start ({data.start!r}) must be strictly before end ({data.end!r})"
            )

        return data


# **************************************************************************************


class CPFEphemeris(BaseModel):
    mjd: Annotated[
        int,
        Field(
            ge=0,
            description="Modified Julian Date for the position epoch; basis for time-tagged interpolation",
        ),
    ]

    seconds_of_day: Annotated[
        float,
        Field(
            ge=0,
            description="UTC seconds of day for the position epoch; high-precision time marker",
        ),
    ]

    leap_second: Annotated[
        int,
        Field(
            ge=0,
            description="Leap second flag (0 if none or the new leap second value); adjusts timing for UTC irregularities",
        ),
    ]

    direction_position: Annotated[
        Direction,
        Field(
            description="Direction flag for position record; translates raw 0/1/2 into common epoch, transmit, or receive, respectively"
        ),
    ]

    position: Annotated[
        Position,
        Field(
            description="Geocentric X, Y, Z position in meters; foundational data for pointing and ranging"
        ),
    ]

    direction_velocity: Annotated[
        Optional[Direction],
        Field(
            description="Direction flag for velocity record; translates raw 0/1/2 into common epoch, transmit, or receive, respectively"
        ),
    ]

    velocity: Annotated[
        Optional[Velocity],
        Field(
            description="Geocentric X, Y, Z velocity in m/s; needed for polynomial interpolation of orbit"
        ),
    ]

    direction_stellar_aberration: Annotated[
        Optional[Direction],
        Field(
            description="Direction flag for stellar aberration record; translates raw 0/1/2 into common epoch, transmit, or receive, respectively"
        ),
    ]

    stellar_aberration: Annotated[
        Optional[Position],
        Field(
            description="X, Y, Z stellar aberration corrections in meters; used to remove light-time effects from pointing"
        ),
    ]

    relativistic_range_correction: Annotated[
        Optional[float],
        Field(
            description="One-way relativistic range correction in seconds; corrects for gravitational time dilation",
        ),
    ]

    @computed_field(  # type: ignore[misc]
        description="Computed UTC datetime for the position epoch; derived from MJD and seconds of day",
    )
    @property
    def at(self) -> datetime:
        # The Modified Julian Date epoch starts at 1858-11-17 00:00:00 UTC. We then
        # apply to the MJD offset and the seconds of day to compute the full UTC
        # datetime:
        return (
            convert_mjd_to_datetime(self.mjd) + timedelta(seconds=self.seconds_of_day)
        ).replace(tzinfo=timezone.utc)

    @field_validator(
        "direction_position",
        "direction_velocity",
        "direction_stellar_aberration",
        mode="before",
    )
    def convert_direction_flag(cls, v: int | str | None) -> Direction | None:
        # If an optional field is missing, just leave it as None:
        if v is None:
            return None

        directions: Dict[int, Direction] = {
            0: "Common Epoch",
            1: "Transmit",
            2: "Receive",
        }

        if isinstance(v, str) and v in directions.values():
            return cast(Direction, v)

        if isinstance(v, int) and v in directions.keys():
            return directions[v]

        raise ValueError(
            "Direction flag must be one of 0 (Common Epoch), 1 (Transmit), or 2 (Receive)"
        )


# **************************************************************************************
