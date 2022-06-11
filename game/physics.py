import math
import statistics


def _limit(value, min_value, max_value):
    """Limit value by min_value and max_value."""
    return statistics.median([min_value, value, max_value])


def _apply_acceleration(
    speed: float, speed_limit: float, forward: bool = True
) -> float:
    """Change speed — accelerate or brake — according to force direction."""

    speed_limit = abs(speed_limit)

    speed_fraction = speed / speed_limit

    # If the ship is stationary, start sharply.
    # If the ship is already flying fast, add speed slowly.
    delta = math.cos(speed_fraction) * 0.75

    result_speed = speed + delta if forward else speed - delta
    result_speed = _limit(result_speed, -speed_limit, speed_limit)

    # If the speed is close to zero, stop completely.
    if abs(result_speed) < 0.1:
        result_speed = 0

    return result_speed


def update_speed(
    row_speed: float,
    column_speed: float,
    rows_direction: int,
    columns_direction: int,
    row_speed_limit: int = 2,
    column_speed_limit: int = 2,
    fading: float = 0.8,
) -> tuple[float, float]:
    """Update speed smootly to make control handy for player. Return new speed value (row_speed, column_speed)

    rows_direction — is a force direction by rows axis. Possible values:
       -1 — if force pulls up
       0  — if force has no effect
       1  — if force pulls down
    columns_direction — is a force direction by colums axis. Possible values:
       -1 — if force pulls left
       0  — if force has no effect
       1  — if force pulls right
    """

    if rows_direction not in (-1, 0, 1):
        raise ValueError(
            f"Wrong rows_direction value {rows_direction}. Expects -1, 0 or 1."
        )

    if columns_direction not in (-1, 0, 1):
        raise ValueError(
            f"Wrong columns_direction value {columns_direction}. Expects -1, 0 or 1."
        )

    if fading < 0 or fading > 1:
        raise ValueError(f"Wrong fading value {fading}. Expects float between 0 and 1.")

    row_speed *= fading
    column_speed *= fading

    row_speed_limit, column_speed_limit = abs(row_speed_limit), abs(column_speed_limit)

    if rows_direction != 0:
        row_speed = _apply_acceleration(row_speed, row_speed_limit, rows_direction > 0)

    if columns_direction != 0:
        column_speed = _apply_acceleration(
            column_speed, column_speed_limit, columns_direction > 0
        )

    return row_speed, column_speed
