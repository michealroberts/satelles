# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.matrix import (
    get_rotation_matrix_x,
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
# **************************************************************************************



if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
