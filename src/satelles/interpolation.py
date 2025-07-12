# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from abc import ABC, abstractmethod
from math import nan
from typing import List

from .models import Position, Velocity

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


class Base3DKinematicInterpolator(ABC):
    """
    Base class for interpolators.

    This class is not intended to be instantiated directly.

    It serves as a base for specific interpolation implementations.
    """

    def __init__(
        self,
        positions: List[Position],
        velocities: List[Velocity],
    ):
        # Ensure we have at least two positions to interpolate:
        if len(positions) < 2:
            raise ValueError("Need at least two positions to interpolate.")

        # Ensure we have at least two velocities to interpolate:
        if len(velocities) < 2:
            raise ValueError("Need at least two velocities to interpolate.")

        # Ensure that the number of positions matches the number of velocities, as well
        # as that they all have the same time attribute 'at':
        if any(
            position.at != velocity.at
            for position, velocity in zip(positions, velocities)
        ):
            raise ValueError(
                "All positions and velocities must have the same time attribute 'at'."
            )

        # Keep the raw list of positions sorted by time; avoids duplicating time/coordinate arrays:
        self.positions: List[Position] = sorted(positions, key=lambda p: p.at)

        # Keep the raw list of velocities sorted by time; avoids duplicating time/coordinate arrays:
        self.velocities: List[Velocity] = sorted(velocities, key=lambda v: v.at)

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


class Hermite3DPositionInterpolator(Base3DPositionInterpolator):
    """
    Cubic Hermite interpolation for 3D positions.

    This class implements cubic Hermite interpolation for 3D positions represented
    by the `Position` class, which includes x, y, z coordinates and a time attribute `at`.
    Velocity at sample points is estimated via finite differences to shape the curve smoothly.
    """

    def __init__(self, positions: List[Position]):
        super().__init__(positions)

        # Prepare and compute velocity estimates at each sample via finite differences:
        self.velocities: List[Velocity] = self._get_derived_velocities()

    def _get_derived_velocities(self) -> List[Velocity]:
        """
        Prepare and compute velocity estimates for each position.

        Returns:
            List[Velocity]: List of estimated velocities corresponding to each position.
        """
        n = len(self.positions)

        velocities: List[Velocity] = []

        for i, position in enumerate(self.positions):
            t_i = position.at

            # Estimate derivative at the start via forward difference:
            if i == 0:
                position_next = self.positions[1]
                dt = position_next.at - t_i

                if dt == 0:
                    raise ValueError(
                        f"Division by zero detected: position_next.at ({position_next.at}) and t_i ({t_i}) are equal."
                    )

                vx = (position_next.x - position.x) / dt
                vy = (position_next.y - position.y) / dt
                vz = (position_next.z - position.z) / dt
            # Estimate derivative at the end via backward difference:
            elif i == n - 1:
                position_previous = self.positions[-2]
                dt = t_i - position_previous.at
                vx = (position.x - position_previous.x) / dt
                vy = (position.y - position_previous.y) / dt
                vz = (position.z - position_previous.z) / dt
            # Estimate derivative in the interior via central difference:
            else:
                position_previous = self.positions[i - 1]
                position_next = self.positions[i + 1]
                dt = position_next.at - position_previous.at
                vx = (position_next.x - position_previous.x) / dt
                vy = (position_next.y - position_previous.y) / dt
                vz = (position_next.z - position_previous.z) / dt

            velocities.append(Velocity(at=t_i, vx=vx, vy=vy, vz=vz))

        return velocities

    def get_interpolated_position(self, at: float) -> Position:
        """
        Get the interpolated position at the specified time 'at'.

        Args:
            at (float): The time at which to interpolate the position.

        Returns:
            Position: The interpolated position at the specified time.
        """
        # Raise error if 'at' is before the first sample time:
        if at < self.positions[0].at:
            raise ValueError(
                f"Cannot interpolate before the first sample time: {self.positions[0].at}"
            )

        # Raise error if 'at' is after the last sample time:
        if at > self.positions[-1].at:
            raise ValueError(
                f"Cannot interpolate after the last sample time: {self.positions[-1].at}"
            )

        # Initialize position coordinates to NaN as the fallback:
        x = y = z = nan

        # Find the interval that contains 'at':
        for i in range(len(self.positions) - 1):
            position = self.positions[i]
            position_next = self.positions[i + 1]
            t_i, t_j = position.at, position_next.at

            # Skip intervals that do not contain the query time:
            if not (t_i <= at <= t_j):
                continue

            # Calculate the normalized time (tau) within the interval [t0, t1]:
            dt = position_next.at - t_i

            if abs(dt) < 1e-10:
                # If the time difference is too small, use the first position:
                return Position(
                    x=position.x,
                    y=position.y,
                    z=position.z,
                    at=t_i,
                )

            τ = (at - t_i) / dt

            # Calculate Hermite basis functions for cubic interpolation:
            h00 = 2 * τ**3 - 3 * τ**2 + 1
            h10 = τ**3 - 2 * τ**2 + τ
            h01 = -2 * τ**3 + 3 * τ**2
            h11 = τ**3 - τ**2

            # Retrieve precomputed velocity estimates:
            v0 = self.velocities[i]
            v1 = self.velocities[i + 1]

            # Interpolate the position using the Hermite basis functions:
            x = (
                h00 * position.x
                + h10 * v0.vx * dt
                + h01 * position_next.x
                + h11 * v1.vx * dt
            )

            y = (
                h00 * position.y
                + h10 * v0.vy * dt
                + h01 * position_next.y
                + h11 * v1.vy * dt
            )

            z = (
                h00 * position.z
                + h10 * v0.vz * dt
                + h01 * position_next.z
                + h11 * v1.vz * dt
            )
            break

        return Position(x=x, y=y, z=z, at=at)


# **************************************************************************************
