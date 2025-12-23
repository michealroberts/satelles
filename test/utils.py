# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest

from satelles.common import CartesianCoordinate

# **************************************************************************************


class SatellesTestCase(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self,
        expected: CartesianCoordinate,
        actual: CartesianCoordinate,
        places: int = 6,
    ) -> None:
        self.assertAlmostEqual(expected["x"], actual["x"], places=places)
        self.assertAlmostEqual(expected["y"], actual["y"], places=places)
        self.assertAlmostEqual(expected["z"], actual["z"], places=places)


# **************************************************************************************
