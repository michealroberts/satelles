# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Tuple

from .satellite import Satellite

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


def parse_scientific_notation(value: str) -> float:
    """
    Parse a string in the form ±DDDDD±D, where the first part is the mantissa (with an
    implicit decimal) and the second part is the exponent.

    Args:
        value: The value to parse.

    Returns:
        The value as a float.
    """
    pattern = re.compile(r"^([+-]?)(\d{5})([+-]\d)$")

    match = pattern.match(value)

    if not match:
        return 0.0

    sign = -1 if match.group(1) == "-" else 1

    mantissa = int(match.group(2)) / 1e5

    exponent = int(match.group(3))

    return sign * mantissa * (10**exponent)


# **************************************************************************************


def parse_id_field(value: Any) -> Optional[int]:
    """
    Parse a string as an integer, with support for base-36 encoding.

    Args:
        value: The value to parse.

    Returns:
        The value as an integer, or None if the value is not a valid integer
    """
    if not isinstance(value, str):
        return None
    try:
        if value and value[0].isalpha():
            return int(value, 36)
        else:
            return int(value, 10)
    except ValueError:
        return None


# **************************************************************************************


def parse_classification_field(value: Any) -> Optional[str]:
    """
    Parse a classification field, which is a single character representing the
    classification of the satellite.

    Args:
        value: The value to parse.

    Returns:
        The classification of the satellite as a string, or None if the value is not
        valid, e.g., either one of "U", "C", or "S".
    """
    if not isinstance(value, str):
        return None

    v = value.strip().upper()

    if len(v) != 1:
        return None

    if v not in {"U", "C", "S"}:
        raise ValueError("Invalid classification field. Must be one of: U, C, S")

    return v


# **************************************************************************************


def parse_designator_field(value: Any) -> Optional[str]:
    """
    Parse a string as a designator field.

    Args:
        value: The value to parse.

    Returns:
        The value as a string, or None if the value is not a valid designator.
    """
    if not isinstance(value, str):
        return None
    return value.strip()


# **************************************************************************************


def parse_epoch_field(value: Any) -> Optional[Tuple[int, float, float]]:
    if not isinstance(value, str):
        return None
    try:
        # The first two digits represent the year (with a cutoff at 57):
        year = int(value[:2])
        if year < 57:
            year += 2000
        else:
            year += 1900
        day = float(value[2:])
    except ValueError:
        return None

    # Compute the date corresponding to the day of year (note: day 1 is January 1):
    dt = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=day - 1)

    # Convert Unix timestamp to Julian date:
    jd = dt.timestamp() / 86400 + 2440587.5

    return (year, day, jd)


# **************************************************************************************


def parse_bstar_drag_term_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    return parse_scientific_notation(value)


# **************************************************************************************


def parse_ephemeris_type_field(value: Any) -> Optional[int]:
    if not isinstance(value, str):
        return None
    try:
        return int(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_set_number_field(value: Any) -> Optional[int]:
    if not isinstance(value, str):
        return None
    try:
        return int(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_raan_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_inclination_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_eccentricity_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        # The eccentricity field has an implicit leading zero.
        return float("0." + value.strip())
    except ValueError:
        return None


# **************************************************************************************


def parse_argument_of_perigee_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_mean_anomaly_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************s


def parse_mean_motion_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_first_derivative_of_mean_motion_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    try:
        return float(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_second_derivative_of_mean_motion_field(value: Any) -> Optional[float]:
    if not isinstance(value, str):
        return None
    return parse_scientific_notation(value)


# **************************************************************************************


def parse_number_of_revolutions_field(value: Any) -> Optional[int]:
    if not isinstance(value, str):
        return None
    try:
        return int(value)
    except ValueError:
        return None


# **************************************************************************************


def parse_tle(tle: str) -> Optional[Satellite]:
    """
    Parse a TLE string and return a Satellite instance if successful, otherwise return None.

    The TLE string can be in one of two formats:
      - Three-line set (name, line1, line2)
      - Two-line set (line1, line2), in which case the satellite name is set to an empty string.

    Args:
        tle: The TLE string to parse.

    Returns:
        A Satellite instance if parsing is successful, otherwise None.
    """
    # Split the TLE into lines and remove any empty lines:
    lines = [line.strip() for line in tle.splitlines() if line.strip()]

    if len(lines) == 2:
        name = ""
        line1, line2 = lines
    elif len(lines) >= 3:
        name = lines[0]
        line1, line2 = lines[1], lines[2]
    else:
        return None

    # Match the TLE to the line 1 regular expression:
    m1 = line1_regex.match(line1)

    # Match the TLE to the line 2 regular expression:
    m2 = line2_regex.match(line2)

    if not m1 or not m2:
        return None

    id_field = m1.group("id")
    classification_field = m1.group("classification")
    designator_field = m1.group("designator")
    year_field = m1.group("year")
    day_field = m1.group("day")
    fdmm_field = m1.group("first_derivative_of_mean_motion")
    sdmm_field = m1.group("second_derivative_of_mean_motion")
    drag_field = m1.group("drag")
    ephemeris_field = m1.group("ephemeris")
    set_field = m1.group("set")
    inclination_field = m2.group("inclination")
    raan_field = m2.group("raan")
    eccentricity_field = m2.group("eccentricity")
    argument_of_perigee_field = m2.group("argument_of_perigee")
    mean_anomaly_field = m2.group("mean_anomaly")
    mean_motion_field = m2.group("mean_motion")
    number_of_revolutions_field = m2.group("number_of_revolutions")

    id = parse_id_field(id_field)

    if id is None:
        return None

    classification = parse_classification_field(classification_field)

    if classification is None:
        return None

    designator = parse_designator_field(designator_field)

    if designator is None:
        return None

    epoch = parse_epoch_field(f"{year_field}{day_field}")
    if epoch is None:
        return None

    year, day, jd = epoch

    fdmm = parse_first_derivative_of_mean_motion_field(fdmm_field)
    if fdmm is None:
        return None

    sdmm = parse_second_derivative_of_mean_motion_field(sdmm_field)
    if sdmm is None:
        return None

    drag = parse_bstar_drag_term_field(drag_field)
    if drag is None:
        return None

    ephemeris = parse_ephemeris_type_field(ephemeris_field)
    if ephemeris is None:
        return None

    set = parse_set_number_field(set_field)
    if set is None:
        return None

    inclination = parse_inclination_field(inclination_field)
    if inclination is None:
        return None

    raan = parse_raan_field(raan_field)
    if raan is None:
        return None

    eccentricity = parse_eccentricity_field(eccentricity_field)
    if eccentricity is None:
        return None

    argument_of_perigee = parse_argument_of_perigee_field(argument_of_perigee_field)
    if argument_of_perigee is None:
        return None

    mean_anomaly = parse_mean_anomaly_field(mean_anomaly_field)
    if mean_anomaly is None:
        return None

    mean_motion = parse_mean_motion_field(mean_motion_field)
    if mean_motion is None:
        return None

    number_of_revolutions = parse_number_of_revolutions_field(
        number_of_revolutions_field
    )
    if number_of_revolutions is None:
        return None

    # Assemble the satellite using the parsed fields and return it:
    try:
        satellite = Satellite(
            id=id,
            name=name,
            classification=classification,
            designator=designator,
            year=year,
            day=day,
            jd=jd,
            ephemeris=ephemeris,
            set=set,
            drag=drag,
            raan=raan,
            inclination=inclination,
            eccentricity=eccentricity,
            argument_of_perigee=argument_of_perigee,
            mean_anomaly=mean_anomaly,
            mean_motion=mean_motion,
            first_derivative_of_mean_motion=fdmm,
            second_derivative_of_mean_motion=sdmm,
            number_of_revolutions=number_of_revolutions,
        )
    except Exception as error:
        print(error)
        return None

    return satellite


# **************************************************************************************
