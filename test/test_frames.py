# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import datetime, timezone

from satelles.common import CartesianCoordinate
from satelles.frames import ECEF, ECI

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
                "x": 1.0,
                "y": 2.0,
                "z": 3.0,
            }
        )

        self.assertCoordinatesAlmostEqual(result, expected_position)


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
                "x": 1.7748323217117372,
                "y": -1.3601361070890385,
                "z": 3.0,
            }
        )

        self.assertCoordinatesAlmostEqual(result, expected_position)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
