import time
import curses

import animation


def draw_screen_with_border(canvas: curses.window):
    curses.curs_set(False)
    curses.update_lines_cols()
    canvas.border()

    row, column = (5, 20)
    frame_lengths = (2, 0.3, 0.5, 0.3, 0)

    coroutine = animation.blink("*", canvas, row, column)
    for timeout in frame_lengths:
        coroutine.send(None)
        canvas.refresh()
        time.sleep(timeout)
    time.sleep(10)


def init():
    curses.wrapper(draw_screen_with_border)


if __name__ == "__main__":
    init()
