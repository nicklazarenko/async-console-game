import random
import time
import curses

import animation


def draw_screen_with_border(canvas: curses.window):
    curses.curs_set(False)
    curses.update_lines_cols()
    canvas.border()

    coroutines = []
    TICK_TIMEOUT = 0.1
    screen_rows, screen_columns = canvas.getmaxyx()
    stars_count = round(screen_rows * screen_columns * 0.25)
    print(stars_count)
    for _ in range(stars_count):
        coroutines.append(
            animation.blink(
                symbol=random.choice("+*.:"),
                canvas=canvas,
                row=random.randint(1, screen_rows - 2),
                column=random.randint(1, screen_columns - 2),
            )
        )

    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)


def init():
    curses.wrapper(draw_screen_with_border)


if __name__ == "__main__":
    init()
