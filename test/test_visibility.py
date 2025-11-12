# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime

from celerity.coordinates import GeographicCoordinate

from satelles.tle import TLE
from satelles.visibility import is_visible

# **************************************************************************************

# GPS-26 NORAD ID 40534
GPS_26_TLE = """
0 NAVSTAR 73 (USA 260)
1 40534U 15013A   22124.84670919 -.00000014  00000-0  00000-0 0  9997
2 40534  53.7322 266.5007 0068550  20.6560 339.5943  2.00555251 51657
"""

# **************************************************************************************

# GPS-25 NORAD ID 36585
GPS_25_TLE = """
0 NAVSTAR 65 (USA 213)
1 36585U 10022A   22124.99665188 -.00000013  00000-0  00000-0 0  9990
2 36585  54.8305 269.2708 0103481  56.7033 124.9904  2.00563155 87426
"""

# **************************************************************************************


class TestIsVisible(unittest.TestCase):
    def setUp(self) -> None:
        # Set the observer to be in San Francisco, CA, USA:
        self.observer: GeographicCoordinate = GeographicCoordinate(
            latitude=37.7749,
            longitude=-122.4194,
            elevation=0.0,
        )

    def test_gps26_should_be_visible(self) -> None:
        """
        Test that GPS-26 is visible from San Francisco, CA, USA.
        """
        when = datetime(2021, 5, 15, 12, 0, 0)

        satellite = TLE(tle_string=GPS_26_TLE).as_satellite()

        # Check if the satellite is visible from the observer's location:
        visible = is_visible(
            when=when,
            satellite=satellite,
            observer=self.observer,
            horizon=0.0,
        )

        self.assertTrue(visible)

    def test_gps13_should_not_be_visible(self) -> None:
        """
        Test that GPS-13 is not visible from San Francisco, CA, USA.
        """
        when = datetime(2021, 5, 15, 12, 0, 0)

        satellite = TLE(tle_string=GPS_25_TLE).as_satellite()

        # Check if the satellite is visible from the observer's location:
        visible = is_visible(
            when=when,
            satellite=satellite,
            observer=self.observer,
            horizon=0.0,
        )

        self.assertFalse(visible)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
