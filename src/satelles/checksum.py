# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************


def perform_checksum_compute(tle_line_string: str) -> str:
    """
    Compute the TLE checksum for a given TLE line string and return it as a formatted string.

    According to TLE formatting:
      - Every digit in the string is added to a running total.
      - For every '-' character encountered, 1 is added.
      - All other characters are ignored.
      - Finally, the total is taken modulo 10.

    Args:
        tle_line_string: A string representing one line of a TLE record.

    Returns:
        A single-digit checksum as a string.
    """
    total = 0

    for char in tle_line_string:
        if char.isdigit():
            total += int(char)
        elif char == "-":
            total += 1

    checksum = total % 10

    return f"{checksum}"


# **************************************************************************************
