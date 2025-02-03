#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes that create programs from templates
Created on Fri Jan 31 14:00:05 2025

@author: hilton
"""

from models import Model
from datafiles import DataFile

class ProgramWriter:
    def __init__(self, method : str) -> None:
        pass 


class ClangProgramWriter(ProgramWriter):
    caput = '#'

    def __init__(self, 
                 code_id : int, model : Model, datafile : str) -> None:
        """
        Construct a ClangProgramWriter object

        Parameters
        ----------
        code_id : int
            DESCRIPTION.
        model : Model
            DESCRIPTION.
        datafile : str
            DESCRIPTION.

        Returns
        -------
        None
            No return at all, just initialize instance.

        """
        self.code_id = code_id
        self.model = model
        self.datafile = datafile
        
        # TODO create the program name:
        self.pgm_name = f'{self.code_id:04d}_{model.name()}'
    
    
class PythonProgramWriter(ProgramWriter):
    pass 

class RlangProgramWriter(ProgramWriter):
    pass

#   int L; // Number of values to extrapolate
# 	int N; // length of time series
# 	int method;
# 	int optmethod;// Valid only for MLE estimation
