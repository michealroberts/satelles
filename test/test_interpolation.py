# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import isfinite
from typing import List

from satelles import BarycentricLagrange3DPositionInterpolator
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

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
