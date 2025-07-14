# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import isfinite
from typing import List

from satelles import (
    BarycentricLagrange3DPositionInterpolator,
    Hermite3DPositionInterpolator,
)
from satelles.models import Position

# **************************************************************************************


class TestBarycentricLagrange3DPositionInterpolator(unittest.TestCase):
    def setUp(self) -> None:
        self.positions: List[Position] = [
            Position(
                x=8784072.022,
                y=-547370.762,
                z=8570228.005,
                at=0.0,
            ),
            Position(
                x=8977853.029,
                y=-761246.656,
                z=8352633.966,
                at=60.0,
            ),
            Position(
                x=9162987.348,
                y=-976206.356,
                z=8128575.502,
                at=120.0,
            ),
            Position(
                x=9339329.301,
                y=-1192011.707,
                z=7898228.137,
                at=180.0,
            ),
            Position(
                x=9506742.0,
                y=-1408422.789,
                z=7661772.117,
                at=240.0,
            ),
            Position(
                x=9665097.457,
                y=-1625198.174,
                z=7419392.278,
                at=300.0,
            ),
            Position(
                x=9814276.685,
                y=-1842095.185,
                z=7171277.892,
                at=360.0,
            ),
            Position(
                x=9954169.781,
                y=-2058870.156,
                z=6917622.520,
                at=420.0,
            ),
            Position(
                x=10084676.017,
                y=-2275278.693,
                z=6658623.858,
                at=480.0,
            ),
            Position(
                x=10205703.902,
                y=-2491075.937,
                z=6394483.585,
                at=540.0,
            ),
        ]

    def test_initialization_requires_at_least_two_positions(self) -> None:
        """Interpolator must be initialized with at least two positions."""
        with self.assertRaises(ValueError):
            BarycentricLagrange3DPositionInterpolator(self.positions[:1])

    def test_two_point_interpolation_linear(self) -> None:
        """With exactly two samples, interpolation is linear between them."""
        positions: List[Position] = [
            Position(
                x=0.0,
                y=0.0,
                z=0.0,
                at=0.0,
            ),
            Position(
                x=10.0,
                y=20.0,
                z=30.0,
                at=10.0,
            ),
        ]

        interpolator = BarycentricLagrange3DPositionInterpolator(positions)

        position = interpolator.get_interpolated_position(5.0)
        self.assertEqual(position.at, 5.0)
        self.assertAlmostEqual(position.x, 5.0, places=9)
        self.assertAlmostEqual(position.y, 10.0, places=9)
        self.assertAlmostEqual(position.z, 15.0, places=9)

    def test_exact_sample_points(self) -> None:
        """At each sample time, interpolation returns the original Position exactly."""
        interpolator = BarycentricLagrange3DPositionInterpolator(self.positions)

        for expected in self.positions:
            position = interpolator.get_interpolated_position(expected.at)
            self.assertEqual(position.at, expected.at)
            self.assertAlmostEqual(position.x, expected.x, places=9)
            self.assertAlmostEqual(position.y, expected.y, places=9)
            self.assertAlmostEqual(position.z, expected.z, places=9)

    def test_midpoint_between_first_two(self) -> None:
        """
        Interpolation at t=30 (between the 1st and 2nd positions) lies within their
        value range.
        """
        interpolator = BarycentricLagrange3DPositionInterpolator(self.positions)

        # Define time at the midpoint between the first two positions:
        at: float = 30.0
        actual = interpolator.get_interpolated_position(at)
        a, b = self.positions[0], self.positions[1]

        self.assertTrue(min(a.x, b.x) <= actual.x <= max(a.x, b.x))
        self.assertTrue(min(a.y, b.y) <= actual.y <= max(a.y, b.y))
        self.assertTrue(min(a.z, b.z) <= actual.z <= max(a.z, b.z))
        self.assertEqual(actual.at, at)

    def test_arbitrary_midpoint_within_bounds(self) -> None:
        """
        Interpolation at t=150 (between the 3rd and 4th positions) lies within their
        value range.
        """
        interpolator = BarycentricLagrange3DPositionInterpolator(self.positions)

        # Define time between positions[2] (120) and positions[3] (180):
        at: float = 150.0
        actual = interpolator.get_interpolated_position(at)
        a, b = self.positions[2], self.positions[3]

        self.assertTrue(min(a.x, b.x) <= actual.x <= max(a.x, b.x))
        self.assertTrue(min(a.y, b.y) <= actual.y <= max(a.y, b.y))
        self.assertTrue(min(a.z, b.z) <= actual.z <= max(a.z, b.z))
        self.assertEqual(actual.at, at)

    def test_out_of_bounds_behavior(self) -> None:
        """
        Querying before the first sample or after the last should still return a
        Position with 'at' set to the query time, and at least one coordinate finite.
        """
        interpolator = BarycentricLagrange3DPositionInterpolator(self.positions)

        before = interpolator.get_interpolated_position(-60.0)
        after = interpolator.get_interpolated_position(600.0)

        self.assertEqual(before.at, -60.0)
        self.assertEqual(after.at, 600.0)

        self.assertTrue(
            any(isfinite(position) for position in (before.x, before.y, before.z))
        )
        self.assertTrue(
            any(isfinite(position) for position in (after.x, after.y, after.z))
        )


# **************************************************************************************


class TestHermite3DPositionInterpolator(unittest.TestCase):
    def setUp(self) -> None:
        self.positions: List[Position] = [
            Position(
                x=8784072.022,
                y=-547370.762,
                z=8570228.005,
                at=0.0,
            ),
            Position(
                x=8977853.029,
                y=-761246.656,
                z=8352633.966,
                at=60.0,
            ),
            Position(
                x=9162987.348,
                y=-976206.356,
                z=8128575.502,
                at=120.0,
            ),
            Position(
                x=9339329.301,
                y=-1192011.707,
                z=7898228.137,
                at=180.0,
            ),
            Position(
                x=9506742.0,
                y=-1408422.789,
                z=7661772.117,
                at=240.0,
            ),
            Position(
                x=9665097.457,
                y=-1625198.174,
                z=7419392.278,
                at=300.0,
            ),
            Position(
                x=9814276.685,
                y=-1842095.185,
                z=7171277.892,
                at=360.0,
            ),
            Position(
                x=9954169.781,
                y=-2058870.156,
                z=6917622.520,
                at=420.0,
            ),
            Position(
                x=10084676.017,
                y=-2275278.693,
                z=6658623.858,
                at=480.0,
            ),
            Position(
                x=10205703.902,
                y=-2491075.937,
                z=6394483.585,
                at=540.0,
            ),
        ]

    def test_initialization_requires_at_least_two_positions(self) -> None:
        """Interpolator must be initialized with at least two positions."""
        with self.assertRaises(ValueError):
            Hermite3DPositionInterpolator(self.positions[:1])

    def test_two_point_interpolation_linear(self) -> None:
        """With exactly two samples, interpolation is linear between them."""
        positions: List[Position] = [
            Position(
                x=0.0,
                y=0.0,
                z=0.0,
                at=0.0,
            ),
            Position(
                x=10.0,
                y=20.0,
                z=30.0,
                at=10.0,
            ),
        ]

        interpolator = Hermite3DPositionInterpolator(positions)

        position = interpolator.get_interpolated_position(5.0)
        self.assertEqual(position.at, 5.0)
        self.assertAlmostEqual(position.x, 5.0, places=9)
        self.assertAlmostEqual(position.y, 10.0, places=9)
        self.assertAlmostEqual(position.z, 15.0, places=9)

    def test_exact_sample_points(self) -> None:
        """At each sample time, interpolation returns the original Position exactly."""
        interpolator = Hermite3DPositionInterpolator(self.positions)

        for expected in self.positions:
            position = interpolator.get_interpolated_position(expected.at)
            self.assertEqual(position.at, expected.at)
            self.assertAlmostEqual(position.x, expected.x, places=9)
            self.assertAlmostEqual(position.y, expected.y, places=9)
            self.assertAlmostEqual(position.z, expected.z, places=9)

    def test_midpoint_between_first_two(self) -> None:
        """
        Interpolation at t=30 (between the 1st and 2nd positions) lies within their
        value range.
        """
        interpolator = Hermite3DPositionInterpolator(self.positions)

        # Define time at the midpoint between the first two positions:
        at: float = 30.0
        actual = interpolator.get_interpolated_position(at)
        a, b = self.positions[0], self.positions[1]

        self.assertTrue(min(a.x, b.x) <= actual.x <= max(a.x, b.x))
        self.assertTrue(min(a.y, b.y) <= actual.y <= max(a.y, b.y))
        self.assertTrue(min(a.z, b.z) <= actual.z <= max(a.z, b.z))
        self.assertEqual(actual.at, at)

    def test_arbitrary_midpoint_within_bounds(self) -> None:
        """
        Interpolation at t=150 (between the 3rd and 4th positions) lies within their
        value range.
        """
        interpolator = Hermite3DPositionInterpolator(self.positions)

        # Define time between positions[2] (120) and positions[3] (180):
        at: float = 150.0
        actual = interpolator.get_interpolated_position(at)
        a, b = self.positions[2], self.positions[3]

        self.assertTrue(min(a.x, b.x) <= actual.x <= max(a.x, b.x))
        self.assertTrue(min(a.y, b.y) <= actual.y <= max(a.y, b.y))
        self.assertTrue(min(a.z, b.z) <= actual.z <= max(a.z, b.z))
        self.assertEqual(actual.at, at)

    def test_out_of_bounds_behavior(self) -> None:
        """
        Querying before the first sample or after the last should still return a
        Position with 'at' set to the query time, and at least one coordinate finite.
        """
        interpolator = Hermite3DPositionInterpolator(self.positions)

        with self.assertRaises(ValueError):
            interpolator.get_interpolated_position(-60.0)

        with self.assertRaises(ValueError):
            interpolator.get_interpolated_position(600.0)

    def test_interpolation_at_specific_epoch_timestamps(self) -> None:
        """
        Test interpolation at a specific epoch timestamp, ensuring the result is
        within the expected range of the surrounding positions.
        """
        positions: List[Position] = [
            Position(
                x=-184511.6953189489,
                y=6847746.881617692,
                z=11099.5448507028,
                at=1723510800.0,
            ),
            Position(
                x=-553320.796092768,
                y=6776094.229947866,
                z=844998.042655855,
                at=1723510920.0,
            ),
            Position(
                x=-912267.9542356991,
                y=6583665.700405683,
                z=1663836.2291468324,
                at=1723511040.0,
            ),
            Position(
                x=-1254960.3162454353,
                y=6273926.881670678,
                z=2453028.318304866,
                at=1723511160.0,
            ),
            Position(
                x=-1575298.1845573059,
                y=5852429.458345277,
                z=3198524.9389684894,
                at=1723511280.0,
            ),
            Position(
                x=-1867583.0047119157,
                y=5326710.190080691,
                z=3887062.0219569616,
                at=1723511400.0,
            ),
            Position(
                x=-2126618.020929868,
                y=4706155.043456231,
                z=4506395.249857609,
                at=1723511520.0,
            ),
            Position(
                x=-2347799.873225814,
                y=4001831.003033132,
                z=5045516.035678472,
                at=1723511640.0,
            ),
            Position(
                x=-2527199.5783852055,
                y=3226288.618034939,
                z=5494845.345910571,
                at=1723511760.0,
            ),
            Position(
                x=-2661631.52875502,
                y=2393338.8127440577,
                z=5846402.086805565,
                at=1723511880.0,
            ),
        ]

        interpolator = Hermite3DPositionInterpolator(positions)

        # Base epoch time (2024-08-13T01:00:00Z):
        base = 1723510800.0

        # 01:11:30 UTC corresponds to 11 minutes and 30 seconds after 01:00.
        # This is calculated as (11 * 60 + 30) = 690 seconds:
        at = base + 690.0
        actual = interpolator.get_interpolated_position(at)

        self.assertEqual(actual.at, at)
        self.assertAlmostEqual(actual.x, -2065238.4030487437, places=9)
        self.assertAlmostEqual(actual.y, 4869603.41999027, places=9)
        self.assertAlmostEqual(actual.z, 4358673.416049888, places=9)

        # Interpolate at 01:03:45 UTC (3 minutes 45 seconds after 01:00 → 225 seconds):
        at = base + 225.0
        actual = interpolator.get_interpolated_position(at)

        self.assertEqual(actual.at, at)
        self.assertAlmostEqual(actual.x, -868159.7281853468, places=9)
        self.assertAlmostEqual(actual.y, 6614222.38183977, places=9)
        self.assertAlmostEqual(actual.z, 1562807.8822666958, places=9)

        # Interpolate at 01:07:00 UTC (7 minutes after 01:00 → 420 seconds):
        at = base + 420.0
        actual = interpolator.get_interpolated_position(at)

        self.assertEqual(actual.at, at)
        self.assertAlmostEqual(actual.x, -1418289.1274109124, places=9)
        self.assertAlmostEqual(actual.y, 6076716.888540836, places=9)
        self.assertAlmostEqual(actual.z, 2832086.369165492, places=9)

        # Interpolate at 01:15:30 UTC (15 minutes 30 seconds after 01:00 → 930 seconds):
        at = base + 930.0
        actual = interpolator.get_interpolated_position(at)

        self.assertEqual(actual.at, at)
        self.assertAlmostEqual(actual.x, -2486443.8451187215, places=9)
        self.assertAlmostEqual(actual.y, 3426100.572506782, places=9)
        self.assertAlmostEqual(actual.z, 5391373.677205545, places=9)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
