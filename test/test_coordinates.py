# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import cos, degrees, sin

from satelles import (
    get_eccentric_anomaly,
    get_perifocal_coordinate,
)

# **************************************************************************************


class TestGetPerifocalPosition(unittest.TestCase):
    def test_zero_eccentricity(self):
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.0
        mean_anomaly = 1.0
        true_anomaly = 2.0

        expected_r = semi_major_axis
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)

    def test_nonzero_eccentricity(self):
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.1
        mean_anomaly = 1.2
        true_anomaly = 2.5

        # Compute the eccentric anomaly (E) using get_eccentric_anomaly:
        E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)

        expected_r = semi_major_axis * (1 - eccentricity * cos(E))
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)

    def test_negative_true_anomaly(self):
        """
        Test that a negative true anomaly (provided in degrees) yields the correct
        perifocal coordinates.
        """
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.2
        mean_anomaly = 0.8
        true_anomaly = -1.0

        # Compute the eccentric anomaly (E) using get_eccentric_anomaly:
        E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)
        expected_r = semi_major_axis * (1 - eccentricity * cos(E))
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
