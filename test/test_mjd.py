# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import unittest
from datetime import timedelta

from satelles.mjd import MJD_EPOCH_AS_DATETIME

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
