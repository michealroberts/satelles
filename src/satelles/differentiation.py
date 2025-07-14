# **************************************************************************************

# @package        satelles
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from math import factorial
from typing import List

# **************************************************************************************


def compute_finite_difference_weights(
    xs: List[float], x0: float, order: int
) -> List[float]:
    """
    Compute finite-difference weights for approximating the derivative at x0.

    Args:
        xs: List of x values for the stencil.
        x0: The point at which to compute the derivative.
        order: The order of the derivative to compute (0 for function value, 1 for
               first derivative, etc.).

    Raises:
        ValueError: If the order is negative or exceeds the number of stencil points.
        ZeroDivisionError: If the stencil is degenerate (e.g., all xs are the same).

    Returns:
        A list of weights corresponding to the stencil points for the specified derivative
        order. The length of the list will match the number of stencil points.
    """
    n = len(xs)

    # Validate that order is non-negative and less than the number of stencil points:
    if order < 0 or order >= n:
        raise ValueError(
            f"Invalid order {order}: must be non-negative and less than the number of stencil points ({n})."
        )

    # Build matrix of Taylor terms: row k has (xs[j] - x0)**k / k!:
    matrix: List[List[float]] = [
        [(xs[j] - x0) ** k / factorial(k) for j in range(n)] for k in range(n)
    ]

    # Build vector so only the desired derivative order is targeted:
    vector: List[float] = [1.0 if k == order else 0.0 for k in range(n)]

    # Forward elimination to make matrix upper-triangular and apply same operations
    # to vector:
    for i in range(n):
        pivot = matrix[i][i]

        if abs(pivot) < 1e-14:
            raise ZeroDivisionError(f"Degenerate stencil: zero pivot at row {i}")

        # Normalize row so pivot becomes 1 (keeps equation balanced):
        inverse_pivot = 1.0 / pivot

        for j in range(i, n):
            matrix[i][j] *= inverse_pivot

        vector[i] *= inverse_pivot

        # Eliminate entries below pivot to zero out this column:
        for r in range(i + 1, n):
            factor = matrix[r][i]
            for j in range(i, n):
                matrix[r][j] -= factor * matrix[i][j]
            vector[r] -= factor * vector[i]

    # Back substitution solve for weights from the upper-triangular system:
    weights: List[float] = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = vector[i]
        for j in range(i + 1, n):
            total -= matrix[i][j] * weights[j]
        weights[i] = total

    return weights


# **************************************************************************************
