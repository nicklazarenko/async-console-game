import os
import random
import time
import curses

from game import animation


TICK_TIMEOUT = 0.1
STARS_FRACTION = 0.2
SPACESHIP_TIMEOUT = 2

coroutines = []  # main event loop should be accessible outside of the module


def load_frames() -> dict[str, str]:
    package_dir, _ = os.path.split(__file__)
    frames_dir = os.path.join(package_dir, "frames")

    frames = {}
    for filename in os.listdir(frames_dir):
        with open(os.path.join(frames_dir, filename)) as content:
            frames[filename] = content.read()

    return frames


def run_loop(canvas: curses.window):
    curses.curs_set(False)
    curses.update_lines_cols()
    canvas.nodelay(True)

    frames = load_frames()
    screen_rows, screen_columns = canvas.getmaxyx()

    stars_count = round(screen_rows * screen_columns * STARS_FRACTION)
    for _ in range(stars_count):
        coroutines.append(
            animation.blink(
                canvas=canvas,
                row=random.randint(1, screen_rows - 2),
                column=random.randint(1, screen_columns - 2),
                symbol=random.choice("+*.:"),
            )
        )

    coroutines.append(
        animation.animate_spaceship(
            canvas,
            screen_rows // 2,
            screen_columns // 2 - 2,
            frames,
            SPACESHIP_TIMEOUT,
        )
    )
    coroutines.append(animation.fire(canvas, screen_rows // 2, screen_columns // 2))

    coroutines.append(animation.fill_orbit_with_garbage(canvas, frames))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TICK_TIMEOUT)


def main():
    curses.wrapper(run_loop)
