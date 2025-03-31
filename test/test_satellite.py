# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from typing import Any, Dict

from pydantic import ValidationError

from satelles.satellite import ID, OrbitalElements, Satellite

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
            "argument_of_perigee": 296.7755,
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
        self.assertAlmostEqual(model.argument_of_perigee, 296.7755)
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
        # Combine valid data from ID and OrbitalElements
        self.base_id: Dict[str, Any] = {
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
        self.base_oe: Dict[str, Any] = {
            "drag": 0.00002182,
            "raan": 257.8333,
            "inclination": 51.6433,
            "eccentricity": 0.0001675,
            "argument_of_perigee": 296.7755,
            "mean_anomaly": 73.3782,
            "mean_motion": 15.542259,
            "first_derivative_of_mean_motion": -0.00002182,
            "second_derivative_of_mean_motion": 0.0,
            "number_of_revolutions": 12345,
        }
        self.valid_satellite_data: Dict[str, Any] = {
            **self.base_id,
            **self.base_oe,
            "reference_frame": "TEME",  # valid input; should map to human readable
            "center": "EARTH",  # valid input; should map to "Earth"
        }

    def test_valid_optional_fields(self) -> None:
        sat = Satellite(**self.valid_satellite_data)
        self.assertEqual(sat.reference_frame, "True Equator, Mean Equinox")
        self.assertEqual(sat.center, "Earth")

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
        sat = Satellite(**data)
        self.assertIsNone(sat.reference_frame)
        self.assertIsNone(sat.center)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
