#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an automatically generated test
Created on Mon Feb 10 20:06:16 2025

@author: hilton
"""

import sys      # argv, exit()
import os.path  # exists()
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
    
    parser = argparse.ArgumentParser(description='Start a program')
    
    help_str : str = 'Statistical model to be used'
    choices : List[str] = ['AR', 'ARIMA', 'SARIMA', 'SARIMAX']
    parser.add_argument('-m', '--model', choices=choices, 
                        required=True, help=help_str
                       )
    
    help_str : str = 'Statistical library'
    choices = ['ctsa', 'forecast', 'pmdarima', 'statsmodels']
    parser.add_argument('-l', '--library', 
                        choices=choices,
                        required=True, 
                        help=help_str
                       )
    
    help_str : str = 'Parameter identification number'
    parser.add_argument('-p', '--parameter', type=int, required=True, 
                        help=help_str
                       )
    
    help_str : str = 'Data identification number'
    parser.add_argument('-d', '--data', type=int, required=True, 
                        help=help_str
                       )
    
    result = parser.parse_args(argv[1 : ])
    
    # Normal function termination
    return result 
  
    
def interpret_args(args : argparse.Namespace) -> SimpleNamespace:
    result : SimpleNamespace = SimpleNamespace()
    
    code_name : str = ''
    
    code_name = args.model.lower() + '_' + args.library.lower() + '_'
    code_name += f'p{args.parameter:04d}_d{args.data:04d}'
    
    result.code_name = code_name
    
    executable : str = args.library.lower() + '/' + result.code_name
    if not os.path.exists(executable):
        msg : str = f'{sys.argv[0]}: ERROR could not find executable '
        msg += f'\'{executable}\''
        print(msg)
        
        # Return to indicate failure
        return None
        
    result.executable = executable
    
    # Normal function termination
    return result 

def main(argv : List[str]) -> int:
    
    args : argparse.Namespace = parse_cli(argv)
    
    if args is None: 
        print(f'{argv[0]}: ERROR Could not parse command line')
        
        # Return to indicate failure
        return 1 
    
    print(args)
    
    params : SimpleNamespace = interpret_args(args)
    if params is None: 
        print(f'{argv[0]}: ERROR Could not interpret command line')
        
        # Return to indicate failure
        return 2 
    
    print(params)
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
