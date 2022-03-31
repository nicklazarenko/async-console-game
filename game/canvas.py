import time
import curses

import animation


def draw_screen_with_border(canvas: curses.window):
    curses.curs_set(False)
    curses.update_lines_cols()
    canvas.border()

    row, column = (5, 20)

    while True:
        animation.dim("*", canvas, row, column)


def init():
    curses.wrapper(draw_screen_with_border)


if __name__ == "__main__":
    init()
