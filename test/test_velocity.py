# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import degrees, isclose, pi, sqrt

from satelles.constants import GRAVITATIONAL_CONSTANT
from satelles.earth import EARTH_MASS
from satelles.velocity import get_perifocal_velocity

# **************************************************************************************

MU = EARTH_MASS * GRAVITATIONAL_CONSTANT

# **************************************************************************************


class TestGetPerifocalVelocity(unittest.TestCase):
    def test_circular_orbit(self):
        """
        For a circular orbit (eccentricity = 0) at true anomaly 0.
        """
        semi_major_axis = 7000e3
        eccentricity = 0.0
        true_anomaly = 0.0

        result = get_perifocal_velocity(semi_major_axis, true_anomaly, eccentricity)
        expected_vx = 0.0
        expected_vy = sqrt(MU / semi_major_axis)

        self.assertTrue(isclose(result["vx"], expected_vx, rel_tol=1e-9))
        self.assertTrue(isclose(result["vy"], expected_vy, rel_tol=1e-9))
        self.assertTrue(isclose(result["vz"], 0.0, rel_tol=1e-9))

    def test_eccentric_orbit(self):
        semi_major_axis = 10000.0
        eccentricity = 0.5
        true_anomaly = degrees(pi / 2)

        result = get_perifocal_velocity(semi_major_axis, true_anomaly, eccentricity)

        self.assertTrue(isclose(result["vx"], -230535.72646454026, rel_tol=1e-9))
        self.assertTrue(isclose(result["vy"], 115267.86323227016, rel_tol=1e-9))
        self.assertTrue(isclose(result["vz"], 0.0, rel_tol=1e-9))

    def test_invalid_semi_latus_rectum(self):
        """
        Test that if the semi-latus rectum is non-positive (e.g., if eccentricity >= 1),
        the function raises a ValueError.
        """
        semi_major_axis = 10000.0
        # Parabolic orbit (p would be zero)
        eccentricity = 1.0
        true_anomaly = 0.0

        with self.assertRaises(ValueError):
            get_perifocal_velocity(semi_major_axis, true_anomaly, eccentricity)

        eccentricity = 1.1  # Hyperbolic orbit (p becomes negative):
        with self.assertRaises(ValueError):
            get_perifocal_velocity(semi_major_axis, true_anomaly, eccentricity)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
