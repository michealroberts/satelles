# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from dataclasses import dataclass
from enum import Enum
from math import cos, isclose, radians, sin, sqrt
from sys import float_info
from typing import Dict, Literal, Tuple, TypedDict, cast

from satelles.common import CartesianCoordinate
from satelles.matrix import Matrix3x3
from satelles.vector import normalise as vector_normalise

# **************************************************************************************

TOLERANCE = float_info.epsilon


# **************************************************************************************


class EulerRotation(TypedDict):
    """
    Typed dictionary for Euler rotation angles.
    """

    roll: float
    pitch: float
    yaw: float


# **************************************************************************************


class QuaternionEulerOrder(Enum):
    """
    Enumeration for quaternion Euler angle orders.
    """

    ROLL_PITCH_YAW = "xyz"
    ROLL_YAW_PITCH = "xzy"
    PITCH_ROLL_YAW = "yxz"
    PITCH_YAW_ROLL = "yzx"
    YAW_ROLL_PITCH = "zxy"
    YAW_PITCH_ROLL = "zyx"


# **************************************************************************************


class QuaternionEulerKind(Enum):
    """
    Enumeration for quaternion Euler angle kinds.
    """

    INTRINSIC = "intrinsic"
    EXTRINSIC = "extrinsic"


# **************************************************************************************


@dataclass(frozen=True)
class Quaternion:
    """
    A class representing a quaternion for 3D rotations.
    """

    w: float
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        """
        Returns the magnitude of the quaternion.

        Returns:
            float: The magnitude of the quaternion.
        """
        return sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalise(self) -> "Quaternion":
        """
        Returns the normalized (unit) quaternion.

        Returns:
            Quaternion: The normalized quaternion.
        """
        magnitude = self.magnitude()

        if isclose(magnitude, 0.0, abs_tol=TOLERANCE):
            raise ValueError("Cannot normalize a zero-length quaternion.")

        return Quaternion(
            w=self.w / magnitude,
            x=self.x / magnitude,
            y=self.y / magnitude,
            z=self.z / magnitude,
        )

    def conjugate(self) -> "Quaternion":
        """
        Returns the conjugate of the quaternion.

        Returns:
            Quaternion: The conjugate quaternion.
        """
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> "Quaternion":
        """
        Returns the inverse of the quaternion.

        Returns:
            Quaternion: The inverse quaternion.
        """
        mm = self.magnitude() ** 2

        if isclose(mm, 0.0, abs_tol=TOLERANCE):
            raise ValueError("Cannot invert a zero-length quaternion.")

        conjugate = self.conjugate()

        return Quaternion(
            w=conjugate.w / mm,
            x=conjugate.x / mm,
            y=conjugate.y / mm,
            z=conjugate.z / mm,
        )

    def multiply(self, other: "Quaternion") -> "Quaternion":
        """
        Multiplies this quaternion by another quaternion.

        Args:
            other (Quaternion): The other quaternion to multiply with.

        Returns:
            Quaternion: The resulting quaternion from the multiplication.
        """
        return Quaternion(
            w=self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x=self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y=self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z=self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        return self.multiply(other)

    def __matmul__(self, other: "Quaternion") -> "Quaternion":
        return self.multiply(other)

    def rotate_vector(self, vector: CartesianCoordinate) -> CartesianCoordinate:
        """
        Rotates a 3D vector using this quaternion.

        Args:
            vector (CartesianCoordinate): The vector to rotate.

        Returns:
            CartesianCoordinate: The rotated vector.
        """
        normalised = self.normalise()

        q = Quaternion(0.0, vector["x"], vector["y"], vector["z"])

        rotated = normalised @ q @ normalised.conjugate()

        return CartesianCoordinate(
            x=rotated.x,
            y=rotated.y,
            z=rotated.z,
        )

    @classmethod
    def identity(cls) -> "Quaternion":
        """
        Returns the identity quaternion.

        Returns:
            Quaternion: The identity quaternion.
        """
        return cls(1.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_axis_angle(axis: CartesianCoordinate, angle: float) -> "Quaternion":
        """
        Creates a quaternion from an axis-angle representation.

        Conventions:
            Right-hand active rotation rule applies for the direction of rotation.
            The axis is a 3D vector representing the axis of rotation.
            The axis may be non-unit; it will be normalised internally.
            The angle is in degrees.

        Args:
            axis (CartesianCoordinate): The axis of rotation.
            angle (float): The rotation angle, (in degrees).
        """
        # Calculate the normalised axis:
        normal = vector_normalise(axis)

        # Calculate the half-angle value:
        half_angle = angle / 2.0

        # Calculate the sine of the half-angle:
        s = sin(radians(half_angle))

        return Quaternion(
            w=cos(radians(half_angle)),
            x=normal["x"] * s,
            y=normal["y"] * s,
            z=normal["z"] * s,
        )

    @staticmethod
    def from_rotation_matrix(
        matrix: Matrix3x3,
    ) -> "Quaternion":
        """
        Creates a quaternion from a rotation matrix.

        Args:
            matrix (Matrix3x3): The rotation matrix.

        Returns:
            Quaternion: The resulting quaternion.
        """
        r00, r01, r02 = matrix[0]
        r10, r11, r12 = matrix[1]
        r20, r21, r22 = matrix[2]

        trace = r00 + r11 + r22

        # Best numerical stability when the trace is positive. Suitable when the
        # orientation is near the identity.
        if trace > 0.0:
            s = sqrt(trace + 1.0) * 2.0
            w = 0.25 * s
            x = (r21 - r12) / s
            y = (r02 - r20) / s
            z = (r10 - r01) / s

        # Largest diagonal entry is r00, implying the major rotation component is
        # about X:
        elif (r00 > r11) and (r00 > r22):
            s = sqrt(1.0 + r00 - r11 - r22) * 2.0
            w = (r21 - r12) / s
            x = 0.25 * s
            y = (r01 + r10) / s
            z = (r02 + r20) / s

        # Largest diagonal entry is r11, implying the major rotation component is
        # about Y:
        elif r11 > r22:
            s = sqrt(1.0 + r11 - r00 - r22) * 2.0
            w = (r02 - r20) / s
            x = (r01 + r10) / s
            y = 0.25 * s
            z = (r12 + r21) / s

        # Largest diagonal entry is r22, implying the major rotation component is
        # about Z:
        else:
            s = sqrt(1.0 + r22 - r00 - r11) * 2.0
            w = (r10 - r01) / s
            x = (r02 + r20) / s
            y = (r12 + r21) / s
            z = 0.25 * s

        # Normalise to guard against numerical drift / non-ideal inputs:
        magnitude = sqrt(w**2 + x**2 + y**2 + z**2)

        if isclose(magnitude, 0.0, abs_tol=TOLERANCE):
            raise ValueError(
                "Cannot create quaternion from zero-length rotation matrix."
            )

        return Quaternion(
            w=w / magnitude,
            x=x / magnitude,
            y=y / magnitude,
            z=z / magnitude,
        )

    @staticmethod
    def from_euler_rotation(
        rotation: EulerRotation,
        order: QuaternionEulerOrder = QuaternionEulerOrder.YAW_PITCH_ROLL,
        kind: QuaternionEulerKind = QuaternionEulerKind.INTRINSIC,
    ) -> "Quaternion":
        """
        Creates a quaternion from Euler angles.

        Conventions:
            Right-hand active rotation rule applies for the direction of rotation.
            Intrinsic rotations (rotations are applied in the rotating frame).
            Rotation order: yaw (Z), then pitch (Y), then roll (X).
            The roll, pitch and yaw angles are in degrees.

        Args:
            rotation (EulerRotation): The Euler rotation angles.
            order (QuaternionEulerOrder): The order of Euler rotations.
            kind (QuaternionEulerKind): The kind of Euler rotations.

        Returns:
            Quaternion: The resulting quaternion.
        """
        x_axis = CartesianCoordinate(x=1.0, y=0.0, z=0.0)

        y_axis = CartesianCoordinate(x=0.0, y=1.0, z=0.0)

        z_axis = CartesianCoordinate(x=0.0, y=0.0, z=1.0)

        roll = rotation["roll"]

        pitch = rotation["pitch"]

        yaw = rotation["yaw"]

        angle_by_axis: Dict[
            Literal["x", "y", "z"], Tuple[float, CartesianCoordinate]
        ] = {
            "x": (roll, x_axis),
            "y": (pitch, y_axis),
            "z": (yaw, z_axis),
        }

        factors: list[Quaternion] = []

        for axis in order.value:
            angle, vector = angle_by_axis[cast(Literal["x", "y", "z"], axis)]

            factors.append(Quaternion.from_axis_angle(vector, angle))

        if kind.value == "intrinsic":
            q = factors[0] * factors[1] * factors[2]
        elif kind.value == "extrinsic":
            q = factors[2] * factors[1] * factors[0]
        else:
            raise ValueError("kind must be 'intrinsic' or 'extrinsic'.")

        return q.normalise()


# **************************************************************************************
