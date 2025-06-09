# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re

# **************************************************************************************

e10_regex = re.compile(
    # Record type: "10" ephemeris data record for position:
    r"^10\s+"
    # Direction flag (0 = geocentric, 1 = transmit, 2 = receive):
    r"(?P<direction>[0-2])\s+"
    # Modified Julian Date (integer, 1–5 digits):
    r"(?P<mjd>\d{1,5})\s+"
    # Seconds of day (floating point with exactly 6 decimals):
    r"(?P<seconds>\d+\.\d{1,6})\s+"
    # Leap second flag (0 = no leap second, or the value of the leap second):
    r"(?P<leap_second>\d{1,2})\s+"
    # X coordinate (meters; optional sign, digits before decimal, dot, 3 decimals):
    r"(?P<x>[+-]?\d+\.\d{3})\s+"
    # Y coordinate (meters; optional sign, digits before decimal, dot, 3 decimals):
    r"(?P<y>[+-]?\d+\.\d{3})\s+"
    # Z coordinate (meters; optional sign, digits before decimal, dot, 3 decimals):
    r"(?P<z>[+-]?\d+\.\d{3})"
    r"$"
)

# **************************************************************************************

e20_regex = re.compile(
    # Record type: "20" ephemeris data record for velocity:
    r"^20\s+"
    # Direction flag (0 = geocentric, 1 = transmit, 2 = receive):
    r"(?P<direction>[0-2])\s+"
    # Geocentric X velocity (m/s; optional sign, digits before decimal, dot, 6 decimals):
    r"(?P<vx>[+-]?\d+\.\d{6})\s+"
    # Geocentric Y velocity (m/s; optional sign, digits before decimal, dot, 6 decimals):
    r"(?P<vy>[+-]?\d+\.\d{6})\s+"
    # Geocentric Z velocity (m/s; optional sign, digits before decimal, dot, 6 decimals):
    r"(?P<vz>[+-]?\d+\.\d{6})$"
)

# **************************************************************************************

e30_regex = re.compile(
    # Record type: "30" ephemeris data record for stellar aberration and relativistic
    # range corrections:
    r"^30\s+"
    # Direction flag (0 = common epoch, 1 = transmit, 2 = receive):
    r"(?P<direction>[0-2])\s+"
    # X stellar aberration correction (m; optional sign, digits before decimal,
    # dot, zero or more decimals):
    r"(?P<x_aberration>[+-]?\d+\.\d*)\s+"
    # Y stellar aberration correction (m; optional sign, digits before decimal,
    # dot, zero or more decimals):
    r"(?P<y_aberration>[+-]?\d+\.\d*)\s+"
    # Z stellar aberration correction (m; optional sign, digits before decimal,
    # dot, zero or more decimals):
    r"(?P<z_aberration>[+-]?\d+\.\d*)\s+"
    # Relativistic range correction (nsec; digits before decimal, dot, 1 decimal):
    r"(?P<relativistic_range_correction_in_nanoseconds>\d+\.\d{1})$"
)

# **************************************************************************************
