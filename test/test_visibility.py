# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import time
import unittest
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from celerity.coordinates import GeographicCoordinate

from satelles.coordinates import convert_ecef_to_lla, convert_eci_to_ecef
from satelles.satellite import Satellite
from satelles.tle import TLE
from satelles.visibility import is_illuminated, is_visible

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


class TestIsIlluminated(unittest.TestCase):
    # Expected states from an independent ERFA reference (two-body ISS position, ERFA
    # Sun on the equator of date, cylinder rule), each over 1,000 km from the boundary:

    def get_satellite(self) -> Satellite:
        return TLE(tle_string=ISS_TLE).as_satellite()

    def test_sunlit_before_eclipse(self) -> None:
        # The ERFA reference places the ISS 2,718 km sunward of the terminator plane:
        when = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

        self.assertTrue(is_illuminated(when=when, satellite=self.get_satellite()))

    def test_in_shadow_mid_eclipse(self) -> None:
        # The ERFA reference places the ISS on the anti-Sun side, 5,048 km from the
        # Sun–Earth line, i.e., 1,330 km inside the shadow cylinder:
        when = datetime(2008, 9, 20, 12, 30, 0, tzinfo=timezone.utc)

        self.assertFalse(is_illuminated(when=when, satellite=self.get_satellite()))

    def test_sunlit_on_day_side(self) -> None:
        # The ERFA reference places the ISS 4,475 km sunward of the terminator plane:
        when = datetime(2008, 9, 20, 13, 20, 0, tzinfo=timezone.utc)

        self.assertTrue(is_illuminated(when=when, satellite=self.get_satellite()))

    def test_in_shadow_next_orbit(self) -> None:
        # The ERFA reference places the ISS on the anti-Sun side, 5,003 km from the
        # Sun–Earth line, i.e., 1,375 km inside the shadow cylinder:
        when = datetime(2008, 9, 20, 14, 5, 0, tzinfo=timezone.utc)

        self.assertFalse(is_illuminated(when=when, satellite=self.get_satellite()))

    def test_aware_datetime_converted_to_utc(self) -> None:
        # 08:30 in UTC-4 is 12:30 UTC, mid-eclipse:
        when = datetime(2008, 9, 20, 8, 30, 0, tzinfo=timezone(timedelta(hours=-4)))

        self.assertFalse(is_illuminated(when=when, satellite=self.get_satellite()))

    def test_does_not_mutate_satellite(self) -> None:
        satellite = self.get_satellite()

        is_illuminated(
            when=datetime(2008, 9, 20, 12, 30, 0, tzinfo=timezone.utc),
            satellite=satellite,
        )

        # The caller's satellite should not have had its time set by is_illuminated:
        with self.assertRaises(ValueError):
            satellite.eci_coordinate

    @unittest.skipUnless(hasattr(time, "tzset"), "requires time.tzset (POSIX only)")
    def test_naive_datetime_treated_as_utc(self) -> None:
        when = datetime(2008, 9, 20, 12, 30, 0, tzinfo=timezone.utc)

        # Read as New York local time (UTC-4), 12:30 would be 16:30 UTC, when the ERFA
        # reference places the ISS 3,750 km sunward of the terminator plane:
        with host_timezone("America/New_York"):
            illuminated = is_illuminated(
                when=when.replace(tzinfo=None),
                satellite=self.get_satellite(),
            )

        self.assertFalse(illuminated)

        self.assertEqual(
            illuminated,
            is_illuminated(when=when, satellite=self.get_satellite()),
        )


# **************************************************************************************


class TestIsIlluminatedEclipseCrossing(unittest.TestCase):
    # ERFA reference: one shadow interval, 12:16:40.948–12:47:59.487 UTC (1,878.539 s).
    # A 1 s tolerance catches a Sun in the J2000.0 frame (~3 s at exit in 2008):

    start = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

    # The sampling step, and the time span of one ISS orbit (1 / 15.72125391 days):
    step = timedelta(seconds=10)

    period = timedelta(days=1 / 15.72125391)

    @classmethod
    def setUpClass(cls) -> None:
        cls.satellite = TLE(tle_string=ISS_TLE).as_satellite()

        cls.transitions = cls.get_transitions()

    @classmethod
    def get_illuminated(cls, when: datetime) -> bool:
        return is_illuminated(when=when, satellite=cls.satellite)

    @classmethod
    def get_crossing(cls, before: datetime, after: datetime) -> datetime:
        # Bisect the instant the illumination state changes (to within 1 ms):
        state = cls.get_illuminated(before)

        while after - before > timedelta(milliseconds=1):
            midpoint = before + (after - before) / 2

            if cls.get_illuminated(midpoint) == state:
                before = midpoint
            else:
                after = midpoint

        return before + (after - before) / 2

    @classmethod
    def get_transitions(cls) -> List[Tuple[datetime, bool]]:
        # Each (instant, illuminated after the instant) state change over one orbit:
        transitions: List[Tuple[datetime, bool]] = []

        when = cls.start

        state = cls.get_illuminated(when)

        while when < cls.start + cls.period:
            after = when + cls.step

            illuminated = cls.get_illuminated(after)

            if illuminated != state:
                transitions.append((cls.get_crossing(when, after), illuminated))

            state = illuminated

            when = after

        return transitions

    def test_single_contiguous_shadow_interval(self) -> None:
        # One shadow entry followed by one shadow exit:
        self.assertEqual(len(self.transitions), 2)
        self.assertFalse(self.transitions[0][1])
        self.assertTrue(self.transitions[1][1])

    def test_shadow_entry_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.transitions[0][0],
            datetime(2008, 9, 20, 12, 16, 40, 948000, tzinfo=timezone.utc),
            delta=timedelta(seconds=1),
        )

    def test_shadow_exit_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.transitions[1][0],
            datetime(2008, 9, 20, 12, 47, 59, 487000, tzinfo=timezone.utc),
            delta=timedelta(seconds=1),
        )

    def test_shadow_duration_is_plausible_for_iss(self) -> None:
        duration = self.transitions[1][0] - self.transitions[0][0]

        self.assertGreater(duration, timedelta(minutes=30))
        self.assertLess(duration, timedelta(minutes=40))

        self.assertAlmostEqual(
            duration.total_seconds(),
            1878.539,
            delta=1.0,
        )


# **************************************************************************************


def get_shadow_transitions(
    satellite: Satellite,
    start: datetime,
    span: timedelta,
    step: timedelta = timedelta(seconds=10),
) -> List[Tuple[datetime, bool]]:
    # Each (instant, illuminated after the instant) state change over the span, sampled
    # every step and bisected to within 1 ms:
    def get_illuminated(when: datetime) -> bool:
        return is_illuminated(when=when, satellite=satellite)

    transitions: List[Tuple[datetime, bool]] = []

    when = start

    state = get_illuminated(when)

    while when < start + span:
        after = when + step

        illuminated = get_illuminated(after)

        if illuminated != state:
            before, until = when, after

            while until - before > timedelta(milliseconds=1):
                midpoint = before + (until - before) / 2

                if get_illuminated(midpoint) == state:
                    before = midpoint
                else:
                    until = midpoint

            transitions.append((before + (until - before) / 2, illuminated))

        state = illuminated

        when = after

    return transitions


# **************************************************************************************


class TestIsIlluminatedReferenceFrame(unittest.TestCase):
    # The ISS elements relabelled EME2000 (or ICRF). ERFA reference in the J2000 frame:
    # 12:16:39.934–12:47:56.801 UTC (1,876.867 s). An unrotated position is off by
    # +1.06 s (entry) and +2.76 s (exit), so a 0.5 s tolerance catches it:

    start = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

    # The time span of one ISS orbit (1 / 15.72125391 days):
    period = timedelta(days=1 / 15.72125391)

    entry = datetime(2008, 9, 20, 12, 16, 39, 934000, tzinfo=timezone.utc)

    exit = datetime(2008, 9, 20, 12, 47, 56, 801000, tzinfo=timezone.utc)

    @classmethod
    def get_satellite(cls, reference_frame: Optional[str]) -> Satellite:
        # The long names are what the Satellite reference frame validator stores:
        return (
            TLE(tle_string=ISS_TLE)
            .as_satellite()
            .model_copy(update={"reference_frame": reference_frame})
        )

    @classmethod
    def setUpClass(cls) -> None:
        cls.eme2000 = get_shadow_transitions(
            satellite=cls.get_satellite("Epoch Mean Equinox 2000"),
            start=cls.start,
            span=cls.period,
        )

        cls.icrf = get_shadow_transitions(
            satellite=cls.get_satellite("International Celestial Reference Frame"),
            start=cls.start,
            span=cls.period,
        )

    def test_eme2000_single_contiguous_shadow_interval(self) -> None:
        self.assertEqual(len(self.eme2000), 2)
        self.assertFalse(self.eme2000[0][1])
        self.assertTrue(self.eme2000[1][1])

    def test_eme2000_shadow_entry_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.eme2000[0][0],
            self.entry,
            delta=timedelta(seconds=0.5),
        )

    def test_eme2000_shadow_exit_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.eme2000[1][0],
            self.exit,
            delta=timedelta(seconds=0.5),
        )

    def test_eme2000_shadow_duration_matches_reference(self) -> None:
        self.assertAlmostEqual(
            (self.eme2000[1][0] - self.eme2000[0][0]).total_seconds(),
            1876.867,
            delta=0.5,
        )

    def test_icrf_single_contiguous_shadow_interval(self) -> None:
        self.assertEqual(len(self.icrf), 2)
        self.assertFalse(self.icrf[0][1])
        self.assertTrue(self.icrf[1][1])

    def test_icrf_shadow_entry_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.icrf[0][0],
            self.entry,
            delta=timedelta(seconds=0.5),
        )

    def test_icrf_shadow_exit_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.icrf[1][0],
            self.exit,
            delta=timedelta(seconds=0.5),
        )

    def test_unspecified_reference_frame_raises(self) -> None:
        with self.assertRaises(ValueError):
            is_illuminated(
                when=datetime(2008, 9, 20, 12, 30, 0, tzinfo=timezone.utc),
                satellite=self.get_satellite(None),
            )


# **************************************************************************************

# Synthetic TLEs (not real objects, but with valid checksums) for circular orbits with
# an epoch at the geometric March equinox of 2026 (from ERFA, the instant the Sun's
# declination on the true equator of date is zero, so the Sun is at right ascension 0°
# on the equator). Each satellite is at right ascension 180°, i.e., directly opposite
# the Sun, at its epoch:
EQUINOX = datetime(2026, 3, 20, 14, 37, 22, 524672, tzinfo=timezone.utc)

# An equatorial low Earth orbit (15.5 rev/day, a = 6,794.863 km):
LEO_EQUATORIAL_TLE = """
TEST LEO EQUATORIAL
1 90001U 26001A   26079.60928848  .00000000  00000-0  00000-0 0  9998
2 90001   0.0000   0.0000 0000000   0.0000 180.0000 15.50000000    13
"""

# A polar low Earth orbit whose plane contains the Sun–Earth line ("noon–midnight"):
LEO_NOON_MIDNIGHT_TLE = """
TEST LEO NOON-MIDNIGHT
1 90002U 26001A   26079.60928848  .00000000  00000-0  00000-0 0  9999
2 90002  90.0000   0.0000 0000000   0.0000 180.0000 15.50000000    13
"""

# A polar low Earth orbit whose plane is perpendicular to the Sun–Earth line
# ("dawn–dusk"):
LEO_DAWN_DUSK_TLE = """
TEST LEO DAWN-DUSK
1 90003U 26001A   26079.60928848  .00000000  00000-0  00000-0 0  9990
2 90003  90.0000  90.0000 0000000   0.0000 180.0000 15.50000000    13
"""

# A geostationary orbit (1.00273791 rev/day, a = 42,164.168 km):
GEO_EQUINOX_TLE = """
TEST GEO EQUINOX
1 90004U 26001A   26079.60928848  .00000000  00000-0  00000-0 0  9991
2 90004   0.0000   0.0000 0000000   0.0000 180.0000  1.00273791    15
"""

# A geostationary orbit with an epoch at the June solstice of 2026 (2026-06-21 08:00
# UTC, when the Sun's declination is 23.44°):
GEO_SOLSTICE_TLE = """
TEST GEO SOLSTICE
1 90005U 26001A   26172.33333333  .00000000  00000-0  00000-0 0  9995
2 90005   0.0000   0.0000 0000000   0.0000 180.0000  1.00273791    16
"""

# **************************************************************************************


class TestIsIlluminatedEquinoxGeometry(unittest.TestCase):
    # Closed form, no ephemeris. With the orbit plane containing the Sun–Earth line, the
    # shadow lasts 2·asin(R / a) / (n − ω), centred when the satellite is opposite the
    # Sun, where ω is the Sun's in-plane rate (λ̇·cos ε equatorial, λ̇·sin ε polar, with
    # λ̇ ≈ 0.9940°/day and ε = 23.4362°). Dawn–dusk (~417 km clear) and GEO at the
    # solstice (~10,393 km clear) are never in shadow. Tolerances are ~3× (LEO, 0.5 s)
    # and ~2× (GEO, 5 s) the effect of the 0.01° solar theory accuracy:

    # The time span of one LEO orbit (1 / 15.5 days):
    leo = timedelta(days=1 / 15.5)

    # The time span of one GEO orbit (1 / 1.00273791 days, i.e., one sidereal day):
    geo = timedelta(days=1 / 1.00273791)

    @classmethod
    def get_transitions(
        cls,
        tle: str,
        start: datetime,
        span: timedelta,
        step: timedelta = timedelta(seconds=10),
    ) -> List[Tuple[datetime, bool]]:
        return get_shadow_transitions(
            satellite=TLE(tle_string=tle).as_satellite(),
            start=start,
            span=span,
            step=step,
        )

    @classmethod
    def setUpClass(cls) -> None:
        # Sample one orbit centred on the epoch, when each satellite opposes the Sun:
        cls.leo_equatorial = cls.get_transitions(
            tle=LEO_EQUATORIAL_TLE,
            start=EQUINOX - cls.leo / 2,
            span=cls.leo,
        )

        cls.leo_noon_midnight = cls.get_transitions(
            tle=LEO_NOON_MIDNIGHT_TLE,
            start=EQUINOX - cls.leo / 2,
            span=cls.leo,
        )

        cls.leo_dawn_dusk = cls.get_transitions(
            tle=LEO_DAWN_DUSK_TLE,
            start=EQUINOX - cls.leo / 2,
            span=cls.leo,
        )

        cls.geo_equinox = cls.get_transitions(
            tle=GEO_EQUINOX_TLE,
            start=EQUINOX - cls.geo / 2,
            span=cls.geo,
            step=timedelta(seconds=60),
        )

        cls.geo_solstice = cls.get_transitions(
            tle=GEO_SOLSTICE_TLE,
            start=datetime(2026, 6, 21, 8, 0, 0, tzinfo=timezone.utc) - cls.geo / 2,
            span=cls.geo,
            step=timedelta(seconds=60),
        )

    def get_interval(
        self, transitions: List[Tuple[datetime, bool]]
    ) -> Tuple[datetime, datetime]:
        # The (entry, exit) of the single, contiguous shadow interval:
        self.assertEqual(len(transitions), 2)
        self.assertFalse(transitions[0][1])
        self.assertTrue(transitions[1][1])

        return transitions[0][0], transitions[1][0]

    def test_leo_equatorial_shadow_duration_matches_closed_form(self) -> None:
        entry, exit = self.get_interval(self.leo_equatorial)

        self.assertAlmostEqual((exit - entry).total_seconds(), 2162.814, delta=0.5)

    def test_leo_equatorial_shadow_is_centred_opposite_sun(self) -> None:
        entry, exit = self.get_interval(self.leo_equatorial)

        self.assertAlmostEqual(
            entry + (exit - entry) / 2,
            EQUINOX,
            delta=timedelta(seconds=0.5),
        )

    def test_leo_noon_midnight_shadow_duration_matches_closed_form(self) -> None:
        entry, exit = self.get_interval(self.leo_noon_midnight)

        self.assertAlmostEqual((exit - entry).total_seconds(), 2162.614, delta=0.5)

    def test_leo_noon_midnight_shadow_is_centred_opposite_sun(self) -> None:
        entry, exit = self.get_interval(self.leo_noon_midnight)

        self.assertAlmostEqual(
            entry + (exit - entry) / 2,
            EQUINOX,
            delta=timedelta(seconds=0.5),
        )

    def test_leo_dawn_dusk_is_never_in_shadow(self) -> None:
        self.assertEqual(self.leo_dawn_dusk, [])

        self.assertTrue(
            is_illuminated(
                when=EQUINOX,
                satellite=TLE(tle_string=LEO_DAWN_DUSK_TLE).as_satellite(),
            )
        )

    def test_geo_equinox_shadow_duration_matches_closed_form(self) -> None:
        entry, exit = self.get_interval(self.geo_equinox)

        self.assertAlmostEqual((exit - entry).total_seconds(), 4175.376, delta=5.0)

    def test_geo_equinox_shadow_is_centred_opposite_sun(self) -> None:
        entry, exit = self.get_interval(self.geo_equinox)

        self.assertAlmostEqual(
            entry + (exit - entry) / 2,
            EQUINOX,
            delta=timedelta(seconds=5),
        )

    def test_geo_solstice_is_never_in_shadow(self) -> None:
        self.assertEqual(self.geo_solstice, [])

        self.assertTrue(
            is_illuminated(
                when=datetime(2026, 6, 21, 8, 0, 0, tzinfo=timezone.utc),
                satellite=TLE(tle_string=GEO_SOLSTICE_TLE).as_satellite(),
            )
        )


# **************************************************************************************


class TestIsIlluminatedGeostationaryReferenceFrame(unittest.TestCase):
    # GEO magnifies frame offsets (1″ ≈ 0.067 s). As EME2000, the orbit is rotated by
    # precession (ζ + z ≈ 0.3359°), so its shadow comes ~80.60 s earlier (ERFA: 80.557
    # s). Absolute tolerance 5 s (~2× the solar theory effect); the Sun's error is
    # common to both, so the difference is checked to 1 s:

    start = EQUINOX - timedelta(days=1 / 1.00273791) / 2

    span = timedelta(days=1 / 1.00273791)

    @classmethod
    def setUpClass(cls) -> None:
        satellite = TLE(tle_string=GEO_EQUINOX_TLE).as_satellite()

        cls.teme = get_shadow_transitions(
            satellite=satellite,
            start=cls.start,
            span=cls.span,
            step=timedelta(seconds=60),
        )

        cls.eme2000 = get_shadow_transitions(
            satellite=satellite.model_copy(
                update={"reference_frame": "Epoch Mean Equinox 2000"}
            ),
            start=cls.start,
            span=cls.span,
            step=timedelta(seconds=60),
        )

    def test_teme_single_contiguous_shadow_interval(self) -> None:
        self.assertEqual([state for _, state in self.teme], [False, True])

    def test_eme2000_single_contiguous_shadow_interval(self) -> None:
        self.assertEqual([state for _, state in self.eme2000], [False, True])

    def test_teme_shadow_entry_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.teme[0][0],
            datetime(2026, 3, 20, 14, 2, 34, 403000, tzinfo=timezone.utc),
            delta=timedelta(seconds=5),
        )

    def test_teme_shadow_exit_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.teme[1][0],
            datetime(2026, 3, 20, 15, 12, 9, 777000, tzinfo=timezone.utc),
            delta=timedelta(seconds=5),
        )

    def test_eme2000_shadow_entry_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.eme2000[0][0],
            datetime(2026, 3, 20, 14, 1, 14, 141000, tzinfo=timezone.utc),
            delta=timedelta(seconds=5),
        )

    def test_eme2000_shadow_exit_matches_reference(self) -> None:
        self.assertAlmostEqual(
            self.eme2000[1][0],
            datetime(2026, 3, 20, 15, 10, 48, 924000, tzinfo=timezone.utc),
            delta=timedelta(seconds=5),
        )

    def test_eme2000_shadow_is_earlier_by_precession(self) -> None:
        teme = self.teme[0][0] + (self.teme[1][0] - self.teme[0][0]) / 2

        eme2000 = self.eme2000[0][0] + (self.eme2000[1][0] - self.eme2000[0][0]) / 2

        self.assertAlmostEqual(
            (eme2000 - teme).total_seconds(),
            -80.557,
            delta=1.0,
        )


# **************************************************************************************

# Synthetic TLEs (not real objects, but with valid checksums) with the ISS elements of
# ISS_TLE, but with epochs at 12:00 UTC on dates spanning 35 years:
ISS_LIKE_2000_TLE = """
TEST ISS-LIKE 2000
1 90010U 26001A   00080.50000000  .00000000  00000-0  00000-0 0  9992
2 90010  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391    16
"""

ISS_LIKE_2015_TLE = """
TEST ISS-LIKE 2015
1 90010U 26001A   15172.50000000  .00000000  00000-0  00000-0 0  9990
2 90010  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391    16
"""

ISS_LIKE_2026_TLE = """
TEST ISS-LIKE 2026
1 90010U 26001A   26312.50000000  .00000000  00000-0  00000-0 0  9998
2 90010  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391    16
"""

ISS_LIKE_2035_TLE = """
TEST ISS-LIKE 2035
1 90010U 26001A   35266.50000000  .00000000  00000-0  00000-0 0  9996
2 90010  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391    16
"""

# **************************************************************************************


class TestIsIlluminatedAcrossEpochs(unittest.TestCase):
    # ERFA reference transitions (TEME frame) over one orbit from each epoch, to 0.5 s.
    # A Sun not on the equinox of date agrees in 2000 but is seconds off by 2026/2035:

    period = timedelta(days=1 / 15.72125391)

    def assertTransitionsMatchReference(
        self,
        tle: str,
        start: datetime,
        expected: List[Tuple[datetime, bool]],
    ) -> None:
        transitions = get_shadow_transitions(
            satellite=TLE(tle_string=tle).as_satellite(),
            start=start,
            span=self.period,
        )

        self.assertEqual(
            [state for _, state in transitions],
            [state for _, state in expected],
        )

        for (actual, _), (reference, _) in zip(transitions, expected):
            self.assertAlmostEqual(actual, reference, delta=timedelta(seconds=0.5))

    def test_transitions_in_2000(self) -> None:
        self.assertTransitionsMatchReference(
            tle=ISS_LIKE_2000_TLE,
            start=datetime(2000, 3, 20, 12, 0, 0, tzinfo=timezone.utc),
            expected=[
                (datetime(2000, 3, 20, 12, 37, 7, 595000, tzinfo=timezone.utc), False),
                (datetime(2000, 3, 20, 13, 8, 55, 413000, tzinfo=timezone.utc), True),
            ],
        )

    def test_transitions_in_2015(self) -> None:
        self.assertTransitionsMatchReference(
            tle=ISS_LIKE_2015_TLE,
            start=datetime(2015, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
            expected=[
                (datetime(2015, 6, 21, 12, 48, 22, 205000, tzinfo=timezone.utc), False),
                (datetime(2015, 6, 21, 13, 22, 59, 644000, tzinfo=timezone.utc), True),
            ],
        )

    def test_transitions_in_2026(self) -> None:
        self.assertTransitionsMatchReference(
            tle=ISS_LIKE_2026_TLE,
            start=datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc),
            expected=[
                (datetime(2026, 11, 8, 12, 32, 28, 357000, tzinfo=timezone.utc), True),
                (datetime(2026, 11, 8, 13, 27, 51, 94000, tzinfo=timezone.utc), False),
            ],
        )

    def test_transitions_in_2035(self) -> None:
        self.assertTransitionsMatchReference(
            tle=ISS_LIKE_2035_TLE,
            start=datetime(2035, 9, 23, 12, 0, 0, tzinfo=timezone.utc),
            expected=[
                (datetime(2035, 9, 23, 12, 23, 10, 314000, tzinfo=timezone.utc), True),
                (datetime(2035, 9, 23, 13, 22, 56, 893000, tzinfo=timezone.utc), False),
            ],
        )


# **************************************************************************************


class TestIsIlluminatedFullDay(unittest.TestCase):
    # 24 hours (~16 orbits) of ISS shadow intervals vs the ERFA reference, to 0.5 s:

    start = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

    # The ERFA reference shadow entries and exits (in seconds from the start):
    offsets = [
        1000.948,
        2879.487,
        6497.220,
        8376.600,
        11993.492,
        13873.710,
        17489.763,
        19370.817,
        22986.033,
        24867.922,
        28482.303,
        30365.025,
        33978.571,
        35862.125,
        39474.839,
        41359.223,
        44971.106,
        46856.319,
        50467.372,
        52353.411,
        55963.638,
        57850.502,
        61459.903,
        63347.590,
        66956.167,
        68844.675,
        72452.430,
        74341.759,
        77948.692,
        79838.839,
        83444.954,
        85335.918,
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.transitions = get_shadow_transitions(
            satellite=TLE(tle_string=ISS_TLE).as_satellite(),
            start=cls.start,
            span=timedelta(days=1),
        )

    def test_sixteen_alternating_shadow_intervals(self) -> None:
        # Each shadow entry is followed by a shadow exit:
        self.assertEqual(
            [state for _, state in self.transitions],
            [False, True] * 16,
        )

    def test_transitions_match_reference(self) -> None:
        for (actual, _), offset in zip(self.transitions, self.offsets):
            self.assertAlmostEqual(
                (actual - self.start).total_seconds(),
                offset,
                delta=0.5,
            )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
