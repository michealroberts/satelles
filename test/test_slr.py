# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import datetime
from typing import List

from pydantic import ValidationError

from satelles.models import Position, Velocity
from satelles.slr import CPFHeader

# **************************************************************************************


class TestCPFHeaderModel(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_position_data: List[Position] = [
            Position(
                x=1234.5,
                y=-987.6,
                z=0.0,
            )
        ]

        self.valid_velocity_data: List[Velocity] = [
            Velocity(
                vx=1.0,
                vy=2.0,
                vz=3.0,
            )
        ]

        self.valid_cpf_data = {
            "norad_id": "12345",
            "cospar_id": "2025-001A",
            "sic": "5678",
            "ephemeris_source": "ESA",
            "year": 2025,
            "month": 6,
            "day": 6,
            "hour": 12,
            "ephemeris_sequence_number": 100,
            "sub_daily_sequence_number": 5,
            "target_name": "TARGET1",
            "start": datetime(2025, 6, 6, 0, 0, 0),
            "end": datetime(2025, 6, 7, 0, 0, 0),
            "interval": 60,
            "tiv_compatibility": 1,
            "target_class": 3,  # → "Synchronous Transponder"
            "reference_frame": 2,  # → "Geocentric Space Fixed Mean Of Date (J2000)"
            "rotational_angle_type": 2,
            "center_of_mass_correction": 1,  # → True
            "location_dynamics": 5,  # → "Mars Surface"
            "mjd": 60000,
            "seconds_of_day": 43200.5,
            "leap_second": 0,
            "direction_position": 1,  # → "Transmit"
            "positions": self.valid_position_data,
            "direction_velocity": 2,  # → "Receive"
            "velocities": self.valid_velocity_data,
            "direction_stellar_aberration": 0,  # → "Common Epoch"
            "stellar_aberrations": self.valid_position_data,
            "relativistic_range_correction": 0.123,
            "notes": "satelles",
        }

    def test_valid_cpf_fields(self) -> None:
        """
        A CPF constructed via model_validate with fully valid data
        should succeed, and integer-coded fields map correctly.
        """
        cpf = CPFHeader.model_validate(self.valid_cpf_data)
        self.assertEqual(cpf.target_class, "Synchronous Transponder")
        self.assertEqual(
            cpf.reference_frame,
            "Geocentric Space Fixed Mean Of Date (J2000)",
        )
        self.assertTrue(cpf.center_of_mass_correction)
        self.assertEqual(cpf.location_dynamics, "Mars Surface")
        self.assertEqual(cpf.norad_id, "12345")
        self.assertEqual(cpf.cospar_id, "2025-001A")
        self.assertEqual(cpf.sic, "5678")
        self.assertEqual(cpf.ephemeris_source, "ESA")
        self.assertEqual(cpf.year, 2025)
        self.assertEqual(cpf.month, 6)
        self.assertEqual(cpf.day, 6)
        self.assertEqual(cpf.hour, 12)
        self.assertEqual(cpf.ephemeris_sequence_number, 100)
        self.assertEqual(cpf.sub_daily_sequence_number, 5)
        self.assertEqual(cpf.target_name, "TARGET1")
        self.assertEqual(cpf.interval, 60)
        self.assertEqual(cpf.tiv_compatibility, True)
        self.assertEqual(cpf.start, datetime(2025, 6, 6, 0, 0, 0))
        self.assertEqual(cpf.end, datetime(2025, 6, 7, 0, 0, 0))
        self.assertEqual(cpf.notes, "satelles")

    def test_year_below_minimum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["year"] = 1949
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("year", str(cm.exception))

    def test_year_above_maximum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["year"] = 3101
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("year", str(cm.exception))

    def test_month_below_minimum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["month"] = 0
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("month", str(cm.exception))

    def test_month_above_maximum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["month"] = 13
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("month", str(cm.exception))

    def test_day_below_minimum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["day"] = 0
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("day", str(cm.exception))

    def test_day_above_maximum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["day"] = 32
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("day", str(cm.exception))

    def test_hour_below_minimum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["hour"] = -1
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("hour", str(cm.exception))

    def test_hour_above_maximum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["hour"] = 24
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("hour", str(cm.exception))

    def test_interval_below_minimum_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["interval"] = 0
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("interval", str(cm.exception))

    def test_tiv_compatibility_invalid_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["tiv_compatibility"] = 2
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("tiv_compatibility", str(cm.exception))

    def test_rotational_angle_type_invalid_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["rotational_angle_type"] = 3
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("rotational_angle_type", str(cm.exception))

    def test_target_name_length_exceeded_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["target_name"] = "X" * 11
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("target_name", str(cm.exception))

    def test_valid_convert_target_class(self) -> None:
        data = dict(self.valid_cpf_data)
        data["target_class"] = 1
        cpf = CPFHeader.model_validate(data)
        self.assertEqual(cpf.target_class, "Passive Retro-Reflector")

    def test_invalid_convert_target_class_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["target_class"] = 2
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("target_class", str(cm.exception))

    def test_valid_convert_reference_frame(self) -> None:
        data = dict(self.valid_cpf_data)
        data["reference_frame"] = 1
        cpf = CPFHeader.model_validate(data)
        self.assertEqual(cpf.reference_frame, "Geocentric Space Fixed Inertial (ECI)")

    def test_invalid_convert_reference_frame_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["reference_frame"] = 3
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("reference_frame", str(cm.exception))

    def test_valid_convert_center_of_mass_correction(self) -> None:
        data = dict(self.valid_cpf_data)
        data["center_of_mass_correction"] = 0
        cpf = CPFHeader.model_validate(data)
        self.assertFalse(cpf.center_of_mass_correction)

    def test_invalid_convert_center_of_mass_correction_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["center_of_mass_correction"] = 2
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("center_of_mass_correction", str(cm.exception))

    def test_valid_convert_location_dynamics(self) -> None:
        data = dict(self.valid_cpf_data)
        data["location_dynamics"] = 2
        cpf = CPFHeader.model_validate(data)
        self.assertEqual(cpf.location_dynamics, "Lunar Orbit")

    def test_invalid_convert_location_dynamics_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["location_dynamics"] = 11
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("location_dynamics", str(cm.exception))

    def test_notes_optional(self) -> None:
        data = dict(self.valid_cpf_data)
        data.pop("notes", None)
        cpf = CPFHeader.model_validate(data)
        self.assertIsNone(cpf.notes)

    def test_notes_length_exceeded_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["notes"] = "Y" * 11
        with self.assertRaises(ValidationError) as cm:
            CPFHeader.model_validate(data)
        self.assertIn("notes", str(cm.exception))

    def test_start_must_be_before_end_raises(self) -> None:
        data = dict(self.valid_cpf_data)
        data["start"] = datetime(2025, 6, 7)
        data["end"] = datetime(2025, 6, 6)
        with self.assertRaises(ValidationError):
            CPFHeader.model_validate(data)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
