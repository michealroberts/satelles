# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from celerity.common import GeographicCoordinate

from satelles import convert_ecef_to_enu, convert_enu_to_horizontal, convert_lla_to_ecef

# **************************************************************************************

# A location on the Earth's surface, defined by geographic coordinates (e.g., in Slough, UK):
observer = GeographicCoordinate(
    latitude=51.51084959252545,
    longitude=-0.5930215986816242,
    elevation=0.0,
)

# **************************************************************************************

# An aircraft's location, defined by geographic coordinates (e.g., just taking off from Heathrow Airport):
aircraft = GeographicCoordinate(
    latitude=51.46570730163472,
    longitude=-0.5195854299267121,
    elevation=100.0,
)

# **************************************************************************************


def main() -> None:
    # Convert the aircraft's geographic coordinates to ECEF (Earth-Centered, Earth-Fixed):
    ecef = convert_lla_to_ecef(aircraft)

    # Convert the ECEF coordinates to ENU (East-North-Up) coordinates relative to the observer:
    enu = convert_ecef_to_enu(ecef=ecef, observer=observer)

    # Convert the ENU coordinates of the aircraft to horizontal coordinates:
    horizontal = convert_enu_to_horizontal(enu=enu)

    print(f"Aircraft Horizontal Coordinates: {horizontal}")


# **************************************************************************************

if __name__ == "__main__":
    main()

# **************************************************************************************
