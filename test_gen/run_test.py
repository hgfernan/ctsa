#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an automatically generated test
Created on Mon Feb 10 20:06:16 2025

@author: hilton
"""

import sys      # argv, exit()
import argparse # class ArgumentParser, class Namespace

from types  import SimpleNamespace
from typing import List

# TODO parse command line 
# TODO get the executable name and the number of test
# TODO run the code 
    # TODO if executable succeeds, 
        # TODO save the success report with the name and number of test
        # TODO updates the test summary with the result
    # TODO if executable fails, 
        # TODO save the fail report with the name and number of test
        # TODO updates the test summary with the result
  
def parse_cli(argv : List[str]) -> argparse.Namespace:
    result : argparse.Namespace = argparse.Namespace()
    
    parser = argparse.ArgumentParser(argv[1 : ])
    
    help_str : str = 'Statistical model to be used'
    parser.add_argument('-m', '--model', type=str, required=True, 
                        help=help_str
                       )
    
    help_str : str = 'Statistical library'
    libs : List[str] = ['ctsa', 'forecast', 'pmdarima', 'statsmodels']
    parser.add_argument('-l', '--library', 
                        choices=libs,
                        required=True, 
                        help=help_str
                       )
    
    help_str : str = 'Statistical library'
    parser.add_argument('-l', '--library', type=str, required=True, 
                        help=help_str
                       )
    
    # Normal function termination
    return result 
  
def interpret_args() -> SimpleNamespace:
    result : SimpleNamespace = SimpleNamespace()
    
    # Normal function termination
    return result 

def main(argv : List[str]) -> int:
    
    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
