# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import time
import unittest
from datetime import datetime, timedelta, timezone
from math import cos, degrees, sin, sqrt
from typing import Any, Dict

from pydantic import ValidationError

from satelles import TLE
from satelles.common import CartesianCoordinate
from satelles.coordinates import convert_eci_to_equatorial, convert_perifocal_to_eci
from satelles.covariance import Covariance
from satelles.satellite import ID, OrbitalElements, Satellite

from .utils import host_timezone

# **************************************************************************************


class TestIDModel(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_data: Dict[str, Any] = {
            "id": 25544,
            "name": "ISS (ZARYA)",
            "classification": "U",
            "designator": "1998-067A",
            "year": 2021,
            "day": 123.456789,
            "jd": 2459365.456789,
            "ephemeris": 0,
            "set": 999,
        }

    def test_valid_id(self) -> None:
        model: ID = ID(**self.valid_data)
        self.assertEqual(model.id, 25544)
        self.assertEqual(model.name, "ISS (ZARYA)")
        self.assertEqual(model.classification, "Unclassified")
        self.assertEqual(model.designator, "1998-067A")
        self.assertEqual(model.year, 2021)
        self.assertEqual(model.day, 123.456789)
        self.assertEqual(model.jd, 2459365.456789)
        self.assertEqual(model.ephemeris, 0)
        self.assertEqual(model.set, 999)

    def test_negative_id(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["id"] = -1
        with self.assertRaises(ValidationError):
            ID(**data)

    def test_year_out_of_range(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["year"] = 1800
        with self.assertRaises(ValidationError):
            ID(**data)
        data["year"] = 2200
        with self.assertRaises(ValidationError):
            ID(**data)

    def test_day_out_of_range(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["day"] = 0
        with self.assertRaises(ValidationError):
            ID(**data)
        data["day"] = 400
        with self.assertRaises(ValidationError):
            ID(**data)

    def test_missing_field(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        del data["name"]
        with self.assertRaises(ValidationError):
            ID(**data)

    def test_invalid_classification(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["classification"] = "X"
        with self.assertRaises(ValidationError):
            ID(**data)


# **************************************************************************************


class TestOrbitalElements(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_data: Dict[str, Any] = {
            "drag": 0.00002182,
            "raan": 257.8333,
            "inclination": 51.6433,
            "eccentricity": 0.0001675,
            "argument_of_pericenter": 296.7755,
            "mean_anomaly": 73.3782,
            "mean_motion": 15.542259,
            "first_derivative_of_mean_motion": -0.00002182,
            "second_derivative_of_mean_motion": 0.0,
            "number_of_revolutions": 12345,
        }

    def test_valid_orbital_elements(self) -> None:
        model: OrbitalElements = OrbitalElements(**self.valid_data)
        self.assertAlmostEqual(model.drag, 0.00002182)
        self.assertAlmostEqual(model.raan, 257.8333)
        self.assertAlmostEqual(model.inclination, 51.6433)
        self.assertAlmostEqual(model.eccentricity, 0.0001675)
        self.assertAlmostEqual(model.argument_of_pericenter, 296.7755)
        self.assertAlmostEqual(model.mean_anomaly, 73.3782)
        self.assertAlmostEqual(model.mean_motion, 15.542259)
        self.assertAlmostEqual(model.first_derivative_of_mean_motion, -0.00002182)
        self.assertAlmostEqual(model.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(model.number_of_revolutions, 12345)

    def test_motion_positive(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["mean_motion"] = 0
        with self.assertRaises(ValidationError):
            OrbitalElements(**data)

    def test_revolution_non_negative(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        data["number_of_revolutions"] = -1
        with self.assertRaises(ValidationError):
            OrbitalElements(**data)

    def test_missing_field(self) -> None:
        data: Dict[str, Any] = self.valid_data.copy()
        del data["drag"]
        with self.assertRaises(ValidationError):
            OrbitalElements(**data)


# **************************************************************************************


class TestSatelliteOptionalFields(unittest.TestCase):
    def setUp(self) -> None:
        self.identifier: Dict[str, Any] = {
            "id": 25544,
            "name": "ISS (ZARYA)",
            "classification": "U",
            "designator": "1998-067A",
            "year": 2021,
            "day": 123.456789,
            "jd": 2459365.456789,
            "ephemeris": 0,
            "set": 999,
        }

        self.orbital_elements: Dict[str, Any] = {
            "drag": 0.00002182,
            "raan": 257.8333,
            "inclination": 51.6433,
            "eccentricity": 0.0001675,
            "argument_of_pericenter": 296.7755,
            "mean_anomaly": 73.3782,
            "mean_motion": 15.542259,
            "first_derivative_of_mean_motion": -0.00002182,
            "second_derivative_of_mean_motion": 0.0,
            "number_of_revolutions": 12345,
        }

        self.valid_satellite_data: Dict[str, Any] = {
            **self.identifier,
            **self.orbital_elements,
            "reference_frame": "TEME",
            "center": "EARTH",
            "mass": 1200,
            "solar_radiation_pressure_area": 20.0,
            "solar_radiation_pressure_coefficient": 1.2,
            "drag_area": 10.0,
            "drag_coefficient": 2.2,
            "gravitational_coefficient": 398600.4418,
        }

    def test_valid_optional_fields(self) -> None:
        satellite = Satellite(**self.valid_satellite_data)
        self.assertEqual(satellite.reference_frame, "True Equator, Mean Equinox")
        self.assertEqual(satellite.center, "Earth")

    def test_invalid_reference_frame(self) -> None:
        data = self.valid_satellite_data.copy()
        data["reference_frame"] = "XYZ"
        with self.assertRaises(ValidationError):
            Satellite(**data)

    def test_invalid_center(self) -> None:
        data = self.valid_satellite_data.copy()
        data["center"] = "PLUTOY"  # assuming "PLUTOY" is not allowed
        with self.assertRaises(ValidationError):
            Satellite(**data)

    def test_optional_fields_missing(self) -> None:
        # Test that missing optional fields are allowed.
        data = self.valid_satellite_data.copy()
        del data["reference_frame"]
        del data["center"]
        satellite = Satellite(**data)
        self.assertIsNone(satellite.reference_frame)
        self.assertIsNone(satellite.center)


# **************************************************************************************


@unittest.skipUnless(hasattr(time, "tzset"), "requires time.tzset (POSIX only)")
class TestSatelliteAt(unittest.TestCase):
    def setUp(self) -> None:
        self.satellite = TLE(
            tle_string="""
            ISS (ZARYA)
            1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
            2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
            """
        ).as_satellite()

    def test_at_treats_naive_datetime_as_utc(self) -> None:
        # Use a host timezone well away from UTC, so a local-time interpretation of the
        # naive datetime would shift the position by several hours of orbital motion:
        with host_timezone("America/New_York"):
            self.satellite.at(when=datetime(2008, 9, 20, 12, 0, 0))
            naive = self.satellite.eci_coordinate

            self.satellite.at(when=datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc))
            aware = self.satellite.eci_coordinate

        self.assertEqual(naive, aware)

    def test_at_converts_aware_datetime_to_utc(self) -> None:
        offset = timezone(timedelta(hours=5))

        self.satellite.at(when=datetime(2008, 9, 20, 17, 0, 0, tzinfo=offset))
        shifted = self.satellite.eci_coordinate

        self.satellite.at(when=datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc))
        utc = self.satellite.eci_coordinate

        self.assertEqual(shifted, utc)


# **************************************************************************************


class TestSatelliteECICoordinate(unittest.TestCase):
    """
    TLE elements are referred to the True Equator, Mean Equinox (TEME) frame, while the
    library's ECI frame is true-of-date (TOD). The two differ by a rotation about the
    z-axis through the equation of the equinoxes (EoE): r_TOD = ROT3(-EoE) · r_TEME.

    Reference values are from ERFA (pyerfa 2.0.1.5) at 2021-05-15T00:00:00 UTC, i.e.,
    TT = UTC + 69.184 s: eqeq94 gives EoE = -7.74605512156816e-05 rad (-15.977″), and
    rxp(rz(-EoE), r_TEME) gives the TOD position below. The library evaluates the EoE
    with an abbreviated nutation series that agrees with eqeq94 to 0.022″ here (about
    0.45 m at this radius), so positions are compared to sub-metre.
    """

    # The equation of the equinoxes from ERFA eqeq94 (in radians):
    EQUATION_OF_THE_EQUINOXES = -7.74605512156816e-05

    # The TOD position from ERFA, rxp(rz(-EoE), r_TEME) (in meters):
    ERFA_TRUE_OF_DATE = {
        "x": -3000153.4322423385,
        "y": -3039262.275147238,
        "z": 5283984.920004229,
    }

    def setUp(self) -> None:
        self.when = datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        self.satellite = TLE(
            tle_string="""
            1 25544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9003
            2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2422
            """
        ).as_satellite()

        self.satellite.at(when=self.when)

    def get_elements_frame_coordinate(
        self, satellite: Satellite
    ) -> CartesianCoordinate:
        # Rotating the perifocal position by ω, i and Ω from the TLE elements gives
        # the position in the frame of those elements, i.e., TEME:
        return convert_perifocal_to_eci(
            perifocal=satellite.perifocal_coordinate,
            argument_of_perigee=satellite.argument_of_pericenter,
            inclination=satellite.inclination,
            raan=satellite.raan,
        )

    def get_distance(self, a: CartesianCoordinate, b: CartesianCoordinate) -> float:
        return sqrt(
            (a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2 + (a["z"] - b["z"]) ** 2
        )

    def test_eci_coordinate_matches_erfa_true_of_date_position(self) -> None:
        eci = self.satellite.eci_coordinate

        self.assertLess(self.get_distance(eci, self.ERFA_TRUE_OF_DATE), 1.0)

    def test_eci_coordinate_is_teme_rotated_by_equation_of_the_equinoxes(self) -> None:
        teme = self.get_elements_frame_coordinate(self.satellite)

        E = self.EQUATION_OF_THE_EQUINOXES

        # An active rotation by +EoE about the z-axis (passive ROT3(-EoE)):
        expected = CartesianCoordinate(
            x=teme["x"] * cos(E) - teme["y"] * sin(E),
            y=teme["x"] * sin(E) + teme["y"] * cos(E),
            z=teme["z"],
        )

        eci = self.satellite.eci_coordinate

        self.assertLess(self.get_distance(eci, expected), 1.0)

    def test_equatorial_right_ascension_shifts_by_equation_of_the_equinoxes(
        self,
    ) -> None:
        teme = convert_eci_to_equatorial(
            eci=self.get_elements_frame_coordinate(self.satellite)
        )

        equatorial = self.satellite.equatorial_coordinate

        # The RA moves by the EoE (-0.0044382°); allow 0.05″ for the abbreviated
        # nutation series used by the library:
        self.assertAlmostEqual(
            equatorial["ra"] - teme["ra"],
            degrees(self.EQUATION_OF_THE_EQUINOXES),
            delta=0.05 / 3600,
        )

    def test_equatorial_declination_unchanged_by_teme_rotation(self) -> None:
        teme = convert_eci_to_equatorial(
            eci=self.get_elements_frame_coordinate(self.satellite)
        )

        equatorial = self.satellite.equatorial_coordinate

        # A rotation about the z-axis leaves the declination unchanged:
        self.assertAlmostEqual(equatorial["dec"], teme["dec"], delta=1e-9)

    def test_eci_coordinate_rotates_teme_stored_as_frame_code(self) -> None:
        # The validator currently stores the long name ("True Equator, Mean Equinox");
        # the rotation must still apply if the frame is stored as its code instead:
        self.satellite.reference_frame = "TEME"

        eci = self.satellite.eci_coordinate

        self.assertLess(self.get_distance(eci, self.ERFA_TRUE_OF_DATE), 1.0)

    def test_eci_coordinate_unchanged_for_non_teme_reference_frames(self) -> None:
        data: Dict[str, Any] = {
            "id": 25544,
            "name": "ISS (ZARYA)",
            "classification": "U",
            "designator": "98067A",
            "year": 2020,
            "day": 62.59097222,
            "jd": self.satellite.jd,
            "ephemeris": 0,
            "set": 900,
            "drag": 0.00010270,
            "raan": 147.1064,
            "inclination": 51.6442,
            "eccentricity": 0.0004607,
            "argument_of_pericenter": 95.6506,
            "mean_anomaly": 329.8285,
            "mean_motion": 15.49249062,
            "first_derivative_of_mean_motion": 0.00016717,
            "second_derivative_of_mean_motion": 0.0,
            "number_of_revolutions": 242,
        }

        for reference_frame in (None, "ICRF", "EME2000"):
            with self.subTest(reference_frame=reference_frame):
                satellite = Satellite(**data, reference_frame=reference_frame)

                satellite.at(when=self.when)

                self.assertEqual(
                    satellite.eci_coordinate,
                    self.get_elements_frame_coordinate(satellite),
                )


# **************************************************************************************


class TestSatelliteRoundTrip(unittest.TestCase):
    """
    A validated Satellite must survive a dump / re-validate round trip, i.e., every
    validator must accept the value it normalises to.
    """

    def setUp(self) -> None:
        self.data: Dict[str, Any] = {
            "id": 25544,
            "name": "ISS (ZARYA)",
            "classification": "U",
            "designator": "1998-067A",
            "year": 2021,
            "day": 123.456789,
            "jd": 2459365.456789,
            "ephemeris": 0,
            "set": 999,
            "drag": 0.00002182,
            "raan": 257.8333,
            "inclination": 51.6433,
            "eccentricity": 0.0001675,
            "argument_of_pericenter": 296.7755,
            "mean_anomaly": 73.3782,
            "mean_motion": 15.542259,
            "first_derivative_of_mean_motion": -0.00002182,
            "second_derivative_of_mean_motion": 0.0,
            "number_of_revolutions": 12345,
            "reference_frame": "TEME",
            "center": "EARTH",
        }

    def test_model_dump_round_trip(self) -> None:
        satellite = Satellite(**self.data)

        self.assertEqual(Satellite(**satellite.model_dump()), satellite)

    def test_model_dump_json_round_trip(self) -> None:
        satellite = Satellite(**self.data)

        self.assertEqual(
            Satellite.model_validate_json(satellite.model_dump_json()), satellite
        )

    def test_model_dump_round_trip_with_covariance(self) -> None:
        covariance = Covariance(
            reference_frame="TEME",
            **{
                name: float(index + 1)
                for index, name in enumerate(Covariance.model_fields)
                if name != "reference_frame"
            },
        )

        satellite = Satellite(**self.data, covariance=covariance)

        self.assertEqual(Satellite(**satellite.model_dump()), satellite)

    def test_tle_satellite_model_dump_round_trip(self) -> None:
        satellite = TLE(
            tle_string="""
            ISS (ZARYA)
            1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
            2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
            """
        ).as_satellite()

        self.assertEqual(Satellite(**satellite.model_dump()), satellite)

    def test_classification_accepts_normalised_value(self) -> None:
        for code, name in (
            ("U", "Unclassified"),
            ("C", "Classified"),
            ("S", "Secret"),
        ):
            with self.subTest(code=code):
                satellite = Satellite(**{**self.data, "classification": name})
                self.assertEqual(satellite.classification, name)

    def test_reference_frame_accepts_normalised_value(self) -> None:
        for name in (
            "True Equator, Mean Equinox",
            "International Celestial Reference Frame",
            "Epoch Mean Equinox 2000",
        ):
            with self.subTest(name=name):
                satellite = Satellite(**{**self.data, "reference_frame": name})
                self.assertEqual(satellite.reference_frame, name)

    def test_center_accepts_normalised_value(self) -> None:
        satellite = Satellite(**{**self.data, "center": "Earth"})
        self.assertEqual(satellite.center, "Earth")


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
