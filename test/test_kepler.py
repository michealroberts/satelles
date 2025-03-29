# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import pi, sin

from satelles import (
    EARTH_MASS,
    GRAVITATIONAL_CONSTANT,
    get_eccentric_anomaly,
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


class TestEccentricAnomaly(unittest.TestCase):
    def test_zero_eccentricity(self):
        """
        For zero eccentricity (e = 0), Kepler's equation simplifies to E = M.
        """
        for M in [0, pi / 6, pi, 2 * pi]:
            with self.subTest(mean_anomaly=M):
                E = get_eccentric_anomaly(M, 0)
                self.assertAlmostEqual(E, M, places=8)

    def test_convergence_residual(self):
        """
        Check that the computed eccentric anomaly satisfies Kepler's Equation
        within the convergence tolerance.
        """
        e = 0.5
        # Test a range of mean anomaly values.
        for M in [0.0, 0.1, 1.0, pi / 2, pi, 3 * pi / 2, 2 * pi]:
            with self.subTest(mean_anomaly=M):
                E = get_eccentric_anomaly(M, e)
                # The residual should be close to zero.
                residual = E - e * sin(E) - M
                self.assertAlmostEqual(residual, 0, places=8)

    def test_negative_mean_anomaly(self):
        """
        Test that the function correctly handles negative mean anomalies.
        """
        e = 0.1
        M = -0.5  # radians
        E = get_eccentric_anomaly(M, e)
        residual = E - e * sin(E) - M
        self.assertAlmostEqual(residual, 0, places=8)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
