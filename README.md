![pypi](https://img.shields.io/pypi/v/satelles.svg)
![versions](https://img.shields.io/pypi/pyversions/satelles.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![satelles/test](https://github.com/michealroberts/satelles/actions/workflows/test.yml/badge.svg)](https://github.com/michealroberts/satelles/actions/workflows/test.yml)

# Satelles

Modern, type-safe, zero-dependency python library for TLE, OMM et al. handling and orbit propagation to accurately locate your satellites in the sky.

## Installation

We recommend using [uv](https://uv.astral.sh) to manage your Python environments. 

To install `satelles` into your uv environment, run:

```bash
uv add satelles
```

_Alternatively_, you can install `satelles` using your preferred environment or package manager of choice, e.g., `poetry`, `conda`, or `pip`:

```bash
pip install satelles
```

```bash
poetry add satelles
```

```bash
conda install satelles
```

## Usage

```python
from datetime import datetime, timezone

from satelles import TLE

issTLE: str = """        
  1 25544U 98067A   20062.59097222  .00016717  00000-0  10270-3 0  9006
  2 25544  51.6442 147.1064 0004607  95.6506 329.8285 15.49249062  2423
"""

satellite = TLE(tle_string=issTLE).as_satellite()

satellite.at(when=datetime(2021, 5, 15, 0, 0, 0, tzinfo=timezone.utc))

# Get the Earth Centric Inertial (ECI) coordinate of the satellite at the given time:
eci = satellite.eci_coordinate

# Get the Equatorial Coordinate of the satellite at the given time:
equatorial = satellite.equatorial_coordinate
...
```

As the API is fully typed, you can use your IDE's autocompletion to see all the available methods and properties.

We have also provided further usage examples in the [examples](./examples) directory.

## Milestones

- [X] Type-safe modern 3.6+ Python
- [X] Fully unit tested
- [X] Simpler API using Pydantic base models for validation
- [X] Zero-external dependencies (pure Python 3.6+ with no external C/C++ dependencies)
- [ ] Example API usage
- [X] Fully supported Two-Line Element (TLE) parsing and operations
- [ ] Fully supported Orbital Mean Elements Message (OMM) parsing and operations
- [ ] Fully supported TLE to OMM conversion
- [ ] Fully supported laser ranging formats (e.g., CPF and CRD).
- [X] Fully supported Earth Centred-Earth Fixed (ECEF) to East-North-Up (ENU) conversion
- [X] Fully supported Earth Centric Inertial (ECI) to Equatorial Coordinate System (ECS) conversion
- [X] Fully supported Earth Centric Inertial (ECI) to Topocentric Coordinate System (TCS) conversion
- [ ] Fully supported SPG4-XP propagation from TLE or OMM
- [X] Fully supported symplectic Verlet numerical propagation
- [X] Fully supported Runge-Kutta 4th order numerical propagation
- [X] Modified Julian Date utilities

---

### License

This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.