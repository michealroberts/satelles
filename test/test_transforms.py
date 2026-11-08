# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone
from math import asin, atan2, cos, degrees, radians, sin, sqrt

from satelles.coordinates import CartesianCoordinate
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
            w=-0.7737985519625099,
            x=0.0,
            y=0.0,
            z=0.6334317650550239,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.5716637145331898,
            x=0.0,
            y=0.0,
            z=0.8204880239748267,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

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
            w=-0.7737985519625099,
            x=0.0,
            y=0.0,
            z=-0.6334317650550239,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eci_to_ecef_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.5716637145331898,
            x=0.0,
            y=0.0,
            z=-0.8204880239748267,
        )

        self.assertAlmostEqual(transform.rotation.w, expected_rotation.w, places=15)
        self.assertAlmostEqual(transform.rotation.x, expected_rotation.x, places=15)
        self.assertAlmostEqual(transform.rotation.y, expected_rotation.y, places=15)
        self.assertAlmostEqual(transform.rotation.z, expected_rotation.z, places=15)

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
