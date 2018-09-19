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
        curses.echo()
        curses.cbreak()
        stdscr.keypad(True)
        self.y_max = curses.LINES
        self.x_max = curses.COLS

        self.add_bar()

        while True:
            c = self.stdscr.getch()

            # quit option
            if c == ord('q'):
                break

            elif c == curses.KEY_UP:
                y, x = curses.getsyx()
                self.stdscr.move(y - 1, x)

            elif c == curses.KEY_DOWN:
                y, x = curses.getsyx()
                self.stdscr.move(y + 1, x)

            elif c == curses.KEY_LEFT:
                y, x = curses.getsyx()
                self.stdscr.move(y, x - 1)

            elif c == curses.KEY_RIGHT:
                y, x = curses.getsyx()
                self.stdscr.move(y, x + 1)

            elif c == ord('h') or c == ord('p'):
                # echo the key
                pass

            # any non number or h/p
            elif c < ord('0') or c > ord('9'):
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
        pass


if __name__ == '__main__':
    tab = Tab('C#G#D#G#CD#')
    tab.edit()
