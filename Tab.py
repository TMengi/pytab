""" Tab.py

The main object for the module
"""
__author__ = "Tyler McCown"
__date__ = "18 September 2018"

import re
import curses

tuning_regex = re.compile("\w#?")
rows_regex = re.compile("\d+:(.+)")


class Tab(object):

    def __init__(self, tuning='EADGBE', capo=None):
        """
        Object to input and store guitar tablature data.

        :param tuning: string representing open notes
        :param capo: optional integer for capo
        """
        self.tuning = tuning_regex.findall(tuning)
        self.capo = capo
        self.tab = ''

    def screen(self, stdscr):
        """
        curses display
        """
        self.stdscr = stdscr
        curses.curs_set(1)
        curses.cbreak()
        stdscr.keypad(True)
        self.y_max = curses.LINES
        self.x_max = curses.COLS

        self.stdscr.addstr(0, 0, "Tuning: {} {} {} {} {} {}".format(*self.tuning))
        self.y_loc = 2

        if self.capo is not None:
            self.stdscr.addstr(1, 0, "Capo {}".format(self.capo))
            self.y_loc += 1

        self.add_bar()

        while True:
            c = self.stdscr.getch()

            # quit key
            if c == ord('q'):
                self.write('out.txt')
                break

            # cursor movement with arrow keys or wasd
            elif c == curses.KEY_UP or c == ord('w'):
                y, x = curses.getsyx()
                self.stdscr.move(max(0, y - 1), x)
            elif c == curses.KEY_DOWN or c == ord('s'):
                y, x = curses.getsyx()
                self.stdscr.move(min(self.y_max - 1, y + 1), x)
            elif c == curses.KEY_LEFT or c == ord('a'):
                y, x = curses.getsyx()
                self.stdscr.move(y, max(0, x - 1))
            elif c == curses.KEY_RIGHT or c == ord('d'):
                y, x = curses.getsyx()
                self.stdscr.move(y, min(self.x_max - 1, x + 1))

            # keys for the tab
            elif ord('0') <= c <= ord('9') \
                    or c == ord('h') \
                    or c == ord('p') \
                    or c == ord('/')\
                    or c == ord('-')\
                    or c == ord('|'):
                coords = curses.getsyx()
                self.stdscr.addch(c)
                self.stdscr.move(*coords)

            # insert new bar
            elif c == curses.KEY_IC:
                self.add_bar()

            else:
                pass

    def add_bar(self):
        """
        prints another bar on the curses display for editing

        :param x: x location for new bar
        :param y: y location for new bar
        :return: (x, y) coord of end of bar
        """
        bar = "----------------|"

        num_bars = min(4, self.x_max // len(bar))
        tune_width = max((len(s) for s in self.tuning))

        for i, string in enumerate(self.tuning):
            self.stdscr.addstr(self.y_loc, 0, f"{string:{tune_width}}|" + bar * num_bars)
            self.y_loc += 1

        self.y_loc += 1

    def edit(self):
        """
        opens a curses display to edit the tab
        """
        curses.wrapper(self.screen)

    def write(self, file_name):
        """
        writes the tab to an output file

        :param file_name: string for output file name
        """
        with open(file_name, 'w+b') as f:
            self.stdscr.putwin(f)

        self.format_file(file_name)

    def format_file(self, file_name):
        with open(file_name, 'rb') as f:
            file_string = f.read()[4:].decode('utf-8')
            file_string = re.sub("\s{2:}", '', file_string).replace('\s', ' ')
            rows = rows_regex.findall(file_string)

        with open(file_name, 'w') as f_new:
            for line in rows:
                f_new.write(line + '\n')


if __name__ == '__main__':
    tab = Tab('C#G#D#G#CD#')
    tab.edit()
