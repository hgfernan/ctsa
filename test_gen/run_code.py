#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an automatically generated test
Created on Mon Feb 10 20:06:16 2025

@author: hilton
"""

import sys      # argv, exit()
import signal   # Signal
# import os.path  # exists()
import argparse # class ArgumentParser, class Namespace
import subprocess # class CalledProcessError, run()


from types  import SimpleNamespace
from typing import List

def get_executable_root() -> str:
    """
    Return the executable path

    Returns
    -------
    str
        The binary executable path.

    """
    # TODO how to recover the compilation model (debug, release, etc.)
    return '../Bin/DEBUG/'

def get_out_prefix(library : str, model : str) -> str :
    """
    Return the base path where output file folders should be placed

    Parameters
    ----------
    library : str
        The library that is used.
    model : str
        The library that is used.

    Returns
    -------
    str
        A base path where the output folders will be placed.

    """
    return get_executable_root() + '/' + library.lower() + '/' + model.lower()

def bld_range(first : int, last : int = None) -> range:
    """
    Return a closed interval interval range from the left and right limits,
    inclusive. Handle the case when the right limit is None.

    Parameters
    ----------
    first : int
        The left limit of the closed interval.
    last : int, optional
        The right limit of the closed interval. The default is None, when
        the interval is only the first .

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    range
        A closed interval of the limits, as a standard Python `range` object.

    """
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
    """
    Parse command line parameters using the standard module `argparse`

    Parameters
    ----------
    argv : List[str]
        The command line parameters as the usual argument list of strings.

    Returns
    -------
    result : argparse.Namespace
        A list of parameters in a class-like structure.

    """
    result : argparse.Namespace = argparse.Namespace()

    desc : str = 'Start sequentially a series of programs'
    parser = argparse.ArgumentParser(description=desc)

    help_str : str = 'Statistical library'
    choices = ['ctsa', 'forecast', 'pmdarima', 'statsmodels']
    parser.add_argument('-l', '--library',
                        choices=choices,
                        required=True,
                        help=help_str
                       )

    help_str = 'Statistical model to be used'
    choices : List[str] = ['AR', 'ARIMA', 'SARIMA', 'SARIMAX']
    parser.add_argument('-m', '--model', choices=choices,
                        required=True, help=help_str
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

    help_str = 'Last of a range of data identification numbers, '
    help_str += 'including'
    parser.add_argument('-d', '--data_last', type=int,
                        help=help_str
                       )

    result = parser.parse_args(argv[1 : ])

    # Normal function termination
    return result


def bld_code_name(library : str,model : str,
                  param_id : int, data_id : int) -> str:
    """
    Build the code name from library, statistical model, parameter and data.

    Parameters
    ----------
    library : str
        The library the code is build upon.
    model : str
        The statistical model implemented by the code.
    param_id : int
        The identification of the program parameters as a number.
    data_id : int
        The identification of the data file as a number.

    Returns
    -------
    str
        The full name of the code.

    """

    result : str = model.lower() + '_' + library.lower() + '_'
    result += f'p{param_id:04d}_d{data_id:04d}'

    # normal function termination
    return result


def bld_executable_path(library : str, code_name : str) -> str:
    """
    Build the executable path from library and code name

    Parameters
    ----------
    library : str
        The library the code is built upon.
    code_name : str
        The name of the code.

    Returns
    -------
    str
        Library path plus code name.

    """
    result : str = library + '/' + code_name

    # Normal function termination
    return result


def interpret_args(args : argparse.Namespace) -> SimpleNamespace:
    """
    Interpret command line arguments, generating ranges.

    A future version will confirm all needed folders are available.

    Parameters
    ----------
    args : argparse.Namespace
        The result of a command line parsing using Python's `argparse`.

    Returns
    -------
    SimpleNamespace
        Program parameters as a class-like structure, or None in case
        of failure.

    """
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


# TODO get executable id from database
# TODO save json result in the database 
# TODO generate log and error msgs for this executin
# TODO save execution results in the database

def main(argv : List[str]) -> int:
    """
    Parse command line, execute programs and save their results

    Parameters
    ----------
    argv : List[str]
        Command line parameters.

    Returns
    -------
    int
        0 if execution is without problems, an error code otherwise.

    """

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

    exec_id :int = 1
    for param_id in params.param_range:
        for data_id in params.data_range:
            code_name : str = \
                bld_code_name(params.library, params.model, param_id, data_id)
            print(code_name)

            executable_name = \
                bld_executable_path(params.library, code_name)

            try:
                # TODO get the exec_id from the database
                print([executable_name, str(exec_id)])
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
                    err_name += f'/exec_errs/{exec_id:04d}.err'
                    with open(err_name, 'w', encoding='utf-8') as err_f:
                        err_f.write(err_str)

                log_str : str = proc.stdout.decode(encoding='utf-8')
                log_name : str = get_out_prefix(params.library, params.model)
                log_name += f'/exec_logs/{exec_id:04d}.log'
                with open(log_name, 'w', encoding='utf-8') as log_f:
                    log_f.write(log_str)

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
            
            finally:
                exec_id += 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
