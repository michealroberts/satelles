# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import time
import unittest
from datetime import datetime, timezone

from celerity.coordinates import GeographicCoordinate

from satelles.coordinates import convert_ecef_to_lla, convert_eci_to_ecef
from satelles.satellite import Satellite
from satelles.tle import TLE
from satelles.visibility import is_visible

from .utils import host_timezone

# **************************************************************************************

# GPS-26 NORAD ID 40534
GPS_26_TLE = """
0 NAVSTAR 73 (USA 260)
1 40534U 15013A   22124.84670919 -.00000014  00000-0  00000-0 0  9997
2 40534  53.7322 266.5007 0068550  20.6560 339.5943  2.00555251 51657
"""

# **************************************************************************************

# ISS (ZARYA) NORAD ID 25544, with an epoch of 2008-09-20 12:25:40 UTC:
ISS_TLE = """
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
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
        Test that GPS-26 is visible from San Francisco, CA, USA (the reference SGP4
        implementation places it at an altitude of +32.3° at this time).
        """
        when = datetime(2022, 5, 5, 10, 30, 0, tzinfo=timezone.utc)

        satellite = TLE(tle_string=GPS_26_TLE).as_satellite()

        # Check if the satellite is visible from the observer's location:
        visible = is_visible(
            when=when,
            satellite=satellite,
            observer=self.observer,
            horizon=0.0,
        )

        self.assertTrue(visible)

    def test_gps25_should_not_be_visible(self) -> None:
        """
        Test that GPS-25 is not visible from San Francisco, CA, USA (the reference SGP4
        implementation places it at an altitude of -32.0° at this time).
        """
        when = datetime(2022, 5, 5, 10, 30, 0, tzinfo=timezone.utc)

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


class TestIsVisibleTopocentric(unittest.TestCase):
    """
    The ISS orbits at ~350 km, so it is above an observer's horizon only within a
    central angle of acos(R / (R + h)) ≈ 18.5° of the point directly beneath it.
    """

    def setUp(self) -> None:
        self.when = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

        satellite = self.get_satellite()

        satellite.at(when=self.when)

        ecef = convert_eci_to_ecef(eci=satellite.eci_coordinate, when=self.when)

        # The sub-satellite point (directly beneath the ISS) at this time:
        self.subpoint = convert_ecef_to_lla(ecef)

    def get_satellite(self) -> Satellite:
        return TLE(tle_string=ISS_TLE).as_satellite()

    def get_observer(self, offset: float) -> GeographicCoordinate:
        """
        Get an observer offset from the sub-satellite point along its meridian (in
        degrees), moving towards the equator.
        """
        latitude = self.subpoint["latitude"]

        return GeographicCoordinate(
            latitude=latitude - offset if latitude >= 0 else latitude + offset,
            longitude=self.subpoint["longitude"],
            elevation=0.0,
        )

    def test_visible_directly_beneath_satellite(self) -> None:
        # A horizon of 30° or more is allowed, but warns:
        with self.assertWarns(UserWarning):
            visible = is_visible(
                when=self.when,
                satellite=self.get_satellite(),
                observer=self.get_observer(offset=0.0),
                horizon=80.0,
            )

        self.assertTrue(visible)

    def test_visible_inside_horizon_circle(self) -> None:
        self.assertTrue(
            is_visible(
                when=self.when,
                satellite=self.get_satellite(),
                observer=self.get_observer(offset=10.0),
                horizon=0.0,
            )
        )

    def test_not_visible_outside_horizon_circle(self) -> None:
        # The geocentric direction to the ISS is ~30° above this observer's horizon,
        # but the ISS itself is well below it (i.e., parallax must be accounted for):
        self.assertFalse(
            is_visible(
                when=self.when,
                satellite=self.get_satellite(),
                observer=self.get_observer(offset=60.0),
                horizon=0.0,
            )
        )

    def test_does_not_mutate_satellite(self) -> None:
        satellite = self.get_satellite()

        is_visible(
            when=self.when,
            satellite=satellite,
            observer=self.get_observer(offset=0.0),
            horizon=0.0,
        )

        # The caller's satellite should not have had its time set by is_visible:
        with self.assertRaises(ValueError):
            satellite.eci_coordinate

    @unittest.skipUnless(hasattr(time, "tzset"), "requires time.tzset (POSIX only)")
    def test_naive_datetime_treated_as_utc(self) -> None:
        with host_timezone("America/New_York"), self.assertWarns(UserWarning):
            visible = is_visible(
                when=self.when.replace(tzinfo=None),
                satellite=self.get_satellite(),
                observer=self.get_observer(offset=0.0),
                horizon=80.0,
            )

        self.assertTrue(visible)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
