# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************


import unittest

from satelles import (
    get_hohmann_transfer_eccentricity,
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
if __name__ == "__main__":
    unittest.main()


# **************************************************************************************
