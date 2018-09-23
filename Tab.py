""" Tab.py

The main object for the module
"""
__author__ = "Tyler McCown"
__date__ = "18 September 2018"

import curses
import re
import time

tuning_regex = re.compile("\w#?")
rows_regex = re.compile("\d+:(\w.+)")


class Tab(object):

    def __init__(self, title: str=None, artist: str=None, tuning: str='EADGBE', capo: int=None, n: int=12, m: int=4):
        """
        Object to input and store guitar tablature data.

        :param title: song title
        :param artist: artist name
        :param tuning: open notes
        :param capo: capo fret number
        :param n: number of notes to put in a measure
        :param m: maximum measures to put in one row
        """
        # user-passed
        self.title = title
        self.artist = artist
        self.tuning = tuning_regex.findall(tuning)
        self.capo = capo
        self.n = n
        self.m = m

        # defined later when screen is created
        self.stdscr = None
        self.y_max = None
        self.x_max = None
        self.y_loc = None

    def screen(self, stdscr):
        """
        curses display
        """
        self.stdscr = stdscr
        stdscr.keypad(True)
        self.y_max = curses.LINES - 1
        self.x_max = curses.COLS - 1
        self.y_loc = 0

        # === print header === #
        # title and artist
        if self.title is not None:
            self.stdscr.addstr(self.y_loc, 0, self.title)
            if self.artist is not None:
                self.stdscr.addstr(self.y_loc, len(self.title), f" - {self.artist}")
            self.y_loc += 1

        # tuning
        self.stdscr.addstr(self.y_loc, 0, "Tuning: {} {} {} {} {} {}".format(*self.tuning))
        self.y_loc += 1

        # capo
        if self.capo is not None:
            self.stdscr.addstr(self.y_loc, 0, "Capo {}".format(self.capo))
            self.y_loc += 1
        self.y_loc += 1

        # add an empty bar
        self.add_bar()

        # run key processing loop
        self.loop()

    def loop(self):
        """
        loop to process keypresses in curses display
        """
        while True:
            c = self.stdscr.getch()

            # quit key
            if c == ord('q'):
                break

            # save key
            elif c == ord('o'):
                # save file
                name = '_'.join(self.title.lower().split()) + '.tab'
                self.write(name)

                # display a message and return cursor to same place
                coord = curses.getsyx()
                curses.curs_set(0)
                self.stdscr.addstr(self.y_max, 0, f"file saved: {name}", curses.A_BOLD)
                self.stdscr.refresh()
                time.sleep(1)
                self.stdscr.addstr(self.y_max, 0, ' ' * self.x_max)
                self.stdscr.move(*coord)
                curses.curs_set(1)

            # cursor movement with arrow keys or wasd
            elif c == curses.KEY_UP or c == ord('w'):
                y, x = curses.getsyx()
                self.stdscr.move(max(0, y - 1), x)
            elif c == curses.KEY_DOWN or c == ord('s'):
                y, x = curses.getsyx()
                self.stdscr.move(min(self.y_max, y + 1), x)
            elif c == curses.KEY_LEFT or c == ord('a'):
                y, x = curses.getsyx()
                self.stdscr.move(y, max(0, x - 1))
            elif c == curses.KEY_RIGHT or c == ord('d'):
                y, x = curses.getsyx()
                self.stdscr.move(y, min(self.x_max, x + 1))

            # valid letter and symbol keys for tab
            elif ord('0') <= c <= ord('9') \
                    or c == ord('x') \
                    or c == ord('h') \
                    or c == ord('p') \
                    or c == ord('/')\
                    or c == ord('-')\
                    or c == ord('|'):
                coords = curses.getsyx()
                self.stdscr.addch(c)
                self.stdscr.move(*coords)

            # key to insert new bar
            elif c == curses.KEY_IC:
                self.add_bar()

            # other keys do nothing
            else:
                pass


    def add_bar(self):
        """
        prints another bar to the curses display for editing
        """
        bar = '-' * self.n * 2 + '|'

        # save original cursor location
        coord = curses.getsyx()

        # calculate how many bars to print and figure out spacing for tuning column
        num_bars = min(self.m, self.x_max // len(bar))
        tune_width = max((len(s) for s in self.tuning))

        # print strings in reversed order
        for i, string in enumerate(reversed(self.tuning)):
            self.stdscr.addstr(self.y_loc, 0, f"{string:{tune_width}}|" + bar * num_bars)
            self.y_loc += 1

        self.y_loc += 1

        # replace cursor in original spot
        self.stdscr.move(*coord)

    def edit(self):
        """
        opens a curses display to edit the tab
        """
        curses.wrapper(self.screen)

    def write(self, file_name: str):
        """
        writes the tab to an output file

        :param file_name: output file name
        """
        # dump screen to file
        with open(file_name, 'w+b') as f:
            self.stdscr.putwin(f)

        # open dump file and read lines as binary
        with open(file_name, 'rb') as f:
            file_string = f.read()[4:].decode('utf-8')
            file_string = re.sub("\s{2:}", '', file_string).replace('\s', ' ')
            rows = rows_regex.findall(file_string)

        # write lines to new
        with open(file_name, 'w') as f_new:
            f_new.write('\n'.join(rows))


if __name__ == '__main__':
    tab = Tab(title="Even the Darkness has Arms", artist="The Barr Brothers", tuning='DGDGBD', n=16, m=1)
    tab.edit()
