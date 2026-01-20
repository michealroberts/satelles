# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone
from math import atan2, cos, degrees, radians, sin, sqrt

from celerity.constants import c as SPEED_OF_LIGHT
from celerity.coordinates import (
    EquatorialCoordinate,
    GeographicCoordinate,
    HorizontalCoordinate,
)
from celerity.temporal import get_greenwich_sidereal_time

from satelles import (
    EARTH_EQUATORIAL_RADIUS,
    EARTH_FLATTENING_FACTOR,
    CartesianCoordinate,
    TopocentricCoordinate,
    convert_ecef_to_eci,
    convert_ecef_to_enu,
    convert_ecef_to_lla,
    convert_eci_to_ecef,
    convert_eci_to_equatorial,
    convert_eci_to_perifocal,
    convert_eci_to_topocentric,
    convert_enu_to_horizontal,
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
        E = radians(get_eccentric_anomaly(degrees(mean_anomaly), eccentricity))

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
        E = radians(get_eccentric_anomaly(degrees(mean_anomaly), eccentricity))
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


class TestConvertECEFToECI(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self, coord1: CartesianCoordinate, coord2: CartesianCoordinate, places: int = 4
    ) -> None:
        self.assertAlmostEqual(coord1["x"], coord2["x"], places=places)
        self.assertAlmostEqual(coord1["y"], coord2["y"], places=places)
        self.assertAlmostEqual(coord1["z"], coord2["z"], places=places)

    def test_identity(self) -> None:
        """
        Verifies the conversion from ECEF to ECI coordinates for a specific
        date and time.
        """
        ecef: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.7748323217117372,
                "y": -1.3601361070890385,
                "z": 3.0,
            }
        )
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        result = convert_ecef_to_eci(ecef, when)
        expected: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}

        self.assertCoordinatesAlmostEqual(result, expected)

    def test_rotation_90_degrees(self) -> None:
        """
        With GMST = 90°, ECEF (0,-1,0) should become ECI (1,0,0).
        """
        ecef: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 0,
                "y": -1,
                "z": 0.0,
            }
        )

        when = datetime(
            2025, 1, 1, 23, 12, 35, 600000
        )  # A time roughly giving 90° GMST

        result = convert_ecef_to_eci(ecef, when)
        expected: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}

        self.assertCoordinatesAlmostEqual(result, expected, 4)

    def test_nontrivial_rotation(self) -> None:
        """
        With a realistic GMST, ECEF coordinates rotate correctly to ECI.
        """
        eci: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 1.0,
                "z": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 3, 0, 0)

        GMST = get_greenwich_sidereal_time(date=when)

        ecef: CartesianCoordinate = CartesianCoordinate(
            {
                "x": (eci["x"] * cos(radians(GMST * 15)))
                + (eci["y"] * sin(radians(GMST * 15))),
                "y": -(eci["x"] * sin(radians(GMST * 15)))
                + (eci["y"] * cos(radians(GMST * 15))),
                "z": eci["z"],
            }
        )

        expected = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 1.0,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_eci(ecef, when)
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
        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        result = convert_eci_to_ecef(eci, when)
        expected: CartesianCoordinate = CartesianCoordinate(
            {
                "x": 1.7748277327858684,
                "y": -1.3601420951261578,
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

        expected: CartesianCoordinate = CartesianCoordinate(
            {
                "x": -0.270401038619395,
                "y": -1.3881222130322506,
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


class TestConvertECIToPerifocal(unittest.TestCase):
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
        eci: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}
        result = convert_eci_to_perifocal(eci, 0, 0, 0)
        expected: CartesianCoordinate = {"x": 1.0, "y": 2.0, "z": 3.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_argument_of_perigee_only(self) -> None:
        """
        For input (0, 1, 0) with argument_of_perigee 90° (and other angles zero),
        the expected result should be (1, 0, 0).
        """
        eci: CartesianCoordinate = {"x": 0.0, "y": 1.0, "z": 0.0}
        result = convert_eci_to_perifocal(eci, 90, 0, 0)
        expected: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_all_rotations(self) -> None:
        """
        Test with all angles set to 90° for input (0, 0, 1).
        Step-by-step:
          - Rotate (0, 0, 1) by 90° about z: (0, 0, 1) (unchanged)
          - Rotate (0, 0, 1) by 90° about x: (0, -1, 0)
          - Rotate (0, -1, 0) by 90° about z: (1, 0, 0)
        Expected result: (0, 0, 1)
        """
        eci: CartesianCoordinate = {"x": 0.0, "y": 0.0, "z": 1.0}
        result = convert_eci_to_perifocal(eci, 90, 90, 90)
        expected: CartesianCoordinate = {"x": 1.0, "y": 0.0, "z": 0.0}
        self.assertCoordinatesAlmostEqual(result, expected)

    def test_complex_rotation(self) -> None:
        """
        For input (-0.70710678, 0.70710678, 1.0) with angles (45, 45, 45):
        Expected result (approximately): (1, 1, 0)
        """
        eci: CartesianCoordinate = {"x": -0.70710678, "y": 0.70710678, "z": 1.0}
        result = convert_eci_to_perifocal(eci, 45, 45, 45)
        expected: CartesianCoordinate = {"x": 1.0, "y": 1.0, "z": 0.0}
        self.assertCoordinatesAlmostEqual(result, expected)


# **************************************************************************************


class TestConvertECIToTopocentric(unittest.TestCase):
    def assertTopocentricAlmostEqual(
        self,
        result: TopocentricCoordinate,
        expected: TopocentricCoordinate,
        places: int = 4,
    ) -> None:
        self.assertEqual(result["at"], expected["at"])
        self.assertAlmostEqual(result["altitude"], expected["altitude"], places=places)
        self.assertAlmostEqual(result["azimuth"], expected["azimuth"], places=places)
        self.assertAlmostEqual(result["range"], expected["range"], places=places)
        self.assertAlmostEqual(
            result["time_of_flight"], expected["time_of_flight"], places=places
        )

    def test_directly_overhead(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite 400km directly above should have
        altitude=90° and range=400km.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        height = 400_000.0

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS + height,
                "y": 0.0,
                "z": 0.0,
            }
        )

        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=90.0,
            azimuth=0.0,
            range=400_000.0,
            time_of_flight=2 * 400_000.0 / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)

    def test_pure_east(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite at ECEF (R, R, 0) should have
        azimuth=90° and altitude=0°.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": EARTH_EQUATORIAL_RADIUS,
                "z": 0.0,
            }
        )
        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=0.0,
            azimuth=90.0,
            range=EARTH_EQUATORIAL_RADIUS,
            time_of_flight=2 * EARTH_EQUATORIAL_RADIUS / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)

    def test_pure_north(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite at ECEF (R, 0, R) should have
        azimuth=0° and altitude=0°.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": 0.0,
                "z": EARTH_EQUATORIAL_RADIUS,
            }
        )

        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=0.0,
            azimuth=0.0,
            range=EARTH_EQUATORIAL_RADIUS,
            time_of_flight=2 * EARTH_EQUATORIAL_RADIUS / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)

    def test_pure_west(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite at ECEF (R, -R, 0) should have
        azimuth=270° and altitude=0°.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": -EARTH_EQUATORIAL_RADIUS,
                "z": 0.0,
            }
        )
        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=0.0,
            azimuth=270.0,
            range=EARTH_EQUATORIAL_RADIUS,
            time_of_flight=2 * EARTH_EQUATORIAL_RADIUS / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)

    def test_pure_south(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite at ECEF (R, 0, -R) should have
        azimuth=180° and altitude=0°.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": 0.0,
                "z": -EARTH_EQUATORIAL_RADIUS,
            }
        )
        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=0.0,
            azimuth=180.0,
            range=EARTH_EQUATORIAL_RADIUS,
            time_of_flight=2 * EARTH_EQUATORIAL_RADIUS / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)

    def test_northeast_elevated(self) -> None:
        """
        At latitude=0°, longitude=0°, a satellite offset +100km in each of up, east,
        and north should have azimuth=45°.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        when = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        offset = 100_000.0

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS + offset,
                "y": offset,
                "z": offset,
            }
        )

        eci = convert_ecef_to_eci(ecef=ecef, when=when)

        expected_range = sqrt(offset**2 + offset**2 + offset**2)

        result = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)

        expected = TopocentricCoordinate(
            at=when,
            altitude=degrees(atan2(offset, sqrt(offset**2 + offset**2))),
            azimuth=45.0,
            range=expected_range,
            time_of_flight=2 * expected_range / SPEED_OF_LIGHT,
        )

        self.assertTopocentricAlmostEqual(result, expected)


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
        observer = GeographicCoordinate(
            {
                "latitude": 10.0,
                "longitude": 20.0,
                "elevation": 100.0,
            }
        )
        site_ecef = convert_lla_to_ecef(lla=observer)

        result = convert_ecef_to_enu(ecef=site_ecef, observer=observer)
        expected = CartesianCoordinate({"x": 0.0, "y": 0.0, "z": 0.0})

        self.assertCoordinatesAlmostEqual(result, expected)

    def test_pure_east(self):
        """
        At latitude=0°, longitude=0°, an offset of +1 m in ECEF y should map to +1 m East.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )
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
        At latitude=0°, longitude=0°, an offset of +1 m in ECEF z should map to +1 m North.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )
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
        At latitude=0°, longitude=0°, an offset of +1 m in ECEF x should map to +1 m Up.
        """
        observer = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )
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


class TestConvertEnuToHorizontal(unittest.TestCase):
    def assertHorizontalCoordinatesAlmostEqual(
        self,
        result: HorizontalCoordinate,
        expected: HorizontalCoordinate,
        places: int = 6,
    ) -> None:
        """
        Assert that two HorizontalCoordinate objects have alt and az equal within tolerance.
        """
        self.assertAlmostEqual(result["alt"], expected["alt"], places=places)
        self.assertAlmostEqual(result["az"], expected["az"], places=places)

    def test_pure_north_vector_has_zero_azimuth_and_zero_elevation(self) -> None:
        """
        An ENU vector pointing straight north (east=0, north>0, up=0) should have
        azimuth 0° and elevation 0°.
        """
        enu = CartesianCoordinate({"x": 0.0, "y": 10.0, "z": 0.0})
        expected = HorizontalCoordinate({"az": 0.0, "alt": 0.0})
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)

    def test_pure_east_vector_has_ninety_degree_azimuth_and_zero_elevation(
        self,
    ) -> None:
        """
        An ENU vector pointing straight east (east>0, north=0, up=0) should have
        azimuth 90° and elevation 0°.
        """
        enu = CartesianCoordinate({"x": 10.0, "y": 0.0, "z": 0.0})
        expected = HorizontalCoordinate({"az": 90.0, "alt": 0.0})
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)

    def test_pure_south_vector_has_180_degree_azimuth_and_zero_elevation(self) -> None:
        """
        An ENU vector pointing straight south (east=0, north<0, up=0) should have
        azimuth 180° and elevation 0°.
        """
        enu = CartesianCoordinate({"x": 0.0, "y": -5.0, "z": 0.0})
        expected = HorizontalCoordinate({"az": 180.0, "alt": 0.0})
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)

    def test_pure_west_vector_has_270_degree_azimuth_and_zero_elevation(self) -> None:
        """
        An ENU vector pointing straight west (east<0, north=0, up=0) should have
        azimuth 270° and elevation 0°.
        """
        enu = CartesianCoordinate({"x": -8.0, "y": 0.0, "z": 0.0})
        expected = HorizontalCoordinate({"az": 270.0, "alt": 0.0})
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)

    def test_diagonal_vector_with_upward_component(self) -> None:
        """
        An ENU vector with equal east and north and positive up should have
        azimuth 45° and elevation tan⁻¹(up/horizontal_distance).
        """
        east = 1.0
        north = 1.0
        up = 1.0
        enu = CartesianCoordinate(
            {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0,
            }
        )
        expected = HorizontalCoordinate(
            {
                "az": 45.0,
                "alt": degrees(atan2(up, sqrt(east**2 + north**2))),
            }
        )
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)

    def test_northwest_quadrant_vector_wraps_azimuth_to_315(self) -> None:
        """
        An ENU vector in the northwest quadrant (east<0, north>0) should wrap
        azimuth to 360-45=315°.
        """
        enu = CartesianCoordinate({"x": -1.0, "y": 1.0, "z": 0.0})
        expected = HorizontalCoordinate({"az": 315.0, "alt": 0.0})
        result = convert_enu_to_horizontal(enu)
        self.assertHorizontalCoordinatesAlmostEqual(result, expected)


# **************************************************************************************


class TestConvertECEFToLLA(unittest.TestCase):
    def assertGeographicAlmostEqual(
        self,
        coord1: GeographicCoordinate,
        coord2: GeographicCoordinate,
        places: int = 6,
    ) -> None:
        self.assertAlmostEqual(coord1["latitude"], coord2["latitude"], places=places)
        self.assertAlmostEqual(coord1["longitude"], coord2["longitude"], places=places)
        self.assertAlmostEqual(coord1["elevation"], coord2["elevation"], places=places)

    def test_equator_prime_meridian(self) -> None:
        """
        At ECEF (R, 0, 0), the result should be latitude=0°, longitude=0°, elevation=0.
        """
        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS,
                "y": 0.0,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_equator_ninety_east(self) -> None:
        """
        At ECEF (0, R, 0), the result should be latitude=0°, longitude=90°, elevation=0.
        """
        ecef = CartesianCoordinate(
            {
                "x": 0.0,
                "y": EARTH_EQUATORIAL_RADIUS,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 90.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_equator_ninety_west(self) -> None:
        """
        At ECEF (0, -R, 0), the result should be latitude=0°, longitude=-90°, elevation=0.
        """
        ecef = CartesianCoordinate(
            {
                "x": 0.0,
                "y": -EARTH_EQUATORIAL_RADIUS,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": -90.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_equator_antimeridian(self) -> None:
        """
        At ECEF (-R, 0, 0), the result should be latitude=0°, longitude=180°, elevation=0.
        """
        ecef = CartesianCoordinate(
            {
                "x": -EARTH_EQUATORIAL_RADIUS,
                "y": 0.0,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 180.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_north_pole(self) -> None:
        """
        At the North Pole, latitude=90°, longitude=0° (by convention), elevation=0.
        """
        a = EARTH_EQUATORIAL_RADIUS
        f = EARTH_FLATTENING_FACTOR
        e2 = f * (2 - f)
        b = a * sqrt(1 - e2)

        ecef = CartesianCoordinate(
            {
                "x": 0.0,
                "y": 0.0,
                "z": b,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 90.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_south_pole(self) -> None:
        """
        At the South Pole, latitude=-90°, longitude=0° (by convention), elevation=0.
        """
        a = EARTH_EQUATORIAL_RADIUS
        f = EARTH_FLATTENING_FACTOR
        e2 = f * (2 - f)
        b = a * sqrt(1 - e2)

        ecef = CartesianCoordinate(
            {
                "x": 0.0,
                "y": 0.0,
                "z": -b,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": -90.0,
                "longitude": 0.0,
                "elevation": 0.0,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_with_elevation(self) -> None:
        """
        At latitude=0°, longitude=0° with height=1000m, ECEF x = R + h.
        """
        h = 1000.0

        ecef = CartesianCoordinate(
            {
                "x": EARTH_EQUATORIAL_RADIUS + h,
                "y": 0.0,
                "z": 0.0,
            }
        )

        result = convert_ecef_to_lla(ecef)

        expected = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": h,
            }
        )

        self.assertGeographicAlmostEqual(result, expected)

    def test_roundtrip_equator(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA should return the original coordinates.
        """
        original = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 45.0,
                "elevation": 500.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original)

    def test_roundtrip_mid_latitude(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for a mid-latitude location.
        """
        original = GeographicCoordinate(
            {
                "latitude": 45.0,
                "longitude": 45.0,
                "elevation": 1000.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original)

    def test_roundtrip_southern_hemisphere(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for a southern hemisphere location.
        """
        original = GeographicCoordinate(
            {
                "latitude": -33.8688,
                "longitude": 151.2093,
                "elevation": 58.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original, places=4)

    def test_roundtrip_negative_longitude(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for a negative longitude (western hemisphere).
        """
        original = GeographicCoordinate(
            {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "elevation": 10.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original, places=4)

    def test_roundtrip_high_altitude(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for a high altitude (e.g., aircraft or satellite).
        """
        original = GeographicCoordinate(
            {
                "latitude": 51.4700,
                "longitude": -0.4543,
                "elevation": 10_000.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original, places=4)

    def test_roundtrip_near_pole(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for a location near the North Pole.
        """
        original = GeographicCoordinate(
            {
                "latitude": 89.0,
                "longitude": 45.0,
                "elevation": 0.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original, places=4)

    def test_geostationary_orbit_altitude(self) -> None:
        """
        Round-trip: LLA → ECEF → LLA for geostationary orbit altitude (~35,786 km).
        """
        original = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 35_786_000.0,
            }
        )

        ecef = convert_lla_to_ecef(original)
        result = convert_ecef_to_lla(ecef)

        self.assertGeographicAlmostEqual(result, original, places=2)


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
        At latitude=0°, longitude=0°, height=0, x should equal Earth's equatorial
        radius, y and z should be 0.
        """
        lla = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 0.0,
                "elevation": 0.0,
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
        At latitude=0°, longitude=90°, height=0, y should equal Earth's equatorial
        radius, x and z should be 0.
        """
        lla = GeographicCoordinate(
            {
                "latitude": 0.0,
                "longitude": 90.0,
                "elevation": 0.0,
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
        At latitude=90°, longitude arbitrary, height=0; x and y remain zero, z = a * √(1-e²) for the pole.
        """
        a = EARTH_EQUATORIAL_RADIUS
        f = EARTH_FLATTENING_FACTOR
        e2 = f * (2 - f)
        expected_z = a * sqrt(1 - e2)

        lla = GeographicCoordinate(
            {
                "latitude": 90.0,
                "longitude": 0.0,
                "elevation": 0.0,
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
        For a point at latitude=45°, longitude=45° with height above the ellipsoid,
        changes in each ECEF component match h times the local unit vectors.
        """
        h = 1000.0
        phi = radians(45.0)
        lam = radians(45.0)

        base = GeographicCoordinate(
            {
                "latitude": 45.0,
                "longitude": 45.0,
                "elevation": 0.0,
            }
        )
        elevated = GeographicCoordinate(
            {
                "latitude": 45.0,
                "longitude": 45.0,
                "elevation": h,
            }
        )

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
