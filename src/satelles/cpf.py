# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re

# **************************************************************************************

h1_regex = re.compile(
    # Record type: "H1"
    r"^H1\s+"
    # Literal "CPF" indicating a Consolidated Prediction Format record:
    r"CPF\s+"
    # 1‐digit version number (e.g., 2):
    r"(?P<version>\d)\s+"
    # 3‐char ephemeris source (e.g., HON, UTX, SGF, OPA, ESA, DGF):
    r"(?P<ephemeris_source>[A-Za-z0-9]{3})\s+"
    # 4‐digit year (e.g., 2025):
    r"(?P<year>\d{4})\s+"
    # 1‐ or 2‐digit month (1–12):
    r"(?P<month>\d{1,2})\s+"
    # 1‐ or 2‐digit day (1–31):
    r"(?P<day>\d{1,2})\s+"
    # 1‐ or 2‐digit hour (0–23):
    r"(?P<hour>\d{1,2})\s+"
    # 1–3‐digit epi. sequence number (000–366):
    r"(?P<ephemeris_sequence_number>\d{1,3})\s+"
    # 1‐ or 2‐digit sub‐daily sequence number (00–99):
    r"(?P<sub_daily_sequence_number>\d{1,2})\s+"
    # Up to 10‐char target name (no spaces):
    r"(?P<target_name>\S{1,10})"
    # Optional notes field (up to 10 chars, no spaces):
    r"(?:\s+(?P<notes>\S{1,10}))?"
    r"$"
)

# **************************************************************************************

h2_regex = re.compile(
    # Record type: "H2"
    r"^H2\s+"
    # 8-digit COSPAR ID (compressed; e.g., "7603901" → "07603901"):
    r"(?P<cospar_id>\d{1,8})\s+"
    # 4-digit SIC (Satellite ID Code; e.g., "1234"):
    r"(?P<sic>\d{1,4})\s+"
    # 8-digit NORAD ID (e.g., "0000510" → "00000510"):
    r"(?P<norad_id>\d{1,8})\s+"
    # 4-digit start year (e.g., "2025"):
    r"(?P<start_year>\d{4})\s+"
    # 2-digit start month (01–12):
    r"(?P<start_month>\d{1,2})\s+"
    # 2-digit start day (01–31):
    r"(?P<start_day>\d{1,2})\s+"
    # 2-digit start hour (00–23):
    r"(?P<start_hour>\d{1,2})\s+"
    # 2-digit start minute (00–59):
    r"(?P<start_minute>\d{1,2})\s+"
    # 2-digit start second (00–59):
    r"(?P<start_second>\d{1,2})\s+"
    # 4-digit end year (e.g., "2025"):
    r"(?P<end_year>\d{4})\s+"
    # 2-digit end month (01–12):
    r"(?P<end_month>\d{1,2})\s+"
    # 2-digit end day (01–31):
    r"(?P<end_day>\d{1,2})\s+"
    # 2-digit end hour (00–23):
    r"(?P<end_hour>\d{1,2})\s+"
    # 2-digit end minute (00–59):
    r"(?P<end_minute>\d{1,2})\s+"
    # 2-digit end second (00–59):
    r"(?P<end_second>\d{1,2})\s+"
    # 5-digit time‐between‐entries in seconds (00000–99999):
    r"(?P<interval>\d{1,5})\s+"
    # 1-digit compatibility with TIVs (0 or 1):
    r"(?P<tiv_compat>\d)\s+"
    # 1-digit target class (1–5):
    r"(?P<target_class>\d)\s+"
    # 2-digit reference frame (00–02):
    r"(?P<reference_frame>\d{1,2})\s+"
    # 1-digit rotational angle type (0–2):
    r"(?P<rot_angle_type>\d)\s+"
    # 1-digit center-of-mass correction flag (0 or 1):
    r"(?P<com_correction>\d)\s+"
    # 2-digit target location/dynamics code (01–10):
    r"(?P<location_dynamics>\d{1,2})"
    r"$"
)

# **************************************************************************************

e10_regex = re.compile(
    # Record type: "10" ephemeris data record for position:
    r"^10\s+"
    # Direction flag (0 = geocentric, 1 = fire, 2 = return):
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
