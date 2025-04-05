# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, field_validator

# **************************************************************************************


class Covariance(BaseModel):
    reference_frame: Annotated[
        Optional[str],
        Field(
            description="Reference frame used for covariance propagation",
            default=None,
        ),
    ]

    # Position covariance block (3x3):
    cx_x: Annotated[
        float,
        Field(description="Covariance element CX_X"),
    ]

    cy_x: Annotated[
        float,
        Field(description="Covariance element CY_X"),
    ]

    cy_y: Annotated[
        float,
        Field(description="Covariance element CY_Y"),
    ]

    cz_x: Annotated[
        float,
        Field(description="Covariance element CZ_X"),
    ]

    cz_y: Annotated[
        float,
        Field(description="Covariance element CZ_Y"),
    ]

    cz_z: Annotated[
        float,
        Field(description="Covariance element CZ_Z"),
    ]

    # Cross-covariance block (position-velocity, 3x3):
    cx_dot_x: Annotated[
        float,
        Field(description="Covariance derivative element CX_DOT_X"),
    ]

    cx_dot_y: Annotated[
        float,
        Field(description="Covariance derivative element CX_DOT_Y"),
    ]

    cx_dot_z: Annotated[
        float,
        Field(description="Covariance derivative element CX_DOT_Z"),
    ]

    cy_dot_x: Annotated[
        float,
        Field(description="Covariance derivative element CY_DOT_X"),
    ]

    cy_dot_y: Annotated[
        float,
        Field(description="Covariance derivative element CY_DOT_Y"),
    ]

    cy_dot_z: Annotated[
        float,
        Field(description="Covariance derivative element CY_DOT_Z"),
    ]

    cz_dot_x: Annotated[
        float,
        Field(description="Covariance derivative element CZ_DOT_X"),
    ]

    cz_dot_y: Annotated[
        float,
        Field(description="Covariance derivative element CZ_DOT_Y"),
    ]

    cz_dot_z: Annotated[
        float,
        Field(description="Covariance derivative element CZ_DOT_Z"),
    ]

    # Velocity covariance block (3x3) using second derivatives:
    cx_dot_x_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CX_DOT_X_DOT"),
    ]

    cy_dot_x_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CY_DOT_X_DOT"),
    ]

    cy_dot_y_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CY_DOT_Y_DOT"),
    ]

    cz_dot_x_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CZ_DOT_X_DOT"),
    ]

    cz_dot_y_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CZ_DOT_Y_DOT"),
    ]

    cz_dot_z_dot: Annotated[
        float,
        Field(description="Second derivative covariance element CZ_DOT_Z_DOT"),
    ]

    @field_validator("reference_frame")
    def validate_reference_frame(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        mapping = {
            "KVN": "KVN",
            "TEME": "True Equator, Mean Equinox",
            "ICRF": "International Celestial Reference Frame",
            "EME2000": "Epoch Mean Equinox 2000",
        }

        if value is not None and value.upper() not in mapping.keys():
            raise ValueError(f"Reference frame must be one of {list(mapping.keys())}")

        return mapping.get(value.upper()) if value else None

    def to_matrix(self) -> List[List[float]]:
        """
        Construct a full 6x6 symmetric covariance matrix from the OMM fields.

        The state vector order is assumed to be: [x, y, z, vx, vy, vz].
        """
        # Build the 6x6 matrix row by row and column by column:
        return [
            [
                self.cx_x,
                self.cy_x,
                self.cz_x,
                self.cx_dot_x,
                self.cx_dot_y,
                self.cx_dot_z,
            ],
            [
                self.cy_x,
                self.cy_y,
                self.cz_y,
                self.cy_dot_x,
                self.cy_dot_y,
                self.cy_dot_z,
            ],
            [
                self.cz_x,
                self.cz_y,
                self.cz_z,
                self.cz_dot_x,
                self.cz_dot_y,
                self.cz_dot_z,
            ],
            [
                self.cx_dot_x,
                self.cy_dot_x,
                self.cz_dot_x,
                self.cx_dot_x_dot,
                self.cy_dot_x_dot,
                self.cz_dot_x_dot,
            ],
            [
                self.cx_dot_y,
                self.cy_dot_y,
                self.cz_dot_y,
                self.cy_dot_x_dot,
                self.cy_dot_y_dot,
                self.cz_dot_y_dot,
            ],
            [
                self.cx_dot_z,
                self.cy_dot_z,
                self.cz_dot_z,
                self.cz_dot_x_dot,
                self.cz_dot_y_dot,
                self.cz_dot_z_dot,
            ],
        ]


# **************************************************************************************
