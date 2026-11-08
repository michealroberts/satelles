# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************


import unittest
from math import degrees, pi, sqrt

from satelles import (
    HohmannTransferParameters,
    get_hohmann_transfer_eccentricity,
    get_hohmann_transfer_parameters,
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

# The standard gravitational parameter of the Earth, GM (in m³/s²):
EARTH_GM = 3.986004418e14

# **************************************************************************************


def get_target_offset_from_arrival_point(r1: float, r2: float, φ: float) -> float:
    """
    Propagate the target analytically over the Hohmann time of flight, starting φ
    degrees ahead of the chaser, and return its angular offset (in degrees, folded
    into [0, 180]) from the transfer arrival point, which lies 180° from the chaser's
    departure point.
    """
    # The time of flight is half the period of the transfer ellipse (Kepler's third law):
    tof = pi * sqrt(((r1 + r2) / 2) ** 3 / EARTH_GM)

    # The target moves on a circular orbit of radius r2 at its mean motion:
    n = sqrt(EARTH_GM / r2**3)

    # The target's angle at arrival, measured from the chaser's departure point:
    θ = φ + degrees(n * tof)

    # Angular offset from the arrival point (180°), modulo 360°:
    δ = (θ - 180) % 360

    return min(δ, 360 - δ)


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

        # The target sweeps ~2958.41° during the transfer, so the unwrapped phase angle
        # is 180° - 2958.41° = -2778.41°, which wraps to +101.59°:
        self.assertAlmostEqual(φ, 101.591652637, places=6)

    def test_phase_angle_descent_2_to_1_ratio(self) -> None:
        """
        Test phase angle for a 2:1 orbital radius ratio descent.
        """
        φ = get_hohmann_transfer_phase_angle(
            r1=14_000_000,
            r2=7_000_000,
        )

        # φ = 180° * (1 - (3 / 2)^(3/2)), so the target must start behind the chaser:
        self.assertAlmostEqual(φ, -150.681115276, places=6)

    def test_phase_angle_descent_large_ratio_wraps(self) -> None:
        """
        Test that a large descent phase angle is wrapped into [-180, 180).
        """
        φ = get_hohmann_transfer_phase_angle(
            r1=30_000_000,
            r2=10_000_000,
        )

        # φ = 180° * (1 - 2^(3/2)) = -329.12°, which wraps to +30.88°:
        self.assertAlmostEqual(φ, 30.883117546, places=6)

    def test_phase_angle_diametrically_opposite_maps_to_minus_180(self) -> None:
        """
        Test that a phase angle of exactly ±180° is returned as -180°.
        """
        φ = get_hohmann_transfer_phase_angle(
            r1=70_000_000,
            r2=10_000_000,
        )

        # For r1 = 7 * r2, a / r2 = 4, so φ = 180° * (1 - 4^(3/2)) = -1260° ≡ ±180°:
        self.assertEqual(φ, -180.0)

    def test_phase_angle_ascent_target_arrives_at_transfer_apoapsis(self) -> None:
        """
        Test that, starting φ ahead, the target reaches the transfer apoapsis at arrival.
        """
        for r1, r2 in [
            (7_000_000, 7_500_000),
            (7_000_000, 14_000_000),
            (7_000_000, 70_000_000),
            (6_678_000, 42_164_000),
            (LEO_RADIUS_IN_METERS, GEO_RADIUS_IN_METERS),
        ]:
            with self.subTest(r1=r1, r2=r2):
                φ = get_hohmann_transfer_phase_angle(r1=r1, r2=r2)

                self.assertLess(
                    get_target_offset_from_arrival_point(r1=r1, r2=r2, φ=φ), 1e-9
                )

    def test_phase_angle_descent_target_arrives_at_transfer_periapsis(self) -> None:
        """
        Test that, starting φ ahead, the target reaches the transfer periapsis at arrival.
        """
        for r1, r2 in [
            (7_500_000, 7_000_000),
            (14_000_000, 7_000_000),
            (30_000_000, 10_000_000),
            (70_000_000, 10_000_000),
            (42_164_000, 6_678_000),
            (GEO_RADIUS_IN_METERS, LEO_RADIUS_IN_METERS),
        ]:
            with self.subTest(r1=r1, r2=r2):
                φ = get_hohmann_transfer_phase_angle(r1=r1, r2=r2)

                self.assertLess(
                    get_target_offset_from_arrival_point(r1=r1, r2=r2, φ=φ), 1e-9
                )

                self.assertGreaterEqual(φ, -180)
                self.assertLess(φ, 180)

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


class TestGetHohmannTransferParameters(unittest.TestCase):
    """
    Tests for the get_hohmann_transfer_parameters function.
    """

    def test_leo_to_geo_returns_correct_semi_major_axis(self) -> None:
        """
        Test that LEO to GEO transfer returns correct semi-major axis.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertEqual(result.a, 19_393_000)

    def test_leo_to_geo_returns_correct_eccentricity(self) -> None:
        """
        Test that LEO to GEO transfer returns correct eccentricity.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.e, 0.8453, delta=0.0001)

    def test_leo_to_geo_returns_correct_delta_v1(self) -> None:
        """
        Test that LEO to GEO transfer returns correct Δv1 (departure burn).
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.Δv1, -4131.43, delta=1.0)

    def test_leo_to_geo_returns_correct_delta_v2(self) -> None:
        """
        Test that LEO to GEO transfer returns correct Δv2 (arrival burn).
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.Δv2, 2024.77, delta=1.0)

    def test_leo_to_geo_returns_correct_total_delta_v(self) -> None:
        """
        Test that LEO to GEO transfer returns correct total Δv.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.Δv, 6156.2077, delta=1.0)

    def test_leo_to_geo_returns_correct_transfer_time(self) -> None:
        """
        Test that LEO to GEO transfer returns correct transfer time.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.T, 13438.4289, delta=1.0)

    def test_leo_to_geo_returns_correct_phase_angle(self) -> None:
        """
        Test that LEO to GEO transfer returns correct phase angle.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.φ, 108.19, delta=0.1)

    def test_geo_to_leo_returns_correct_semi_major_axis(self) -> None:
        """
        Test that GEO to LEO transfer returns same semi-major axis as ascent.
        """
        result = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertEqual(result.a, 19_393_000)

    def test_geo_to_leo_returns_correct_eccentricity(self) -> None:
        """
        Test that GEO to LEO transfer returns same eccentricity as ascent.
        """
        result = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.e, 0.8453, delta=0.0001)

    def test_geo_to_leo_returns_correct_total_delta_v(self) -> None:
        """
        Test that GEO to LEO transfer returns same total Δv as ascent.
        """
        result = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.Δv, 6156.2077, delta=1.0)

    def test_geo_to_leo_returns_correct_transfer_time(self) -> None:
        """
        Test that GEO to LEO transfer returns same transfer time as ascent.
        """
        result = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.T, 13438.4289, delta=1.0)

    def test_geo_to_leo_returns_correct_phase_angle(self) -> None:
        """
        Test that GEO to LEO transfer returns the wrapped descent phase angle.
        """
        result = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(result.φ, 101.591652637, places=6)

    def test_2_to_1_ratio_returns_correct_semi_major_axis(self) -> None:
        """
        Test semi-major axis for a 2:1 orbital radius ratio.
        """
        result = get_hohmann_transfer_parameters(
            r1=10_000_000,
            r2=20_000_000,
        )

        self.assertEqual(result.a, 15_000_000)

    def test_2_to_1_ratio_returns_correct_eccentricity(self) -> None:
        """
        Test eccentricity for a 2:1 orbital radius ratio.
        """
        result = get_hohmann_transfer_parameters(
            r1=10_000_000,
            r2=20_000_000,
        )

        self.assertAlmostEqual(result.e, 0.3333, delta=0.0001)

    def test_2_to_1_ratio_returns_correct_phase_angle(self) -> None:
        """
        Test phase angle for a 2:1 orbital radius ratio.
        """
        result = get_hohmann_transfer_parameters(
            r1=10_000_000,
            r2=20_000_000,
        )

        self.assertAlmostEqual(result.φ, 63.1, delta=0.5)

    def test_raises_error_for_zero_r1(self) -> None:
        """
        Test that function raises ValueError for zero initial radius.
        """
        with self.assertRaises(ValueError) as context:
            get_hohmann_transfer_parameters(
                r1=0,
                r2=10_000_000,
            )

        self.assertIn("r1 must be positive", str(context.exception))

    def test_raises_error_for_negative_r1(self) -> None:
        """
        Test that function raises ValueError for negative initial radius.
        """
        with self.assertRaises(ValueError) as context:
            get_hohmann_transfer_parameters(
                r1=-5_000_000,
                r2=10_000_000,
            )

        self.assertIn("r1 must be positive", str(context.exception))

    def test_raises_error_for_zero_r2(self) -> None:
        """
        Test that function raises ValueError for zero final radius.
        """
        with self.assertRaises(ValueError) as context:
            get_hohmann_transfer_parameters(
                r1=10_000_000,
                r2=0,
            )

        self.assertIn("r2 must be positive", str(context.exception))

    def test_raises_error_for_negative_r2(self) -> None:
        """
        Test that function raises ValueError for negative final radius.
        """
        with self.assertRaises(ValueError) as context:
            get_hohmann_transfer_parameters(
                r1=10_000_000,
                r2=-5_000_000,
            )

        self.assertIn("r2 must be positive", str(context.exception))

    def test_raises_error_for_equal_radii(self) -> None:
        """
        Test that function raises ValueError when radii are equal.
        """
        with self.assertRaises(ValueError) as context:
            get_hohmann_transfer_parameters(
                r1=10_000_000,
                r2=10_000_000,
            )

        self.assertIn("must be different", str(context.exception))

    def test_returns_hohmann_transfer_parameters_instance(self) -> None:
        """
        Test that function returns a HohmannTransferParameters instance.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertIsInstance(result, HohmannTransferParameters)

    def test_result_contains_input_radii(self) -> None:
        """
        Test that result contains the input radii.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertEqual(result.r1, LEO_RADIUS_IN_METERS)
        self.assertEqual(result.r2, GEO_RADIUS_IN_METERS)

    def test_semi_major_axis_symmetric(self) -> None:
        """
        Test that semi-major axis is the same for ascent and descent.
        """
        ascent = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        descent = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertEqual(ascent.a, descent.a)

    def test_eccentricity_symmetric(self) -> None:
        """
        Test that eccentricity is the same for ascent and descent.
        """
        ascent = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        descent = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertEqual(ascent.e, descent.e)

    def test_total_delta_v_symmetric(self) -> None:
        """
        Test that total Δv is the same for ascent and descent.
        """
        ascent = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        descent = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertAlmostEqual(ascent.Δv, descent.Δv, places=6)

    def test_transfer_time_symmetric(self) -> None:
        """
        Test that transfer time is the same for ascent and descent.
        """
        ascent = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        descent = get_hohmann_transfer_parameters(
            r1=GEO_RADIUS_IN_METERS,
            r2=LEO_RADIUS_IN_METERS,
        )

        self.assertEqual(ascent.T, descent.T)

    def test_large_ratio_descent_returns_wrapped_phase_angle(self) -> None:
        """
        Test that a large-ratio descent returns a phase angle wrapped into [-180, 180).
        """
        result = get_hohmann_transfer_parameters(
            r1=30_000_000,
            r2=10_000_000,
        )

        self.assertAlmostEqual(result.φ, 30.883117546, places=6)

    def test_total_delta_v_is_positive(self) -> None:
        """
        Test that total Δv is always positive.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertGreater(result.Δv, 0)

    def test_transfer_time_is_positive(self) -> None:
        """
        Test that transfer time is always positive.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertGreater(result.T, 0)

    def test_eccentricity_less_than_one(self) -> None:
        """
        Test that eccentricity is always less than 1 for valid transfers.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertLess(result.e, 1)
        self.assertGreaterEqual(result.e, 0)

    def test_semi_major_axis_between_radii(self) -> None:
        """
        Test that semi-major axis is between the two radii.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertGreater(
            result.a,
            min(
                LEO_RADIUS_IN_METERS,
                GEO_RADIUS_IN_METERS,
            ),
        )

        self.assertLess(
            result.a,
            max(
                LEO_RADIUS_IN_METERS,
                GEO_RADIUS_IN_METERS,
            ),
        )

    def test_phase_angle_within_bounds(self) -> None:
        """
        Test that phase angle is within [-180, 180] degrees.
        """
        result = get_hohmann_transfer_parameters(
            r1=LEO_RADIUS_IN_METERS,
            r2=GEO_RADIUS_IN_METERS,
        )

        self.assertGreaterEqual(result.φ, -180)
        self.assertLessEqual(result.φ, 180)


# **************************************************************************************


if __name__ == "__main__":
    unittest.main()


# **************************************************************************************
