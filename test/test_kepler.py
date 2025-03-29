# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import pi

from satelles import (
    EARTH_MASS,
    GRAVITATIONAL_CONSTANT,
    get_semi_major_axis,
)

# **************************************************************************************


class TestSemiMajorAxis(unittest.TestCase):
    def test_get_semi_major_axis_default_mass(self):
        """
        Test the semi_major_axis function with default mass (0.0).
        """
        mean_motion = 15.48908877  # in revolutions per day
        result = get_semi_major_axis(mean_motion)

        # Manual calculation of expected semi-major axis:
        μ = GRAVITATIONAL_CONSTANT * EARTH_MASS
        n = (mean_motion * 2 * pi) / 86400  # convert rev/day to rad/s
        expected = (μ / n**2) ** (1 / 3)

        self.assertAlmostEqual(result, expected, places=5)

    def test_get_semi_major_axis_with_mass(self):
        """
        Test the semi_major_axis function with a non-zero satellite mass.
        """
        mean_motion = 15.48908877  # in revolutions per day
        satellite_mass = 1000.0  # in kg
        result = get_semi_major_axis(mean_motion, satellite_mass)

        # Expected gravitational parameter includes the satellite mass:
        μ = GRAVITATIONAL_CONSTANT * (EARTH_MASS + satellite_mass)
        n = (mean_motion * 2 * pi) / 86400
        expected = (μ / n**2) ** (1 / 3)

        self.assertAlmostEqual(result, expected, places=5)

    def test_mass_none(self):
        """
        Test that passing None as the mass defaults to 0.0.
        """
        mean_motion = 15.48908877  # in revolutions per day
        result = get_semi_major_axis(mean_motion, None)

        μ = GRAVITATIONAL_CONSTANT * (EARTH_MASS + 0.0)
        n = (mean_motion * 2 * pi) / 86400
        expected = (μ / n**2) ** (1 / 3)

        self.assertAlmostEqual(result, expected, places=5)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
