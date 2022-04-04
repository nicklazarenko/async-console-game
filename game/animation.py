import asyncio
import curses
import random
import time


def dim(char: str, canvas: curses.window, row: int, column: int):
    canvas.addstr(row, column, char, curses.A_DIM)
    canvas.refresh()
    time.sleep(2)
    canvas.addstr(row, column, char)
    canvas.refresh()
    time.sleep(0.3)
    canvas.addstr(row, column, char, curses.A_BOLD)
    canvas.refresh()
    time.sleep(0.5)
    canvas.addstr(row, column, char)
    canvas.refresh()
    time.sleep(0.3)


async def blink(symbol: str, canvas: curses.window, row: int, column: int):
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


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

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
