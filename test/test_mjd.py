# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import timedelta

from satelles.mjd import MJD_EPOCH_AS_DATETIME, convert_mjd_to_datetime

# **************************************************************************************


class TestMJDEpochAsDatetime(unittest.TestCase):
    def test_mjd_epoch_as_datetime(self):
        # Check that the MJD epoch corresponds to 1858-11-17 00:00:00 UTC:
        self.assertEqual(MJD_EPOCH_AS_DATETIME.year, 1858)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.month, 11)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.day, 17)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.hour, 0)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.minute, 0)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.second, 0)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.microsecond, 0)
        self.assertEqual(MJD_EPOCH_AS_DATETIME.tzinfo.utcoffset(None), timedelta(0))


# **************************************************************************************


class TestConvertMJDToDatetime(unittest.TestCase):
    def test_mjd_zero(self):
        """MJD 0 should map exactly to 1858-11-17 00:00:00 UTC."""
        result = convert_mjd_to_datetime(0.0)
        self.assertEqual(result, MJD_EPOCH_AS_DATETIME)

    def test_mjd_one(self):
        """MJD 1 should be one day after the epoch."""
        result = convert_mjd_to_datetime(1.0)
        self.assertEqual(result, MJD_EPOCH_AS_DATETIME + timedelta(days=1))

    def test_mjd_fractional(self):
        """A fractional MJD should advance by fractional days."""
        mjd_value = 0.5
        result = convert_mjd_to_datetime(mjd_value)
        self.assertEqual(result, MJD_EPOCH_AS_DATETIME + timedelta(days=0.5))

    def test_large_mjd(self):
        """Test a large MJD (e.g., 60000) against a known reference."""
        result = convert_mjd_to_datetime(59349)
        self.assertEqual(result, MJD_EPOCH_AS_DATETIME + timedelta(days=59349.0))
        self.assertEqual(result.year, 2021)
        self.assertEqual(result.month, 5)
        self.assertEqual(result.day, 15)
        self.assertEqual(result.hour, 0)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(result.microsecond, 0)
        self.assertEqual(result.tzinfo.utcoffset(None), timedelta(0))

    def test_large_mjd_fractional(self):
        result = convert_mjd_to_datetime(59349.25)
        self.assertEqual(result, MJD_EPOCH_AS_DATETIME + timedelta(days=59349.25))
        self.assertEqual(result.year, 2021)
        self.assertEqual(result.month, 5)
        self.assertEqual(result.day, 15)
        self.assertEqual(result.hour, 6)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(result.microsecond, 0)
        self.assertEqual(result.tzinfo.utcoffset(None), timedelta(0))


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
