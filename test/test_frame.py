# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime

from satelles.body import Body
from satelles.common import CartesianCoordinate
from satelles.frame import Frame, Reference, Transform
from satelles.quaternion import Quaternion

# **************************************************************************************


class TestReference(unittest.TestCase):
    def test_is_inertial(self):
        self.assertTrue(Reference.ECI.is_inertial)
        self.assertTrue(Reference.ICRF.is_inertial)
        self.assertTrue(Reference.EME2000.is_inertial)
        self.assertTrue(Reference.TEME.is_inertial)
        self.assertFalse(Reference.ECEF.is_inertial)
        self.assertFalse(Reference.ITRF.is_inertial)
        self.assertFalse(Reference.TOPOCENTRIC.is_inertial)

    def test_is_rotating(self):
        self.assertTrue(Reference.ECEF.is_rotating)
        self.assertTrue(Reference.ITRF.is_rotating)
        self.assertTrue(Reference.TOPOCENTRIC.is_rotating)
        self.assertFalse(Reference.ECI.is_rotating)
        self.assertFalse(Reference.ICRF.is_rotating)
        self.assertFalse(Reference.EME2000.is_rotating)
        self.assertFalse(Reference.TEME.is_rotating)


# **************************************************************************************


class TestTransform(unittest.TestCase):
    def test_identity_transform_leaves_vector_unchanged(self) -> None:
        """
        Test that the identity transform leaves a vector unchanged.
        """
        identity = Transform(
            rotation=Quaternion.identity(),
            translation=CartesianCoordinate(x=0.0, y=0.0, z=0.0),
        )

        vector = CartesianCoordinate(x=1.0, y=-2.0, z=3.5)

        result = identity.apply_to_position(vector)

        self.assertAlmostEqual(result["x"], 1.0, places=12)
        self.assertAlmostEqual(result["y"], -2.0, places=12)
        self.assertAlmostEqual(result["z"], 3.5, places=12)

    def test_inverse_transform_round_trip(self) -> None:
        """
        Test 90° rotation about +Z, plus a translation
        """
        z = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        rotation = Quaternion.from_axis_angle(axis=z, angle=90.0)

        translation = CartesianCoordinate(x=1.0, y=2.0, z=3.0)

        transform = Transform(
            rotation=rotation,
            translation=translation,
        )

        inverse = transform.inverse()

        origin = CartesianCoordinate(x=4.0, y=0.0, z=-1.0)

        # Apply forward then inverse; we should get back the origin (within tolerance):
        forward = transform.apply_to_position(origin)

        original = inverse.apply_to_position(forward)

        self.assertAlmostEqual(original["x"], origin["x"], places=10)
        self.assertAlmostEqual(original["y"], origin["y"], places=10)
        self.assertAlmostEqual(original["z"], origin["z"], places=10)

    def test_compose_matches_sequential_application(self) -> None:
        """
        Test that composing two transforms matches applying them sequentially.
        """
        AB = Transform(
            rotation=Quaternion.identity(),
            translation=CartesianCoordinate(x=1.0, y=0.0, z=0.0),
        )  # A -> B

        BC = Transform(
            rotation=Quaternion.identity(),
            translation=CartesianCoordinate(x=0.0, y=2.0, z=0.0),
        )  # B -> C

        # (B->C) ∘ (A->B) = A->C:
        composed = BC.compose(AB)

        origin = CartesianCoordinate(x=0.0, y=0.0, z=0.0)

        sequential = BC.apply_to_position(AB.apply_to_position(origin))

        original = composed.apply_to_position(origin)

        self.assertAlmostEqual(original["x"], sequential["x"], places=12)
        self.assertAlmostEqual(original["y"], sequential["y"], places=12)
        self.assertAlmostEqual(original["z"], sequential["z"], places=12)


# **************************************************************************************


class TestFrame(unittest.TestCase):
    def test_same_frame_identity(self) -> None:
        """Transform to the same frame should be identity."""
        time = datetime(2025, 1, 1)

        root = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=None,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="ROOT",
        )

        transform = root.transform_to(time, root)

        position = CartesianCoordinate(
            x=3.0,
            y=-1.0,
            z=5.0,
        )
        result = transform.apply_to_position(position)

        self.assertAlmostEqual(result["x"], position["x"])
        self.assertAlmostEqual(result["y"], position["y"])
        self.assertAlmostEqual(result["z"], position["z"])

    def test_child_to_parent_translation(self) -> None:
        """Child to parent transform should map child origin to parent offset."""
        time = datetime(2025, 1, 1)

        root = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=None,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="ROOT",
        )

        child = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=root,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=1.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="CHILD",
        )

        transform = child.transform_to(time, root)

        position = CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        )
        result = transform.apply_to_position(position)

        self.assertAlmostEqual(result["x"], 1.0)
        self.assertAlmostEqual(result["y"], 0.0)
        self.assertAlmostEqual(result["z"], 0.0)

    def test_parent_to_child_inverse(self) -> None:
        """Parent to child transform should be inverse of child to parent."""
        time = datetime(2025, 1, 1)

        root = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=None,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="ROOT",
        )

        child = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=root,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=1.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="CHILD",
        )

        forward = root.transform_to(time, child)
        backward = child.transform_to(time, root)

        origin_root = CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        )
        origin_child = forward.apply_to_position(origin_root)
        origin_back = backward.apply_to_position(origin_child)

        self.assertAlmostEqual(origin_child["x"], -1.0)
        self.assertAlmostEqual(origin_child["y"], 0.0)
        self.assertAlmostEqual(origin_child["z"], 0.0)

        self.assertAlmostEqual(origin_back["x"], origin_root["x"])
        self.assertAlmostEqual(origin_back["y"], origin_root["y"])
        self.assertAlmostEqual(origin_back["z"], origin_root["z"])

    def test_sibling_frames_via_common_ancestor(self) -> None:
        """Sibling frames should transform correctly via common ancestor."""
        time = datetime(2025, 1, 1)

        root = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=None,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="ROOT",
        )

        first = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=root,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=1.0,
                    y=0.0,
                    z=0.0,
                ),
            ),
            name="FIRST",
        )

        second = Frame(
            reference=Reference.ECI,
            origin=Body.EARTH,
            is_inertial=True,
            parent=root,
            transform_to_parent=lambda time: Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=2.0,
                    z=0.0,
                ),
            ),
            name="SECOND",
        )

        transform = first.transform_to(time, second)

        position = CartesianCoordinate(
            x=0.0,
            y=0.0,
            z=0.0,
        )
        result = transform.apply_to_position(position)

        self.assertAlmostEqual(result["x"], 1.0)
        self.assertAlmostEqual(result["y"], -2.0)
        self.assertAlmostEqual(result["z"], 0.0)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
