# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import isclose, sqrt

from satelles import (
    EARTH_MASS,
    EARTH_MEAN_RADIUS,
    GRAVITATIONAL_CONSTANT,
    CartesianCoordinate,
    get_gravitational_acceleration,
)
from satelles.common import Acceleration

# **************************************************************************************


class TestGravitationalAcceleration(unittest.TestCase):
    def setUp(self) -> None:
        # Compute Earth's gravitational parameter in SI units.
        self.mu = EARTH_MASS * GRAVITATIONAL_CONSTANT  # ~3.986004418e14 m^3/s^2

    def test_on_unit_vector(self) -> None:
        # Test a simple case: r = (1,0,0).
        # Expected acceleration: a = -μ * (1,0,0) because |r|=1 so r^3=1.
        r: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        acceleration: Acceleration = get_gravitational_acceleration(r, μ=self.mu)
        self.assertTrue(isclose(acceleration["ax"], -self.mu, rel_tol=1e-9))
        self.assertTrue(isclose(acceleration["ay"], 0.0, abs_tol=1e-12))
        self.assertTrue(isclose(acceleration["az"], 0.0, abs_tol=1e-12))

    def test_on_earth_surface(self) -> None:
        r: CartesianCoordinate = {"x": EARTH_MEAN_RADIUS, "y": 0.0, "z": 0.0}
        acceleration: Acceleration = get_gravitational_acceleration(r, μ=self.mu)
        # Compute magnitude of the acceleration vector:
        acceleration_magnitude = sqrt(
            acceleration["ax"] ** 2 + acceleration["ay"] ** 2 + acceleration["az"] ** 2
        )
        # Expected acceleration = μ / r^2.
        expected_acceleration = self.mu / (EARTH_MEAN_RADIUS**2)
        self.assertTrue(
            isclose(acceleration_magnitude, expected_acceleration, rel_tol=1e-5)
        )
        # The acceleration should point in the negative x-direction:
        self.assertTrue(acceleration["ax"] < 0)
        self.assertAlmostEqual(acceleration["ay"], 0.0, places=9)
        self.assertAlmostEqual(acceleration["az"], 0.0, places=9)

    def test_zero_vector(self) -> None:
        # Test that passing a zero vector raises a ValueError.
        r: CartesianCoordinate = {"x": 0.0, "y": 0.0, "z": 0.0}
        with self.assertRaises(ValueError):
            get_gravitational_acceleration(r, μ=self.mu)

    def test_random_vector(self) -> None:
        # Test with a nontrivial vector.
        r: CartesianCoordinate = {"x": 7000e3, "y": 8000e3, "z": 9000e3}  # in meters
        acceleration: Acceleration = get_gravitational_acceleration(r, μ=self.mu)
        r_magnitude = sqrt(r["x"] ** 2 + r["y"] ** 2 + r["z"] ** 2)
        expected_factor = -self.mu / (r_magnitude**3)
        self.assertAlmostEqual(acceleration["ax"], expected_factor * r["x"], places=9)
        self.assertAlmostEqual(acceleration["ay"], expected_factor * r["y"], places=9)
        self.assertAlmostEqual(acceleration["az"], expected_factor * r["z"], places=9)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
