# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************


import unittest

from satelles import (
    get_hohmann_transfer_eccentricity,
    get_hohmann_transfer_phase_angle,
    get_hohmann_transfer_semi_major_axis,
)

# **************************************************************************************

# The approximate radii for LEO orbits (in meters):
LEO_RADIUS_IN_METERS = 3_000_000  # (approx. 300 km altitude)

# **************************************************************************************

# The approximate radii for GEO orbits (in meters):
GEO_RADIUS_IN_METERS = 35_786_000  # (approx. 35,786 km altitude)

# **************************************************************************************


class TestGetHohmannTransferSemiMajorAxis(unittest.TestCase):
    def test_semi_major_axis_leo_to_geo(self) -> None:
        """
        Test semi-major axis calculation for a LEO to GEO transfer.
        """
        a = get_hohmann_transfer_semi_major_axis(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(
            a,
            (LEO_RADIUS_IN_METERS + GEO_RADIUS_IN_METERS) / 2,
            places=6,
        )

    def test_semi_major_axis_geo_to_leo(self) -> None:
        """
        Test semi-major axis calculation for a GEO to LEO transfer.
        """
        a = get_hohmann_transfer_semi_major_axis(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(
            a,
            (GEO_RADIUS_IN_METERS + LEO_RADIUS_IN_METERS) / 2,
            places=6,
        )


# **************************************************************************************


class TestGetHohmannTransferEccentricity(unittest.TestCase):
    def test_eccentricity_leo_to_geo(self) -> None:
        """
        Test eccentricity calculation for a LEO to GEO transfer.
        """
        e = get_hohmann_transfer_eccentricity(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(e, 0.845305, places=6)
        self.assertTrue(0 < e < 1)

    def test_eccentricity_geo_to_leo(self) -> None:
        """
        Test eccentricity calculation for a GEO to LEO transfer.
        """
        e = get_hohmann_transfer_eccentricity(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(e, 0.845305, places=6)
        self.assertTrue(0 < e < 1)

    def test_eccentricity_circular_orbit(self) -> None:
        """
        Test eccentricity calculation for a circular orbit transfer.
        """
        r = 10_000_000  # Arbitrary radius

        e = get_hohmann_transfer_eccentricity(
            r1=r,
            r2=r,
        )

        self.assertEqual(e, 0.0)

    def test_r1_plus_r2_zero_raises_value_error(self) -> None:
        """
        Test that r1 + r2 being zero raises ValueError.
        """
        r1 = 10_000_000

        r2 = -r1

        with self.assertRaises(ValueError):
            get_hohmann_transfer_eccentricity(r1=r1, r2=r2)


# **************************************************************************************


class TestGetHohmannTransferPhaseAngle(unittest.TestCase):
    def test_phase_angle_ascent_leo_to_geo(self) -> None:
        """
        Test phase angle for a LEO to GEO transfer (ascent).
        """
        φ = get_hohmann_transfer_phase_angle(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        # Phase angle should be positive for ascent (target ahead):
        self.assertGreater(φ, 0)
        # Expected value approximately 108.19° for LEO to GEO transfer:
        self.assertAlmostEqual(φ, 108.19, delta=1.0)

    def test_phase_angle_descent_geo_to_leo(self) -> None:
        """
        Test phase angle for a GEO to LEO transfer (descent).
        """
        φ = get_hohmann_transfer_phase_angle(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        # Phase angle should be negative for descent (target behind):
        self.assertLess(φ, 0)

        # Should be symmetric with the ascent case:
        self.assertAlmostEqual(φ, -108.19, delta=1.0)

    def test_phase_angle_symmetry(self) -> None:
        """
        Test that ascent and descent phase angles are symmetric (opposite signs).
        """
        φ_ascent = get_hohmann_transfer_phase_angle(
            r1=7_000_000,
            r2=14_000_000,
        )

        φ_descent = get_hohmann_transfer_phase_angle(
            r1=14_000_000,
            r2=7_000_000,
        )

        self.assertAlmostEqual(φ_ascent, -φ_descent, places=9)

    def test_phase_angle_small_transfer(self) -> None:
        """
        Test phase angle for a small orbital transfer (close orbits).
        """
        r1 = 7_000_000
        r2 = 7_500_000

        φ = get_hohmann_transfer_phase_angle(
            r1=r1,
            r2=r2,
        )

        self.assertGreater(φ, 0)
        self.assertLess(φ, 30)

    def test_phase_angle_large_transfer(self) -> None:
        """
        Test phase angle for a large orbital transfer (distant orbits).
        """
        r1 = 7_000_000
        r2 = 70_000_000

        φ = get_hohmann_transfer_phase_angle(
            r1=r1,
            r2=r2,
        )

        # For large transfers, phase angle approaches but stays below 180°:
        self.assertGreater(φ, 100)
        self.assertLess(φ, 180)

    def test_phase_angle_2_to_1_ratio(self) -> None:
        """
        Test phase angle for a 2:1 orbital radius ratio.
        """
        r1 = 10_000_000
        r2 = 20_000_000

        φ = get_hohmann_transfer_phase_angle(
            r1=r1,
            r2=r2,
        )

        # For 2:1 ratio, expected phase angle ≈ 63.1° for ascent:
        self.assertAlmostEqual(φ, 63.1, delta=1.5)

    def test_phase_angle_negative_r1_raises_value_error(self) -> None:
        """
        Test that a negative initial orbit radius raises ValueError.
        """
        with self.assertRaises(ValueError):
            get_hohmann_transfer_phase_angle(
                r1=-7_000_000,
                r2=14_000_000,
            )

    def test_phase_angle_negative_r2_raises_value_error(self) -> None:
        """
        Test that a negative final orbit radius raises ValueError.
        """
        with self.assertRaises(ValueError):
            get_hohmann_transfer_phase_angle(
                r1=7_000_000,
                r2=-14_000_000,
            )

    def test_phase_angle_equal_radii_raises_value_error(self) -> None:
        """
        Test that equal orbit radii raises ValueError.
        """
        with self.assertRaises(ValueError):
            get_hohmann_transfer_phase_angle(
                r1=10_000_000,
                r2=10_000_000,
            )


# **************************************************************************************


if __name__ == "__main__":
    unittest.main()


# **************************************************************************************
