# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import cos, degrees, pi, radians

from satelles.kepler import get_eccentric_anomaly, get_semi_major_axis
from satelles.orbit import OrbitClassification, classify_orbit, get_orbital_radius

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
                E = radians(get_eccentric_anomaly(degrees(mean_anomaly), eccentricity))
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
        E = radians(get_eccentric_anomaly(degrees(mean_anomaly), eccentricity))
        expected_radius = semi_major_axis * (1 - eccentricity * cos(E))
        r = get_orbital_radius(
            semi_major_axis,
            degrees(mean_anomaly),
            eccentricity,
        )
        self.assertAlmostEqual(r, expected_radius, places=6)


# **************************************************************************************


class TestClassifyOrbit(unittest.TestCase):
    def test_classify_leo_orbit(self):
        """
        A near-circular LEO orbit (ISS-like, ~400 km altitude) should be classified
        as LEO.
        """
        # ISS-like mean motion: ~15.49 rev/day → semi-major axis ≈ 6,782 km
        iss_semi_major_axis = get_semi_major_axis(15.48908877)
        classification = classify_orbit(iss_semi_major_axis, 0.0001428)
        self.assertEqual(classification, OrbitClassification.LEO)

    def test_classify_meo_orbit(self):
        """
        A GPS-like orbit (~20,200 km altitude) should be classified as MEO.
        """
        # GPS-like mean motion: ~2.006 rev/day → semi-major axis ≈ 26,350 km
        gps_semi_major_axis = get_semi_major_axis(2.00555251)
        classification = classify_orbit(gps_semi_major_axis, 0.0068550)
        self.assertEqual(classification, OrbitClassification.MEO)

    def test_classify_geo_orbit(self):
        """
        A geostationary orbit (~35,786 km altitude) should be classified as GEO.
        """
        # Use the canonical GEO semi-major axis directly:
        classification = classify_orbit(42_164_200.0, 0.0001)
        self.assertEqual(classification, OrbitClassification.GEO)

    def test_classify_heo_orbit(self):
        """
        A Molniya-like orbit with high eccentricity should be classified as HEO.
        """
        # Molniya orbit: mean motion ~2.006 rev/day, eccentricity ~0.74
        molniya_semi_major_axis = get_semi_major_axis(2.00555251)
        classification = classify_orbit(molniya_semi_major_axis, 0.7454195)
        self.assertEqual(classification, OrbitClassification.HEO)

    def test_heo_takes_precedence_over_geo(self):
        """
        Even when the semi-major axis lies within the GEO band, a high eccentricity
        must still yield an HEO classification.
        """
        classification = classify_orbit(42_164_200.0, 0.73)
        self.assertEqual(classification, OrbitClassification.HEO)

    def test_classify_just_below_geo_band_is_meo(self):
        """
        An orbit with a semi-major axis just below the GEO band should be MEO.
        """
        # 600 km below the GEO centre — outside the ±500 km band:
        below_geo = 42_164_200.0 - 600_000.0
        classification = classify_orbit(below_geo, 0.001)
        self.assertEqual(classification, OrbitClassification.MEO)

    def test_classify_just_above_geo_band_is_meo(self):
        """
        An orbit with a semi-major axis just above the GEO band should be MEO.
        """
        # 600 km above the GEO centre — outside the ±500 km band:
        above_geo = 42_164_200.0 + 600_000.0
        classification = classify_orbit(above_geo, 0.001)
        self.assertEqual(classification, OrbitClassification.MEO)

    def test_classify_circular_leo_boundary(self):
        """
        An orbit whose semi-major axis is exactly at the LEO/MEO boundary
        (2,000 km altitude) should be classified as MEO (boundary is exclusive for LEO).
        """
        from satelles.orbit import LEO_SEMI_MAJOR_AXIS_LIMIT

        # At the boundary the condition is strictly less-than, so the boundary
        # value itself falls into MEO:
        classification = classify_orbit(LEO_SEMI_MAJOR_AXIS_LIMIT, 0.0)
        self.assertEqual(classification, OrbitClassification.MEO)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
