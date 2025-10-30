# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles import (
    CartesianCoordinate,
    Matrix3x3,
    Quaternion,
    QuaternionEulerKind,
    QuaternionEulerOrder,
)
from satelles import (
    normalise as vector_normalise,
)

# **************************************************************************************


class TestQuaternionCore(unittest.TestCase):
    def test_identity_magnitude_and_rotate(self) -> None:
        """
        Identity quaternion has magnitude 1 and leaves vectors unchanged.
        """
        q = Quaternion.identity()
        self.assertAlmostEqual(q.magnitude(), 1.0, places=12)

        v = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], v["x"], places=6)
        self.assertAlmostEqual(r["y"], v["y"], places=6)
        self.assertAlmostEqual(r["z"], v["z"], places=6)

    def test_normalise_zero_raises(self):
        """
        Normalising a zero quaternion raises ValueError.
        """
        q = Quaternion(0.0, 0.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            q.normalise()

    def test_conjugate_inverse_unit(self) -> None:
        """
        For a unit quaternion, inverse equals conjugate.
        """
        q = Quaternion.from_axis_angle(CartesianCoordinate(x=0.0, y=0.0, z=1.0), 45.0)
        qn = q.normalise()
        self.assertAlmostEqual(qn.magnitude(), 1.0, places=12)

        self.assertAlmostEqual(qn.inverse().w, qn.conjugate().w, places=12)
        self.assertAlmostEqual(qn.inverse().x, qn.conjugate().x, places=12)
        self.assertAlmostEqual(qn.inverse().y, qn.conjugate().y, places=12)
        self.assertAlmostEqual(qn.inverse().z, qn.conjugate().z, places=12)

    def test_multiply_composes_rotations(self) -> None:
        """
        Composition: rotate by yaw 90 then pitch 90 equals applying the composed quaternion.
        """
        z_axis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)
        y_axis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)

        q_yaw_90 = Quaternion.from_axis_angle(z_axis, 90.0)
        q_pitch_90 = Quaternion.from_axis_angle(y_axis, 90.0)

        # Intrinsic ZYX convention: roll * pitch * yaw
        q_composed = q_pitch_90 * q_yaw_90

        v = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r_seq = q_pitch_90.rotate_vector(q_yaw_90.rotate_vector(v))
        r_cmp = q_composed.rotate_vector(v)

        self.assertAlmostEqual(r_seq["x"], r_cmp["x"], places=6)
        self.assertAlmostEqual(r_seq["y"], r_cmp["y"], places=6)
        self.assertAlmostEqual(r_seq["z"], r_cmp["z"], places=6)

    def test_rotate_vector_basic_axes(self) -> None:
        """
        Rotations about principal axes by 90 degrees map basis vectors as expected.
        """
        x_axis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        y_axis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        z_axis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        qz90 = Quaternion.from_axis_angle(z_axis, 90.0)
        qy90 = Quaternion.from_axis_angle(y_axis, 90.0)
        qx90 = Quaternion.from_axis_angle(x_axis, 90.0)

        # +Z 90°: (1,0,0) -> (0,1,0)
        r = qz90.rotate_vector(CartesianCoordinate(x=1.0, y=0.0, z=0.0))
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 1.0, places=6)
        self.assertAlmostEqual(r["z"], 0.0, places=6)

        # +Y 90°: (1,0,0) -> (0,0,-1)
        r = qy90.rotate_vector(CartesianCoordinate(x=1.0, y=0.0, z=0.0))
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 0.0, places=6)
        self.assertAlmostEqual(r["z"], -1.0, places=6)

        # +X 90°: (0,1,0) -> (0,0,1)
        r = qx90.rotate_vector(CartesianCoordinate(x=0.0, y=1.0, z=0.0))
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 0.0, places=6)
        self.assertAlmostEqual(r["z"], 1.0, places=6)


# **************************************************************************************


class TestQuaternionFromAxisAngle(unittest.TestCase):
    def test_from_axis_angle_z_90_rotates_x_to_y(self):
        """
        Axis-angle about +Z by 90 degrees rotates (1,0,0) to (0,1,0).
        """
        z_axis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)
        q = Quaternion.from_axis_angle(z_axis, 90.0)
        v = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 1.0, places=6)
        self.assertAlmostEqual(r["z"], 0.0, places=6)

    def test_from_axis_angle_normalises_axis(self) -> None:
        """
        Axis may be non-unit; result must match using the normalised axis.
        """
        axis = CartesianCoordinate(x=0.0, y=0.0, z=10.0)
        axis_unit = vector_normalise(axis)

        q_raw = Quaternion.from_axis_angle(axis, 45.0)
        q_unit = Quaternion.from_axis_angle(axis_unit, 45.0)

        # Compare by rotating a vector (avoids ±q ambiguity)
        v = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r_raw = q_raw.rotate_vector(v)
        r_unit = q_unit.rotate_vector(v)
        self.assertAlmostEqual(r_raw["x"], r_unit["x"], places=6)
        self.assertAlmostEqual(r_raw["y"], r_unit["y"], places=6)
        self.assertAlmostEqual(r_raw["z"], r_unit["z"], places=6)


# **************************************************************************************


class TestQuaternionFromRotationMatrix(unittest.TestCase):
    def test_from_rotation_matrix_identity(self) -> None:
        """
        Identity matrix produces the identity quaternion (up to sign).
        """
        identity: Matrix3x3 = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )
        q = Quaternion.from_rotation_matrix(identity)
        v = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], v["x"], places=6)
        self.assertAlmostEqual(r["y"], v["y"], places=6)
        self.assertAlmostEqual(r["z"], v["z"], places=6)

    def test_from_rotation_matrix_z_90(self) -> None:
        """
        Rotation matrix for +Z 90° rotates (1,0,0) to (0,1,0).
        """
        Rz90: Matrix3x3 = (
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )
        q = Quaternion.from_rotation_matrix(Rz90)
        v = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 1.0, places=6)
        self.assertAlmostEqual(r["z"], 0.0, places=6)

    def test_from_rotation_matrix_y_90(self) -> None:
        """
        Rotation matrix for +Y 90° rotates (1,0,0) to (0,0,-1).
        """
        Ry90: Matrix3x3 = (
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, 0.0),
        )
        q = Quaternion.from_rotation_matrix(Ry90)
        v = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 0.0, places=6)
        self.assertAlmostEqual(r["z"], -1.0, places=6)

    def test_from_rotation_matrix_x_90(self) -> None:
        """
        Rotation matrix for +X 90° rotates (0,1,0) to (0,0,1).
        """
        Rx90: Matrix3x3 = (
            (1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
            (0.0, 1.0, 0.0),
        )
        q = Quaternion.from_rotation_matrix(Rx90)
        v = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        r = q.rotate_vector(v)
        self.assertAlmostEqual(r["x"], 0.0, places=6)
        self.assertAlmostEqual(r["y"], 0.0, places=6)
        self.assertAlmostEqual(r["z"], 1.0, places=6)


# **************************************************************************************


class TestQuaternionFromEulerAngles(unittest.TestCase):
    def test_zero_angles_is_identity(self) -> None:
        """
        Zero roll, pitch, yaw yields the identity rotation (default: intrinsic Z-Y-X).
        """
        quaternion = Quaternion.from_euler_rotation(
            rotation={"roll": 0.0, "pitch": 0.0, "yaw": 0.0}
        )
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        rotated = quaternion.rotate_vector(vector)
        self.assertAlmostEqual(rotated["x"], vector["x"], places=6)
        self.assertAlmostEqual(rotated["y"], vector["y"], places=6)
        self.assertAlmostEqual(rotated["z"], vector["z"], places=6)

    def test_yaw_plus_ninety_about_z_axis_default_order(self) -> None:
        """
        Yaw +90° (about Z) rotates (1,0,0) to (0,1,0) under the default intrinsic Z-Y-X.
        """
        quaternion = Quaternion.from_euler_rotation(
            rotation={"roll": 0.0, "pitch": 0.0, "yaw": 90.0}
        )
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        rotated = quaternion.rotate_vector(vector)
        self.assertAlmostEqual(rotated["x"], 0.0, places=6)
        constitution = rotated["y"]
        self.assertAlmostEqual(constitution, 1.0, places=6)
        self.assertAlmostEqual(rotated["z"], 0.0, places=6)

    def test_pitch_plus_ninety_about_y_axis_default_order(self) -> None:
        """
        Pitch +90° (about Y) rotates (1,0,0) to (0,0,-1) under the default intrinsic Z-Y-X.
        """
        quaternion = Quaternion.from_euler_rotation(
            rotation={"roll": 0.0, "pitch": 90.0, "yaw": 0.0}
        )
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        rotated = quaternion.rotate_vector(vector)
        self.assertAlmostEqual(rotated["x"], 0.0, places=6)
        self.assertAlmostEqual(rotated["y"], 0.0, places=6)
        self.assertAlmostEqual(rotated["z"], -1.0, places=6)

    def test_roll_plus_ninety_about_x_axis_default_order(self) -> None:
        """
        Roll +90° (about X) rotates (0,1,0) to (0,0,1) under the default intrinsic Z-Y-X.
        """
        quaternion = Quaternion.from_euler_rotation(
            rotation={"roll": 90.0, "pitch": 0.0, "yaw": 0.0}
        )
        vector = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        rotated = quaternion.rotate_vector(vector)
        self.assertAlmostEqual(rotated["x"], 0.0, places=6)
        self.assertAlmostEqual(rotated["y"], 0.0, places=6)
        self.assertAlmostEqual(rotated["z"], 1.0, places=6)

    def test_intrinsic_zyx_matches_axis_angle_composition(self) -> None:
        """
        Intrinsic Z-Y-X equals qz(yaw) * qy(pitch) * qx(roll). With roll=0: qz(yaw) * qy(pitch).
        """
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 0.0
        pitch = 30.0
        yaw = 45.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.YAW_PITCH_ROLL,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(zaxis, yaw)
        second = Quaternion.from_axis_angle(yaxis, pitch)
        third = Quaternion.from_axis_angle(xaxis, roll)
        composition = first * second * third

        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_xyz_matches_axis_angle_composition(self) -> None:
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 20.0
        pitch = 30.0
        yaw = 40.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.ROLL_PITCH_YAW,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(xaxis, roll)
        second = Quaternion.from_axis_angle(yaxis, pitch)
        third = Quaternion.from_axis_angle(zaxis, yaw)
        composition = first * second * third

        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_xzy_matches_axis_angle_composition(self) -> None:
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 21.0
        pitch = 31.0
        yaw = 41.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.ROLL_YAW_PITCH,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(xaxis, roll)
        second = Quaternion.from_axis_angle(zaxis, yaw)
        third = Quaternion.from_axis_angle(yaxis, pitch)
        composition = first * second * third

        vector = CartesianCoordinate(x=-2.0, y=0.5, z=4.0)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_yxz_matches_axis_angle_composition(self) -> None:
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 22.0
        pitch = 32.0
        yaw = 42.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.PITCH_ROLL_YAW,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(yaxis, pitch)
        second = Quaternion.from_axis_angle(xaxis, roll)
        third = Quaternion.from_axis_angle(zaxis, yaw)
        composition = first * second * third

        vector = CartesianCoordinate(x=0.25, y=-1.5, z=2.0)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_yzx_matches_axis_angle_composition(self) -> None:
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 23.0
        pitch = 33.0
        yaw = 43.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.PITCH_YAW_ROLL,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(yaxis, pitch)
        second = Quaternion.from_axis_angle(zaxis, yaw)
        third = Quaternion.from_axis_angle(xaxis, roll)
        composition = first * second * third

        vector = CartesianCoordinate(x=-0.5, y=3.0, z=-1.0)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_zxy_matches_axis_angle_composition(self) -> None:
        xaxis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        yaxis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        zaxis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = 24.0
        pitch = 34.0
        yaw = 44.0

        euler = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.YAW_ROLL_PITCH,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        first = Quaternion.from_axis_angle(zaxis, yaw)
        second = Quaternion.from_axis_angle(xaxis, roll)
        third = Quaternion.from_axis_angle(yaxis, pitch)
        composition = first * second * third

        vector = CartesianCoordinate(x=2.0, y=-0.25, z=0.75)
        r1 = euler.rotate_vector(vector)
        r2 = composition.rotate_vector(vector)

        self.assertAlmostEqual(r1["x"], r2["x"], places=6)
        self.assertAlmostEqual(r1["y"], r2["y"], places=6)
        self.assertAlmostEqual(r1["z"], r2["z"], places=6)

    def test_intrinsic_vs_extrinsic_differ_for_xyz(self) -> None:
        """
        Intrinsic vs extrinsic for the same angles and order produces different rotations.
        """
        roll = 25.0
        pitch = 35.0
        yaw = 45.0
        vector = CartesianCoordinate(x=0.5, y=-1.0, z=2.0)

        intrinsic = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.ROLL_PITCH_YAW,
            kind=QuaternionEulerKind.INTRINSIC,
        )
        extrinsic = Quaternion.from_euler_rotation(
            rotation={"roll": roll, "pitch": pitch, "yaw": yaw},
            order=QuaternionEulerOrder.ROLL_PITCH_YAW,
            kind=QuaternionEulerKind.EXTRINSIC,
        )

        r_intrinsic = intrinsic.rotate_vector(vector)
        r_extrinsic = extrinsic.rotate_vector(vector)

        difference = (
            abs(r_intrinsic["x"] - r_extrinsic["x"])
            + abs(r_intrinsic["y"] - r_extrinsic["y"])
            + abs(r_intrinsic["z"] - r_extrinsic["z"])
        )
        self.assertGreater(difference, 1e-6)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
