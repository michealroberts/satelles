# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from typing import Any, Dict

from pydantic import ValidationError

from satelles.satellite import ID

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
        self.assertEqual(model.classification, "U")
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

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
