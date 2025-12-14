# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional

from .body import Body
from .common import CartesianCoordinate
from .origin import Origin
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


@dataclass(frozen=True)
class Frame:
    """
    A class representing a reference frame for positions and velocities.
    """

    # The reference model for this frame, e.g., "ECI", "ECEF", etc.:
    reference: Reference

    # The origin for this frame (a Body or an Origin), e.g., "Earth", "Moon", or a
    # specific origin point:
    origin: Body | Origin

    # Whether this frame is inertial (non-rotating) or not:
    is_inertial: bool

    # The parent frame of this frame (optional), None if this is a root frame:
    parent: Optional["Frame"]

    # Function to get the transform from this frame to its parent frame, for a root
    # frame this should return the identity transform:
    transform_to_parent: TransformProvider

    # Human-readable name for this particular instance of the frame (optional):
    name: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"{self.name} {self.origin.name} {self.reference.value}"
            if self.name
            else f"{self.origin.name} {self.reference.value}"
        )

    def transform_to(self, when: datetime, other: "Frame") -> Transform:
        """
        Get the transform from this frame to another frame at a given time.

        Args:
            when (datetime): The time at which to compute the transform.
            other (Frame): The target frame to transform to.

        Returns:
            Transform: The transform from this frame to the other frame.
        """
        # Handle the case where both frames are the same:
        if self == other:
            return Transform(
                rotation=Quaternion.identity(),
                translation=CartesianCoordinate(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
            )

        ancestors: List[Frame] = []

        # Find the common ancestor frame:
        base: Optional["Frame"] = self

        # Walk up the tree from this frame to the root, collecting ancestors:
        while base is not None:
            ancestors.append(base)
            base = base.parent

        other_ancestors: List[Frame] = []

        base = other

        # Walk up the tree from the other frame to the root, collecting ancestors:
        while base is not None:
            other_ancestors.append(base)
            base = base.parent

        # Find the common ancestor frame:
        common_ancestor: Optional[Frame] = None

        for frame in ancestors:
            if frame in other_ancestors:
                common_ancestor = frame
                break

        # If no common ancestor was found, raise an error (as we cannot transform):
        if common_ancestor is None:
            raise ValueError(
                f"No common ancestor between {self.name or self.reference.value} "
                f"and {other.name or other.reference.value}"
            )

        # Build the transform from this frame up to the common ancestor:
        upward_transform = Transform(
            rotation=Quaternion.identity(),
            translation=CartesianCoordinate(
                x=0.0,
                y=0.0,
                z=0.0,
            ),
        )

        base = self

        # Walk up to the common ancestor, accumulating transforms:
        while base != common_ancestor:
            if not base.parent:
                raise ValueError(
                    "Reached root frame before common ancestor when walking from self."
                )

            transform = base.transform_to_parent(when)
            upward_transform = transform.compose(upward_transform)
            base = base.parent

        # Build the transform from the other frame up to the common ancestor:
        downward_transform = Transform(
            rotation=Quaternion.identity(),
            translation=CartesianCoordinate(
                x=0.0,
                y=0.0,
                z=0.0,
            ),
        )

        base = other

        # Walk up to the common ancestor, accumulating transforms:
        while base != common_ancestor:
            if base.parent is None:
                raise ValueError(
                    "Reached root frame before common ancestor when walking from other."
                )

            step = base.transform_to_parent(when)
            downward_transform = step.compose(downward_transform)
            base = base.parent

        # Invert the downward transform to get from common ancestor to other:
        downward_transform = downward_transform.inverse()

        # Combine the upward and downward transforms to get from this to other:
        return downward_transform.compose(upward_transform)


# **************************************************************************************
