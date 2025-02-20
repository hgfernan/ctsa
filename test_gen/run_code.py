#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an automatically generated test
Created on Mon Feb 10 20:06:16 2025

@author: hilton
"""

import sys      # argv, exit()
import signal   # Signal
import os.path  # exists()
import argparse # class ArgumentParser, class Namespace
import subprocess # class CalledProcessError, run()


from types  import SimpleNamespace
from typing import List

def get_executable_root() -> str:
    return '../Bin/DEBUG'

def get_out_prefix(library : str, model : str) -> str :
    return get_executable_root() + '/' + library.lower() + '/' + model.lower()

def bld_range(first : int, last : int = None) -> range:
    if first is None:
        msg : str = 'The first parameter must be an integer, not `None`'
        raise ValueError(msg)
    
    _last : int = last
    if _last is None: 
        _last = first
        
    _first = min(first, _last)
    _last = max(first, _last)
    
    result : range = range(_first, _last + 1)

    # Normal function termination
    return result        
    
    
def parse_cli(argv : List[str]) -> argparse.Namespace:
    result : argparse.Namespace = argparse.Namespace()
    
    desc : str = 'Start sequentially a series of programs'
    parser = argparse.ArgumentParser(description=desc)
    
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
    
    help_str = 'First of a range of parameter identification numbers'
    parser.add_argument('-P', '--param_first', type=int, required=True,
                        help=help_str
                       )
    
    help_str = 'Last of a range of parameter identification numbers, '
    help_str += 'including'
    parser.add_argument('-p', '--param_last', type=int, 
                        help=help_str
                       )
    
    help_str = 'First of a range of data identification numbers'
    parser.add_argument('-D', '--data_first', type=int, required=True, 
                        help=help_str
                       )
    
    help_str = 'First of a range of data identification numbers, '
    help_str += 'including'
    parser.add_argument('-d', '--data_last', type=int,
                        help=help_str
                       )
    
    result = parser.parse_args(argv[1 : ])
    
    # Normal function termination
    return result 


def bld_code_name(model : str, library : str, 
                  param_id : int, data_id : int) -> str:
    
    result : str = model.lower() + '_' + library.lower() + '_'
    result += f'p{param_id:04d}_d{data_id:04d}'
    
    # normal function termination
    return result


def bld_executable_path(library : str, code_name : str) -> str:
    result : str = library + '/' + code_name
    
    # Normal function termination
    return result 

    
def interpret_args(args : argparse.Namespace) -> SimpleNamespace:
    result : SimpleNamespace = SimpleNamespace()
    
    result.model = args.model 
    result.library = args.library
    
    result.param_range = bld_range(args.param_first, args.param_last)
    result.param_first, result.param_last = \
        result.param_range.start, result.param_range.stop - 1
    
    result.data_range = bld_range(args.data_first, args.data_last)
    result.data_first, result.data_last = \
        result.data_range.start, result.data_range.stop - 1
    
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
    
    for param_id in params.param_range:
        for data_id in params.data_range:
            code_name : str = \
                bld_code_name(params.model, params.library, param_id, data_id)
            print(code_name)
            
            executable_name = \
                bld_executable_path(params.library, code_name)
            
            try:
                # TODO get the exec_id from the database
                exec_id = 1
                proc = subprocess.run([executable_name, str(exec_id)], 
                                    cwd=get_executable_root(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, 
                                    check=True
                                   )
                
                err_str : str = proc.stderr.decode(encoding='utf-8')
                if len(err_str) > 0:
                    err_name : str = \
                        get_out_prefix(params.library, params.model)
                    err_name + f'/exec_errs/{exec_id:04d}.err'
                    err_f = open(err_name, 'w')
                    err_f.write(err_str)
                    err_f.close()
                
                log_str : str = proc.stdout.decode(encoding='utf-8')
                log_name : str = get_out_prefix(params.library, params.model)
                log_name += f'/exec_logs/{exec_id:04d}.log'
                log_f = open(log_name, 'w')
                log_f.write(log_str)
                log_f.close()
                
            except FileNotFoundError as exc:
                print(f'{type(exc).__name__}: {str(exc)}')
                print(dir(exc))
            
                # print(f'exc.returncode {exc.returncode}')    
                # print(exc.output)    
                print(exc.__dict__)
                
            except subprocess.CalledProcessError as exc:
                print(f'{type(exc).__name__}: {str(exc)}')
                print(dir(exc))
            
                print(f'exc.returncode {exc.returncode}')    
                print(exc.output)    
                print(exc.__dict__)
                
                print(exc.stdout)
                print(signal.Signals(-exc.returncode).name)
    
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
