# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.cpf import e10_regex, e20_regex, e30_regex, h1_regex, h2_regex

# **************************************************************************************

apollo_15_h1 = "H1 CPF 2 OPA 2025 06 04 18 155 1 apollo15 OPA_ELP96"

apollo_15_h2 = "H2 103 103 0 2025 6 5 0 0 0 2025 6 9 23 45 0 900 0 1 0 0 0 3"

apollo_15_10 = (
    "10 1 60835   85500.0 0       352072320.278       -83567364.603      -173273869.404"
)

apollo_15_20 = "20 1 2190.123456 -1850.654321 2100.987654"

apollo_15_30 = "30 1        3430.     -39000.       2982.    26.0"

# **************************************************************************************

galileo_101_h1 = "H1 CPF  2 ESA 2025  6  5 10 156 01 galileo101"

galileo_101_h2 = "H2  1106001 7101    37846 2025  6  4 23 59 42 2025  6  9 23 59 42   900 1 1  0 0 0  1"

galileo_101_10 = (
    "10 0 60835  86382.000000  0      -9151185.629      25534182.361      11819411.299"
)

galileo_101_20 = "20 0 -350.123456 720.654321 1800.987654"

galileo_101_30 = "30 0 -500.123456 250.654321 -100.000000 1.5"

# **************************************************************************************

glonass_105_h1 = "H1 CPF  2  NER 2025  6  5 12  156 01 glonass105"

glonass_105_h2 = "H2  0705202 9105    32276 2025  6  5  0  0  0 2025  6  8 23 45  0   900 1 1  0 0 0 1"

glonass_105_10 = "10 0 60834  85500.00000  0  -3027287.597  18473674.047  17310722.799"

glonass_105_20 = "20 0 -1800.123456 3600.654321 5400.987654"

glonass_105_30 = "30 0 -2000.123456 1500.654321 -300.000000 2.0"

# **************************************************************************************

lageos_h1 = "H1 CPF  2  DGF 2025 06 05 10 156 01 lageos1    NONE"

lageos_h2 = "H2  7603901 1155     8820 2025 06 05 00 00 00 2025 06 12 00 00 00    60 1 1  0 0 0 1"

lageos_10 = (
    "10 0 60837  86340.000000  0       3105278.540      -5872619.369     -10373183.293"
)

lageos_20 = "20 0 750.123456 -620.654321 -1300.987654"

lageos_30 = "30 0 800.123456 -700.654321 -200.000000 2.5"

# **************************************************************************************

lares_h1 = "H1 CPF  2  DGF 2025 06 05 11 156 01 lares      NONE"

lares_h2 = "H2  1200601 5987    38077 2025 06 05 00 00 00 2025 06 12 00 00 00    30 1 1  0 0 0 1"

lares_10 = (
    "10 0 60837  86370.000000  0       4909758.210      -5452680.749       2690387.910"
)

lares_20 = "20 0 400.123456 300.654321 -500.987654"

lares_30 = "30 0 500.123456 400.654321 -100.000000 3.0"

# **************************************************************************************


class TestCPFH1Regex(unittest.TestCase):
    def test_valid_apollo_15(self):
        m = h1_regex.match(apollo_15_h1)
        self.assertIsNotNone(m, "Apollo 15 H1 should match")
        self.assertEqual(m.group("version"), "2")
        self.assertEqual(m.group("ephemeris_source"), "OPA")
        self.assertEqual(m.group("year"), "2025")
        self.assertEqual(m.group("month"), "06")
        self.assertEqual(m.group("day"), "04")
        self.assertEqual(m.group("hour"), "18")
        self.assertEqual(m.group("ephemeris_sequence_number"), "155")
        self.assertEqual(m.group("sub_daily_sequence_number"), "1")
        self.assertEqual(m.group("target_name"), "apollo15")
        self.assertEqual(m.group("notes"), "OPA_ELP96")

    def test_valid_galileo_101(self):
        m = h1_regex.match(galileo_101_h1)
        self.assertIsNotNone(m, "Galileo 101 H1 should match")
        self.assertEqual(m.group("version"), "2")
        self.assertEqual(m.group("ephemeris_source"), "ESA")
        self.assertEqual(m.group("year"), "2025")
        # Month and day can be single‐digit, so "6" and "5":
        self.assertEqual(m.group("month"), "6")
        self.assertEqual(m.group("day"), "5")
        self.assertEqual(m.group("hour"), "10")
        self.assertEqual(m.group("ephemeris_sequence_number"), "156")
        self.assertEqual(m.group("sub_daily_sequence_number"), "01")
        self.assertEqual(m.group("target_name"), "galileo101")
        # Since no notes are provided, group("notes") must be None:
        self.assertIsNone(m.group("notes"))

    def test_valid_glonass_105(self):
        m = h1_regex.match(glonass_105_h1)
        self.assertIsNotNone(m, "Glonass 105 H1 should match")
        self.assertEqual(m.group("version"), "2")
        self.assertEqual(m.group("ephemeris_source"), "NER")
        self.assertEqual(m.group("year"), "2025")
        self.assertEqual(m.group("month"), "6")
        self.assertEqual(m.group("day"), "5")
        self.assertEqual(m.group("hour"), "12")
        self.assertEqual(m.group("ephemeris_sequence_number"), "156")
        self.assertEqual(m.group("sub_daily_sequence_number"), "01")
        self.assertEqual(m.group("target_name"), "glonass105")
        # Since no notes are provided, group("notes") must be None:
        self.assertIsNone(m.group("notes"))

    def test_valid_lageos(self):
        m = h1_regex.match(lageos_h1)
        self.assertIsNotNone(m, "Lageos H1 should match")
        self.assertEqual(m.group("version"), "2")
        self.assertEqual(m.group("ephemeris_source"), "DGF")
        self.assertEqual(m.group("year"), "2025")
        self.assertEqual(m.group("month"), "06")
        self.assertEqual(m.group("day"), "05")
        self.assertEqual(m.group("hour"), "10")
        self.assertEqual(m.group("ephemeris_sequence_number"), "156")
        self.assertEqual(m.group("sub_daily_sequence_number"), "01")
        self.assertEqual(m.group("target_name"), "lageos1")
        self.assertEqual(m.group("notes"), "NONE")

    def test_valid_lares(self):
        m = h1_regex.match(lares_h1)
        self.assertIsNotNone(m, "Lares H1 should match")
        self.assertEqual(m.group("version"), "2")
        self.assertEqual(m.group("ephemeris_source"), "DGF")
        self.assertEqual(m.group("year"), "2025")
        self.assertEqual(m.group("month"), "06")
        self.assertEqual(m.group("day"), "05")
        self.assertEqual(m.group("hour"), "11")
        self.assertEqual(m.group("ephemeris_sequence_number"), "156")
        self.assertEqual(m.group("sub_daily_sequence_number"), "01")
        self.assertEqual(m.group("target_name"), "lares")
        self.assertEqual(m.group("notes"), "NONE")

    def test_invalid_not_h1(self):
        bad_line = "H2 CPF 2 OPA 2025 06 04 18 155 1 apollo15 OPA_ELP96"
        self.assertIsNone(
            h1_regex.match(bad_line), "Record type other than H1 should fail"
        )

    def test_invalid_not_cpf(self):
        bad_line = "H1 CPX 2 OPA 2025 06 04 18 155 1 apollo15 OPA_ELP96"
        self.assertIsNone(
            h1_regex.match(bad_line), "Literal 'CPF' spelled incorrectly should fail"
        )

    def test_invalid_missing_fields(self):
        # Missing sub‐daily seq. no., target_name, and notes
        bad_line = "H1 CPF 2 OPA 2025 06 04 18 155"
        self.assertIsNone(h1_regex.match(bad_line), "Too few fields should fail")

    def test_invalid_bad_date(self):
        # Non‐numeric year field should fail
        bad_line = "H1 CPF 2 OPA YYYY 06 04 18 155 1 apollo15 OPA_ELP96"
        self.assertIsNone(
            h1_regex.match(bad_line), "Non-numeric year field should fail"
        )


# **************************************************************************************


class TestCPFH2Regex(unittest.TestCase):
    def test_valid_apollo_15_h2(self):
        m = h2_regex.match(apollo_15_h2)
        self.assertIsNotNone(m, "Apollo 15 H2 should match")
        self.assertEqual(m.group("cospar_id"), "103")
        self.assertEqual(m.group("sic"), "103")
        self.assertEqual(m.group("norad_id"), "0")
        self.assertEqual(m.group("start_year"), "2025")
        self.assertEqual(m.group("start_month"), "6")
        self.assertEqual(m.group("start_day"), "5")
        self.assertEqual(m.group("start_hour"), "0")
        self.assertEqual(m.group("start_minute"), "0")
        self.assertEqual(m.group("start_second"), "0")
        self.assertEqual(m.group("end_year"), "2025")
        self.assertEqual(m.group("end_month"), "6")
        self.assertEqual(m.group("end_day"), "9")
        self.assertEqual(m.group("end_hour"), "23")
        self.assertEqual(m.group("end_minute"), "45")
        self.assertEqual(m.group("end_second"), "0")
        self.assertEqual(m.group("interval"), "900")
        self.assertEqual(m.group("tiv_compat"), "0")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rot_angle_type"), "0")
        self.assertEqual(m.group("com_correction"), "0")
        self.assertEqual(m.group("location_dynamics"), "3")

    def test_valid_galileo_101_h2(self):
        m = h2_regex.match(galileo_101_h2)
        self.assertIsNotNone(m, "Galileo 101 H2 should match")
        self.assertEqual(m.group("cospar_id"), "1106001")
        self.assertEqual(m.group("sic"), "7101")
        self.assertEqual(m.group("norad_id"), "37846")
        self.assertEqual(m.group("start_year"), "2025")
        self.assertEqual(m.group("start_month"), "6")
        self.assertEqual(m.group("start_day"), "4")
        self.assertEqual(m.group("start_hour"), "23")
        self.assertEqual(m.group("start_minute"), "59")
        self.assertEqual(m.group("start_second"), "42")
        self.assertEqual(m.group("end_year"), "2025")
        self.assertEqual(m.group("end_month"), "6")
        self.assertEqual(m.group("end_day"), "9")
        self.assertEqual(m.group("end_hour"), "23")
        self.assertEqual(m.group("end_minute"), "59")
        self.assertEqual(m.group("end_second"), "42")
        self.assertEqual(m.group("interval"), "900")
        self.assertEqual(m.group("tiv_compat"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rot_angle_type"), "0")
        self.assertEqual(m.group("com_correction"), "0")
        self.assertEqual(m.group("location_dynamics"), "1")

    def test_valid_glonass_105_h2(self):
        m = h2_regex.match(glonass_105_h2)
        self.assertIsNotNone(m, "Glonass 105 H2 should match")
        self.assertEqual(m.group("cospar_id"), "0705202")
        self.assertEqual(m.group("sic"), "9105")
        self.assertEqual(m.group("norad_id"), "32276")
        self.assertEqual(m.group("start_year"), "2025")
        self.assertEqual(m.group("start_month"), "6")
        self.assertEqual(m.group("start_day"), "5")
        self.assertEqual(m.group("start_hour"), "0")
        self.assertEqual(m.group("start_minute"), "0")
        self.assertEqual(m.group("start_second"), "0")
        self.assertEqual(m.group("end_year"), "2025")
        self.assertEqual(m.group("end_month"), "6")
        self.assertEqual(m.group("end_day"), "8")
        self.assertEqual(m.group("end_hour"), "23")
        self.assertEqual(m.group("end_minute"), "45")
        self.assertEqual(m.group("end_second"), "0")
        self.assertEqual(m.group("interval"), "900")
        self.assertEqual(m.group("tiv_compat"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rot_angle_type"), "0")
        self.assertEqual(m.group("com_correction"), "0")
        self.assertEqual(m.group("location_dynamics"), "1")

    def test_valid_lageos_h2(self):
        m = h2_regex.match(lageos_h2)
        self.assertIsNotNone(m, "Lageos H2 should match")
        self.assertEqual(m.group("cospar_id"), "7603901")
        self.assertEqual(m.group("sic"), "1155")
        self.assertEqual(m.group("norad_id"), "8820")
        self.assertEqual(m.group("start_year"), "2025")
        self.assertEqual(m.group("start_month"), "06")
        self.assertEqual(m.group("start_day"), "05")
        self.assertEqual(m.group("start_hour"), "00")
        self.assertEqual(m.group("start_minute"), "00")
        self.assertEqual(m.group("start_second"), "00")
        self.assertEqual(m.group("end_year"), "2025")
        self.assertEqual(m.group("end_month"), "06")
        self.assertEqual(m.group("end_day"), "12")
        self.assertEqual(m.group("end_hour"), "00")
        self.assertEqual(m.group("end_minute"), "00")
        self.assertEqual(m.group("end_second"), "00")
        self.assertEqual(m.group("interval"), "60")
        self.assertEqual(m.group("tiv_compat"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rot_angle_type"), "0")
        self.assertEqual(m.group("com_correction"), "0")
        self.assertEqual(m.group("location_dynamics"), "1")

    def test_valid_lares_h2(self):
        m = h2_regex.match(lares_h2)
        self.assertIsNotNone(m, "Lares H2 should match")
        self.assertEqual(m.group("cospar_id"), "1200601")
        self.assertEqual(m.group("sic"), "5987")
        self.assertEqual(m.group("norad_id"), "38077")
        self.assertEqual(m.group("start_year"), "2025")
        self.assertEqual(m.group("start_month"), "06")
        self.assertEqual(m.group("start_day"), "05")
        self.assertEqual(m.group("start_hour"), "00")
        self.assertEqual(m.group("start_minute"), "00")
        self.assertEqual(m.group("start_second"), "00")
        self.assertEqual(m.group("end_year"), "2025")
        self.assertEqual(m.group("end_month"), "06")
        self.assertEqual(m.group("end_day"), "12")
        self.assertEqual(m.group("end_hour"), "00")
        self.assertEqual(m.group("end_minute"), "00")
        self.assertEqual(m.group("end_second"), "00")
        self.assertEqual(m.group("interval"), "30")
        self.assertEqual(m.group("tiv_compat"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rot_angle_type"), "0")
        self.assertEqual(m.group("com_correction"), "0")
        self.assertEqual(m.group("location_dynamics"), "1")

    def test_invalid_not_h2(self):
        bad_line = "H1 103 103 0 2025 6 5 0 0 0 2025 6 9 23 45 0 900 0 1 0 0 0 3"
        self.assertIsNone(
            h2_regex.match(bad_line), "Record type other than H2 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "H2 103 103 0 2025 6 5 0 0 0 2025 6"
        self.assertIsNone(h2_regex.match(bad_line), "Too few fields should fail")

    def test_invalid_non_numeric(self):
        bad_line = "H2 ABCDEFGH 103 0 2025 6 5 0 0 0 2025 6 9 23 45 0 900 0 1 0 0 0 3"
        self.assertIsNone(h2_regex.match(bad_line), "Non-numeric COSPAR ID should fail")


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
