# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2026 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles import (
    convert_distance_to_light_travel_time,
    convert_light_travel_time_to_distance,
)

# **************************************************************************************


class TestConvertDistanceToLightTravelTime(unittest.TestCase):
    def test_convert_distance_to_light_travel_time_for_zero_distance(self) -> None:
        self.assertEqual(
            convert_distance_to_light_travel_time(0.0),
            0.0,
        )

    def test_convert_distance_to_light_travel_time_for_one_meter(self) -> None:
        self.assertAlmostEqual(
            convert_distance_to_light_travel_time(1.0),
            3.3356409519815204e-09,
            places=21,
        )

    def test_convert_distance_to_light_travel_time_for_negative_distance(self) -> None:
        with self.assertRaises(ValueError):
            convert_distance_to_light_travel_time(-1.0)


# **************************************************************************************


class TestConvertLightTravelTimeToDistance(unittest.TestCase):
    def test_convert_light_travel_time_to_distance_for_zero_time(self) -> None:
        self.assertEqual(
            convert_light_travel_time_to_distance(0.0),
            0.0,
        )

    def test_convert_light_travel_time_to_distance_for_one_second(self) -> None:
        self.assertEqual(
            convert_light_travel_time_to_distance(1.0),
            299792458.0,
        )

    def test_convert_light_travel_time_to_distance_for_negative_time(self) -> None:
        with self.assertRaises(ValueError):
            convert_light_travel_time_to_distance(-1.0)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
