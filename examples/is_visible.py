# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone

from celerity.common import GeographicCoordinate

from satelles import TLE, is_visible

# **************************************************************************************

# Set some observer to be in San Francisco, CA, USA:
observer = GeographicCoordinate(
    latitude=37.7749,
    longitude=-122.4194,
    elevation=0.0,
)

# **************************************************************************************

if __name__ == "__main__":
    # Define a TLE string for the ISS (International Space Station) as an example:
    tle_string = """
    0 ISS (ZARYA)
    1 25544U 98067A   23274.64916667  .00001234  00000-0  41828-5 0  9993
    2 25544  51.6456  16.5711 0002280  15.8555 344.1575 15.50105970368857
    """

    # Create a TLE object from the string, and get the satellite object:
    satellite = TLE(tle_string=tle_string).as_satellite()

    # Get the current time in UTC:
    when = datetime.now(timezone.utc)

    # Check if the satellite is visible from the observer's location:
    visible = is_visible(
        when=when,
        satellite=satellite,
        observer=observer,
        horizon=6.0,
    )

    print(f"Is ISS (ZARYA) Visible?: {visible}")

# **************************************************************************************
