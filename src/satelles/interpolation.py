# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from abc import ABC, abstractmethod
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

        # Keep the raw list of positions sorted by time; avoids duplicating time/coordinate arrays
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
