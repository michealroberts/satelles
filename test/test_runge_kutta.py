# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import isclose, sqrt

from satelles import (
    EARTH_MASS,
    GRAVITATIONAL_CONSTANT,
    CartesianCoordinate,
    RungeKuttaPropagationParameters,
    Velocity,
    propagate_rk4,
)

# **************************************************************************************

# For testing, compute Earth's gravitational parameter:
MU = EARTH_MASS * GRAVITATIONAL_CONSTANT

# **************************************************************************************


class TestPropagateRungeKutta4(unittest.TestCase):
    def setUp(self) -> None:
        # Define an initial state for testing:
        self.initial_position: CartesianCoordinate = {"x": 7000e3, "y": 0.0, "z": 0.0}
        self.initial_velocity: Velocity = {"vx": 0.0, "vy": 7.5e3, "vz": 0.0}
        self.params: RungeKuttaPropagationParameters = {
            "timestep": 10.0,
            "number_of_steps": 100,
        }

    def test_propagation_outputs(self) -> None:
        """
        Test that the propagation function returns the expected number of
        positions and velocities.
        """
        positions, velocities = propagate_rk4(
            self.initial_position, self.initial_velocity, self.params, μ=MU
        )

        # Check that we have as many positions and velocities as steps:
        self.assertEqual(len(positions), self.params["number_of_steps"])
        self.assertEqual(len(velocities), self.params["number_of_steps"])

        for position in positions:
            for key in ["x", "y", "z"]:
                self.assertIn(key, position)

        for velocity in velocities:
            for key in ["vx", "vy", "vz"]:
                self.assertIn(key, velocity)

    def test_zero_steps(self) -> None:
        """
        If number_of_steps is zero, expect empty lists.
        """
        params: RungeKuttaPropagationParameters = {
            "timestep": 10.0,
            "number_of_steps": 0,
        }
        positions, velocities = propagate_rk4(
            self.initial_position, self.initial_velocity, params, μ=MU
        )
        self.assertEqual(len(positions), 0)
        self.assertEqual(len(velocities), 0)

    def test_energy_conservation(self):
        """
        Over a small time interval, the energy should be nearly conserved.
        """

        def energy(r: CartesianCoordinate, v: Velocity) -> float:
            kinetic = 0.5 * (v["vx"] ** 2 + v["vy"] ** 2 + v["vz"] ** 2)
            magnitude = sqrt(r["x"] ** 2 + r["y"] ** 2 + r["z"] ** 2)
            potential = -MU / magnitude
            return kinetic + potential

        initial_energy = energy(self.initial_position, self.initial_velocity)

        positions, velocities = propagate_rk4(
            self.initial_position, self.initial_velocity, self.params, μ=MU
        )

        final_energy = energy(positions[-1], velocities[-1])

        self.assertTrue(
            isclose(initial_energy, final_energy, rel_tol=1e-3),
            msg=f"Initial energy {initial_energy} not close to final energy {final_energy}",
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
