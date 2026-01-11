# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************


import unittest

from satelles import (
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


if __name__ == "__main__":
    unittest.main()


# **************************************************************************************
