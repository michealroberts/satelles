# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re
import unittest
from datetime import datetime, timezone
from math import isclose as is_close
from typing import Dict, Optional, Tuple

from satelles import TLE
from satelles.tle import (
    line1_regex,
    line2_regex,
    parse_tle,
)

# **************************************************************************************


iss2LE: str = """        
  1 25544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

iss3LE: str = """
  ISS (ZARYA)             
  1 25544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

iss3LEClassified: str = """
  ISS (ZARYA)             
  1 25544C 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

iss3LESecret: str = """
  ISS (ZARYA)             
  1 25544S 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

iss3LEWithAlpha5: str = """
  ISS (ZARYA)             
  1 E5544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 E5544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

iss3LEWithAlpha5Zeroth: str = """
  0 ISS (ZARYA)             
  1 E5544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 E5544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

starlink5833: str = """
  0 STARLINK-5833
  1 55773U 23028AJ  25098.97241231  .00000576  00000-0  56023-4 0  9993
  2 55773  70.0000 348.4786 0001618 274.5576  85.5398 14.98332157  6399                                               
"""


# **************************************************************************************


class TestTLERegex(unittest.TestCase):
    def extract_lines(self, tle: str) -> Tuple[str, str]:
        """
        Extracts and returns the TLE line1 and line2 from a multi-line string.
        """
        lines = [line.strip() for line in tle.splitlines() if line.strip()]
        # TLE lines start with "1" or "2"
        tle_lines = [
            line for line in lines if line.startswith("1") or line.startswith("2")
        ]

        if len(tle_lines) < 2:
            raise ValueError("Not enough TLE lines found")

        return tle_lines[0], tle_lines[1]

    def check_line1(self, line: str, expected: Dict[str, str]) -> None:
        match: Optional[re.Match] = line1_regex.match(line)

        self.assertIsNotNone(match, "Line1 regex did not match")

        if not match or match is None:
            self.fail()

        groups: Dict[str, str] = match.groupdict()

        for key, value in expected.items():
            self.assertEqual(
                groups[key],
                value,
                f"Mismatch for {key}: expected {value}, got {groups[key]}",
            )

    def check_line2(self, line: str, expected: Dict[str, str]) -> None:
        match: Optional[re.Match] = line2_regex.match(line)

        self.assertIsNotNone(match, "Line2 regex did not match")

        if not match or match is None:
            self.fail()

        groups: Dict[str, str] = match.groupdict()

        for key, value in expected.items():
            self.assertEqual(
                groups[key],
                value,
                f"Mismatch for {key}: expected {value}, got {groups[key]}",
            )

    def test_iss2LE(self) -> None:
        line1, line2 = self.extract_lines(iss2LE)
        expected_line1 = {
            "id": "25544",
            "classification": "U",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "25544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_iss3LE(self) -> None:
        line1, line2 = self.extract_lines(iss3LE)
        # For iss3LE, the TLE lines are identical to iss2LE.
        expected_line1 = {
            "id": "25544",
            "classification": "U",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "25544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_iss3LEClassified(self) -> None:
        line1, line2 = self.extract_lines(iss3LEClassified)
        expected_line1 = {
            "id": "25544",
            "classification": "C",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "25544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_iss3LESecret(self) -> None:
        line1, line2 = self.extract_lines(iss3LESecret)
        expected_line1 = {
            "id": "25544",
            "classification": "S",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "25544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_iss3LEWithAlpha5(self) -> None:
        line1, line2 = self.extract_lines(iss3LEWithAlpha5)
        expected_line1 = {
            "id": "E5544",
            "classification": "U",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "E5544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_iss3LEWithAlpha5Zeroth(self) -> None:
        line1, line2 = self.extract_lines(iss3LEWithAlpha5Zeroth)
        expected_line1 = {
            "id": "E5544",
            "classification": "U",
            "designator": "98067A",
            "year": "20",
            "day": "062.59097222",
            "first_derivative_of_mean_motion": ".00016717",
            "second_derivative_of_mean_motion": "00000-0",
            "drag": "10270-3",
            "ephemeris": "0",
            "set": "9006",
        }
        expected_line2 = {
            "id": "E5544",
            "inclination": "51.6442",
            "raan": "147.1064",
            "eccentricity": "0004607",
            "argument_of_perigee": "95.6506",
            "mean_anomaly": "329.8285",
            "mean_motion": "15.49249062",
            "number_of_revolutions": "2423",
        }
        self.check_line1(line1, expected_line1)
        self.check_line2(line2, expected_line2)

    def test_serialize_to_parts_iss2LE(self) -> None:
        tle = TLE(tle_string=iss2LE)

        parts = tle.serialize_to_parts()

        self.assertEqual(parts[0], "")
        self.assertEqual(
            parts[1],
            "1 25544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006",
        )
        self.assertEqual(
            parts[2],
            "2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423",
        )

    def test_serialize_to_parts_iss3LEWithAlpha5(self) -> None:
        tle = TLE(tle_string=iss3LEWithAlpha5)

        parts = tle.serialize_to_parts()

        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0], "ISS (ZARYA)")
        self.assertEqual(
            parts[1],
            "1 E5544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006",
        )
        self.assertEqual(
            parts[2],
            "2 E5544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423",
        )


# **************************************************************************************


class TestTLEParser(unittest.TestCase):
    def test_parse_tle_defined(self):
        # Simply verify that parse_tle is defined and callable:
        self.assertTrue(callable(parse_tle))

    def test_parse_2le(self):
        satellite = parse_tle(iss2LE)
        self.assertIsNotNone(satellite, "2LE TLE should be parsed successfully")
        self.assertEqual(satellite.name, "")
        self.assertEqual(satellite.classification, "Unclassified")
        self.assertEqual(satellite.designator, "98067A")
        self.assertEqual(satellite.year, 2020)
        self.assertAlmostEqual(satellite.day, 62.59097222)
        self.assertAlmostEqual(satellite.inclination, 51.6442)
        self.assertAlmostEqual(satellite.raan, 147.1064)
        self.assertAlmostEqual(satellite.eccentricity, 0.0004607)
        self.assertAlmostEqual(satellite.argument_of_pericenter, 95.6506)
        self.assertAlmostEqual(satellite.mean_anomaly, 329.8285)
        self.assertAlmostEqual(satellite.mean_motion, 15.49249062)
        self.assertAlmostEqual(satellite.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqual(satellite.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(satellite.number_of_revolutions, 2423)

    def test_parse_3le_unclassified(self):
        satellite = parse_tle(iss3LE)
        self.assertIsNotNone(satellite, "3LE TLE should be parsed successfully")
        self.assertEqual(satellite.name, "ISS (ZARYA)")
        self.assertEqual(satellite.classification, "Unclassified")
        self.assertEqual(satellite.designator, "98067A")
        self.assertEqual(satellite.year, 2020)
        self.assertAlmostEqual(satellite.day, 62.59097222)
        self.assertAlmostEqual(satellite.inclination, 51.6442)
        self.assertAlmostEqual(satellite.raan, 147.1064)
        self.assertAlmostEqual(satellite.eccentricity, 0.0004607)
        self.assertAlmostEqual(satellite.argument_of_pericenter, 95.6506)
        self.assertAlmostEqual(satellite.mean_anomaly, 329.8285)
        self.assertAlmostEqual(satellite.mean_motion, 15.49249062)
        self.assertAlmostEqual(satellite.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqual(satellite.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(satellite.number_of_revolutions, 2423)

    def test_parse_3le_classified(self):
        satellite = parse_tle(iss3LEClassified)
        self.assertIsNotNone(
            satellite, "3LE TLE with Classified should be parsed successfully"
        )
        self.assertEqual(satellite.name, "ISS (ZARYA)")
        self.assertEqual(satellite.classification, "Classified")
        self.assertEqual(satellite.designator, "98067A")
        self.assertEqual(satellite.year, 2020)
        self.assertAlmostEqual(satellite.day, 62.59097222)
        self.assertAlmostEqual(satellite.inclination, 51.6442)
        self.assertAlmostEqual(satellite.raan, 147.1064)
        self.assertAlmostEqual(satellite.eccentricity, 0.0004607)
        self.assertAlmostEqual(satellite.argument_of_pericenter, 95.6506)
        self.assertAlmostEqual(satellite.mean_anomaly, 329.8285)
        self.assertAlmostEqual(satellite.mean_motion, 15.49249062)
        self.assertAlmostEqual(satellite.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqual(satellite.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(satellite.number_of_revolutions, 2423)

    def test_parse_3le_secret(self):
        satellite = parse_tle(iss3LESecret)
        self.assertIsNotNone(
            satellite, "3LE TLE with Secret should be parsed successfully"
        )
        self.assertEqual(satellite.name, "ISS (ZARYA)")
        self.assertEqual(satellite.classification, "Secret")
        self.assertEqual(satellite.designator, "98067A")
        self.assertEqual(satellite.year, 2020)
        self.assertAlmostEqual(satellite.day, 62.59097222)
        self.assertAlmostEqual(satellite.inclination, 51.6442)
        self.assertAlmostEqual(satellite.raan, 147.1064)
        self.assertAlmostEqual(satellite.eccentricity, 0.0004607)
        self.assertAlmostEqual(satellite.argument_of_pericenter, 95.6506)
        self.assertAlmostEqual(satellite.mean_anomaly, 329.8285)
        self.assertAlmostEqual(satellite.mean_motion, 15.49249062)
        self.assertAlmostEqual(satellite.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqual(satellite.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(satellite.number_of_revolutions, 2423)

    def test_parse_3le_with_alpha5(self):
        satellite = parse_tle(iss3LEWithAlpha5)
        self.assertIsNotNone(
            satellite, "3LE TLE with alpha-5 should be parsed successfully"
        )
        self.assertEqual(satellite.name, "ISS (ZARYA)")
        self.assertEqual(satellite.classification, "Unclassified")
        # The id field is parsed using base-36 when the first character is a letter.
        # Expected value for "E5544" in base-36 is 23754532.
        self.assertEqual(satellite.id, 23754532)

    def test_invalid_tle(self):
        with self.assertRaises(ValueError, msg="Invalid TLE format"):
            parse_tle("")


# **************************************************************************************


class TestTLE(unittest.TestCase):
    def assertAlmostEqualFloat(self, a, b, tol=1e-8):
        self.assertTrue(is_close(a, b, rel_tol=tol), f"{a} != {b}")

    def test_parse_2le(self):
        tle = TLE(iss2LE)
        self.assertEqual(tle.name, "")
        self.assertEqual(tle.classification, "Unclassified")
        self.assertEqual(tle.designator, "98067A")
        self.assertEqual(tle.year, 2020)
        self.assertAlmostEqualFloat(tle.day, 62.59097222)
        self.assertAlmostEqualFloat(tle.right_ascension_of_the_ascending_node, 147.1064)
        self.assertAlmostEqualFloat(tle.inclination, 51.6442)
        self.assertAlmostEqualFloat(tle.eccentricity, 0.0004607)
        self.assertAlmostEqualFloat(tle.argument_of_perigee, 95.6506)
        self.assertAlmostEqualFloat(tle.mean_anomaly, 329.8285)
        self.assertAlmostEqualFloat(tle.mean_motion, 15.49249062)
        self.assertAlmostEqualFloat(tle.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqualFloat(tle.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(tle.number_of_revolutions, 2423)
        self.assertEqual(tle.ephemeris, 0)
        self.assertEqual(tle.set, 9006)
        # b_star_drag is parsed from "10270-3": 10270/1e5 * 10^-3 = 0.00010270
        self.assertAlmostEqualFloat(tle.b_star_drag, 0.00010270)

        with self.assertRaises(ValueError):
            _ = tle._satellite.perifocal_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.equatorial_coordinate

        when = datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        tle._satellite.at(when=when)

        cartesian = tle._satellite.perifocal_coordinate

        self.assertAlmostEqualFloat(cartesian["x"], 6620059.856849059)
        self.assertAlmostEqualFloat(cartesian["y"], -1527527.3878711176)
        self.assertAlmostEqualFloat(cartesian["z"], 0.0)

        perifocal_velocity = tle._satellite.perifocal_velocity

        self.assertAlmostEqualFloat(perifocal_velocity["vx"], 1721.755285)
        self.assertAlmostEqualFloat(perifocal_velocity["vy"], 7465.340542)
        self.assertAlmostEqualFloat(perifocal_velocity["vz"], 0.0)

        eci = tle._satellite.eci_coordinate

        self.assertAlmostEqualFloat(eci["x"], -2999918.0003107865)
        self.assertAlmostEqualFloat(eci["y"], -3039494.659567604)
        self.assertAlmostEqualFloat(eci["z"], 5283984.920004229)

        equatorial = tle._satellite.equatorial_coordinate

        self.assertAlmostEqualFloat(equatorial["ra"], 225.37545, tol=1e-5)
        self.assertAlmostEqualFloat(equatorial["dec"], 51.054300, tol=1e-5)

    def test_parse_3le_unclassified(self):
        tle = TLE(iss3LE)
        self.assertEqual(tle.name, "ISS (ZARYA)")
        self.assertEqual(tle.classification, "Unclassified")
        self.assertEqual(tle.designator, "98067A")
        self.assertEqual(tle.year, 2020)
        self.assertAlmostEqualFloat(tle.day, 62.59097222)
        self.assertAlmostEqualFloat(tle.right_ascension_of_the_ascending_node, 147.1064)
        self.assertAlmostEqualFloat(tle.inclination, 51.6442)
        self.assertAlmostEqualFloat(tle.eccentricity, 0.0004607)
        self.assertAlmostEqualFloat(tle.argument_of_perigee, 95.6506)
        self.assertAlmostEqualFloat(tle.mean_anomaly, 329.8285)
        self.assertAlmostEqualFloat(tle.mean_motion, 15.49249062)
        self.assertAlmostEqualFloat(tle.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqualFloat(tle.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(tle.number_of_revolutions, 2423)
        self.assertEqual(tle.ephemeris, 0)
        self.assertEqual(tle.set, 9006)
        self.assertAlmostEqualFloat(tle.b_star_drag, 0.00010270)

        with self.assertRaises(ValueError):
            _ = tle._satellite.perifocal_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.eci_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.equatorial_coordinate

        when = datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        tle._satellite.at(when=when)

        cartesian = tle._satellite.perifocal_coordinate

        self.assertAlmostEqualFloat(cartesian["x"], 6620059.856849059)
        self.assertAlmostEqualFloat(cartesian["y"], -1527527.3878711176)
        self.assertAlmostEqualFloat(cartesian["z"], 0.0)

        perifocal_velocity = tle._satellite.perifocal_velocity

        self.assertAlmostEqualFloat(perifocal_velocity["vx"], 1721.755285)
        self.assertAlmostEqualFloat(perifocal_velocity["vy"], 7465.340542)
        self.assertAlmostEqualFloat(perifocal_velocity["vz"], 0.0)

        eci = tle._satellite.eci_coordinate

        self.assertAlmostEqualFloat(eci["x"], -2999918.0003107865)
        self.assertAlmostEqualFloat(eci["y"], -3039494.659567604)
        self.assertAlmostEqualFloat(eci["z"], 5283984.920004229)

        equatorial = tle._satellite.equatorial_coordinate

        self.assertAlmostEqualFloat(equatorial["ra"], 225.37545, tol=1e-5)
        self.assertAlmostEqualFloat(equatorial["dec"], 51.054300, tol=1e-5)

    def test_parse_3le_classified(self):
        tle = TLE(iss3LEClassified)
        self.assertEqual(tle.name, "ISS (ZARYA)")
        self.assertEqual(tle.classification, "Classified")
        self.assertEqual(tle.designator, "98067A")
        self.assertEqual(tle.year, 2020)
        self.assertAlmostEqualFloat(tle.day, 62.59097222)
        self.assertAlmostEqualFloat(tle.right_ascension_of_the_ascending_node, 147.1064)
        self.assertAlmostEqualFloat(tle.inclination, 51.6442)
        self.assertAlmostEqualFloat(tle.eccentricity, 0.0004607)
        self.assertAlmostEqualFloat(tle.argument_of_perigee, 95.6506)
        self.assertAlmostEqualFloat(tle.mean_anomaly, 329.8285)
        self.assertAlmostEqualFloat(tle.mean_motion, 15.49249062)
        self.assertAlmostEqualFloat(tle.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqualFloat(tle.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(tle.number_of_revolutions, 2423)
        self.assertEqual(tle.ephemeris, 0)
        self.assertEqual(tle.set, 9006)
        self.assertAlmostEqualFloat(tle.b_star_drag, 0.00010270)

        with self.assertRaises(ValueError):
            _ = tle._satellite.perifocal_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.eci_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.equatorial_coordinate

        when = datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        tle._satellite.at(when=when)

        cartesian = tle._satellite.perifocal_coordinate

        self.assertAlmostEqualFloat(cartesian["x"], 6620059.856849059)
        self.assertAlmostEqualFloat(cartesian["y"], -1527527.3878711176)
        self.assertAlmostEqualFloat(cartesian["z"], 0.0)

        perifocal_velocity = tle._satellite.perifocal_velocity

        self.assertAlmostEqualFloat(perifocal_velocity["vx"], 1721.755285)
        self.assertAlmostEqualFloat(perifocal_velocity["vy"], 7465.340542)
        self.assertAlmostEqualFloat(perifocal_velocity["vz"], 0.0)

        eci = tle._satellite.eci_coordinate

        self.assertAlmostEqualFloat(eci["x"], -2999918.0003107865)
        self.assertAlmostEqualFloat(eci["y"], -3039494.659567604)
        self.assertAlmostEqualFloat(eci["z"], 5283984.920004229)

        equatorial = tle._satellite.equatorial_coordinate

        self.assertAlmostEqualFloat(equatorial["ra"], 225.37545, tol=1e-5)
        self.assertAlmostEqualFloat(equatorial["dec"], 51.054300, tol=1e-5)

    def test_parse_3le_secret(self):
        tle = TLE(iss3LESecret)
        self.assertEqual(tle.name, "ISS (ZARYA)")
        self.assertEqual(tle.classification, "Secret")
        self.assertEqual(tle.designator, "98067A")
        self.assertEqual(tle.year, 2020)
        self.assertAlmostEqualFloat(tle.day, 62.59097222)
        self.assertAlmostEqualFloat(tle.right_ascension_of_the_ascending_node, 147.1064)
        self.assertAlmostEqualFloat(tle.inclination, 51.6442)
        self.assertAlmostEqualFloat(tle.eccentricity, 0.0004607)
        self.assertAlmostEqualFloat(tle.argument_of_perigee, 95.6506)
        self.assertAlmostEqualFloat(tle.mean_anomaly, 329.8285)
        self.assertAlmostEqualFloat(tle.mean_motion, 15.49249062)
        self.assertAlmostEqualFloat(tle.first_derivative_of_mean_motion, 0.00016717)
        self.assertAlmostEqualFloat(tle.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(tle.number_of_revolutions, 2423)
        self.assertEqual(tle.ephemeris, 0)
        self.assertEqual(tle.set, 9006)
        self.assertAlmostEqualFloat(tle.b_star_drag, 0.00010270)

        with self.assertRaises(ValueError):
            _ = tle._satellite.perifocal_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.eci_coordinate

        with self.assertRaises(ValueError):
            _ = tle._satellite.equatorial_coordinate

        when = datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc)

        tle._satellite.at(when=when)

        cartesian = tle._satellite.perifocal_coordinate

        self.assertAlmostEqualFloat(cartesian["x"], 6620059.856849059)
        self.assertAlmostEqualFloat(cartesian["y"], -1527527.3878711176)
        self.assertAlmostEqualFloat(cartesian["z"], 0.0)

        perifocal_velocity = tle._satellite.perifocal_velocity

        self.assertAlmostEqualFloat(perifocal_velocity["vx"], 1721.755285)
        self.assertAlmostEqualFloat(perifocal_velocity["vy"], 7465.340542)
        self.assertAlmostEqualFloat(perifocal_velocity["vz"], 0.0)

        eci = tle._satellite.eci_coordinate

        self.assertAlmostEqualFloat(eci["x"], -2999918.0003107865)
        self.assertAlmostEqualFloat(eci["y"], -3039494.659567604)
        self.assertAlmostEqualFloat(eci["z"], 5283984.920004229)

        equatorial = tle._satellite.equatorial_coordinate

        self.assertAlmostEqualFloat(equatorial["ra"], 225.37545, tol=1e-5)
        self.assertAlmostEqualFloat(equatorial["dec"], 51.054300, tol=1e-5)

    def test_parse_3le_with_alpha5(self):
        tle = TLE(iss3LEWithAlpha5)
        self.assertEqual(tle._satellite.name, "ISS (ZARYA)")
        self.assertEqual(tle._satellite.classification, "Unclassified")
        # The id field is parsed using base-36 when the first character is a letter.
        # Expected value for "E5544" in base-36 is 23754532.
        self.assertEqual(tle._satellite.id, 23754532)

    def test_parse_starlink_5833(self):
        tle = TLE(starlink5833)
        self.assertEqual(tle.name, "STARLINK-5833")
        self.assertEqual(tle.classification, "Unclassified")
        self.assertEqual(tle.designator, "23028AJ")
        self.assertEqual(tle.year, 2025)
        self.assertAlmostEqualFloat(tle.day, 98.97241231)
        self.assertAlmostEqualFloat(tle.right_ascension_of_the_ascending_node, 348.4786)
        self.assertAlmostEqualFloat(tle.inclination, 70.0)
        self.assertAlmostEqualFloat(tle.eccentricity, 0.0001618)
        self.assertAlmostEqualFloat(tle.argument_of_perigee, 274.5576)
        self.assertAlmostEqualFloat(tle.mean_anomaly, 85.5398)
        self.assertAlmostEqualFloat(tle.mean_motion, 14.98332157116399)
        self.assertAlmostEqualFloat(tle.first_derivative_of_mean_motion, 0.00000576)
        self.assertAlmostEqualFloat(tle.second_derivative_of_mean_motion, 0.0)
        self.assertEqual(tle.number_of_revolutions, 6399)
        self.assertEqual(tle.ephemeris, 0)
        self.assertEqual(tle.set, 9993)
        self.assertAlmostEqualFloat(tle.b_star_drag, 0.000056023)
        # b_star_drag is parsed from "56023-4": 56023/1e5 * 10^-4 = 0.000056023

    def test_invalid_tle(self):
        with self.assertRaises(ValueError):
            TLE("")


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
