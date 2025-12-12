# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from satelles.coordinates import CartesianCoordinate
from satelles.quaternion import Quaternion
from satelles.transforms import (
    ecef_to_eci_transform_provider,
    identity_transform_provider,
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
            w=-0.7737981347150147,
            x=0.0,
            y=0.0,
            z=0.6334322747631067,
        )

        self.assertEqual(transform.rotation.w, expected_rotation.w)
        self.assertEqual(transform.rotation.x, expected_rotation.x)
        self.assertEqual(transform.rotation.y, expected_rotation.y)
        self.assertEqual(transform.rotation.z, expected_rotation.z)

        when = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)

        transform = ecef_to_eci_transform_provider(when)

        expected_rotation = Quaternion(
            w=-0.5716613583006416,
            x=0.0,
            y=0.0,
            z=0.8204896656423318,
        )

        self.assertEqual(transform.rotation.w, expected_rotation.w)
        self.assertEqual(transform.rotation.x, expected_rotation.x)
        self.assertEqual(transform.rotation.y, expected_rotation.y)
        self.assertEqual(transform.rotation.z, expected_rotation.z)

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

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
