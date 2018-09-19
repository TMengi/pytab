""" Tab.py

The main object for the module
"""
__author__ = "Tyler McCown"
__date__ = "18 September 2018"

import re
import curses

tuning_regex = re.compile("\w#?")


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
            elif c == ord('h') or c == ord('p') or c == ord('/'):
                self.stdscr.addch(c)
            elif ord('0') <= c <= ord('9'):
                self.stdscr.addch(c)

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

        for i, string in enumerate(self.tuning):
            self.stdscr.addstr(i, 0, "{:2}|".format(string) + bar * num_bars)

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


if __name__ == '__main__':
    tab = Tab('C#G#D#G#CD#')
    tab.edit()
