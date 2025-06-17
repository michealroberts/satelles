# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from abc import ABC, abstractmethod
from math import nan
from typing import List

from .models import Position

# **************************************************************************************


class Base3DPositionInterpolator(ABC):
    """
    Base class for interpolators.

    This class is not intended to be instantiated directly.

    It serves as a base for specific interpolation implementations.
    """

    def __init__(self, positions: List[Position]):
        if len(positions) < 2:
            raise ValueError("Need at least two positions to interpolate.")

        # Keep the raw list of positions sorted by time; avoids duplicating time/coordinate arrays:
        self.positions: List[Position] = sorted(positions, key=lambda p: p.at)

    @abstractmethod
    def get_interpolated_position(self, at: float) -> Position:
        """
        Get the interpolated position at the specified time 'at'.

        Args:
            at (float): The time at which to interpolate the position.

        Returns:
            Position: The interpolated position at the specified time.
        """
        raise NotImplementedError(
            "get_interpolated_position() must be implemented in the subclass."
        )


# **************************************************************************************


class BarycentricLagrange3DPositionInterpolator(Base3DPositionInterpolator):
    """
    Barycentric Lagrange interpolation for 3D positions.

    This class implements barycentric Lagrange interpolation for 3D positions
    represented by the `Position` class, which includes x, y, z coordinates and a time
    attribute `at` (typically a float representing Modified Julian Date or seconds since
    epoch).

    The interpolation is performed using precomputed barycentric weights based on the
    sample times, allowing efficient interpolation across multiple dimensions (x, y, z)
    without needing to recompute time lists for each dimension.
    """

    def __init__(self, positions: List[Position]):
        super().__init__(positions)

        # Prepare and compute one barycentric weight per position, based solely on the
        # time attribute `at`:
        self.weights: List[float] = self._prepare_basis_weights()

    def _prepare_basis_weights(self) -> List[float]:
        """
        Prepare and compute barycentric weights for the given positions.

        These weights reflect only the time geometry, so they can be reused across x, y,
        and z interpolation without recomputing time lists.

        Returns:
            List[float]: List of barycentric weights corresponding to each sample.
        """
        weights: List[float] = [1.0] * len(self.positions)

        for i, position_i in enumerate(self.positions):
            at = position_i.at
            product = 1.0
            for j, position_j in enumerate(self.positions):
                if j == i:
                    continue
                product *= at - position_j.at

            weights[i] = 1.0 / product

        return weights

    def get_interpolated_position(self, at: float) -> Position:
        """
        Get the interpolated position at the specified time 'at'.

        Args:
            at (float): The time at which to interpolate the position.

        Returns:
            Position: The interpolated position at the specified time.
        """
        x = y = z = 0.0

        denominator = 0.0

        for position, weight in zip(self.positions, self.weights):
            # If we are at an exact position time, return a new Position instance:
            if at == position.at:
                return Position(
                    x=position.x,
                    y=position.y,
                    z=position.z,
                    at=position.at,
                )

            factor = weight / (at - position.at)
            x += factor * position.x
            y += factor * position.y
            z += factor * position.z

            denominator += factor

        x = x / denominator if denominator != 0 else nan
        y = y / denominator if denominator != 0 else nan
        z = z / denominator if denominator != 0 else nan

        # Final interpolated Position at the specified time 'at':
        # Note: We assume 'at' is a float representing Modified Julian Date (MJD), or a
        # datetime timestamp in seconds since the epoch.
        return Position(
            x=x,
            y=y,
            z=z,
            at=at,
        )


# **************************************************************************************
