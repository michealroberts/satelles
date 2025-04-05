# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from typing import Any, Dict

from pydantic import ValidationError

from satelles import Covariance

# **************************************************************************************


class TestCovarianceFields(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_covariance_data: Dict[str, Any] = {
            "reference_frame": "TEME",
            "cx_x": 3.331349476038534e-04,
            "cy_x": 4.618927349220216e-04,
            "cy_y": 6.782421679971363e-04,
            "cz_x": -3.070007847730449e-04,
            "cz_y": -4.221234189514228e-04,
            "cz_z": 3.231931992380369e-04,
            "cx_dot_x": -3.349365033922630e-07,
            "cx_dot_y": -4.686084221046758e-07,
            "cx_dot_z": 2.484949578400095e-07,
            "cy_dot_x": -2.211832501084875e-07,
            "cy_dot_y": -2.864186892102733e-07,
            "cy_dot_z": 1.798098699846038e-07,
            "cz_dot_x": -3.041346050686871e-07,
            "cz_dot_y": -4.989496988610662e-07,
            "cz_dot_z": 3.540310904497689e-07,
            "cx_dot_x_dot": 4.296022805587290e-10,
            "cy_dot_x_dot": 2.608899201686016e-10,
            "cy_dot_y_dot": 1.767514756338532e-10,
            "cz_dot_x_dot": 1.869263192954590e-10,
            "cz_dot_y_dot": 1.008862586240695e-10,
            "cz_dot_z_dot": 6.224444338635500e-10,
        }

    def test_valid_covariance(self) -> None:
        covariance = Covariance(**self.valid_covariance_data)
        self.assertEqual(covariance.reference_frame, "True Equator, Mean Equinox")
        self.assertAlmostEqual(
            covariance.cx_x,
            self.valid_covariance_data["cx_x"],
        )
        self.assertAlmostEqual(
            covariance.cy_x,
            self.valid_covariance_data["cy_x"],
        )
        self.assertAlmostEqual(
            covariance.cy_y,
            self.valid_covariance_data["cy_y"],
        )
        self.assertAlmostEqual(
            covariance.cz_x,
            self.valid_covariance_data["cz_x"],
        )
        self.assertAlmostEqual(
            covariance.cz_y,
            self.valid_covariance_data["cz_y"],
        )
        self.assertAlmostEqual(
            covariance.cz_z,
            self.valid_covariance_data["cz_z"],
        )
        self.assertAlmostEqual(
            covariance.cx_dot_x,
            self.valid_covariance_data["cx_dot_x"],
        )
        self.assertAlmostEqual(
            covariance.cx_dot_y,
            self.valid_covariance_data["cx_dot_y"],
        )
        self.assertAlmostEqual(
            covariance.cx_dot_z,
            self.valid_covariance_data["cx_dot_z"],
        )
        self.assertAlmostEqual(
            covariance.cy_dot_x,
            self.valid_covariance_data["cy_dot_x"],
        )
        self.assertAlmostEqual(
            covariance.cy_dot_y,
            self.valid_covariance_data["cy_dot_y"],
        )
        self.assertAlmostEqual(
            covariance.cy_dot_z,
            self.valid_covariance_data["cy_dot_z"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_x,
            self.valid_covariance_data["cz_dot_x"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_y,
            self.valid_covariance_data["cz_dot_y"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_z,
            self.valid_covariance_data["cz_dot_z"],
        )
        self.assertAlmostEqual(
            covariance.cx_dot_x_dot,
            self.valid_covariance_data["cx_dot_x_dot"],
        )
        self.assertAlmostEqual(
            covariance.cy_dot_x_dot,
            self.valid_covariance_data["cy_dot_x_dot"],
        )
        self.assertAlmostEqual(
            covariance.cy_dot_y_dot,
            self.valid_covariance_data["cy_dot_y_dot"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_x_dot,
            self.valid_covariance_data["cz_dot_x_dot"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_y_dot,
            self.valid_covariance_data["cz_dot_y_dot"],
        )
        self.assertAlmostEqual(
            covariance.cz_dot_z_dot,
            self.valid_covariance_data["cz_dot_z_dot"],
        )

    def test_to_matrix(self) -> None:
        covariance = Covariance(**self.valid_covariance_data)
        matrix = covariance.to_matrix()
        self.assertEqual(len(matrix), 6, "Matrix should have 6 rows.")

        for idx, row in enumerate(matrix):
            self.assertEqual(len(row), 6, f"Row {idx} should have 6 elements.")

        self.assertAlmostEqual(
            matrix[0][0],
            self.valid_covariance_data["cx_x"],
        )
        self.assertAlmostEqual(
            matrix[0][1],
            self.valid_covariance_data["cy_x"],
        )
        self.assertAlmostEqual(
            matrix[0][2],
            self.valid_covariance_data["cz_x"],
        )
        self.assertAlmostEqual(
            matrix[0][3],
            self.valid_covariance_data["cx_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[0][4],
            self.valid_covariance_data["cx_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[0][5],
            self.valid_covariance_data["cx_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[1][0],
            self.valid_covariance_data["cy_x"],
        )
        self.assertAlmostEqual(
            matrix[1][1],
            self.valid_covariance_data["cy_y"],
        )
        self.assertAlmostEqual(
            matrix[1][2],
            self.valid_covariance_data["cz_y"],
        )
        self.assertAlmostEqual(
            matrix[1][3],
            self.valid_covariance_data["cy_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[1][4],
            self.valid_covariance_data["cy_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[1][5],
            self.valid_covariance_data["cy_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[2][0],
            self.valid_covariance_data["cz_x"],
        )
        self.assertAlmostEqual(
            matrix[2][1],
            self.valid_covariance_data["cz_y"],
        )
        self.assertAlmostEqual(
            matrix[2][2],
            self.valid_covariance_data["cz_z"],
        )
        self.assertAlmostEqual(
            matrix[2][3],
            self.valid_covariance_data["cz_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[2][4],
            self.valid_covariance_data["cz_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[2][5],
            self.valid_covariance_data["cz_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[3][0],
            self.valid_covariance_data["cx_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[3][1],
            self.valid_covariance_data["cy_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[3][2],
            self.valid_covariance_data["cz_dot_x"],
        )
        self.assertAlmostEqual(
            matrix[3][3],
            self.valid_covariance_data["cx_dot_x_dot"],
        )
        self.assertAlmostEqual(
            matrix[3][4],
            self.valid_covariance_data["cy_dot_x_dot"],
        )
        self.assertAlmostEqual(
            matrix[3][5],
            self.valid_covariance_data["cz_dot_x_dot"],
        )
        self.assertAlmostEqual(
            matrix[4][0],
            self.valid_covariance_data["cx_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[4][1],
            self.valid_covariance_data["cy_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[4][2],
            self.valid_covariance_data["cz_dot_y"],
        )
        self.assertAlmostEqual(
            matrix[4][3],
            self.valid_covariance_data["cy_dot_x_dot"],
        )
        self.assertAlmostEqual(
            matrix[4][4],
            self.valid_covariance_data["cy_dot_y_dot"],
        )
        self.assertAlmostEqual(
            matrix[4][5],
            self.valid_covariance_data["cz_dot_y_dot"],
        )
        self.assertAlmostEqual(
            matrix[5][0],
            self.valid_covariance_data["cx_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[5][1],
            self.valid_covariance_data["cy_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[5][2],
            self.valid_covariance_data["cz_dot_z"],
        )
        self.assertAlmostEqual(
            matrix[5][3],
            self.valid_covariance_data["cz_dot_x_dot"],
        )
        self.assertAlmostEqual(
            matrix[5][4],
            self.valid_covariance_data["cz_dot_y_dot"],
        )
        self.assertAlmostEqual(
            matrix[5][5],
            self.valid_covariance_data["cz_dot_z_dot"],
        )

    def test_valid_optional_fields(self) -> None:
        covariance = Covariance(**self.valid_covariance_data)
        self.assertEqual(covariance.reference_frame, "True Equator, Mean Equinox")

    def test_invalid_reference_frame(self) -> None:
        data = self.valid_covariance_data.copy()
        data["reference_frame"] = "XYZ"
        with self.assertRaises(ValidationError):
            Covariance(**data)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
