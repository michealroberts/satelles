# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles import G, GRAVITATIONAL_CONSTANT, SPEED_OF_LIGHT, c
from satelles.earth import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_FLATTENING_FACTOR,
    EARTH_MEAN_RADIUS,
    EARTH_POLAR_RADIUS,
)

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


class TestEarthConstants(unittest.TestCase):
    """
    The WGS-84 reference ellipsoid is defined by a = 6378137 m and 1/f = 298.257223563,
    as returned by ERFA's eform(1) (pyerfa 2.0.1.5): a = 6378137.0 m and
    f = 0.0033528106647474805. The polar radius is derived as b = a * (1 - f).
    """

    def test_earth_equatorial_radius_is_wgs84(self) -> None:
        self.assertEqual(EARTH_EQUATORIAL_RADIUS, 6378137.0)

    def test_earth_flattening_factor_is_wgs84(self) -> None:
        self.assertEqual(EARTH_FLATTENING_FACTOR, 0.0033528106647474805)

    def test_earth_inverse_flattening_is_wgs84(self) -> None:
        self.assertAlmostEqual(1 / EARTH_FLATTENING_FACTOR, 298.257223563, places=9)

    def test_earth_polar_radius_is_wgs84(self) -> None:
        self.assertAlmostEqual(EARTH_POLAR_RADIUS, 6356752.314245179, places=6)

    def test_earth_mean_radius_is_iugg_mean_radius(self) -> None:
        # The IUGG mean radius R1 = (2a + b) / 3 for the WGS-84 ellipsoid (in meters):
        self.assertAlmostEqual(EARTH_MEAN_RADIUS, 6371008.771415059, places=4)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
