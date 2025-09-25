# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import math
import unittest

from satelles import (
    CartesianCoordinate,
    normalise,
    rotate,
)

# **************************************************************************************


class TestNormaliseFunction(unittest.TestCase):
    def test_normalise_non_zero_vector(self):
        """
        Normalise a non-zero vector (3, 4, 0).
        Expected result: (0.6, 0.8, 0.0)
        """
        vector = CartesianCoordinate(x=3.0, y=4.0, z=0.0)
        result = normalise(vector)
        self.assertAlmostEqual(result["x"], 0.6, places=6)
        self.assertAlmostEqual(result["y"], 0.8, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_normalise_zero_vector(self):
        """
        Verify that normalising a zero-length vector raises a ValueError.
        """
        vector = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        with self.assertRaises(ValueError):
            normalise(vector)

    def test_normalise_negative_components(self):
        """
        Normalise a vector with negative components (-1, -1, -1).
        Expected result: (-0.577350, -0.577350, -0.577350)
        """
        vector = CartesianCoordinate(x=-1.0, y=-1.0, z=-1.0)
        result = normalise(vector)
        magnitude = -1.0 / math.sqrt(3)
        self.assertAlmostEqual(result["x"], magnitude, places=6)
        self.assertAlmostEqual(result["y"], magnitude, places=6)
        self.assertAlmostEqual(result["z"], magnitude, places=6)


# **************************************************************************************


class TestRotateFunction(unittest.TestCase):
    def test_rotate_z_axis(self):
        """
        Rotate the vector (1, 0, 0) by 90 degrees about the z-axis.
        Expected result: (0, 1, 0)
        """
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        angle_degrees = math.degrees(math.pi / 2)  # 90 degrees
        result = rotate(vector, angle_degrees, "z")
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 1.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_rotate_x_axis(self):
        """
        Rotate the vector (0, 1, 0) by 90 degrees about the x-axis.
        Expected result: (0, 0, 1)
        """
        vector = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        angle_degrees = math.degrees(math.pi / 2)  # 90 degrees
        result = rotate(vector, angle_degrees, "x")
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 1.0, places=6)

    def test_rotate_y_axis(self):
        """
        Rotate the vector (1, 0, 0) by 90 degrees about the y-axis.
        Expected result: (0, 0, -1)
        """
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        angle_degrees = math.degrees(math.pi / 2)  # 90 degrees
        result = rotate(vector, angle_degrees, "y")
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], -1.0, places=6)

    def test_rotate_negative_angle(self):
        """
        Rotate the vector (1, 0, 0) by -90 degrees about the z-axis.
        Expected result: (0, -1, 0)
        """
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        angle_degrees = math.degrees(-math.pi / 2)  # -90 degrees
        result = rotate(vector, angle_degrees, "z")
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], -1.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_invalid_axis(self):
        """
        Verify that passing an invalid axis raises a ValueError.
        """
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        with self.assertRaises(ValueError):
            rotate(vector, 45, "a")  # "a" is not a valid axis


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
