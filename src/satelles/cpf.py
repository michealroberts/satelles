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
