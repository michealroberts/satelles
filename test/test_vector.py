# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import math
import unittest

from satelles import (
    CartesianCoordinate,
    add,
    angle,
    cross,
    dilate,
    distance,
    dot,
    normalise,
    project,
    reject,
    rotate,
    subtract,
)

# **************************************************************************************


class TestAddFunction(unittest.TestCase):
    def test_add_positive_vectors(self):
        """
        Add two positive vectors (1, 2, 3) + (4, 5, 6).
        Expected result: (5, 7, 9)
        """
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        delta = CartesianCoordinate(x=4.0, y=5.0, z=6.0)
        result = add(vector, delta)
        self.assertAlmostEqual(result["x"], 5.0, places=6)
        self.assertAlmostEqual(result["y"], 7.0, places=6)
        self.assertAlmostEqual(result["z"], 9.0, places=6)

    def test_add_negative_vectors(self):
        """
        Add two negative vectors (-1, -2, -3) + (-4, -5, -6).
        Expected result: (-5, -7, -9)
        """
        vector = CartesianCoordinate(x=-1.0, y=-2.0, z=-3.0)
        delta = CartesianCoordinate(x=-4.0, y=-5.0, z=-6.0)
        result = add(vector, delta)
        self.assertAlmostEqual(result["x"], -5.0, places=6)
        self.assertAlmostEqual(result["y"], -7.0, places=6)
        self.assertAlmostEqual(result["z"], -9.0, places=6)

    def test_add_mixed_vectors(self):
        """
        Add mixed vectors (1, -2, 3) + (-4, 5, -6).
        Expected result: (-3, 3, -3)
        """
        vector = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        delta = CartesianCoordinate(x=-4.0, y=5.0, z=-6.0)
        result = add(vector, delta)
        self.assertAlmostEqual(result["x"], -3.0, places=6)
        self.assertAlmostEqual(result["y"], 3.0, places=6)
        self.assertAlmostEqual(result["z"], -3.0, places=6)


# **************************************************************************************


class TestSubtractFunction(unittest.TestCase):
    def test_subtract_positive_vectors(self):
        """
        Subtract two positive vectors (5, 7, 9) - (1, 2, 3).
        Expected result: (4, 5, 6)
        """
        vector = CartesianCoordinate(x=5.0, y=7.0, z=9.0)
        delta = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        result = subtract(vector, delta)
        self.assertAlmostEqual(result["x"], 4.0, places=6)
        self.assertAlmostEqual(result["y"], 5.0, places=6)
        self.assertAlmostEqual(result["z"], 6.0, places=6)

    def test_subtract_negative_vectors(self):
        """
        Subtract two negative vectors (-1, -2, -3) - (-4, -5, -6).
        Expected result: (3, 3, 3)
        """
        vector = CartesianCoordinate(x=-1.0, y=-2.0, z=-3.0)
        delta = CartesianCoordinate(x=-4.0, y=-5.0, z=-6.0)
        result = subtract(vector, delta)
        self.assertAlmostEqual(result["x"], 3.0, places=6)
        self.assertAlmostEqual(result["y"], 3.0, places=6)
        self.assertAlmostEqual(result["z"], 3.0, places=6)

    def test_subtract_mixed_vectors(self):
        """
        Subtract mixed vectors (1, -2, 3) - (-4, 5, -6).
        Expected result: (5, -7, 9)
        """
        vector = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        delta = CartesianCoordinate(x=-4.0, y=5.0, z=-6.0)
        result = subtract(vector, delta)
        self.assertAlmostEqual(result["x"], 5.0, places=6)
        self.assertAlmostEqual(result["y"], -7.0, places=6)
        self.assertAlmostEqual(result["z"], 9.0, places=6)


# **************************************************************************************


class TestDilateFunction(unittest.TestCase):
    def test_dilate_positive_vector(self):
        """
        Dilate a positive vector (1, 2, 3) by a scale of 2.
        Expected result: (2, 4, 6)
        """
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        scale = 2.0
        result = dilate(vector, scale)
        self.assertAlmostEqual(result["x"], 2.0, places=6)
        self.assertAlmostEqual(result["y"], 4.0, places=6)
        self.assertAlmostEqual(result["z"], 6.0, places=6)

    def test_dilate_negative_vector(self):
        """
        Dilate a negative vector (-1, -2, -3) by a scale of 3.
        Expected result: (-3, -6, -9)
        """
        vector = CartesianCoordinate(x=-1.0, y=-2.0, z=-3.0)
        scale = 3.0
        result = dilate(vector, scale)
        self.assertAlmostEqual(result["x"], -3.0, places=6)
        self.assertAlmostEqual(result["y"], -6.0, places=6)
        self.assertAlmostEqual(result["z"], -9.0, places=6)

    def test_dilate_zero_vector(self):
        """
        Dilate the zero vector (0, 0, 0) by any scale (e.g., 5).
        Expected result: (0, 0, 0)
        """
        vector = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        scale = 5.0
        result = dilate(vector, scale)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)


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


class TestDistanceFunction(unittest.TestCase):
    def test_distance_between_points(self):
        """
        Distance between two points (1, 2, 3) and (4, 5, 6).
        Expected result: sqrt((4-1)^2 + (5-2)^2 + (6-3)^2) = sqrt(27) = 5.196152
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=4.0, y=5.0, z=6.0)
        result = distance(i, j)
        self.assertAlmostEqual(result, math.sqrt(27), places=6)

    def test_distance_same_point(self):
        """
        Distance between the same point (1, 2, 3) and (1, 2, 3).
        Expected result: 0
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        result = distance(i, j)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_distance_negative_coordinates(self):
        """
        Distance between points with negative coordinates (-1, -2, -3) and (4, 5, 6).
        Expected result: sqrt((4+1)^2 + (5+2)^2 + (6+3)^2) = sqrt(155) = 12.449900
        """
        i = CartesianCoordinate(x=-1.0, y=-2.0, z=-3.0)
        j = CartesianCoordinate(x=4.0, y=5.0, z=6.0)
        result = distance(i, j)
        self.assertAlmostEqual(result, math.sqrt(155), places=6)

    def test_distance_mixed_coordinates(self):
        """
        Distance between points with mixed coordinates (1, -2, 3) and (-4, 5, -6).
        Expected result: sqrt((-4-1)^2 + (5+2)^2 + (-6-3)^2) = sqrt(155) = 12.449900
        """
        i = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        j = CartesianCoordinate(x=-4.0, y=5.0, z=-6.0)
        result = distance(i, j)
        self.assertAlmostEqual(result, math.sqrt(155), places=6)


# **************************************************************************************


class TestDotFunction(unittest.TestCase):
    def test_dot_orthogonal_vectors(self):
        """
        Dot product of orthogonal vectors (1, 0, 0) · (0, 1, 0).
        Expected result: 0
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        result = dot(i, j)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_dot_parallel_vectors(self):
        """
        Dot product of parallel vectors (1, 2, 3) · (1, 2, 3).
        Expected result: 1^2 + 2^2 + 3^2 = 14
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        result = dot(i, j)
        self.assertAlmostEqual(result, 14.0, places=6)

    def test_dot_antiparallel_vectors(self):
        """
        Dot product of opposite vectors (1, 0, 0) · (-1, 0, 0).
        Expected result: -1
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=-1.0, y=0.0, z=0.0)
        result = dot(i, j)
        self.assertAlmostEqual(result, -1.0, places=6)

    def test_dot_with_zero_vector(self):
        """
        Dot product of any vector with the zero vector.
        Expected result: 0
        """
        i = CartesianCoordinate(x=5.0, y=-3.0, z=2.0)
        j = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        result = dot(i, j)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_dot_negative_components(self):
        """
        Dot product with negative components: (1, -2, 3) · (-4, 5, -6).
        Expected result: (1 * -4) + (-2 * 5) + (3 * -6) = -4 -10 -18 = -32
        """
        i = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        j = CartesianCoordinate(x=-4.0, y=5.0, z=-6.0)
        result = dot(i, j)
        self.assertAlmostEqual(result, -32.0, places=6)


# **************************************************************************************


class TestCrossFunction(unittest.TestCase):
    def test_cross_orthogonal_vectors(self):
        """
        Cross product of orthogonal vectors (1, 0, 0) x (0, 1, 0).
        Expected result: (0, 0, 1)
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 1.0, places=6)

    def test_cross_non_orthogonal_vectors(self):
        """
        Cross product of non-orthogonal vectors (1, 2, 3) x (4, 5, 6).
        Expected result: (-3, 6, -3)
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=4.0, y=5.0, z=6.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], -3.0, places=6)
        self.assertAlmostEqual(result["y"], 6.0, places=6)
        self.assertAlmostEqual(result["z"], -3.0, places=6)

    def test_cross_parallel_vectors(self):
        """
        Cross product of parallel vectors (1, 2, 3) x (2, 4, 6).
        Expected result: (0, 0, 0)
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=2.0, y=4.0, z=6.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_cross_antiparallel_vectors(self):
        """
        Cross product of opposite vectors (1, 0, 0) x (-1, 0, 0).
        Expected result: (0, 0, 0)
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=-1.0, y=0.0, z=0.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_cross_zero_vector(self):
        """
        Cross product of any vector with the zero vector.
        Expected result: (0, 0, 0)
        """
        i = CartesianCoordinate(x=5.0, y=-3.0, z=2.0)
        j = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_cross_negative_components(self):
        """
        Cross product with negative components: (1, -2, 3) x (-4, 5, -6).
        Expected result: (-3, -6, -3)
        """
        i = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        j = CartesianCoordinate(x=-4.0, y=5.0, z=-6.0)
        result = cross(i, j)
        self.assertAlmostEqual(result["x"], -3.0, places=6)
        self.assertAlmostEqual(result["y"], -6.0, places=6)
        self.assertAlmostEqual(result["z"], -3.0, places=6)


# **************************************************************************************


class TestAngleFunction(unittest.TestCase):
    def test_angle_between_perpendicular_vectors(self):
        """
        Angle between perpendicular vectors (1, 0, 0) and (0, 1, 0).
        Expected result: 90 degrees
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        result = angle(i, j)
        self.assertAlmostEqual(result, 90.0, places=6)

    def test_angle_between_parallel_vectors(self):
        """
        Angle between parallel vectors (1, 2, 3) and (2, 4, 6).
        Expected result: 0 degrees
        """
        i = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        j = CartesianCoordinate(x=2.0, y=4.0, z=6.0)
        result = angle(i, j)
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_angle_between_antiparallel_vectors(self):
        """
        Angle between opposite vectors (1, 0, 0) and (-1, 0, 0).
        Expected result: 180 degrees
        """
        i = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        j = CartesianCoordinate(x=-1.0, y=0.0, z=0.0)
        result = angle(i, j)
        self.assertAlmostEqual(result, 180.0, places=6)


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


class TestProjectFunction(unittest.TestCase):
    def test_project_onto_parallel_vector(self):
        """
        Project (2, 4, 6) onto (1, 2, 3).
        Expected result: (2, 4, 6) because they are parallel.
        """
        vector = CartesianCoordinate(x=2.0, y=4.0, z=6.0)
        onto = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        result = project(vector, onto)
        self.assertAlmostEqual(result["x"], 2.0, places=6)
        self.assertAlmostEqual(result["y"], 4.0, places=6)
        self.assertAlmostEqual(result["z"], 6.0, places=6)

    def test_project_onto_orthogonal_vector(self):
        """
        Project (1, 0, 0) onto (0, 1, 0).
        Expected result: (0, 0, 0) because they are orthogonal.
        """
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        onto = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        result = project(vector, onto)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_project_onto_non_unit_vector(self):
        """
        Project (3, 3, 0) onto (1, 0, 0).
        Expected result: (3, 0, 0).
        """
        vector = CartesianCoordinate(x=3.0, y=3.0, z=0.0)
        onto = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        result = project(vector, onto)
        self.assertAlmostEqual(result["x"], 3.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_project_negative_components(self):
        """
        Project (-3, 6, -9) onto (1, -2, 3).
        Expected: parallel vector scaled correctly.
        """
        vector = CartesianCoordinate(x=-3.0, y=6.0, z=-9.0)
        onto = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        result = project(vector, onto)
        # The input is exactly -3 * onto, so projection = vector
        self.assertAlmostEqual(result["x"], -3.0, places=6)
        self.assertAlmostEqual(result["y"], 6.0, places=6)
        self.assertAlmostEqual(result["z"], -9.0, places=6)

    def test_project_zero_vector_onto_anything(self):
        """
        Project (0, 0, 0) onto any non-zero vector.
        Expected result: (0, 0, 0)
        """
        vector = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        onto = CartesianCoordinate(x=1.0, y=1.0, z=1.0)
        result = project(vector, onto)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_project_onto_zero_vector_raises(self):
        """
        Projection onto a zero vector must raise ValueError.
        """
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        onto = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        with self.assertRaises(ValueError):
            project(vector, onto)


# **************************************************************************************


class TestRejectFunction(unittest.TestCase):
    def test_reject_from_parallel_vector(self):
        """
        Reject (2, 4, 6) from (1, 2, 3).
        Expected result: (0, 0, 0) because they are parallel (projection equals the vector).
        """
        vector = CartesianCoordinate(x=2.0, y=4.0, z=6.0)
        base = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        result = reject(vector, base)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_reject_from_orthogonal_vector(self):
        """
        Reject (1, 0, 0) from (0, 1, 0).
        Expected result: (1, 0, 0) because projection is zero.
        """
        vector = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        base = CartesianCoordinate(x=0.0, y=1.0, z=0.0)
        result = reject(vector, base)
        self.assertAlmostEqual(result["x"], 1.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_reject_from_non_unit_vector(self):
        """
        Reject (3, 3, 0) from (1, 0, 0).
        Expected result: (0, 3, 0).
        """
        vector = CartesianCoordinate(x=3.0, y=3.0, z=0.0)
        base = CartesianCoordinate(x=1.0, y=0.0, z=0.0)
        result = reject(vector, base)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 3.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_reject_negative_components(self):
        """
        Reject (-3, 6, -9) from (1, -2, 3).
        Expected result: (0, 0, 0) because the vector is exactly -3 * base.
        """
        vector = CartesianCoordinate(x=-3.0, y=6.0, z=-9.0)
        base = CartesianCoordinate(x=1.0, y=-2.0, z=3.0)
        result = reject(vector, base)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_reject_zero_vector_from_anything(self):
        """
        Reject (0, 0, 0) from any non-zero vector.
        Expected result: (0, 0, 0)
        """
        vector = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        base = CartesianCoordinate(x=1.0, y=1.0, z=1.0)
        result = reject(vector, base)
        self.assertAlmostEqual(result["x"], 0.0, places=6)
        self.assertAlmostEqual(result["y"], 0.0, places=6)
        self.assertAlmostEqual(result["z"], 0.0, places=6)

    def test_reject_from_zero_vector_raises(self):
        """
        Rejection relative to a zero vector must raise ValueError
        (because projection onto a zero vector is undefined).
        """
        vector = CartesianCoordinate(x=1.0, y=2.0, z=3.0)
        base = CartesianCoordinate(x=0.0, y=0.0, z=0.0)
        with self.assertRaises(ValueError):
            reject(vector, base)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
