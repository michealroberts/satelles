# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.checksum import perform_checksum_compute

# **************************************************************************************


class TestPerformChecksumCompute(unittest.TestCase):
    def test_all_digits(self):
        # "12345" -> 1+2+3+4+5 = 15, 15 % 10 == 5 -> "5"
        line = "12345"
        expected = "5"
        self.assertEqual(perform_checksum_compute(line), expected)

    def test_with_hyphens(self):
        # "-1-2-3-" -> digits: 1,2,3 sum=6; hyphens: 4 of them (4*1) -> total 10, 10 % 10 = 0 -> "0"
        line = "-1-2-3-"
        expected = "0"
        self.assertEqual(perform_checksum_compute(line), expected)

    def test_mixed_characters(self):
        # "12a-3" -> digits: 1,2,3 sum=6; one hyphen: 1 -> total 7, 7 % 10 == 7 -> "7"
        line = "12a-3"
        expected = "7"
        self.assertEqual(perform_checksum_compute(line), expected)

    def test_empty_string(self):
        line = ""
        expected = "0"  # No characters leads to checksum 0.
        self.assertEqual(perform_checksum_compute(line), expected)

    def test_no_digits_or_hyphens(self):
        # Only letters/spaces => checksum should be "0"
        line = "ABC def"
        expected = "0"
        self.assertEqual(perform_checksum_compute(line), expected)

    def test_realistic_tle_line(self):
        # Example TLE line taken from TLE datasets.
        # "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
        # The expected checksum (as usually provided) is "6".
        line = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
        expected = "6"
        self.assertEqual(perform_checksum_compute(line), expected)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
