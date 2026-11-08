# **************************************************************************************
#
# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts
#
# **************************************************************************************

import os
import time
import unittest
from contextlib import contextmanager
from typing import Iterator

from satelles.common import CartesianCoordinate

# **************************************************************************************


class SatellesTestCase(unittest.TestCase):
    def assertCoordinatesAlmostEqual(
        self,
        expected: CartesianCoordinate,
        actual: CartesianCoordinate,
        places: int = 6,
    ) -> None:
        self.assertAlmostEqual(expected["x"], actual["x"], places=places)
        self.assertAlmostEqual(expected["y"], actual["y"], places=places)
        self.assertAlmostEqual(expected["z"], actual["z"], places=places)


# **************************************************************************************


@contextmanager
def host_timezone(name: str) -> Iterator[None]:
    """
    Temporarily set the host (process) timezone, restoring the original afterwards.
    """
    previous = os.environ.get("TZ")

    os.environ["TZ"] = name
    time.tzset()

    try:
        yield
    finally:
        if previous is None:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = previous
        time.tzset()


# **************************************************************************************
