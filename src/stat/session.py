#!/usr/bin/env python
# -*- coding: utf-8-unix -*-
from __future__ import absolute_import, print_function, division, unicode_literals


class Session:
    """Base class for session that can be called, saved, instantiated from
    command line.
    """

    def load_from_dict(self, d):
        """Load this instance from a dictionary.
        """
        raise RuntimeError("Missing implementation")

    def input_wizard(self, csv_filename=None, csv_indices=None):
        """Wizard to input the parameters from console. If csv_filename is given, then data
        will be loaded from the CSV file. The csv_indices is given, then the data will be
        taken from the specified column indices.
        """
        raise RuntimeError("Missing implementation")

    def save_to_dict(self):
        """Save this instance to a dictionary to be serialized.
        """
        raise RuntimeError("Missing implementation")

    def print_report(self):
        """Print report to stdout.
        """
        raise RuntimeError("Missing implementation")

