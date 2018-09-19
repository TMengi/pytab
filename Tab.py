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
