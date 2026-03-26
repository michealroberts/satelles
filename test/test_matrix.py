# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.matrix import (
    get_rotation_matrix_x,
    get_rotation_matrix_y,
    get_rotation_matrix_z,
    multiply,
)

# **************************************************************************************


class TestGetRotationMatrixX(unittest.TestCase):
    def test_get_rotation_matrix_x_0(self) -> None:
        matrix = get_rotation_matrix_x(0.0)

        expected = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_x_90(self) -> None:
        matrix = get_rotation_matrix_x(90.0)

        expected = (
            (1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
            (0.0, 1.0, 0.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_x_180(self) -> None:
        matrix = get_rotation_matrix_x(180.0)

        expected = (
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, -1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)


# **************************************************************************************


class TestGetRotationMatrixY(unittest.TestCase):
    def test_get_rotation_matrix_y_0(self) -> None:
        matrix = get_rotation_matrix_y(0.0)

        expected = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_y_90(self) -> None:
        matrix = get_rotation_matrix_y(90.0)

        expected = (
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
            (-1.0, 0.0, 0.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_y_minus_90(self) -> None:
        matrix = get_rotation_matrix_y(-90.0)

        expected = (
            (0.0, 0.0, -1.0),
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)


# **************************************************************************************


class TestGetRotationMatrixZ(unittest.TestCase):
    def test_get_rotation_matrix_z_0(self) -> None:
        matrix = get_rotation_matrix_z(0.0)

        expected = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_z_90(self) -> None:
        matrix = get_rotation_matrix_z(90.0)

        expected = (
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_get_rotation_matrix_z_180(self) -> None:
        matrix = get_rotation_matrix_z(180.0)

        expected = (
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        for row, expected_row in zip(matrix, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)


# **************************************************************************************


class TestMultiply(unittest.TestCase):
    def test_multiply_by_identity_returns_original(self) -> None:
        identity = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        matrix = get_rotation_matrix_z(90.0)

        self.assertEqual(multiply(identity, matrix), matrix)
        self.assertEqual(multiply(matrix, identity), matrix)

    def test_multiply_identity_by_identity_returns_identity(self) -> None:
        identity = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        result = multiply(identity, identity)

        for row, expected_row in zip(result, identity):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)

    def test_multiply_composes_z_90_and_y_90(self) -> None:
        result = multiply(
            get_rotation_matrix_z(90.0),
            get_rotation_matrix_y(90.0),
        )

        expected = (
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 1.0),
            (-1.0, 0.0, 0.0),
        )

        for row, expected_row in zip(result, expected):
            for value, expected_value in zip(row, expected_row):
                self.assertAlmostEqual(value, expected_value, places=12)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
