# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone
from math import asin, atan2, cos, degrees, radians, sin, sqrt

from celerity.equinox import get_equation_of_the_equinoxes
from celerity.temporal import get_greenwich_sidereal_time, get_ut1_utc_offset
from celerity.utilities import get_normalised_azimuthal_degree

from satelles.coordinates import CartesianCoordinate
from satelles.coordinates import convert_ecef_to_eci, convert_eci_to_ecef
from satelles.earth import EARTH_EQUATORIAL_RADIUS
from satelles.matrix import (
    get_rotation_matrix_x,
    get_rotation_matrix_z,
    multiply,
)
from satelles.quaternion import Quaternion
from satelles.transforms import (
    ecef_to_eci_transform_provider,
    eci_to_ecef_transform_provider,
    eme2000_to_eci_transform_provider,
    identity_transform_provider,
    itrf_to_ecef_transform_provider,
    teme_to_eci_transform_provider,
)
from satelles.vector import distance

# **************************************************************************************

# Dates spanning a range of DUT1 (UT1 - UTC) values, including either side of the
# 2016-12-31 leap second, where |DUT1| is large (-0.41 s and +0.59 s respectively):
EARTH_ROTATION_DATES = [
    datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc),
    datetime(2016, 12, 31, 12, 0, 0, tzinfo=timezone.utc),
    datetime(2017, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
]

# **************************************************************************************

# Independent reference: Greenwich apparent sidereal time (in degrees) from ERFA's
# erfa.gst94 (IAU 1982 GMST plus the IAU 1994 equation of the equinoxes), evaluated
# with UT1 = UTC + DUT1, using the IERS finals (IAU 1980) DUT1 value for each date:
ERFA_GREENWICH_APPARENT_SIDEREAL_TIME = {
    # DUT1 = +0.0462673 s:
    datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc): 281.39265199871454,
    # DUT1 = +0.0289868 s:
    datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc): 249.73283467410334,
    # DUT1 = -0.4077601 s:
    datetime(2016, 12, 31, 12, 0, 0, tzinfo=timezone.utc): 280.3417719624665,
    # DUT1 = +0.5912821 s:
    datetime(2017, 1, 1, 12, 0, 0, tzinfo=timezone.utc): 281.3316049742515,
    # J2000.0 epoch, DUT1 = +0.3554779 s:
    datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc): 280.4585557120934,
    # After the 1998-12-31 leap second, DUT1 = +0.7166631 s:
    datetime(1999, 1, 1, 6, 0, 0, tzinfo=timezone.utc): 190.45343008015703,
    # Before the 2008-12-31 leap second, DUT1 = -0.5918692 s:
    datetime(2008, 12, 31, 18, 0, 0, tzinfo=timezone.utc): 10.53086454304202,
    # Before the 2015-06-30 leap second, DUT1 = -0.6760316 s:
    datetime(2015, 6, 30, 23, 0, 0, tzinfo=timezone.utc): 263.68850601665423,
    # Vallado, "Fundamentals of Astrodynamics and Applications", Example 3-15, with
    # DUT1 = -0.4399498 s:
    datetime(2004, 4, 6, 7, 51, 28, 386009, tzinfo=timezone.utc): 312.8067653918388,
}

# **************************************************************************************

# The equation of the equinoxes in celerity uses the abbreviated four-term nutation in
# longitude (Meeus, "Astronomical Algorithms", ch. 22), which is accurate to 0.5″; a
# missing DUT1 shifts the Earth-rotation angle by up to 0.9 s × 15.04″/s ≈ 13.5″:
ERFA_GREENWICH_APPARENT_SIDEREAL_TIME_TOLERANCE = 0.5 / 3600.0

# **************************************************************************************


def get_greenwich_apparent_sidereal_time(when: datetime) -> float:
    """
    Get the Greenwich apparent sidereal time (in degrees), applying DUT1 (UT1 - UTC)
    to the Greenwich mean sidereal time before adding the equation of the equinoxes.
    """
    dut1 = get_ut1_utc_offset(when)

    GMST = get_greenwich_sidereal_time(date=when, dut1=dut1) * 15.0

    return GMST + get_equation_of_the_equinoxes(date=when)


# **************************************************************************************


class TestIdentityTransformProvider(unittest.TestCase):
    def test_returns_identity_rotation(self) -> None:
        """
        Test that the transform has an identity quaternion rotation.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = identity_transform_provider(when)

        expected_rotation = Quaternion.identity()
        self.assertEqual(transform.rotation.w, expected_rotation.w)
        self.assertEqual(transform.rotation.x, expected_rotation.x)
        self.assertEqual(transform.rotation.y, expected_rotation.y)
        self.assertEqual(transform.rotation.z, expected_rotation.z)

    def test_returns_zero_translation(self) -> None:
        """
        Test that the transform has zero translation.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = identity_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)

    def test_datetime_invariant(self) -> None:
        """
        Test that the function returns the same transform regardless of time.
        """
        when = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = identity_transform_provider(when)

        self.assertEqual(transform.rotation.w, 1.0)
        self.assertEqual(transform.rotation.x, 0.0)
        self.assertEqual(transform.rotation.y, 0.0)
        self.assertEqual(transform.rotation.z, 0.0)

    def test_accepts_none_parameter(self):
        """
        Test that the function works with None as the datetime parameter.
        """
        transform = identity_transform_provider(None)

        self.assertIsNotNone(transform)
        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)

    def test_identity_transform_preserves_vectors(self) -> None:
        """
        Test that applying the identity transform preserves vectors.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        transform = identity_transform_provider(when)
        position = CartesianCoordinate(x=100.0, y=200.0, z=300.0)

        result = transform.apply_to_position(position)
        self.assertEqual(result["x"], position["x"])
        self.assertEqual(result["y"], position["y"])
        self.assertEqual(result["z"], position["z"])

    def test_identity_transform_inverse_is_identity(self) -> None:
        """
        Test that the inverse of an identity transform is also identity.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        transform = identity_transform_provider(when)

        inverse = transform.inverse()

        self.assertEqual(inverse.rotation.w, 1.0)
        self.assertEqual(inverse.rotation.x, 0.0)
        self.assertEqual(inverse.rotation.y, 0.0)
        self.assertEqual(inverse.rotation.z, 0.0)
        self.assertEqual(inverse.translation["x"], 0.0)
        self.assertEqual(inverse.translation["y"], 0.0)
        self.assertEqual(inverse.translation["z"], 0.0)


# **************************************************************************************


class TestECEFToECITransformProvider(unittest.TestCase):
    def test_ecef_to_eci_rotates_z_axis_only(self) -> None:
        """
        Test that the transform has a rotation about the Z-axis only.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.7737996205180773,
            x=0.0,
            y=0.0,
            z=0.6334304597081512,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.5716645816865767,
            x=0.0,
            y=0.0,
            z=0.8204874197969834,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

    def test_ecef_to_eci_rotation_angle_is_apparent_sidereal_time(self) -> None:
        """
        Test that the ECEF to ECI rotation angle about the Z-axis is the Greenwich
        apparent sidereal time, with DUT1 (UT1 - UTC) applied to the mean sidereal time.
        """
        for when in EARTH_ROTATION_DATES:
            with self.subTest(when=when):
                transform = ecef_to_eci_transform_provider(when)

                # Rotate the X-axis to measure the rotation angle about the Z-axis:
                r = transform.rotation.rotate_vector(
                    CartesianCoordinate(x=1.0, y=0.0, z=0.0)
                )

                angle = degrees(atan2(r["y"], r["x"]))

                GAST = get_greenwich_apparent_sidereal_time(when)

                self.assertAlmostEqual(
                    get_normalised_azimuthal_degree(angle),
                    get_normalised_azimuthal_degree(GAST),
                    delta=1e-9,
                )

    def test_ecef_to_eci_rotation_angle_matches_erfa(self) -> None:
        """
        Test that the ECEF to ECI rotation angle about the Z-axis agrees with the
        Greenwich apparent sidereal time from ERFA (erfa.gst94 with UT1 = UTC + DUT1).
        """
        for when, GAST in ERFA_GREENWICH_APPARENT_SIDEREAL_TIME.items():
            with self.subTest(when=when):
                transform = ecef_to_eci_transform_provider(when)

                # Rotate the X-axis to measure the rotation angle about the Z-axis:
                r = transform.rotation.rotate_vector(
                    CartesianCoordinate(x=1.0, y=0.0, z=0.0)
                )

                angle = degrees(atan2(r["y"], r["x"]))

                self.assertAlmostEqual(
                    get_normalised_azimuthal_degree(angle),
                    get_normalised_azimuthal_degree(GAST),
                    delta=ERFA_GREENWICH_APPARENT_SIDEREAL_TIME_TOLERANCE,
                )

    def test_ecef_to_eci_matches_convert_ecef_to_eci(self) -> None:
        """
        Test that the ECEF to ECI transform agrees with convert_ecef_to_eci (with zero
        polar motion) to sub-millimetre precision at the Earth's equatorial radius.
        """
        ecef = CartesianCoordinate(
            x=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * cos(radians(45.0)),
            y=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * sin(radians(45.0)),
            z=EARTH_EQUATORIAL_RADIUS * sin(radians(30.0)),
        )

        for when in EARTH_ROTATION_DATES:
            with self.subTest(when=when):
                transform = ecef_to_eci_transform_provider(when)

                eci = transform.apply_to_position(ecef)

                expected = convert_ecef_to_eci(ecef, when)

                # The residual between the two (in meters):
                self.assertLess(distance(eci, expected), 1e-3)

    def test_ecef_to_eci_matches_vallado_example_3_15(self) -> None:
        """
        Test the ECEF (pseudo Earth-fixed) to ECI (true-of-date) transform against the
        worked IAU-76/FK5 example in Vallado, "Fundamentals of Astrodynamics and
        Applications", Example 3-15 (2004-04-06 07:51:28.386009 UTC).
        """
        when = datetime(2004, 4, 6, 7, 51, 28, 386009, tzinfo=timezone.utc)

        # The pseudo Earth-fixed (PEF) position vector (in km):
        r_pef = CartesianCoordinate(x=-1033.4750313, y=7901.3055856, z=6380.3445327)

        # The expected true-of-date position vector (in km):
        r_tod = CartesianCoordinate(x=5094.5147804, y=6127.3664612, z=6380.3445328)

        transform = ecef_to_eci_transform_provider(when)

        r = transform.apply_to_position(r_pef)

        # The residual between the two (in meters):
        residual = 1000.0 * distance(r, r_tod)

        # The Earth-rotation angle is good to the 0.5″ accuracy of the equation of the
        # equinoxes, i.e., ~19 m at this ~7,970 km equatorial distance; omitting DUT1
        # (-0.44 s) would instead rotate the vector by ~6.6″ (~255 m):
        tolerance = (
            1000.0
            * radians(ERFA_GREENWICH_APPARENT_SIDEREAL_TIME_TOLERANCE)
            * sqrt(r_tod["x"] ** 2 + r_tod["y"] ** 2)
        )

        self.assertLess(residual, tolerance)

    def test_ecef_to_eci_is_inverse_of_eci_to_ecef(self) -> None:
        """
        Test that the ECEF to ECI transform undoes the ECI to ECEF transform, i.e., both
        providers apply the same Earth-rotation angle (with DUT1) in opposite senses.
        """
        eci = CartesianCoordinate(
            x=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * cos(radians(45.0)),
            y=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * sin(radians(45.0)),
            z=EARTH_EQUATORIAL_RADIUS * sin(radians(30.0)),
        )

        for when in EARTH_ROTATION_DATES:
            with self.subTest(when=when):
                ecef = eci_to_ecef_transform_provider(when).apply_to_position(eci)

                r = ecef_to_eci_transform_provider(when).apply_to_position(ecef)

                # The round-trip residual (in meters):
                self.assertLess(distance(r, eci), 1e-6)

    def test_ecef_to_eci_has_zero_translation(self) -> None:
        """
        Test that the transform has zero translation.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************


class TestECIToECEFTransformProvider(unittest.TestCase):
    def test_eci_to_ecef_rotates_z_axis_only(self) -> None:
        """
        Test that the transform has a rotation about the Z-axis only.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = eci_to_ecef_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.7737996205180773,
            x=0.0,
            y=0.0,
            z=-0.6334304597081512,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eci_to_ecef_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.5716645816865767,
            x=0.0,
            y=0.0,
            z=-0.8204874197969834,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

    def test_eci_to_ecef_rotation_angle_is_apparent_sidereal_time(self) -> None:
        """
        Test that the ECI to ECEF rotation angle about the Z-axis is minus the Greenwich
        apparent sidereal time, with DUT1 (UT1 - UTC) applied to the mean sidereal time.
        """
        for when in EARTH_ROTATION_DATES:
            with self.subTest(when=when):
                transform = eci_to_ecef_transform_provider(when)

                # Rotate the X-axis to measure the rotation angle about the Z-axis:
                r = transform.rotation.rotate_vector(
                    CartesianCoordinate(x=1.0, y=0.0, z=0.0)
                )

                angle = degrees(atan2(r["y"], r["x"]))

                GAST = get_greenwich_apparent_sidereal_time(when)

                self.assertAlmostEqual(
                    get_normalised_azimuthal_degree(angle),
                    get_normalised_azimuthal_degree(-GAST),
                    delta=1e-9,
                )

    def test_eci_to_ecef_rotation_angle_matches_erfa(self) -> None:
        """
        Test that the ECI to ECEF rotation angle about the Z-axis agrees with minus the
        Greenwich apparent sidereal time from ERFA (erfa.gst94 with UT1 = UTC + DUT1).
        """
        for when, GAST in ERFA_GREENWICH_APPARENT_SIDEREAL_TIME.items():
            with self.subTest(when=when):
                transform = eci_to_ecef_transform_provider(when)

                # Rotate the X-axis to measure the rotation angle about the Z-axis:
                r = transform.rotation.rotate_vector(
                    CartesianCoordinate(x=1.0, y=0.0, z=0.0)
                )

                angle = degrees(atan2(r["y"], r["x"]))

                self.assertAlmostEqual(
                    get_normalised_azimuthal_degree(angle),
                    get_normalised_azimuthal_degree(-GAST),
                    delta=ERFA_GREENWICH_APPARENT_SIDEREAL_TIME_TOLERANCE,
                )

    def test_eci_to_ecef_matches_convert_eci_to_ecef(self) -> None:
        """
        Test that the ECI to ECEF transform agrees with convert_eci_to_ecef (with zero
        polar motion) to sub-millimetre precision at the Earth's equatorial radius.
        """
        eci = CartesianCoordinate(
            x=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * cos(radians(45.0)),
            y=EARTH_EQUATORIAL_RADIUS * cos(radians(30.0)) * sin(radians(45.0)),
            z=EARTH_EQUATORIAL_RADIUS * sin(radians(30.0)),
        )

        for when in EARTH_ROTATION_DATES:
            with self.subTest(when=when):
                transform = eci_to_ecef_transform_provider(when)

                ecef = transform.apply_to_position(eci)

                expected = convert_eci_to_ecef(eci, when)

                # The residual between the two (in meters):
                self.assertLess(distance(ecef, expected), 1e-3)

    def test_eci_to_ecef_matches_vallado_example_3_15(self) -> None:
        """
        Test the ECI (true-of-date) to ECEF (pseudo Earth-fixed) transform against the
        worked IAU-76/FK5 example in Vallado, "Fundamentals of Astrodynamics and
        Applications", Example 3-15 (2004-04-06 07:51:28.386009 UTC).
        """
        when = datetime(2004, 4, 6, 7, 51, 28, 386009, tzinfo=timezone.utc)

        # The true-of-date position vector (in km):
        r_tod = CartesianCoordinate(x=5094.5147804, y=6127.3664612, z=6380.3445328)

        # The expected pseudo Earth-fixed (PEF) position vector (in km):
        r_pef = CartesianCoordinate(x=-1033.4750313, y=7901.3055856, z=6380.3445327)

        transform = eci_to_ecef_transform_provider(when)

        r = transform.apply_to_position(r_tod)

        # The residual between the two (in meters):
        residual = 1000.0 * distance(r, r_pef)

        # The Earth-rotation angle is good to the 0.5″ accuracy of the equation of the
        # equinoxes, i.e., ~19 m at this ~7,970 km equatorial distance; omitting DUT1
        # (-0.44 s) would instead rotate the vector by ~6.6″ (~255 m):
        tolerance = (
            1000.0
            * radians(ERFA_GREENWICH_APPARENT_SIDEREAL_TIME_TOLERANCE)
            * sqrt(r_pef["x"] ** 2 + r_pef["y"] ** 2)
        )

        self.assertLess(residual, tolerance)

    def test_eci_to_ecef_has_zero_translation(self) -> None:
        """
        Test that the transform has zero translation.
        """
        when = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        transform = eci_to_ecef_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eci_to_ecef_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************


class TestEME2000ToECITransformProvider(unittest.TestCase):
    def test_eme2000_to_eci_matches_vallado_example_3_15(self) -> None:
        """
        Test the EME2000 (J2000) to ECI (true-of-date) transform against the worked
        IAU-76/FK5 example in Vallado, "Fundamentals of Astrodynamics and
        Applications", Example 3-15 (2004-04-06 07:51:28.386009 UTC).
        """
        when = datetime(2004, 4, 6, 7, 51, 28, 386009, tzinfo=timezone.utc)

        # The J2000 position vector (in km):
        r_j2000 = CartesianCoordinate(x=5102.5096, y=6123.01152, z=6378.1363)

        # The expected true-of-date position vector (in km):
        r_tod = CartesianCoordinate(x=5094.5147804, y=6127.3664612, z=6380.3445328)

        transform = eme2000_to_eci_transform_provider(
            when=when,
        )

        r = transform.apply_to_position(r_j2000)

        # The residual between the two (in meters):
        residual = 1000.0 * sqrt(
            (r["x"] - r_tod["x"]) ** 2
            + (r["y"] - r_tod["y"]) ** 2
            + (r["z"] - r_tod["z"]) ** 2
        )

        # Within 1 m at ~10,500 km (~0.02 arcseconds); the current nutation model is
        # not the full 106-term IAU-1980 series, so an exact match is not expected:
        self.assertLess(residual, 1.0)

    def test_eme2000_to_eci_precesses_j2000_equinox(self) -> None:
        """
        Test that the J2000 vernal equinox direction is precessed forwards in time,
        using the rigorous IAU-76 precession formula for right ascension and declination
        as an independent reference.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        T = (2460676.5 - 2451545.0) / 36525.0

        ζ = radians((2306.2181 * T + 0.30188 * T**2 + 0.017998 * T**3) / 3600.0)
        θ = radians((2004.3109 * T - 0.42665 * T**2 - 0.041833 * T**3) / 3600.0)
        z = radians((2306.2181 * T + 1.09468 * T**2 + 0.018203 * T**3) / 3600.0)

        # The rigorous precession of (α0, δ0) = (0, 0) to the mean equinox of date:
        A = sin(ζ)
        B = cos(θ) * cos(ζ)
        C = sin(θ) * cos(ζ)

        expected_ra = degrees(atan2(A, B) + z)
        expected_dec = degrees(asin(C))

        transform = eme2000_to_eci_transform_provider(
            when=when,
        )

        r = transform.apply_to_position(CartesianCoordinate(x=1.0, y=0.0, z=0.0))

        ra = degrees(atan2(r["y"], r["x"]))
        dec = degrees(asin(r["z"]))

        # Precession moves the equinox ~0.32° in RA and ~0.14° in Dec by 2025; allow
        # for nutation, which is at most ~20 arcseconds (~0.006°):
        self.assertGreater(ra, 0.0)
        self.assertGreater(dec, 0.0)
        self.assertAlmostEqual(ra, expected_ra, delta=0.006)
        self.assertAlmostEqual(dec, expected_dec, delta=0.006)

    def test_nutation_matrix_reduces_to_identity_when_nutation_is_zero(
        self,
    ) -> None:
        """
        Test that the nutation matrix is identity when nutation is zero.
        """
        rotation = Quaternion.from_rotation_matrix(
            multiply(
                get_rotation_matrix_x(-23.439292),
                multiply(
                    get_rotation_matrix_z(0.0),
                    get_rotation_matrix_x(23.439292),
                ),
            )
        )

        self.assertAlmostEqual(
            rotation.w,
            1.0,
            places=12,
        )
        self.assertAlmostEqual(
            rotation.x,
            0.0,
            places=12,
        )
        self.assertAlmostEqual(
            rotation.y,
            0.0,
            places=12,
        )
        self.assertAlmostEqual(
            rotation.z,
            0.0,
            places=12,
        )

    def test_eme2000_to_eci_has_zero_translation(self) -> None:
        """
        Test that the EME2000 to ECI transform has zero translation.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eme2000_to_eci_transform_provider(
            when=when,
        )

        self.assertEqual(
            transform.translation["x"],
            0.0,
        )
        self.assertEqual(
            transform.translation["y"],
            0.0,
        )
        self.assertEqual(
            transform.translation["z"],
            0.0,
        )


# **************************************************************************************


class TestITRFToECEFTransformProvider(unittest.TestCase):
    def test_itrf_to_ecef_is_identity(self) -> None:
        """
        Test that the ITRF to ECEF transform is currently coincident.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = itrf_to_ecef_transform_provider(when)

        expected_rotation = Quaternion.identity()

        self.assertEqual(transform.rotation.w, expected_rotation.w)
        self.assertEqual(transform.rotation.x, expected_rotation.x)
        self.assertEqual(transform.rotation.y, expected_rotation.y)
        self.assertEqual(transform.rotation.z, expected_rotation.z)

    def test_itrf_to_ecef_has_zero_translation(self) -> None:
        """
        Test that the ITRF to ECEF transform has zero translation.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = itrf_to_ecef_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************


class TestTEMEToECITransformProvider(unittest.TestCase):
    def test_teme_to_eci_rotates_about_z_axis(self) -> None:
        """
        Test that the TEME to ECI transform is a small rotation about the Z-axis.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = teme_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=0.9999999999998531,
            x=0.0,
            y=0.0,
            z=5.419365470642385e-07,
        )

        self.assertAlmostEqual(
            transform.rotation.w,
            expected_rotation.w,
            places=12,
        )
        self.assertAlmostEqual(
            transform.rotation.x,
            expected_rotation.x,
            places=15,
        )
        self.assertAlmostEqual(
            transform.rotation.y,
            expected_rotation.y,
            places=15,
        )
        self.assertAlmostEqual(
            transform.rotation.z,
            expected_rotation.z,
            places=6,
        )

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = teme_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=0.9999999999960894,
            x=0.0,
            y=0.0,
            z=2.79665571465075e-06,
        )

        self.assertAlmostEqual(
            transform.rotation.w,
            expected_rotation.w,
            places=12,
        )
        self.assertAlmostEqual(
            transform.rotation.x,
            expected_rotation.x,
            places=15,
        )
        self.assertAlmostEqual(
            transform.rotation.y,
            expected_rotation.y,
            places=15,
        )
        self.assertAlmostEqual(
            transform.rotation.z,
            expected_rotation.z,
            places=6,
        )

    def test_teme_to_eci_has_zero_translation(self) -> None:
        """
        Test that the TEME to ECI transform has zero translation.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = teme_to_eci_transform_provider(when)

        self.assertEqual(transform.translation["x"], 0.0)
        self.assertEqual(transform.translation["y"], 0.0)
        self.assertEqual(transform.translation["z"], 0.0)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
