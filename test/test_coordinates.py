# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime
from math import cos, degrees, radians, sin, sqrt

from celerity.coordinates import EquatorialCoordinate, GeographicCoordinate
from celerity.temporal import get_greenwich_sidereal_time

from satelles import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_FLATTENING_FACTOR,
    CartesianCoordinate,
    convert_ecef_to_enu,
    convert_eci_to_ecef,
    convert_eci_to_equatorial,
    convert_lla_to_ecef,
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


class TestConvertECIToECEF(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self, coord1: CartesianCoordinate, coord2: CartesianCoordinate, places: int = 6
    ) -> None:
        self.assertAlmostEqual(coord1["x"], coord2["x"], places=places)
        self.assertAlmostEqual(coord1["y"], coord2["y"], places=places)
        self.assertAlmostEqual(coord1["z"], coord2["z"], places=places)

    def test_identity(self) -> None:
        """
        Verifies the conversion from ECI to ECEF coordinates for a specific
        date and time.
        """
        eci: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}
        when = datetime(2025, 1, 1, 0, 0, 0)

        result = convert_eci_to_ecef(eci, when)
        expected: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.7748323217117372,
                "y": -1.3601361070890385,
                "z": 3.0,
            }
        )
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_rotation_90_degrees(self) -> None:
        """
        With GMST = 90°, ECI (1,0,0) should become ECEF (0,-1,0).
        """
        eci: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
            }
        )
        when = datetime(
            2025, 1, 1, 23, 12, 35, 600000
        )  # A time roughly giving 90° GMST

        result = convert_eci_to_ecef(eci, when)
        expected: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 0,
                "y": -1,
                "z": 0.0,
            }
        )
        self.assertCoordinatesAlmostEqual(result, expected, 4)

    def test_nontrivial_rotation(self) -> None:
        """
        With a realistic GMST, ECI coordinates rotate correctly to ECEF.
        """
        eci: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 1.0,
                "z": 0.0,
            }
        )
        when = datetime(2025, 1, 1, 3, 0, 0)  # Arbitrary realistic datetime

        GMST = get_greenwich_sidereal_time(date=when)

        expected: CartesianCoordinate = CartesianCoordinate(
            {
                "x": cos(radians(GMST * 15.0)) * eci["x"]
                + sin(radians(GMST * 15.0)) * eci["y"],
                "y": -sin(radians(GMST * 15.0)) * eci["x"]
                + cos(radians(GMST * 15.0)) * eci["y"],
                "z": eci["z"],
            }
        )

        result = convert_eci_to_ecef(eci, when)
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


class TestConvertECEFToEastNorthUp(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self, coord1: CartesianCoordinate, coord2: CartesianCoordinate, places: int = 6
    ) -> None:
        self.assertAlmostEqual(coord1["x"], coord2["x"], places=places)
        self.assertAlmostEqual(coord1["y"], coord2["y"], places=places)
        self.assertAlmostEqual(coord1["z"], coord2["z"], places=places)

    def test_zero_offset(self):
        """
        If the satellite ECEF equals the observer's ECEF, ENU should be (0, 0, 0).
        """
        observer = GeographicCoordinate({"lat": 10.0, "lon": 20.0, "el": 100.0})
        site_ecef = convert_lla_to_ecef(lla=observer)

        result = convert_ecef_to_enu(ecef=site_ecef, observer=observer)
        expected = CartesianCoordinate({"x": 0.0, "y": 0.0, "z": 0.0})

        self.assertCoordinatesAlmostEqual(result, expected)

    def test_pure_east(self):
        """
        At lat=0°, lon=0°, an offset of +1 m in ECEF y should map to +1 m East.
        """
        observer = GeographicCoordinate({"lat": 0.0, "lon": 0.0, "el": 0.0})
        site_ecef = convert_lla_to_ecef(lla=observer)
        sat_ecef = CartesianCoordinate(
            {
                "x": site_ecef["x"],
                "y": site_ecef["y"] + 1.0,
                "z": site_ecef["z"],
            }
        )

        result = convert_ecef_to_enu(ecef=sat_ecef, observer=observer)
        expected = CartesianCoordinate({"x": 1.0, "y": 0.0, "z": 0.0})

        self.assertCoordinatesAlmostEqual(result, expected)

    def test_pure_north(self):
        """
        At lat=0°, lon=0°, an offset of +1 m in ECEF z should map to +1 m North.
        """
        observer = GeographicCoordinate({"lat": 0.0, "lon": 0.0, "el": 0.0})
        site_ecef = convert_lla_to_ecef(lla=observer)
        sat_ecef = CartesianCoordinate(
            {
                "x": site_ecef["x"],
                "y": site_ecef["y"],
                "z": site_ecef["z"] + 1.0,
            }
        )

        result = convert_ecef_to_enu(ecef=sat_ecef, observer=observer)
        expected = CartesianCoordinate({"x": 0.0, "y": 1.0, "z": 0.0})

        self.assertCoordinatesAlmostEqual(result, expected)

    def test_pure_up(self):
        """
        At lat=0°, lon=0°, an offset of +1 m in ECEF x should map to +1 m Up.
        """
        observer = GeographicCoordinate({"lat": 0.0, "lon": 0.0, "el": 0.0})
        site_ecef = convert_lla_to_ecef(lla=observer)
        sat_ecef = CartesianCoordinate(
            {
                "x": site_ecef["x"] + 1.0,
                "y": site_ecef["y"],
                "z": site_ecef["z"],
            }
        )

        result = convert_ecef_to_enu(ecef=sat_ecef, observer=observer)
        expected = CartesianCoordinate({"x": 0.0, "y": 0.0, "z": 1.0})

        self.assertCoordinatesAlmostEqual(result, expected)


# **************************************************************************************


class TestConvertLLAToECEF(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self,
        coord1: CartesianCoordinate,
        coord2: CartesianCoordinate,
        places: int = 6,
    ) -> None:
        self.assertAlmostEqual(coord1["x"], coord2["x"], places=places)
        self.assertAlmostEqual(coord1["y"], coord2["y"], places=places)
        self.assertAlmostEqual(coord1["z"], coord2["z"], places=places)

    def test_equator_prime_meridian(self) -> None:
        """
        At lat=0°, lon=0°, height=0, x should equal Earth's equatorial radius, y and z should be 0.
        """
        lla = GeographicCoordinate(
            {
                "lat": 0.0,
                "lon": 0.0,
                "el": 0.0,
            }
        )
        result = convert_lla_to_ecef(lla)

        expected = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": 0.0,
                "z": 0.0,
            }
        )
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_equator_ninety_east(self) -> None:
        """
        At lat=0°, lon=90°, height=0, y should equal Earth's equatorial radius, x and z should be 0.
        """
        lla = GeographicCoordinate(
            {
                "lat": 0.0,
                "lon": 90.0,
                "el": 0.0,
            }
        )
        result = convert_lla_to_ecef(lla)

        expected = CartesianCoordinate(
            {
                "x": 0.0,
                "y": EARTH_EQUATORIAL_RADIUS,
                "z": 0.0,
            }
        )
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_north_pole(self) -> None:
        """
        At lat=90°, lon arbitrary, height=0; x and y remain zero, z matches the implementation's
        value z = a * e² / sqrt(1 - e²), where e² = f * (2 - f).
        """
        a = EARTH_EQUATORIAL_RADIUS
        f = EARTH_FLATTENING_FACTOR
        e2 = f * (2 - f)
        expected_z = a * e2 / sqrt(1 - e2)

        lla = GeographicCoordinate(
            {
                "lat": 90.0,
                "lon": 0.0,
                "el": 0.0,
            }
        )
        result = convert_lla_to_ecef(lla)

        expected = CartesianCoordinate(
            {
                "x": 0.0,
                "y": 0.0,
                "z": expected_z,
            }
        )
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_with_height(self) -> None:
        """
        For a point at lat=45°, lon=45° with height above the ellipsoid,
        changes in each ECEF component match h times the local unit vectors:
          Δx = h·cosφ·cosθ, Δy = h·cosφ·sinθ, Δz = h·sinφ.
        """
        h = 1000.0
        phi = radians(45.0)
        lam = radians(45.0)

        base = GeographicCoordinate({"lat": 45.0, "lon": 45.0, "el": 0.0})
        elevated = GeographicCoordinate({"lat": 45.0, "lon": 45.0, "el": h})

        result0 = convert_lla_to_ecef(base)
        resulth = convert_lla_to_ecef(elevated)

        dx = resulth["x"] - result0["x"]
        dy = resulth["y"] - result0["y"]
        dz = resulth["z"] - result0["z"]

        self.assertAlmostEqual(dx, h * cos(phi) * cos(lam), places=6)
        self.assertAlmostEqual(dy, h * cos(phi) * sin(lam), places=6)
        self.assertAlmostEqual(dz, h * sin(phi), places=6)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
