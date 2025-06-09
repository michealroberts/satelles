# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.slr import (
    e10_regex,
    e20_regex,
    e30_regex,
)

# **************************************************************************************

apollo_15_10 = (
    "10 1 60835   85500.0 0       352072320.278       -83567364.603      -173273869.404"
)

apollo_15_20 = "20 1 2190.123456 -1850.654321 2100.987654"

apollo_15_30 = "30 1        3430.     -39000.       2982.    26.0"

# **************************************************************************************

galileo_101_10 = (
    "10 0 60835  86382.000000  0      -9151185.629      25534182.361      11819411.299"
)

galileo_101_20 = "20 0 -350.123456 720.654321 1800.987654"

galileo_101_30 = "30 0 -500.123456 250.654321 -100.000000 1.5"

# **************************************************************************************

glonass_105_10 = "10 0 60834  85500.00000  0  -3027287.597  18473674.047  17310722.799"

glonass_105_20 = "20 0 -1800.123456 3600.654321 5400.987654"

glonass_105_30 = "30 0 -2000.123456 1500.654321 -300.000000 2.0"

# **************************************************************************************

lageos_10 = (
    "10 0 60837  86340.000000  0       3105278.540      -5872619.369     -10373183.293"
)

lageos_20 = "20 0 750.123456 -620.654321 -1300.987654"

lageos_30 = "30 0 800.123456 -700.654321 -200.000000 2.5"

# **************************************************************************************

lares_10 = (
    "10 0 60837  86370.000000  0       4909758.210      -5452680.749       2690387.910"
)

lares_20 = "20 0 400.123456 300.654321 -500.987654"

lares_30 = "30 0 500.123456 400.654321 -100.000000 3.0"

# **************************************************************************************


class TestCPF10Regex(unittest.TestCase):
    def test_valid_apollo_15_10(self):
        m = e10_regex.match(apollo_15_10)
        self.assertIsNotNone(m, "Apollo 15 record 10 should match")
        self.assertEqual(m.group("direction"), "1")
        self.assertEqual(m.group("mjd"), "60835")
        self.assertEqual(m.group("seconds"), "85500.0")
        self.assertEqual(m.group("leap_second"), "0")
        self.assertEqual(m.group("x"), "352072320.278")
        self.assertEqual(m.group("y"), "-83567364.603")
        self.assertEqual(m.group("z"), "-173273869.404")

    def test_valid_galileo_101_10(self):
        m = e10_regex.match(galileo_101_10)
        self.assertIsNotNone(m, "Galileo 101 record 10 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("mjd"), "60835")
        self.assertEqual(m.group("seconds"), "86382.000000")
        self.assertEqual(m.group("leap_second"), "0")
        self.assertEqual(m.group("x"), "-9151185.629")
        self.assertEqual(m.group("y"), "25534182.361")
        self.assertEqual(m.group("z"), "11819411.299")

    def test_valid_glonass_105_10(self):
        m = e10_regex.match(glonass_105_10)
        self.assertIsNotNone(m, "Glonass 105 record 10 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("mjd"), "60834")
        self.assertEqual(m.group("seconds"), "85500.00000")
        self.assertEqual(m.group("leap_second"), "0")
        self.assertEqual(m.group("x"), "-3027287.597")
        self.assertEqual(m.group("y"), "18473674.047")
        self.assertEqual(m.group("z"), "17310722.799")

    def test_valid_lageos_10(self):
        m = e10_regex.match(lageos_10)
        self.assertIsNotNone(m, "Lageos record 10 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("mjd"), "60837")
        self.assertEqual(m.group("seconds"), "86340.000000")
        self.assertEqual(m.group("leap_second"), "0")
        self.assertEqual(m.group("x"), "3105278.540")
        self.assertEqual(m.group("y"), "-5872619.369")
        self.assertEqual(m.group("z"), "-10373183.293")

    def test_valid_lares_10(self):
        m = e10_regex.match(lares_10)
        self.assertIsNotNone(m, "Lares record 10 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("mjd"), "60837")
        self.assertEqual(m.group("seconds"), "86370.000000")
        self.assertEqual(m.group("leap_second"), "0")
        self.assertEqual(m.group("x"), "4909758.210")
        self.assertEqual(m.group("y"), "-5452680.749")
        self.assertEqual(m.group("z"), "2690387.910")

    def test_invalid_not_10(self):
        bad_line = "11 0 60835 85500.000000 0 0 0"
        self.assertIsNone(
            e10_regex.match(bad_line), "Record type other than 10 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "10 0 60835 85500.000000 0 0"
        self.assertIsNone(
            e10_regex.match(bad_line), "Too few coordinate fields should fail"
        )

    def test_invalid_non_numeric_direction(self):
        bad_line = "10 X 60835 85500.000000 0 0 0"
        self.assertIsNone(
            e10_regex.match(bad_line), "Non-numeric direction flag should fail"
        )


# **************************************************************************************


class TestCPF20Regex(unittest.TestCase):
    def test_valid_apollo_15_20(self):
        m = e20_regex.match(apollo_15_20)
        self.assertIsNotNone(m, "Apollo 15 record 20 should match")
        self.assertEqual(m.group("direction"), "1")
        self.assertEqual(m.group("vx"), "2190.123456")
        self.assertEqual(m.group("vy"), "-1850.654321")
        self.assertEqual(m.group("vz"), "2100.987654")

    def test_valid_galileo_101_20(self):
        m = e20_regex.match(galileo_101_20)
        self.assertIsNotNone(m, "Galileo 101 record 20 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("vx"), "-350.123456")
        self.assertEqual(m.group("vy"), "720.654321")
        self.assertEqual(m.group("vz"), "1800.987654")

    def test_valid_glonass_105_20(self):
        m = e20_regex.match(glonass_105_20)
        self.assertIsNotNone(m, "Glonass 105 record 20 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("vx"), "-1800.123456")
        self.assertEqual(m.group("vy"), "3600.654321")
        self.assertEqual(m.group("vz"), "5400.987654")

    def test_valid_lageos_20(self):
        m = e20_regex.match(lageos_20)
        self.assertIsNotNone(m, "Lageos record 20 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("vx"), "750.123456")
        self.assertEqual(m.group("vy"), "-620.654321")
        self.assertEqual(m.group("vz"), "-1300.987654")

    def test_valid_lares_20(self):
        m = e20_regex.match(lares_20)
        self.assertIsNotNone(m, "Lares record 20 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("vx"), "400.123456")
        self.assertEqual(m.group("vy"), "300.654321")
        self.assertEqual(m.group("vz"), "-500.987654")

    def test_invalid_not_20(self):
        bad_line = "10 0 2190.123456 -1850.654321 2100.987654"
        self.assertIsNone(
            e20_regex.match(bad_line), "Record type other than 20 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "20 0 -350.123456 720.654321"
        self.assertIsNone(
            e20_regex.match(bad_line), "Too few velocity fields should fail"
        )

    def test_invalid_non_numeric_velocity(self):
        bad_line = "20 0 abc.def456 720.654321 1800.987654"
        self.assertIsNone(e20_regex.match(bad_line), "Non-numeric VX field should fail")


# **************************************************************************************


class TestCPF30Regex(unittest.TestCase):
    def test_valid_apollo_15_30(self):
        m = e30_regex.match(apollo_15_30)
        self.assertIsNotNone(m, "Apollo 15 record 30 should match")
        self.assertEqual(m.group("direction"), "1")
        self.assertEqual(m.group("x_aberration"), "3430.")
        self.assertEqual(m.group("y_aberration"), "-39000.")
        self.assertEqual(m.group("z_aberration"), "2982.")
        self.assertEqual(
            m.group("relativistic_range_correction_in_nanoseconds"), "26.0"
        )

    def test_valid_galileo_101_30(self):
        m = e30_regex.match(galileo_101_30)
        self.assertIsNotNone(m, "Galileo 101 record 30 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("x_aberration"), "-500.123456")
        self.assertEqual(m.group("y_aberration"), "250.654321")
        self.assertEqual(m.group("z_aberration"), "-100.000000")
        self.assertEqual(m.group("relativistic_range_correction_in_nanoseconds"), "1.5")

    def test_valid_glonass_105_30(self):
        m = e30_regex.match(glonass_105_30)
        self.assertIsNotNone(m, "Glonass 105 record 30 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("x_aberration"), "-2000.123456")
        self.assertEqual(m.group("y_aberration"), "1500.654321")
        self.assertEqual(m.group("z_aberration"), "-300.000000")
        self.assertEqual(m.group("relativistic_range_correction_in_nanoseconds"), "2.0")

    def test_valid_lageos_30(self):
        m = e30_regex.match(lageos_30)
        self.assertIsNotNone(m, "Lageos record 30 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("x_aberration"), "800.123456")
        self.assertEqual(m.group("y_aberration"), "-700.654321")
        self.assertEqual(m.group("z_aberration"), "-200.000000")
        self.assertEqual(m.group("relativistic_range_correction_in_nanoseconds"), "2.5")

    def test_valid_lares_30(self):
        m = e30_regex.match(lares_30)
        self.assertIsNotNone(m, "Lares record 30 should match")
        self.assertEqual(m.group("direction"), "0")
        self.assertEqual(m.group("x_aberration"), "500.123456")
        self.assertEqual(m.group("y_aberration"), "400.654321")
        self.assertEqual(m.group("z_aberration"), "-100.000000")
        self.assertEqual(m.group("relativistic_range_correction_in_nanoseconds"), "3.0")

    def test_invalid_not_30(self):
        bad_line = "10 1 3430. -39000. 2982. 26.0"
        self.assertIsNone(
            e30_regex.match(bad_line), "Record type other than 30 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "30 1 -500.123456 250.654321"
        self.assertIsNone(
            e30_regex.match(bad_line), "Too few aberration fields should fail"
        )

    def test_invalid_non_numeric_aberration(self):
        bad_line = "30 1 abc.def456 250.654321 -100.000000 1.5"
        self.assertIsNone(
            e30_regex.match(bad_line), "Non-numeric X aberration field should fail"
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
