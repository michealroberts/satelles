# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from math import cos, degrees, sin

from celerity.coordinates import EquatorialCoordinate

from satelles import (
    CartesianCoordinate,
    convert_eci_to_equatorial,
    convert_perifocal_to_eci,
    get_eccentric_anomaly,
    get_perifocal_coordinate,
)

# **************************************************************************************


class TestGetPerifocalPosition(unittest.TestCase):
    def test_zero_eccentricity(self):
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.0
        mean_anomaly = 1.0
        true_anomaly = 2.0

        expected_r = semi_major_axis
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)

    def test_nonzero_eccentricity(self):
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.1
        mean_anomaly = 1.2
        true_anomaly = 2.5

        # Compute the eccentric anomaly (E) using get_eccentric_anomaly:
        E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)

        expected_r = semi_major_axis * (1 - eccentricity * cos(E))
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)

    def test_negative_true_anomaly(self):
        """
        Test that a negative true anomaly (provided in degrees) yields the correct
        perifocal coordinates.
        """
        semi_major_axis = 7_000_000.0  # meters
        eccentricity = 0.2
        mean_anomaly = 0.8
        true_anomaly = -1.0

        # Compute the eccentric anomaly (E) using get_eccentric_anomaly:
        E = get_eccentric_anomaly(degrees(mean_anomaly), eccentricity)
        expected_r = semi_major_axis * (1 - eccentricity * cos(E))
        expected_x = expected_r * cos(true_anomaly)
        expected_y = expected_r * sin(true_anomaly)
        expected_z = 0.0

        result = get_perifocal_coordinate(
            semi_major_axis,
            degrees(mean_anomaly),
            degrees(true_anomaly),
            eccentricity,
        )

        self.assertAlmostEqual(result["x"], expected_x, places=6)
        self.assertAlmostEqual(result["y"], expected_y, places=6)
        self.assertAlmostEqual(result["z"], expected_z, places=6)


# **************************************************************************************


class TestConvertPerifocalToECI(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self, coord1: CartesianCoordinate, coord2: CartesianCoordinate, places: int = 6
    ) -> None:
        self.assertAlmostEqual(coord1["x"], coord2["x"], places=places)
        self.assertAlmostEqual(coord1["y"], coord2["y"], places=places)
        self.assertAlmostEqual(coord1["z"], coord2["z"], places=places)

    def test_identity(self) -> None:
        """
        When all angles are zero, the output should equal the input.
        """
        perifocal: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}
        result = convert_perifocal_to_eci(perifocal, 0, 0, 0)
        expected: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_argument_of_perigee_only(self) -> None:
        """
        For input (1, 0, 0) with argument_of_perigee 90° (and other angles zero),
        the expected result should be (0, 1, 0).
        """
        perifocal: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        result = convert_perifocal_to_eci(perifocal, 90, 0, 0)
        expected: CartesianCoordinate = {"x": 0.0, "y": 1.0, "z": 0.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_all_rotations(self) -> None:
        """
        Test with all angles set to 90° for input (1, 0, 0).
        Step-by-step:
          - Rotate (1, 0, 0) by 90° about z: (0, 1, 0)
          - Rotate (0, 1, 0) by 90° about x: (0, 0, 1)
          - Rotate (0, 0, 1) by 90° about z: (0, 0, 1) (unchanged)
        Expected result: (0, 0, 1)
        """
        perifocal: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        result = convert_perifocal_to_eci(perifocal, 90, 90, 90)
        expected: CartesianCoordinate = {"x": 0.0, "y": 0.0, "z": 1.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_complex_rotation(self) -> None:
        """
        For input (1, 1, 0) with angles (45, 45, 45):
        Expected result (approximately): (-0.70710678, 0.70710678, 1.0)
        """
        perifocal: CartesianCoordinate = {"x": 1.0, "y": 1.0, "z": 0.0}
        result = convert_perifocal_to_eci(perifocal, 45, 45, 45)
        expected: CartesianCoordinate = {"x": -0.70710678, "y": 0.70710678, "z": 1.0}
        self.assertCoordinatesAlmostEqual(result, expected)


# **************************************************************************************


class TestConvertECIToEquatorial(unittest.TestCase):
    def assertEquatorialAlmostEqual(
        self,
        coord1: EquatorialCoordinate,
        coord2: EquatorialCoordinate,
        places: int = 6,
    ) -> None:
        self.assertAlmostEqual(coord1["ra"], coord2["ra"], places=places)
        self.assertAlmostEqual(coord1["dec"], coord2["dec"], places=places)

    def test_positive_x_axis(self) -> None:
        """
        For an ECI coordinate along the +x-axis: (1, 0, 0)
        Expected equatorial coordinates: RA = 0°, Dec = 0°.
        """
        eci: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 0.0, "dec": 0.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_positive_y_axis(self) -> None:
        """
        For an ECI coordinate along the +y-axis: (0, 1, 0)
        Expected equatorial coordinates: RA = 90°, Dec = 0°.
        """
        eci: CartesianCoordinate = {"x": 0.0, "y": 1.0, "z": 0.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 90.0, "dec": 0.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_positive_z_axis(self) -> None:
        """
        For an ECI coordinate along the +z-axis: (0, 0, 1)
        Expected equatorial coordinates: RA = 0° (ambiguous), Dec = 90°.
        """
        eci: CartesianCoordinate = {"x": 0.0, "y": 0.0, "z": 1.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 0.0, "dec": 90.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_negative_x_axis(self) -> None:
        """
        For an ECI coordinate along the -x-axis: (-1, 0, 0)
        Expected equatorial coordinates: RA = 180°, Dec = 0°.
        """
        eci: CartesianCoordinate = {"x": -1.0, "y": 0.0, "z": 0.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 180.0, "dec": 0.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_negative_y(self) -> None:
        """
        For an ECI coordinate: (1, -1, 0)
        Here, RA = degrees(atan2(-1, 1)) = -45°, which should be adjusted to 315°.
        Dec = 0°.
        """
        eci: CartesianCoordinate = {"x": 1.0, "y": -1.0, "z": 0.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 315.0, "dec": 0.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_negative_z(self) -> None:
        """
        For an ECI coordinate: (0, 1, -1)
        r = sqrt(0^2 + 1^2 + (-1)^2) = sqrt(2).
        RA = 90°; Dec = degrees(asin(-1/sqrt(2))) ≈ -45°.
        """
        eci: CartesianCoordinate = {"x": 0.0, "y": 1.0, "z": -1.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 90.0, "dec": -45.0}
        self.assertEquatorialAlmostEqual(result, expected)

    def test_non_trivial(self) -> None:
        """
        For an ECI coordinate: (1, 1, 1)
        r = sqrt(3); RA = degrees(atan2(1, 1)) = 45°;
        Dec = degrees(asin(1/sqrt(3))) ≈ 35.26439°.
        """
        eci: CartesianCoordinate = {"x": 1.0, "y": 1.0, "z": 1.0}
        result = convert_eci_to_equatorial(eci)
        expected: EquatorialCoordinate = {"ra": 45.0, "dec": 35.26439}
        self.assertEquatorialAlmostEqual(result, expected)


# **************************************************************************************


if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
