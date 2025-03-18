# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re
import unittest
from typing import Dict, Optional, Tuple

from satelles.tle import (
    line1_regex,
    line2_regex,
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


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
