# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import datetime, timedelta, timezone

from satelles.mjd import (
    MJD_EPOCH_AS_DATETIME,
    convert_mjd_to_datetime,
    get_modified_julian_date_as_parts,
    get_modified_julian_date_from_parts,
)

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


class TestGetModifiedJulianDateFromParts(unittest.TestCase):
    def test_epoch_parts(self):
        """(0 days, 0 seconds) should return the MJD epoch."""
        dt = get_modified_julian_date_from_parts((0, 0.0))
        self.assertEqual(dt, MJD_EPOCH_AS_DATETIME)

    def test_half_day_offset(self):
        """
        (0 days, 43200 seconds) should return epoch + 0.5 days (i.e., 12:00 UTC on
        the epoch date).
        """
        dt = get_modified_julian_date_from_parts((0, 43200.0))
        expected = MJD_EPOCH_AS_DATETIME + timedelta(hours=12)
        self.assertEqual(dt, expected)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.microsecond, 0)

    def test_large_mjd_parts(self):
        """Test a large MJD (e.g., 59349, 0.0) against a known reference."""
        dt = get_modified_julian_date_from_parts((59349, 0.0))
        expected = MJD_EPOCH_AS_DATETIME + timedelta(days=59349.0)
        self.assertEqual(dt, expected)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 5)
        self.assertEqual(dt.day, 15)
        self.assertEqual(dt.hour, 0)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.microsecond, 0)

    def test_fractional_seconds_of_day_parts(self):
        """
        Test a large fractional MJD (e.g., 59349, 43200.0) to ensure it returns the
        correct datetime.
        """
        dt = get_modified_julian_date_from_parts((59349, 43200.895))
        expected = MJD_EPOCH_AS_DATETIME + timedelta(days=59349.0, seconds=43200.895)
        self.assertEqual(dt, expected)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 5)
        self.assertEqual(dt.day, 15)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.microsecond, 895000)


# **************************************************************************************


class TestGetModifiedJulianDateAsParts(unittest.TestCase):
    def test_mjd_zero(self) -> None:
        """MJD 0 should return (0, 0.0) for parts."""
        when = convert_mjd_to_datetime(0.0)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(when)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertEqual(mjd, 0)
        self.assertEqual(seconds_of_day, 0.0)

    def test_mjd_one(self) -> None:
        """MJD 1 should be one day after the epoch."""
        when = convert_mjd_to_datetime(1.0)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(when)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertEqual(mjd, 1)
        self.assertEqual(seconds_of_day, 0.0)

    def test_mjd_fractional(self) -> None:
        """A fractional MJD should advance by fractional days."""
        when = convert_mjd_to_datetime(0.5)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(when)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 0)
        self.assertAlmostEqual(seconds_of_day, 43200.0, places=5)

    def test_large_mjd(self) -> None:
        """Test a large MJD (e.g., 60000) against a known reference."""
        when = convert_mjd_to_datetime(59349)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(when)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 59349)
        self.assertEqual(seconds_of_day, 0.0)

    def test_large_mjd_fractional(self) -> None:
        """Test a large fractional MJD (e.g., 59349.25)."""
        when = convert_mjd_to_datetime(59349.25)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(when)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 59349)
        self.assertAlmostEqual(seconds_of_day, 21600.0, places=5)

    def test_naive_datetime(self) -> None:
        """Test a naive datetime (assumed UTC) to ensure it works."""
        naive_datetime = datetime(2021, 5, 15, 12, 0, 0)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(naive_datetime)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 59349)
        self.assertAlmostEqual(seconds_of_day, 43200.0, places=5)

    def test_utc_datetime(self) -> None:
        """Test a UTC datetime to ensure it works."""
        utc_datetime = datetime(2021, 5, 15, 12, 0, 0, tzinfo=timezone.utc)
        mjd, seconds_of_day = get_modified_julian_date_as_parts(utc_datetime)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 59349)
        self.assertAlmostEqual(seconds_of_day, 43200.0, places=5)

    def test_non_utc_datetime(self) -> None:
        """Test a non-UTC datetime to ensure it converts to UTC."""
        timezone_offset = -5
        local_datetime = datetime(
            2021, 5, 15, 12, 0, 0, tzinfo=timezone(timedelta(hours=timezone_offset))
        )
        mjd, seconds_of_day = get_modified_julian_date_as_parts(local_datetime)
        self.assertIsInstance(mjd, int)
        self.assertGreaterEqual(mjd, 0)
        self.assertGreaterEqual(seconds_of_day, 0.0)
        self.assertLess(seconds_of_day, 86400.0)
        self.assertEqual(mjd, 59349)
        self.assertAlmostEqual(
            seconds_of_day, 43200.0 - (timezone_offset * 60 * 60), places=5
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
