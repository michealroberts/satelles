# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from satelles.frame import Reference

# **************************************************************************************


class TestReference(unittest.TestCase):
    def test_is_inertial(self):
        self.assertTrue(Reference.ECI.is_inertial)
        self.assertTrue(Reference.ICRF.is_inertial)
        self.assertTrue(Reference.EME2000.is_inertial)
        self.assertTrue(Reference.TEME.is_inertial)
        self.assertFalse(Reference.ECEF.is_inertial)
        self.assertFalse(Reference.ITRF.is_inertial)
        self.assertFalse(Reference.TOPOCENTRIC.is_inertial)

    def test_is_rotating(self):
        self.assertTrue(Reference.ECEF.is_rotating)
        self.assertTrue(Reference.ITRF.is_rotating)
        self.assertTrue(Reference.TOPOCENTRIC.is_rotating)
        self.assertFalse(Reference.ECI.is_rotating)
        self.assertFalse(Reference.ICRF.is_rotating)
        self.assertFalse(Reference.EME2000.is_rotating)
        self.assertFalse(Reference.TEME.is_rotating)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
