# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import atan2, cos, degrees, pi, sin, sqrt

from satelles import (
    EARTH_MASS,
    GRAVITATIONAL_CONSTANT,
    get_eccentric_anomaly,
    get_semi_latus_rectum,
    get_semi_major_axis,
    get_true_anomaly,
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


class TestSemiLatusRectum(unittest.TestCase):
    def test_zero_eccentricity(self):
        """
        With zero eccentricity, the orbit is circular so the semi-latus rectum equals
        the semi-major axis.
        """
        a = 10000.0  # meters
        e = 0.0
        expected = 10000.0
        result = get_semi_latus_rectum(a, e)
        self.assertAlmostEqual(
            result,
            expected,
            msg="Semi-latus rectum should equal semi-major axis for a circular orbit.",
        )

    def test_half_eccentricity(self):
        """
        With an eccentricity of 0.5, p = a * (1 - 0.5^2) = a * 0.75.
        """
        a = 10000.0  # meters
        e = 0.5
        expected = 10000.0 * 0.75  # 7500.0 meters
        result = get_semi_latus_rectum(a, e)
        self.assertAlmostEqual(
            result,
            expected,
            msg="Semi-latus rectum calculation is incorrect for e=0.5.",
        )

    def test_small_eccentricity(self):
        """
        With a small eccentricity, e.g. 0.1, p = a * (1 - 0.1^2) = a * 0.99.
        """
        a = 20000.0  # meters
        e = 0.1
        expected = 20000.0 * 0.99  # 19800.0 meters
        result = get_semi_latus_rectum(a, e)
        self.assertAlmostEqual(
            result,
            expected,
            msg="Semi-latus rectum calculation is incorrect for e=0.1.",
        )

    def test_high_eccentricity(self):
        """
        For a high eccentricity, verify the computed value is correct.
        """
        a = 1.0  # meter
        e = 0.99
        expected = a * (1 - 0.99**2)
        result = get_semi_latus_rectum(a, e)
        self.assertAlmostEqual(
            result,
            expected,
            places=5,
            msg="Semi-latus rectum calculation is incorrect for high eccentricity.",
        )


# **************************************************************************************


class TestEccentricAnomaly(unittest.TestCase):
    def test_zero_eccentricity(self):
        """
        For zero eccentricity (e = 0), Kepler's equation simplifies to E = M.
        """
        for M in [0, pi / 6, pi, 2 * pi]:
            with self.subTest(mean_anomaly=M):
                E = get_eccentric_anomaly(degrees(M), 0)
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
                E = get_eccentric_anomaly(degrees(M), e)
                # The residual should be close to zero.
                residual = E - e * sin(E) - M
                self.assertAlmostEqual(residual, 0, places=8)

    def test_negative_mean_anomaly(self):
        """
        Test that the function correctly handles negative mean anomalies.
        """
        e = 0.1
        M = -0.5  # radians
        E = get_eccentric_anomaly(degrees(M), e)
        residual = E - e * sin(E) - M
        self.assertAlmostEqual(residual, 0, places=8)


# **************************************************************************************


class TestTrueAnomaly(unittest.TestCase):
    def test_zero_eccentricity(self):
        """
        For zero eccentricity (e = 0), the true anomaly should equal the mean anomaly.
        """
        eccentricity = 0.0
        for mean_anomaly in [
            0.0,
            pi / 6,
            pi / 4,
            pi / 2,
            pi,
            2 * pi,
        ]:
            with self.subTest(mean_anomaly=mean_anomaly):
                ν = get_true_anomaly(degrees(mean_anomaly), eccentricity)
                # Normalize mean_anomaly to [0, 2pi) for comparison.
                expected = mean_anomaly % (2 * pi)
                self.assertAlmostEqual(ν, degrees(expected), places=8)

    def test_mean_anomaly_zero(self):
        """
        For any eccentricity, if the mean anomaly is zero, then the true anomaly should be zero.
        """
        mean_anomaly = 0.0
        for eccentricity in [0.0, 0.1, 0.5, 0.9]:
            with self.subTest(eccentricity=eccentricity):
                ν = get_true_anomaly(mean_anomaly, eccentricity)
                self.assertAlmostEqual(ν, 0.0, places=8)

    def test_normalization(self):
        """
        Test that the output true anomaly is normalized to [0, 2π).
        """
        # For a given eccentricity and mean anomaly that leads to a negative true anomaly,
        # check that the returned value is normalized.
        eccentricity = 0.2
        # Choose a mean anomaly that might yield a negative true anomaly before normalization.
        mean_anomaly = -0.5
        ν = get_true_anomaly(mean_anomaly, eccentricity)
        self.assertTrue(0 <= ν < 360)

    def test_invalid_eccentricity(self):
        """
        Check that a ValueError is raised for an eccentricity outside [0, 1).
        """
        with self.assertRaises(ValueError):
            get_true_anomaly(1.0, 1.0)  # e = 1.0 is not allowed for elliptical orbits

    def test_known_value(self):
        """
        Test a known value: Compute the expected true anomaly using the same formulas
        and compare with the function's output.
        """
        eccentricity = 0.1
        mean_anomaly = 0.75
        # Compute the eccentric anomaly using the dependent function.
        E = get_eccentric_anomaly(mean_anomaly, eccentricity)
        expected = 2 * atan2(
            sqrt(1 + eccentricity) * sin(E / 2),
            sqrt(1 - eccentricity) * cos(E / 2),
        )
        # Normalize expected value.
        if expected < 0:
            expected += 2 * pi

        ν = get_true_anomaly(mean_anomaly, eccentricity)
        self.assertAlmostEqual(ν, degrees(expected), places=8)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
