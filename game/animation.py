import curses
import itertools
import random
import statistics
import time

from game import engine
from game import helpers
from game import obstacles
from game import physics


async def blink(canvas: curses.window, row: int, column: int, symbol: str):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await helpers.sleep(random.randint(20, 80))

        canvas.addstr(row, column, symbol)
        await helpers.sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await helpers.sleep(5)

        canvas.addstr(row, column, symbol)
        await helpers.sleep(3)


async def fire(
    canvas: curses.window,
    start_row: int,
    start_column: int,
    rows_speed: float = -0.3,
    columns_speed: float = 0,
):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await helpers.sleep(1)

    canvas.addstr(round(row), round(column), "O")
    await helpers.sleep(1)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await helpers.sleep(1)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed

        for obstacle in engine.obstacle_list:
            if obstacle.has_collision(row, column):
                engine.obstacles_in_last_collisions.append(obstacle)
                return


async def animate_spaceship(
    canvas: curses.window,
    row: int,
    column: int,
    timeout: int = 1,
):
    order = [engine.frames["rocket_frame_1"]] * timeout + [
        engine.frames["rocket_frame_2"]
    ] * timeout
    row_speed = column_speed = 0
    for frame in itertools.cycle(order):
        helpers.draw_frame(canvas, row, column, frame)
        await helpers.sleep(1)
        helpers.draw_frame(canvas, row, column, frame, negative=True)

        rows_direction, columns_direction, space_pressed = helpers.read_controls(canvas)

        if space_pressed:
            engine.coroutines.append(fire(canvas, row, column + 2))

        row_speed, column_speed = physics.update_speed(
            row_speed, column_speed, rows_direction, columns_direction
        )
        row += row_speed
        column += column_speed

        screen_rows, screen_columns = canvas.getmaxyx()
        frame_rows, frame_columns = helpers.get_frame_size(frame)
        row = statistics.median([1, row, screen_rows - frame_rows - 1])
        column = statistics.median(
            [
                1,
                column,
                screen_columns - frame_columns - 1,
            ]
        )

        for obstacle in engine.obstacle_list:
            if obstacle.has_collision(row, column):
                engine.coroutines.append(show_gameover(canvas))
                return


async def fly_garbage(
    canvas: curses.window, column: int, garbage_frame: str, speed: float = 0.5
):
    """Animate garbage, flying from top to bottom. ??olumn position will stay the same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    obstacle = obstacles.Obstacle(row, column, *helpers.get_frame_size(garbage_frame))
    engine.obstacle_list.append(obstacle)
    try:
        while row < rows_number:
            helpers.draw_frame(canvas, row, column, garbage_frame)
            await helpers.sleep(1)
            helpers.draw_frame(canvas, row, column, garbage_frame, negative=True)
            if obstacle in engine.obstacles_in_last_collisions:
                engine.obstacles_in_last_collisions.remove(obstacle)
                rows, columns = helpers.get_frame_size(garbage_frame)
                await explode(canvas, row + rows // 2, column + columns // 2)
                return
            row += speed
            obstacle.row = row
    finally:
        engine.obstacle_list.remove(obstacle)


async def fill_orbit_with_garbage(canvas: curses.window):
    while True:
        garbage_type = random.choice(
            ["duck", "garbage_large", "garbage_small", "garbage_xl", "hubble", "lamp"]
        )
        _, frame_width = helpers.get_frame_size(engine.frames[garbage_type])

        _, columns_number = canvas.getmaxyx()
        column = random.randint(0, columns_number - frame_width - 1)

        engine.coroutines.append(
            fly_garbage(
                canvas, column=column, garbage_frame=engine.frames[garbage_type]
            )
        )

        for _ in range(random.randint(15, 30)):
            await helpers.sleep(1)


async def explode(canvas: curses.window, center_row: int, center_column: int):
    rows, columns = helpers.get_frame_size(engine.frames["explosion_1"])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    for frame in [
        engine.frames["explosion_1"],
        engine.frames["explosion_2"],
        engine.frames["explosion_3"],
        engine.frames["explosion_4"],
    ]:
        helpers.draw_frame(canvas, corner_row, corner_column, frame)
        await helpers.sleep(1)
        helpers.draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await helpers.sleep(1)


async def show_gameover(canvas: curses.window):
    rows, columns = helpers.get_frame_size(engine.frames["gameover"])
    screen_rows, screen_columns = canvas.getmaxyx()

    while True:
        helpers.draw_frame(
            canvas,
            screen_rows / 2 - rows / 2,
            screen_columns / 2 - columns / 2,
            engine.frames["gameover"],
        )
        await helpers.sleep(1)
