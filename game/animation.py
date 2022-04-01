import asyncio
import curses
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
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
