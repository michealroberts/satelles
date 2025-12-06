# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from enum import Enum

# **************************************************************************************


class Reference(Enum):
    """
    Common reference frames used in satellite and celestial orbital mechanics.
    """

    # Earth Centered Inertial:
    ECI = "ECI"

    # Earth Centered Earth Fixed:
    ECEF = "ECEF"

    # International Celestial Reference Frame:
    ICRF = "ICRF"

    # International Terrestrial Reference Frame:
    ITRF = "ITRF"

    # Earth Mean Equator 2000:
    EME2000 = "EME2000"

    # True Equator Mean Equinox:
    TEME = "TEME"

    # Topocentric (e.g., observer's local horizon):
    TOPOCENTRIC = "TOPOCENTRIC"

    @property
    def is_inertial(self) -> bool:
        """
        Whether this reference frame is inertial (non-rotating) or not.
        """
        return self in {
            Reference.ECI,
            Reference.ICRF,
            Reference.EME2000,
            Reference.TEME,
        }

    @property
    def is_rotating(self) -> bool:
        """
        Whether this reference frame is rotating with the Earth or not.
        """
        return self in {
            Reference.ECEF,
            Reference.ITRF,
            Reference.TOPOCENTRIC,
        }


# **************************************************************************************
