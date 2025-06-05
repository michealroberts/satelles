# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.cpf import h1_regex

# **************************************************************************************

apollo_15_h1 = "H1 CPF 2 OPA 2025 06 04 18 155 1 apollo15 OPA_ELP96"

# **************************************************************************************

galileo_101_h1 = "H1 CPF  2 ESA 2025  6  5 10 156 01 galileo101"

# **************************************************************************************

glonass105 = "H1 CPF  2  NER 2025  6  5 12  156 01 glonass105"

# **************************************************************************************

lageos_h1 = "H1 CPF  2  DGF 2025 06 05 10 156 01 lageos1    NONE"

# **************************************************************************************

lares_h1 = "H1 CPF  2  DGF 2025 06 05 11 156 01 lares      NONE"

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

    def test_valid_glonass105(self):
        m = h1_regex.match(glonass105)
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
            h1_regex.match(bad_line), "Non‐numeric year field should fail"
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
