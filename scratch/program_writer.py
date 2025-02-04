#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes that create programs from templates
Created on Fri Jan 31 14:00:05 2025

@author: hilton
"""

from abc import ABC, abstractmethod
from typing import Dict

from models import Model
from datafiles import DataFile

class ProgramWriter(ABC):
    """
    Abstract class for the program writer tasks
    """
    def __init__(self,
                 code_id : int,
                 model : Model,
                 datafile : DataFile) -> None:
        self.code_id = code_id
        self.model = model
        self.datafile = datafile

    @abstractmethod
    def write_header(self):
        """
        Write the program header, with imports

        Returns
        -------
        None.

        """

    @abstractmethod
    def write_data_load(self):
        """
        Write the program fragment where data is loaded

        Returns
        -------
        None.

        Raises
        ------

        Exception for file error

        """

    @abstractmethod
    def write_model_init(self):
        """
        Write the model init fragment, taking care of allocating
        structures

        Returns
        -------
        None.

        """

    @abstractmethod
    def write_fitting(self):
        """
        Write the model fitting fragment

        Returns
        -------
        None.

        """

    @abstractmethod
    def write_summary(self):
        """
        Write the fragment of summary statistics of the model fitting

        Returns
        -------
        None.

        """

    @abstractmethod
    def write_prediction(self):
        """
        Write the model prediction fragment

        Returns
        -------
        None.

        """

    @abstractmethod
    def write_footer(self):
        """
        Write the finishing of the code, eventually releasing allocated
        structures

        Returns
        -------
        None.

        """

class ClangProgramWriter(ProgramWriter):
    """
    Write a C program, from the data file, statistical model and its
    parameters
    """

    model_dict : Dict[str, str] = {
        'ar' : '',
        'arima' : '',
        'auto_arima' : '',
        'sarima' : '',
        'sarimax' : '',
    }

    def __init__(self,
                 code_id : int,
                 model : Model,
                 datafile : DataFile) -> None:
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
        super(ProgramWriter, self).__init__(code_id, model, datafile)

        # HINT create the program name:
        name : str = f'{self.code_id:04d}_{model.name()}'
        name += f'_d{datafile.get_file_id():03d}.c'
        self.pgm_name = name


class PythonProgramWriter(ProgramWriter):
    """
    Write a Python program, from the data file, statistical model and its
    parameters
    """

class RlangProgramWriter(ProgramWriter):
    """
    Write an R program, from the data file, statistical model and its
    parameters
    """

#   int L; // Number of values to extrapolate
# 	int N; // length of time series
# 	int method;
# 	int optmethod;// Valid only for MLE estimation
