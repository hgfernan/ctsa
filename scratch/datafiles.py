#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datafile is a class to hold all information in a `datafiles` row
Created on Sun Feb  2 00:25:00 2025

@author: hilton
"""

import sys # argv, exit()

import pandas # DataFrame

class Datafile:
    def __init__(self, 
                 file_id : int, filename : str, 
                 expected_recs: int, description : str) \
        -> None:
        """
        Open a data file, set associated information

        Parameters
        ----------
        file_id : int
            DESCRIPTION.
        filemane : str
            DESCRIPTION.
        expected_recs : int
            Expected number of records.
        description : str
            DESCRIPTION.

        Raises
        -------
        ValueError
            In case file can't be opened or integer values are negative

        """
        
        self.file_id = file_id
        self.filename = filename
        self.expected_recs = expected_recs
        self.description   = description
        self.data = None
        
        try:
            self.data = pandas.read_csv('data/' + self.filename)
        except FileNotFoundError as exc:
            msg : str = f'{sys.argv[0]}: Could not open file '
            msg += '\'{self.filename}\' for input'
            print(msg)
            print(f'\t{type(exc).__name__}: {str(exc)}')
            
            raise ValueError(msg)
        
        # TODO how to return data ?