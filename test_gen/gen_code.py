#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generation of code from the databases and templates
Created on Mon Feb 24 19:51:18 2025

@author: hilton
"""

# TODO parse command line to get model, library, template, range of params and data
# TODO retrieve data from the database
# TODO for the number of data, template and parameters, generate code

import sys      # argv, exit()
import signal   # Signal
import sqlite3  # connect(), cursor(), execute()
# import os.path  # exists()
import argparse # class ArgumentParser, class Namespace
import subprocess # class CalledProcessError, run()

from typing import List, Tuple

from types  import SimpleNamespace
from typing import List

def parse_cli(argv : List[str]) -> argparse.Namespace:
    parser : argparse.ArgumentParser = argparse.ArgumentParser()
    result : argparse.Namespace = argparse.Namespace()
    

    help_str : str = 'Statistical library'
    choices = ['ctsa', 'forecast', 'pmdarima', 'statsmodels']
    parser.add_argument('-l', '--library',
                        choices=choices,
                        required=True,
                        help=help_str
                       )

    help_str = 'Statistical model to be used'
    choices : List[str] = ['AR', 'ARMA', 'ARIMA', 'SARIMA', 'SARIMAX']
    parser.add_argument('-m', '--model', choices=choices,
                        required=True, help=help_str
                       )

    help_str = 'Number range of parameter identification numbers, '
    help_str += 'including'
    parser.add_argument('-p', '--param_last', type=int,
                        help=help_str
                       )
    
    # Normal function termination
    return result
    
def main(argv : List[str]) -> int:
    args : argparse.Namespace = parse_cli(argv)
    
    print(args)
    
    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    