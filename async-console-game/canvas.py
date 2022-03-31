import time
import curses


def draw_screen_with_border(canvas: curses.window):
    curses.curs_set(False)

    row, column = (5, 20)
    canvas.addstr(row, column, 'Hello, World!')

    while True:
        curses.update_lines_cols()
        canvas.border()
        canvas.refresh()
        time.sleep(1)


if __name__ == '__main__':
    curses.wrapper(draw_screen_with_border)
