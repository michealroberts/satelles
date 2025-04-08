# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from typing import Annotated, Optional

from celerity.coordinates import EquatorialCoordinate
from celerity.temporal import get_julian_date
from pydantic import BaseModel, Field, field_validator

from .common import CartesianCoordinate, Velocity
from .constants import GRAVITATIONAL_CONSTANT
from .coordinates import (
    convert_eci_to_equatorial,
    convert_perifocal_to_eci,
    get_perifocal_coordinate,
)
from .covariance import Covariance
from .earth import EARTH_MASS
from .kepler import get_semi_major_axis, get_true_anomaly
from .velocity import get_perifocal_velocity

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

    argument_of_pericenter: Annotated[
        float,
        Field(
            description="The argument of pericenter of the satellite (in degrees)",
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
    # The date and time of the observation (in UTC):
    _when: Optional[datetime] = None

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

    mass: Annotated[
        Optional[float],
        Field(default=None, description="Satellite mass in kilograms"),
    ]

    solar_radiation_pressure_area: Annotated[
        Optional[float],
        Field(default=None, description="Solar radiation pressure area (AR) in m²"),
    ]

    solar_radiation_pressure_coefficient: Annotated[
        Optional[float],
        Field(default=None, description="Solar radiation pressure coefficient (CR)"),
    ]

    drag_area: Annotated[
        Optional[float],
        Field(default=None, description="Drag area (AD) in m²"),
    ]

    drag_coefficient: Annotated[
        Optional[float],
        Field(default=None, description="Drag coefficient (CD)"),
    ]

    gravitational_coefficient: Annotated[
        Optional[float],
        Field(default=None, description="Gravitational coefficient (GM) in SI units"),
    ]

    covariance: Optional[Covariance] = None

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

    def get_semi_major_axis(self, mass: float = 0.0) -> float:
        """
        Calculate the semi-major axis of the satellite's orbit in meters.

        The semi-major axis is calculated using the mean motion and the gravitational
        constant of the Earth.

        Args:
            mass: The mass of the satellite in kilograms. Default is 0.0 (for a point mass).

        Returns:
            The semi-major axis (in SI meters).
        """
        return get_semi_major_axis(self.mean_motion, mass=mass)

    def get_semi_latus_rectum(self, mass: float = 0.0) -> float:
        """
        Calculate the semi-latus rectum of the satellite's orbit in meters.

        The semi-latus rectum is calculated using the semi-major axis and the
        eccentricity of the orbit.

        Args:
            mass: The mass of the satellite in kilograms. Default is 0.0 (for a point mass).

        Returns:
            The semi-latus rectum (in SI meters).
        """
        return self.get_semi_major_axis(mass=mass) * (1 - self.eccentricity**2)

    @property
    def perifocal_coordinate(self) -> CartesianCoordinate:
        """
        Convert the satellite's orbital elements to a perifocal coordinate system.

        Note:
            The date and time to calculate the position for should be set using the
            `at` method before calling this property.

        Returns:
            A CartesianCoordinate representing the satellite's position in the
            perifocal coordinate system.
        """
        if self._when is None:
            raise ValueError(
                "Please specify a date and time to calculate the position for by calling the at() method."
            )

        # Get the Julian date at the epoch:
        JD = get_julian_date(date=self._when)

        # Get the semi-major axis (in meters) for the TLE:
        a = self.get_semi_major_axis()

        # Get the mean anomaly (in degrees) for the TLE given the mean anomaly at
        # the epoch:
        M = self.mean_anomaly + self.mean_motion * 360 * (JD - self.jd)

        # Get the true anomaly (in degrees) for the TLE given the mean anomaly at
        # the epoch:
        ν = get_true_anomaly(
            mean_anomaly=M,
            eccentricity=self.eccentricity,
        )

        return get_perifocal_coordinate(
            semi_major_axis=a,
            mean_anomaly=M,
            true_anomaly=ν,
            eccentricity=self.eccentricity,
        )

    @property
    def perifocal_velocity(self) -> Velocity:
        """
        Calculate the velocity in the perifocal coordinate system.

        Note:
            The date and time to calculate the position for should be set using the
            `at` method before calling this property.

        Returns:
            A Velocity representing the satellite's velocity in the perifocal
            coordinate system.
        """
        if self._when is None:
            raise ValueError(
                "Please specify a date and time to calculate the position for by calling the at() method."
            )

        # Get the Julian date at the epoch:
        JD = get_julian_date(date=self._when)

        # Get the semi-major axis (in meters) for the TLE:
        a = self.get_semi_major_axis()

        # Get the mean anomaly (in degrees) for the TLE given the mean anomaly at
        # the epoch:
        M = self.mean_anomaly + self.mean_motion * 360 * (JD - self.jd)

        # Get the true anomaly (in degrees) for the TLE given the mean anomaly at
        # the epoch:
        ν = get_true_anomaly(
            mean_anomaly=M,
            eccentricity=self.eccentricity,
        )

        # Calculate the velocity in the perifocal coordinate system:
        return get_perifocal_velocity(
            semi_major_axis=a,
            true_anomaly=ν,
            eccentricity=self.eccentricity,
            μ=EARTH_MASS * GRAVITATIONAL_CONSTANT,
        )

    @property
    def eci_coordinate(self) -> CartesianCoordinate:
        """
        Convert the satellite's orbital elements to an Earth-Centered Inertial (ECI)
        coordinate system.

        Note:
            The date and time to calculate the position for should be set using the
            `at` method before calling this property.

        Returns:
            A CartesianCoordinate representing the satellite's position in the ECI
            coordinate system.
        """
        # Convert the perifocal coordinate to the Earth Centered Inertial (ECI)
        # reference frame:
        return convert_perifocal_to_eci(
            perifocal=self.perifocal_coordinate,
            inclination=self.inclination,
            raan=self.raan,
            argument_of_perigee=self.argument_of_pericenter,
        )

    @property
    def equatorial_coordinate(self) -> EquatorialCoordinate:
        """
        Convert the satellite's orbital elements to an Equatorial coordinate system.

        Note:
            The date and time to calculate the position for should be set using the
            `at` method before calling this property.

        Returns:
            An EquatorialCoordinate representing the satellite's position in the
            equatorial coordinate system.
        """
        # Convert the ECI coordinate to the Equatorial coordinate system:
        return convert_eci_to_equatorial(
            eci=self.eci_coordinate,
        )

    def at(self, when: datetime) -> None:
        """
        Set the TLE to a specific date and time (in UTC).

        Args:
            when: The date and time to set the TLE to.
        """
        self._when = when.astimezone(timezone.utc)


# **************************************************************************************
