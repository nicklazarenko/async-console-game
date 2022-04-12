import asyncio
import curses
import itertools
import random
import statistics
import time

from game import helpers


async def blink(canvas: curses.window, row: int, column: int, symbol: str):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(20, 80)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


async def fire(
    canvas: curses.window,
    start_row: int,
    start_column: int,
    rows_speed: float = -0.3,
    columns_speed: float = 0,
):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed


async def animate_spaceship(
    canvas: curses.window,
    row: int,
    column: int,
    frames: dict[str, str],
    timeout: int = 1,
    move_step: int = 1,
):
    for frame in itertools.cycle([frames["rocket_frame_1"], frames["rocket_frame_2"]]):
        helpers.draw_frame(canvas, row, column, frame)
        canvas.refresh()
        for _ in range(timeout):
            await asyncio.sleep(0)

        helpers.draw_frame(canvas, row, column, frame, negative=True)

        rows_direction, columns_direction, space_pressed = helpers.read_controls(canvas)
        screen_rows, screen_columns = canvas.getmaxyx()
        frame_rows, frame_columns = helpers.get_frame_size(frame)
        row = statistics.median(
            [1, row + rows_direction * move_step, screen_rows - frame_rows - 1]
        )
        column = statistics.median(
            [
                1,
                column + columns_direction * move_step,
                screen_columns - frame_columns - 1,
            ]
        )
