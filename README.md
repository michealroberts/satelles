[![satelles](docs/assets/banner.png)](https://github.com/michealroberts/satelles)

[![pypi](https://img.shields.io/pypi/v/satelles.svg)](https://pypi.org/project/satelles/)
[![versions](https://img.shields.io/pypi/pyversions/satelles.svg)](https://pypi.org/project/satelles/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![satelles/test](https://github.com/michealroberts/satelles/actions/workflows/test.yml/badge.svg)](https://github.com/michealroberts/satelles/actions/workflows/test.yml)

satelles is a small, fully typed Python library for satellite orbit work: parse Two-Line Element sets (TLEs), place a satellite in space at a given time, move positions between Earth-centred inertial and Earth-fixed frames, work out where the satellite sits in an observer's sky (altitude, azimuth and range), and check whether it is in sunlight. It is plain Python on top of [pydantic](https://docs.pydantic.dev) (validated models) and [celerity](https://github.com/michealroberts/celerity) (astronomical time, sidereal time and nutation), and every step is a small, readable function you can call on its own.

> [!IMPORTANT]
> `Satellite` propagates TLE mean elements with two-body Kepler motion, not SGP4. Positions are good to a few tens of kilometres within hours of the TLE epoch and drift by hundreds of kilometres after a day. See [Accuracy & Limitations](#accuracy--limitations).

## Installation

satelles requires Python 3.11 or newer. With [uv](https://docs.astral.sh/uv/):

```bash
uv add satelles
```

or with pip:

```bash
pip install satelles
```

Its runtime dependencies are `celerity` and `pydantic`. Conversions that involve Earth rotation fetch UT1−UTC (DUT1) from the IERS web service, so they need network access.

## Quickstart

Where is the ISS, and how high is it in the sky above Cape Town, about an hour after its TLE epoch?

```python
from datetime import datetime, timezone

from celerity.common import GeographicCoordinate

from satelles import TLE, convert_eci_to_topocentric, is_visible

# A three-line element set for the ISS (epoch 2008-09-20 12:25:40 UTC):
tle = TLE(
    tle_string="""
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""
)

satellite = tle.as_satellite()

# Cape Town (latitude and longitude in degrees, elevation in metres):
observer = GeographicCoordinate(latitude=-33.9249, longitude=18.4241, elevation=25.0)

when = datetime(2008, 9, 20, 13, 22, 0, tzinfo=timezone.utc)

# Set the time to propagate to:
satellite.at(when)

# Geocentric position in metres, in the library's (true-of-date) ECI frame:
eci = satellite.eci_coordinate
print(f"ECI: x={eci['x']:.0f} m, y={eci['y']:.0f} m, z={eci['z']:.0f} m")

# Geocentric right ascension and declination, in degrees:
equatorial = satellite.equatorial_coordinate
print(f"RA {equatorial['ra']:.3f}°, Dec {equatorial['dec']:.3f}°")

# Altitude and azimuth (degrees) and range (metres) for the observer:
topocentric = convert_eci_to_topocentric(eci=eci, when=when, observer=observer)
print(
    f"alt {topocentric['altitude']:.2f}°, az {topocentric['azimuth']:.2f}°, "
    f"range {topocentric['range'] / 1000:.1f} km"
)

# Is it more than 10° above the horizon?
print(is_visible(when=when, satellite=satellite, observer=observer, horizon=10.0))
```

```text
ECI: x=-4521639 m, y=-3453348 m, z=-3604910 m
RA 217.370°, Dec -32.358°
alt 59.53°, az 320.47°, range 417.8 km
True
```

TLEs go stale quickly, so fetch a current one (e.g., from [CelesTrak](https://celestrak.org)) for the day you care about. More scripts live in [`examples/`](./examples).

## Core Concepts

### From a TLE to a `Satellite`

`TLE(tle_string)` parses a two-line set, or a three-line set whose first line is the name (an optional `0 ` prefix is stripped). It checks the line layout, the modulo-10 checksum on each line and that both lines carry the same catalog number, and accepts Alpha-5 catalog numbers (`A0000` is 100000). Any failure raises `ValueError`. Two-digit epoch years below 57 are 20xx, the rest 19xx.

```python
from satelles import TLE

tle = TLE(
    tle_string="""
0 ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""
)

print(tle)
print(tle.name, tle.id, tle.designator, tle.classification)
print(tle.year, tle.day, tle.julian_date)
print(tle.inclination, tle.eccentricity, tle.mean_motion)

# A two-line set parses the same way, with an empty name:
lines = """
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""

print(repr(TLE(tle_string=lines).name))

# A corrupted line fails its checksum:
try:
    TLE(tle_string=lines.replace("0  2927", "0  2928"))
except ValueError as error:
    print(error)
```

```text
<TLE(name='ISS (ZARYA)', id=25544)>
ISS (ZARYA) 25544 98067A Unclassified
2008 264.51782528 2454730.01782528
51.6416 0.0006703 15.72125391
''
Invalid TLE string: Invalid line 1 checksum: expected 7, got 8
```

`tle.as_satellite()` returns the parsed `Satellite`, a pydantic model holding the mean elements: angles in degrees, mean motion in revolutions per day, and the epoch as `year`, `day` and Julian date `jd`. Its `reference_frame` is TEME, the frame TLEs are defined in.

`satellite.at(when)` stores the time on the satellite (it returns `None`); the position properties are then computed on demand:

```python
from datetime import datetime

from satelles import TLE

satellite = TLE(
    tle_string="""
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""
).as_satellite()

# A naive datetime is treated as UTC:
satellite.at(datetime(2008, 9, 20, 13, 22, 0))

print(satellite.get_semi_major_axis())  # metres
print(satellite.perifocal_coordinate)  # metres, in the orbital plane
print(satellite.eci_coordinate)  # metres, true-of-date ECI
print(satellite.equatorial_coordinate)  # degrees
```

```text
6730960.491320576
{'x': -6693191.929095141, 'y': -753250.6316176057, 'z': 0.0}
{'x': -4521638.854624164, 'y': -3453347.579045531, 'z': -3604910.1625963035}
{'ra': 217.3703488844906, 'dec': -32.35848880911684}
```

From a TLE to an observer's sky, step by step:

1. The mean anomaly is advanced from the epoch, `M = M₀ + n·Δt`, and Kepler's equation is solved for the eccentric and true anomalies, giving the position in the orbital (perifocal) plane.
2. That position is rotated by the argument of perigee, inclination and RAAN into TEME (`convert_perifocal_to_eci`).
3. `eci_coordinate` rotates TEME into the library's ECI frame (true equator and equinox of date) by the equation of the equinoxes.
4. `convert_eci_to_topocentric` rotates ECI into ECEF by Greenwich apparent sidereal time, then into the observer's East-North-Up frame, and reads off altitude, azimuth and range.

### Time

Functions that need a time take a `datetime`. Naive datetimes are treated as UTC and aware ones are converted to UTC. TLE epochs are UTC, and Earth rotation is evaluated in UT1 using DUT1 from IERS. There are Modified Julian Date helpers too:

```python
from datetime import datetime

from satelles import convert_mjd_to_datetime, get_modified_julian_date_as_parts

# (integer MJD, seconds since UTC midnight):
print(get_modified_julian_date_as_parts(datetime(2008, 9, 20, 13, 22, 0)))

print(convert_mjd_to_datetime(54729.5))
```

```text
(54729, 48120.0)
2008-09-20 12:00:00+00:00
```

### Coordinate Frames & Transforms

ECI in satelles means **true-of-date**: the true equator and equinox of date. `Satellite.eci_coordinate`, `convert_eci_to_equatorial`, `convert_eci_to_ecef`, `convert_eci_to_topocentric` and `is_visible` all use this frame. It is not GCRF or J2000; use `EME2000` for mean J2000 positions.

There are two ways to move between frames:

- **Conversion functions** in `satelles.coordinates`, such as `convert_eci_to_ecef(eci, when, *, polar_motion=...)` and `convert_ecef_to_eci(...)`. They take and return `CartesianCoordinate` dicts in metres. Polar motion is optional and given in **degrees** (IERS publishes it in arcseconds, so divide by 3600).
- **Frame objects** (`ECEF`, `ECI`, `TEME`, `EME2000` and `ITRF`) linked into a tree. `frame.transform_to(when, other)` returns a `Transform` (a quaternion rotation plus a translation) with `apply_to_position`, `inverse` and `compose`.

ECEF is the root of the tree. ECI and ITRF are its children, and TEME and EME2000 are children of ECI. Each frame has a parent and a `transform_to_parent(when)` provider, and `transform_to` walks up from both frames to their common ancestor, so `TEME.transform_to(when, ECEF)` composes TEME → ECI → ECEF:

```python
from datetime import datetime, timezone

from satelles import ECEF, TEME

when = datetime(2008, 9, 20, 13, 22, 0, tzinfo=timezone.utc)

# The TEME → ECEF transform, composed through the tree (TEME → ECI → ECEF):
transform = TEME.transform_to(when, ECEF)

# A TEME position, e.g., from your own propagator (metres):
teme = {"x": 4_000_000.0, "y": -3_000_000.0, "z": 4_500_000.0}

print(transform.apply_to_position(teme))

# The inverse transform takes you back again:
print(transform.inverse().apply_to_position(transform.apply_to_position(teme)))
```

```text
{'x': -2710631.5137798693, 'y': 4201485.070365413, 'z': 4500000.000000001}
{'x': 4000000.0000000014, 'y': -3000000.0000000005, 'z': 4500000.000000002}
```

The frame tree does not apply polar motion (ITRF and ECEF are the same frame in it); only the conversion functions accept it.

### Observer Geometry

An observer is a celerity `GeographicCoordinate`: geodetic latitude and longitude in degrees (east positive) and elevation in metres above the WGS-84 ellipsoid. Always pass `elevation`; satelles needs it. `convert_eci_to_topocentric` returns a `TopocentricCoordinate` with `altitude` and `azimuth` in degrees, `range` in metres and `time_of_flight`, the two-way light time in seconds.

In the observer's East-North-Up frame (x = east, y = north, z = up), azimuth is measured clockwise from true north in the horizon plane, altitude is the angle above the horizon, and range is the straight-line distance to the satellite. You can also run the steps yourself:

```python
from datetime import datetime, timezone

from celerity.common import GeographicCoordinate

from satelles import (
    TLE,
    convert_ecef_to_enu,
    convert_ecef_to_lla,
    convert_eci_to_ecef,
    convert_enu_to_horizontal,
)

satellite = TLE(
    tle_string="""
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""
).as_satellite()

observer = GeographicCoordinate(latitude=-33.9249, longitude=18.4241, elevation=25.0)

when = datetime(2008, 9, 20, 13, 22, 0, tzinfo=timezone.utc)

satellite.at(when)

# ECI → ECEF, rotating by Greenwich apparent sidereal time (with DUT1):
ecef = convert_eci_to_ecef(eci=satellite.eci_coordinate, when=when)

# The sub-satellite point: geodetic latitude, longitude and height (metres):
print(convert_ecef_to_lla(ecef=ecef))

# ECEF → East-North-Up (metres) relative to the observer:
enu = convert_ecef_to_enu(ecef=ecef, observer=observer)

# ENU → altitude and azimuth (degrees, azimuth clockwise from true north):
print(convert_enu_to_horizontal(enu=enu))
```

```text
{'latitude': -32.523302042522616, 'longitude': 17.06582986190217, 'elevation': 363453.1205373267}
{'alt': 59.525720225289625, 'az': 320.4702355531948}
```

`is_visible(when, satellite, observer, horizon=0.0)` returns `True` when the satellite's topocentric altitude is above `horizon` degrees. It propagates a copy, so your `Satellite` is left untouched. It raises `ValueError` unless `0 <= horizon < 90`, and warns when `horizon >= 30` or when `when` is a day or more from the TLE epoch. It is a geometric test: it does not check whether the satellite is sunlit (see below) or whether the observer's sky is dark.

### Sunlight & Shadow

`is_illuminated(when, satellite)` returns `True` when the satellite is in sunlight. It uses a cylindrical Earth-shadow model: the satellite is in shadow when it is on the far side of the Earth from the Sun and within one Earth equatorial radius of the Sun–Earth line.

The test is made in the true-of-date ECI frame. Satellites parsed from a TLE are TEME, so their `eci_coordinate` is already in that frame; EME2000 and ICRF satellites are rotated into it. Any other `reference_frame`, including an unspecified one, raises `ValueError`. Like `is_visible`, it propagates a copy of the satellite and treats naive datetimes as UTC. It does not use DUT1, so it needs no network access.

```python
from datetime import datetime, timedelta, timezone

from satelles import TLE, is_illuminated

satellite = TLE(
    tle_string="""
ISS (ZARYA)
1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
"""
).as_satellite()

start = datetime(2008, 9, 20, 12, 0, 0, tzinfo=timezone.utc)

# Step through an hour, one second at a time, and print each shadow crossing:
previous = is_illuminated(when=start, satellite=satellite)

for seconds in range(1, 3600):
    when = start + timedelta(seconds=seconds)

    illuminated = is_illuminated(when=when, satellite=satellite)

    if illuminated != previous:
        print(when.time(), "leaves shadow" if illuminated else "enters shadow")

    previous = illuminated
```

```text
12:16:41 enters shadow
12:48:00 leaves shadow
```

A satellite can be seen by eye when it is above the horizon (`is_visible`), sunlit (`is_illuminated`) and the observer's sky is dark. satelles does not check the last condition.

### Numerical Propagation

`propagate_rk4` (fourth-order Runge–Kutta) and `propagate_verlet` (velocity Verlet, symplectic) integrate a Cartesian state in fixed steps under point-mass gravity, with `μ` defaulting to Earth's. Positions are in metres and velocities in metres per second. Each returns the lists of positions and velocities after every step:

```python
from math import pi, sqrt

from satelles import EARTH_MASS, GRAVITATIONAL_CONSTANT, distance, propagate_rk4

μ = GRAVITATIONAL_CONSTANT * EARTH_MASS

# A circular orbit 400 km above the equator:
r = 6_378_137.0 + 400_000.0
position = {"x": r, "y": 0.0, "z": 0.0}
velocity = {"vx": 0.0, "vy": sqrt(μ / r), "vz": 0.0}

# Propagate for exactly one orbital period, in 600 fixed steps (about 9.3 s each):
period = 2 * pi * sqrt(r**3 / μ)

positions, velocities = propagate_rk4(
    position=position,
    velocity=velocity,
    params={"timestep": period / 600, "number_of_steps": 600},
)

# Two-body motion is periodic, so we should be back where we started:
print(f"{distance(positions[-1], position):.3f} m")
```

```text
0.012 m
```

## Features

| Module                                | What It Does                                                                                                   | Key Names                                                                                                                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `tle`                                 | Parse and validate TLEs (checksums, Alpha-5)                                                                   | `TLE`                                                                                                                            |
| `satellite`                           | Mean elements plus a two-body position at a time                                                               | `Satellite`                                                                                                                      |
| `kepler`, `orbit`, `velocity`         | Kepler's equation, anomalies, semi-major axis, orbital radius, perifocal velocity                              | `get_eccentric_anomaly`, `get_true_anomaly`, `get_semi_major_axis`, `get_orbital_radius`, `get_perifocal_velocity`               |
| `coordinates`                         | Perifocal ↔ ECI, ECI ↔ ECEF, ECEF ↔ geodetic (WGS-84), ECEF → ENU → horizontal, ECI → equatorial / topocentric | `convert_eci_to_ecef`, `convert_ecef_to_lla`, `convert_eci_to_topocentric`, …                                                    |
| `frame`, `frames`, `transforms`       | Frame tree and time-dependent transforms                                                                       | `Frame`, `Transform`, `ECEF`, `ECI`, `TEME`, `EME2000`, `ITRF`, `*_transform_provider`                                           |
| `visibility`                          | Above-the-horizon test, and sunlight / Earth-shadow test                                                       | `is_visible`, `is_illuminated`                                                                                                   |
| `runge_kutta`, `symplectic`, `gravity` | Fixed-step two-body integrators                                                                                | `propagate_rk4`, `propagate_verlet`, `get_gravitational_acceleration`                                                            |
| `interpolation`                       | Barycentric Lagrange and cubic Hermite interpolation of sampled positions                                      | `BarycentricLagrange3DPositionInterpolator`, `Hermite3DPositionInterpolator`, `Hermite3DKinematicInterpolator`                   |
| `hohmann`                             | Hohmann transfers between circular orbits (Δv, time of flight, phase angle)                                    | `get_hohmann_transfer_parameters`                                                                                                |
| `covariance`                          | 6×6 position-velocity covariance from CCSDS OMM fields                                                         | `Covariance`                                                                                                                     |
| `mjd`                                 | Modified Julian Date conversions                                                                               | `get_modified_julian_date_as_parts`, `convert_mjd_to_datetime`, …                                                                |
| `light`                               | Light travel time ↔ distance                                                                                   | `convert_distance_to_light_travel_time`, `convert_light_travel_time_to_distance`                                                 |
| `vector`, `matrix`, `quaternion`      | 3-vector, 3×3 rotation matrix and quaternion maths                                                             | `rotate`, `normalise`, `get_rotation_matrix_z`, `Quaternion`, …                                                                  |
| `earth`, `constants`                  | WGS-84 and physical constants (SI units)                                                                       | `EARTH_EQUATORIAL_RADIUS`, `EARTH_FLATTENING_FACTOR`, `EARTH_MASS`, `GRAVITATIONAL_CONSTANT`, `SPEED_OF_LIGHT`                   |

Everything listed is importable from the top-level `satelles` package, and the whole API is typed, so your editor can show the rest.

## Accuracy & Limitations

- **Propagation is two-body, not SGP4.** `Satellite` treats the TLE's mean elements as Keplerian elements and advances only the mean anomaly. It ignores J2 (for the ISS the node regresses about 5° a day), drag (B\*) and the mean-motion derivatives. For the ISS TLE above, the difference from SGP4 ([python-sgp4](https://pypi.org/project/sgp4/) 2.27, compared in TEME) is:

  | Time from epoch     | 0 h    | 1 h   | 6 h   | 1 day  | 3 days  |
  | ------------------- | ------ | ----- | ----- | ------ | ------- |
  | Position difference | 7.5 km | 20 km | 40 km | 475 km | 1347 km |

  `is_visible` warns once you are a day or more from the epoch. For anything precise, propagate with SGP4 and pass the TEME position through the frame tools here.
- **ECI is true-of-date.** Nutation comes from celerity's IAU 2000B series (the model SOFA and ERFA evaluate in `nut00b`) with the IAU 2006 mean obliquity. The equation of the equinoxes, used for TEME → ECI and for apparent sidereal time, is evaluated in celerity 0.47 from a shorter nutation series plus the IAU 1994 complementary terms. In spot checks it was within about 0.15″ of ERFA's `eqeq94` (a few metres at LEO distance), which is negligible next to the propagation error.
- **DUT1 needs the network.** `convert_eci_to_ecef`, `convert_ecef_to_eci`, the ECI↔ECEF transform providers, and everything built on them (`Frame.transform_to` across ECI and ECEF, `convert_eci_to_topocentric`, `is_visible`) fetch UT1−UTC from the IERS web service, once per UTC day queried. Results are cached in memory for six hours. If the request fails, the call raises; there is no offline fallback yet.
- **Polar motion is opt-in.** It is applied only when you pass `polar_motion` to `convert_eci_to_ecef` or `convert_ecef_to_eci`; topocentric coordinates, `is_visible` and the frame tree ignore it. This is an error of about 10 m at the Earth's surface.
- **Topocentric positions are geometric.** They make no correction for atmospheric refraction, light-time or aberration.
- **The Earth's shadow is a sharp cylinder.** `is_illuminated` has no penumbra, because it treats the Sun as a point source at infinity. It models the Earth as a sphere of its equatorial radius and ignores atmospheric refraction and absorption, which in reality blur shadow entry and exit by a few seconds in low Earth orbit. The Sun's position comes from a low-precision solar theory, good to about 0.01°.
- **Interpolation time units.** `Position.at` and `Velocity.at` in `satelles.models` are documented as MJD, but the interpolators treat velocities as derivatives with respect to `at`. With velocities in m/s (as `Hermite3DKinematicInterpolator` expects), `at` must be in seconds, and derived velocities come out per unit of `at`. This is a known open issue.

## Roadmap

- [x] Two-Line Element (TLE) parsing, with checksum and Alpha-5 support
- [x] Two-body (Kepler) positions from TLE mean elements
- [x] ECI (true-of-date) ↔ ECEF with DUT1 and optional polar motion
- [x] ECEF ↔ geodetic, ENU, horizontal and topocentric coordinates
- [x] Sunlit and eclipse checks
- [x] Frame tree: ECEF, ECI, TEME, EME2000 and ITRF
- [x] Runge–Kutta (RK4) and symplectic velocity-Verlet numerical propagation
- [x] Lagrange and Hermite interpolation, Hohmann transfers, covariance, MJD utilities
- [ ] SGP4 (and SGP4-XP) propagation from TLE or OMM
- [ ] Orbit Mean-Elements Message (OMM) parsing, and TLE ↔ OMM conversion
- [ ] Laser ranging formats (CPF and CRD)

## Development

```bash
uv sync --all-extras --dev
```

```bash
uv run pytest
```

```bash
uv run ruff check
```

```bash
uv run ruff format
```

```bash
uv run mypy ./src/satelles --config mypy.ini
```

Some tests fetch DUT1 from IERS, so the test suite needs network access.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.
