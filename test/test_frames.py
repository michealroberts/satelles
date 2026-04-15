# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import datetime, timezone

from satelles.common import CartesianCoordinate
from satelles.frame import Reference
from satelles.frames import (
    ECEF,
    ECI,
    EME2000,
    ITRF,
    TEME,
)

from .utils import SatellesTestCase

# **************************************************************************************


class TestECEFToECITransform(SatellesTestCase):
    def test_transform(self) -> None:
        """Verifies the ECEF to ECI frame transform for a specific date and time."""
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        ecef_position = CartesianCoordinate(
            {
                "x": 1.7748323217117372,
                "y": -1.3601361070890385,
                "z": 3.0,
            }
        )

        transform = ECEF.transform_to(when=when, other=ECI)

        result = transform.apply_to_position(ecef_position)

        expected_position = CartesianCoordinate(
            {
                "x": 0.9999978322532244,
                "y": 2.0000010838719193,
                "z": 3.0,
            }
        )

        self.assertCoordinatesAlmostEqual(expected_position, result)


# **************************************************************************************


class TestECIToECEFTransform(SatellesTestCase):
    def test_transform(self) -> None:
        """Verifies the ECI to ECEF frame transform for a specific date and time."""
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        eci_position = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 2.0,
                "z": 3.0,
            }
        )

        transform = ECI.transform_to(when=when, other=ECEF)

        result = transform.apply_to_position(eci_position)

        expected_position = CartesianCoordinate(
            {
                "x": 1.774830847495764,
                "y": -1.3601380307812398,
                "z": 3.0,
            }
        )

        self.assertCoordinatesAlmostEqual(expected_position, result)


# **************************************************************************************


class TestEME2000Frame(SatellesTestCase):
    def test_reference(self) -> None:
        self.assertEqual(EME2000.reference, Reference.EME2000)

    def test_is_inertial(self) -> None:
        self.assertTrue(EME2000.is_inertial)

    def test_parent(self) -> None:
        self.assertIs(EME2000.parent, ECI)

    def test_name(self) -> None:
        self.assertEqual(EME2000.name, "Earth Mean Equator 2000")

    def test_transform_to_eci(self) -> None:
        """Verifies the EME2000 to ECI frame transform for a specific date and time."""
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        eme2000_position = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
            }
        )

        transform = EME2000.transform_to(when=when, other=ECI)

        result = transform.apply_to_position(eme2000_position)

        expected_position = CartesianCoordinate(
            {
                "x": 0.9999814148813556,
                "y": -0.005592155927888036,
                "z": -0.002428514764262787,
            }
        )

        self.assertCoordinatesAlmostEqual(expected_position, result)

    def test_transform_to_eci_has_zero_translation(self) -> None:
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = EME2000.transform_to(when=when, other=ECI)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************


class TestITRFFrame(SatellesTestCase):
    def test_reference(self) -> None:
        self.assertEqual(ITRF.reference, Reference.ITRF)

    def test_is_not_inertial(self) -> None:
        self.assertFalse(ITRF.is_inertial)

    def test_parent(self) -> None:
        self.assertIs(ITRF.parent, ECEF)

    def test_name(self) -> None:
        self.assertEqual(ITRF.name, "International Terrestrial Reference Frame")

    def test_transform_to_ecef(self) -> None:
        """Verifies the ITRF to ECEF frame transform for a specific date and time."""
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        itrf_position = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 2.0,
                "z": 3.0,
            }
        )

        transform = ITRF.transform_to(when=when, other=ECEF)

        result = transform.apply_to_position(itrf_position)

        expected_position = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 2.0,
                "z": 3.0,
            }
        )

        self.assertCoordinatesAlmostEqual(expected_position, result)

    def test_transform_to_ecef_has_zero_translation(self) -> None:
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = ITRF.transform_to(when=when, other=ECEF)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************


class TestTEMEFrame(SatellesTestCase):
    def test_reference(self) -> None:
        self.assertEqual(TEME.reference, Reference.TEME)

    def test_is_inertial(self) -> None:
        self.assertTrue(TEME.is_inertial)

    def test_parent(self) -> None:
        self.assertIs(TEME.parent, ECI)

    def test_name(self) -> None:
        self.assertEqual(TEME.name, "True Equator Mean Equinox")

    def test_transform_to_eci(self) -> None:
        """Verifies the TEME to ECI frame transform for a specific date and time."""
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        teme_position = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
            }
        )

        transform = TEME.transform_to(when=when, other=ECI)

        result = transform.apply_to_position(teme_position)

        expected_position = CartesianCoordinate(
            {
                "x": 0.9999999999994125,
                "y": 1.0838730941284775e-06,
                "z": 0.0,
            }
        )

        self.assertCoordinatesAlmostEqual(expected_position, result)

    def test_transform_to_eci_has_zero_translation(self) -> None:
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = TEME.transform_to(when=when, other=ECI)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
