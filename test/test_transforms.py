# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone

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
    def test_eme2000_to_eci_rotation_on_2025_01_01(self) -> None:
        """
        Test that the EME2000 to ECI transform is a small precession-nutation rotation.
        """
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eme2000_to_eci_transform_provider(
            when=when,
        )

        expected_rotation = Quaternion(
            w=0.999995353726039,
            x=-2.0660320068660085e-05,
            y=0.001214364707909048,
            z=-0.0027959645637348767,
        )

        self.assertAlmostEqual(
            transform.rotation.w,
            expected_rotation.w,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.x,
            expected_rotation.x,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.y,
            expected_rotation.y,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.z,
            expected_rotation.z,
            places=9,
        )

    def test_eme2000_to_eci_rotation_on_2025_06_01(self) -> None:
        """
        Test that the EME2000 to ECI transform is a small precession-nutation rotation.
        """
        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = eme2000_to_eci_transform_provider(
            when=when,
        )

        expected_rotation = Quaternion(
            w=0.9999951918754822,
            x=-2.0825816935255278e-05,
            y=0.0012331462106853334,
            z=-0.002845196412534039,
        )

        self.assertAlmostEqual(
            transform.rotation.w,
            expected_rotation.w,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.x,
            expected_rotation.x,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.y,
            expected_rotation.y,
            places=9,
        )
        self.assertAlmostEqual(
            transform.rotation.z,
            expected_rotation.z,
            places=9,
        )

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
