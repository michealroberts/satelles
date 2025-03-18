# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re

# **************************************************************************************

line1_regex = re.compile(
    r"^1\s+"
    r"(?P<id>[0-9A-Z]{5})"
    r"(?P<classification>[A-Z])\s+"
    r"(?P<designator>\d{2}\d{3}[A-Z]{1,3})\s+"
    r"(?P<year>\d{2})(?P<day>\d{3}\.\d{8})\s+"
    r"(?P<first_derivative_of_mean_motion>[+-]?\.\d{8})\s+"
    r"(?P<second_derivative_of_mean_motion>[+-]?\d{5}[+-]\d)\s+"
    r"(?P<drag>[+-]?\d{5}[+-]\d)\s+"
    r"(?P<ephemeris>\d)\s+"
    r"(?P<set>\d+)$"
)

# **************************************************************************************

line2_regex = re.compile(
    r"^2\s+"
    r"(?P<id>[0-9A-Z]{5})\s+"
    r"(?P<inclination>\d+\.\d+)\s+"
    r"(?P<raan>\d+\.\d+)\s+"
    r"(?P<eccentricity>\d{7})\s+"
    r"(?P<argument_of_perigee>\d+\.\d+)\s+"
    r"(?P<mean_anomaly>\d+\.\d+)\s+"
    r"(?P<mean_motion>\d+\.\d+)\s+"
    r"(?P<number_of_revolutions>\d+)$"
)

# **************************************************************************************
