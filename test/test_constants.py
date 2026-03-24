# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles import G, GRAVITATIONAL_CONSTANT, SPEED_OF_LIGHT, c

# **************************************************************************************


class TestConstants(unittest.TestCase):
    def test_gravitational_constant(self) -> None:
        self.assertEqual(GRAVITATIONAL_CONSTANT, 6.67430e-11)

    def test_gravitational_constant_alias(self) -> None:
        self.assertEqual(G, GRAVITATIONAL_CONSTANT)

    def test_speed_of_light(self) -> None:
        self.assertEqual(SPEED_OF_LIGHT, 299792458.0)

    def test_speed_of_light_alias(self) -> None:
        self.assertEqual(c, SPEED_OF_LIGHT)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
