# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import cos, degrees, pi

from satelles.kepler import get_eccentric_anomaly
from satelles.orbit import get_orbital_radius

# **************************************************************************************


class TestOrbitalRadius(unittest.TestCase):
    def test_zero_eccentricity(self):
        """
        With zero eccentricity, the orbital radius should equal the semi-major axis,
        regardless of the mean anomaly.
        """
        semi_major_axis = 7_000_000.0  # in meters
        eccentricity = 0.0
        # Test with various mean anomaly values.
        for mean_anomaly in [0, pi / 6, pi / 4, pi, 2 * pi]:
            with self.subTest(mean_anomaly=mean_anomaly):
                r = get_orbital_radius(
                    semi_major_axis,
                    degrees(mean_anomaly),
                    eccentricity,
                )
                self.assertAlmostEqual(r, semi_major_axis, places=6)

    def test_non_zero_eccentricity(self):
        """
        Ensure that the function computes the orbital radius correctly for
        non-zero eccentricities.
        """
        semi_major_axis = 7_000_000.0  # in meters
        eccentricity = 0.1
        # Test with various mean anomaly values.
        for mean_anomaly in [0.75, pi / 3, pi, 2.5]:
            with self.subTest(mean_anomaly=mean_anomaly):
                # Compute the eccentric anomaly.
                E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)
                expected_radius = semi_major_axis * (1 - eccentricity * cos(E))
                r = get_orbital_radius(
                    semi_major_axis,
                    degrees(mean_anomaly),
                    eccentricity,
                )
                self.assertAlmostEqual(r, expected_radius, places=6)

    def test_negative_mean_anomaly(self):
        """
        Ensure that the function computes the orbital radius correctly even when
        the mean anomaly is negative.
        """
        semi_major_axis = 7_000_000.0  # in meters
        eccentricity = 0.2
        mean_anomaly = -0.3
        E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)
        expected_radius = semi_major_axis * (1 - eccentricity * cos(E))
        r = get_orbital_radius(
            semi_major_axis,
            degrees(mean_anomaly),
            eccentricity,
        )
        self.assertAlmostEqual(r, expected_radius, places=6)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
