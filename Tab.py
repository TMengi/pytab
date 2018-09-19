""" Tab.py

The main object for the module
"""
__author__ = "Tyler McCown"
__date__ = "18 September 2018"

import re

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

    def edit(self):
        """
        opens a curses display to edit the tab
        """
        pass

    def write(self, file_name):
        """
        writes the tab to an output file

        :param file_name: string for output file name
        """
        pass
