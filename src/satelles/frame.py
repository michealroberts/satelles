# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable

from .common import CartesianCoordinate
from .quaternion import Quaternion

# **************************************************************************************


class Reference(Enum):
    """
    Common reference frames used in satellite and celestial orbital mechanics.
    """

    # Earth Centered Inertial:
    ECI = "ECI"

    # Earth Centered Earth Fixed:
    ECEF = "ECEF"

    # International Celestial Reference Frame:
    ICRF = "ICRF"

    # International Terrestrial Reference Frame:
    ITRF = "ITRF"

    # Earth Mean Equator 2000:
    EME2000 = "EME2000"

    # True Equator Mean Equinox:
    TEME = "TEME"

    # Topocentric (e.g., observer's local horizon):
    TOPOCENTRIC = "TOPOCENTRIC"

    @property
    def is_inertial(self) -> bool:
        """
        Whether this reference frame is inertial (non-rotating) or not.
        """
        return self in {
            Reference.ECI,
            Reference.ICRF,
            Reference.EME2000,
            Reference.TEME,
        }

    @property
    def is_rotating(self) -> bool:
        """
        Whether this reference frame is rotating with the Earth or not.
        """
        return self in {
            Reference.ECEF,
            Reference.ITRF,
            Reference.TOPOCENTRIC,
        }


# **************************************************************************************


@dataclass(frozen=True)
class Transform:
    """
    A class representing a coordinate transformation between reference frames.
    """

    # The rotation from source to target frame:
    rotation: Quaternion

    # The translation vector from source to target frame:
    translation: CartesianCoordinate

    def apply_to_position(self, position: CartesianCoordinate) -> CartesianCoordinate:
        """
        Apply this transform to a position vector in the source frame.

        Args:
            position (CartesianCoordinate): The position vector in the source frame.

        Returns:
            CartesianCoordinate: The position vector in the target frame.
        """
        # Rotate the position into the target-frame axes:
        rotated = self.rotation.rotate_vector(position)

        # Apply the translation in the target frame:
        return CartesianCoordinate(
            x=rotated["x"] + self.translation["x"],
            y=rotated["y"] + self.translation["y"],
            z=rotated["z"] + self.translation["z"],
        )

    def inverse(self) -> "Transform":
        """
        Return the inverse transform (target -> source).
        """
        # Invert the rotation:
        rotation = self.rotation.inverse()

        # Rotate the inverse position into the target frame:
        translated = rotation.rotate_vector(self.translation)

        # Invert the translation:
        translation = CartesianCoordinate(
            x=-translated["x"],
            y=-translated["y"],
            z=-translated["z"],
        )

        return Transform(
            rotation=rotation,
            translation=translation,
        )

    def compose(self, other: "Transform") -> "Transform":
        """
        Compose two transforms (this: B->C, other: A->B) to get a new transform (A->C).

        Args:
            other (Transform): The transform to apply to the source of this transform.

        Returns:
            Transform: The composed transform from source of other to target of this.
        """
        # Rotate other's translation into this transform's target frame:
        translated = self.rotation.rotate_vector(other.translation)

        translation = CartesianCoordinate(
            x=translated["x"] + self.translation["x"],
            y=translated["y"] + self.translation["y"],
            z=translated["z"] + self.translation["z"],
        )

        return Transform(
            rotation=self.rotation * other.rotation,
            translation=translation,
        )


# **************************************************************************************

TransformProvider = Callable[[datetime], Transform]

# **************************************************************************************
