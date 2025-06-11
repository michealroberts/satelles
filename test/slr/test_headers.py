# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.slr import (
    h1_regex,
    h2_regex,
    h3_regex,
    h4_regex,
    h5_regex,
)

# **************************************************************************************

apollo_15_h1 = "H1 CPF 2 OPA 2025 06 04 18 155 1 apollo15 OPA_ELP96"

apollo_15_h2 = "H2 103 103 0 2025 6 5 0 0 0 2025 6 9 23 45 0 900 0 1 0 0 0 3"

apollo_15_h4 = "H4  1000.0000    0.1234    1000.50      -0.05  86399.999999999999"

# **************************************************************************************

galileo_101_h1 = "H1 CPF  2 ESA 2025  6  5 10 156 01 galileo101"

galileo_101_h2 = "H2  1106001 7101    37846 2025  6  4 23 59 42 2025  6  9 23 59 42   900 1 1  0 0 0  1"

# **************************************************************************************

glonass_105_h1 = "H1 CPF  2  NER 2025  6  5 12  156 01 glonass105"

glonass_105_h2 = "H2  0705202 9105    32276 2025  6  5  0  0  0 2025  6  8 23 45  0   900 1 1  0 0 0 1"

# **************************************************************************************

lageos_h1 = "H1 CPF  2  DGF 2025 06 05 10 156 01 lageos1    NONE"

lageos_h2 = "H2  7603901 1155     8820 2025 06 05 00 00 00 2025 06 12 00 00 00    60 1 1  0 0 0 1"

lageos_h3 = "H3  0.00000  0.00000  0.00000  0.00500  0.00300  0.00200  0.02000  0.01500  0.01000"

lageos_h4 = "H4  2000.0000    2.3456      37.00       0.02  43200.123456789012"

lageos_h5 = "H5  0.2450"

# **************************************************************************************

lares_h1 = "H1 CPF  2  DGF 2025 06 05 11 156 01 lares      NONE"

lares_h2 = "H2  1200601 5987    38077 2025 06 05 00 00 00 2025 06 12 00 00 00    30 1 1  0 0 0 1"

lares_h4 = "H4  5000.0000    5.6789       0.00       0.10  12345.000000123456"

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
        self.assertEqual(m.group("tiv_compatibility"), "0")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rotational_angle_type"), "0")
        self.assertEqual(m.group("center_of_mass_correction"), "0")
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
        self.assertEqual(m.group("tiv_compatibility"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rotational_angle_type"), "0")
        self.assertEqual(m.group("center_of_mass_correction"), "0")
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
        self.assertEqual(m.group("tiv_compatibility"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rotational_angle_type"), "0")
        self.assertEqual(m.group("center_of_mass_correction"), "0")
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
        self.assertEqual(m.group("tiv_compatibility"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rotational_angle_type"), "0")
        self.assertEqual(m.group("center_of_mass_correction"), "0")
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
        self.assertEqual(m.group("tiv_compatibility"), "1")
        self.assertEqual(m.group("target_class"), "1")
        self.assertEqual(m.group("reference_frame"), "0")
        self.assertEqual(m.group("rotational_angle_type"), "0")
        self.assertEqual(m.group("center_of_mass_correction"), "0")
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


class TestCPFH30Regex(unittest.TestCase):
    def test_valid_lageos_h3(self):
        m = h3_regex.match(lageos_h3)
        self.assertIsNotNone(m, "Lageos H3 should match")
        self.assertEqual(m.group("along_track_runoff_at_0_hours"), "0.00000")
        self.assertEqual(m.group("cross_track_runoff_at_0_hours"), "0.00000")
        self.assertEqual(m.group("radial_runoff_at_0_hours"), "0.00000")
        self.assertEqual(m.group("along_track_runoff_at_6_hours"), "0.00500")
        self.assertEqual(m.group("cross_track_runoff_at_6_hours"), "0.00300")
        self.assertEqual(m.group("radial_runoff_at_6_hours"), "0.00200")
        self.assertEqual(m.group("along_track_runoff_at_24_hours"), "0.02000")
        self.assertEqual(m.group("cross_track_runoff_at_24_hours"), "0.01500")
        self.assertEqual(m.group("radial_runoff_at_24_hours"), "0.01000")

    def test_invalid_not_h3(self):
        bad_line = (
            "H2 0.00000 0.00000 0.00000 0.00500 0.00300 0.00200 0.02000 0.01500 0.01000"
        )
        self.assertIsNone(
            h3_regex.match(bad_line), "Record type other than H3 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "H3 0.00000 0.00000 0.00000 0.00500 0.00300"
        self.assertIsNone(h3_regex.match(bad_line), "Too few fields should fail")

    def test_invalid_non_numeric(self):
        bad_line = (
            "H3 abc.defgh 0.00000 0.00500 0.00300 0.00200 0.02000 0.01500 0.01000"
        )
        self.assertIsNone(h3_regex.match(bad_line), "Non-numeric X bias should fail")


# **************************************************************************************


class TestCPFH4Regex(unittest.TestCase):
    def test_valid_apollo_15_h4(self):
        m = h4_regex.match(apollo_15_h4)
        self.assertIsNotNone(m, "Apollo 15 H4 should match")
        self.assertEqual(m.group("pulse_repetition_frequency"), "1000.0000")
        self.assertEqual(m.group("transponder_transmit_delay"), "0.1234")
        self.assertEqual(m.group("transponder_utc_offset"), "1000.50")
        self.assertEqual(m.group("transponder_oscillator_drift"), "-0.05")
        self.assertEqual(
            m.group("transponder_clock_reference_time"), "86399.999999999999"
        )

    def test_valid_lageos_h4(self):
        m = h4_regex.match(lageos_h4)
        self.assertIsNotNone(m, "Lageos H4 should match")
        self.assertEqual(m.group("pulse_repetition_frequency"), "2000.0000")
        self.assertEqual(m.group("transponder_transmit_delay"), "2.3456")
        self.assertEqual(m.group("transponder_utc_offset"), "37.00")
        self.assertEqual(m.group("transponder_oscillator_drift"), "0.02")
        self.assertEqual(
            m.group("transponder_clock_reference_time"), "43200.123456789012"
        )

    def test_valid_lares_h4(self):
        m = h4_regex.match(lares_h4)
        self.assertIsNotNone(m, "Lares H4 should match")
        self.assertEqual(m.group("pulse_repetition_frequency"), "5000.0000")
        self.assertEqual(m.group("transponder_transmit_delay"), "5.6789")
        self.assertEqual(m.group("transponder_utc_offset"), "0.00")
        self.assertEqual(m.group("transponder_oscillator_drift"), "0.10")
        self.assertEqual(
            m.group("transponder_clock_reference_time"), "12345.000000123456"
        )

    def test_invalid_not_h4(self):
        bad_line = "H3 2000.0000 2.3456 37.00 0.02 43200.123456789012"
        self.assertIsNone(
            h4_regex.match(bad_line), "Record type other than H4 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "H4 2000.0000 2.3456 37.00 0.02"
        self.assertIsNone(h4_regex.match(bad_line), "Too few fields should fail")

    def test_invalid_non_numeric(self):
        bad_line = "H4 2000.0000 2.3456 abc.defgh 0.02 43200.123456789012"
        self.assertIsNone(
            h4_regex.match(bad_line), "Non-numeric transponder UTC offset should fail"
        )


# **************************************************************************************


class TestCPFH5Regex(unittest.TestCase):
    def test_valid_lageos_h5(self):
        lageos_h5 = "H5 0.2450"
        m = h5_regex.match(lageos_h5)
        self.assertIsNotNone(m, "Lageos H5 should match")
        self.assertEqual(m.group("center_of_mass_to_reflector_offset"), "0.2450")

    def test_invalid_not_h5(self):
        bad_line = "H2 0.2450"
        self.assertIsNone(
            h5_regex.match(bad_line), "Record type other than H5 should fail"
        )

    def test_invalid_missing_fields(self):
        bad_line = "H5 0.2450 0.1234"
        self.assertIsNone(h5_regex.match(bad_line), "Too many fields should fail")

    def test_invalid_non_numeric(self):
        bad_line = "H5 abc.defgh"
        self.assertIsNone(
            h5_regex.match(bad_line), "Non-numeric center of mass offset should fail"
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
