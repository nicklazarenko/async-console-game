import os
import random
import time
import curses

import animation


TICK_TIMEOUT = 0.1


def load_frames():
    frames = {}
    for filename in os.listdir("frames"):
        with open(f"frames/{filename}") as content:
            frames[filename] = content.read()
    return frames


def draw_screen_with_border(canvas: curses.window):
    curses.curs_set(False)
    curses.update_lines_cols()
    canvas.nodelay(True)

    frames = load_frames()
    coroutines = []

    screen_rows, screen_columns = canvas.getmaxyx()
    stars_count = round(screen_rows * screen_columns * 0.25)
    for _ in range(stars_count):
        coroutines.append(
            animation.blink(
                symbol=random.choice("+*.:"),
                canvas=canvas,
                row=random.randint(1, screen_rows - 2),
                column=random.randint(1, screen_columns - 2),
            )
        )

    coroutines.append(animation.fire(canvas, screen_rows // 2, screen_columns // 2))
    coroutines.append(
        animation.animate_spaceship(
            canvas, screen_rows // 2, screen_columns // 2 - 2, frames
        )
    )

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)


def init():
    curses.wrapper(draw_screen_with_border)


if __name__ == "__main__":
    init()
