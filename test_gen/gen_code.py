#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generation of code from the databases and templates
Created on Mon Feb 24 19:51:18 2025

@author: hilton
"""

# TODO for the number of data, template and parameters, generate code

import sys      # argv, exit()
import sqlite3  # connect(), cursor(), execute()
# import os.path  # exists()
import argparse # class ArgumentParser, class Namespace

from typing import List, Tuple
from types  import SimpleNamespace

# from dh_subs import DoubleHashSubs, NoneType, ItemType

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
    Parse command line parameters using module `argparse`

    Parameters
    ----------
    argv : List[str]
        Command line parameters.

    Returns
    -------
    result : argparse.Namespace
        A structure with arguments parsed from command line.

    """
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

    help_str = 'Ordinal of template for library and statistical model. '
    help_str += 'Starts with 1'
    parser.add_argument('-t', '--template', type=int,
                        help=help_str
                       )

    help_str = 'Ordinal of parameter for template. '
    help_str += 'Starts with 1'
    parser.add_argument('-p', '--parameter', type=int,
                        required=True, help=help_str
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


def interpret_args(args : argparse.Namespace) -> SimpleNamespace:
    """
    Receives parsed command line arguments and generates program
    elements, reading from the database

    Parameters
    ----------
    args : argparse.Namespace
        The result of parsing command line arguments using `argparse`.

    Returns
    -------
    SimpleNamespace
        A list of parsed command line arguments.

    """
    result : SimpleNamespace = SimpleNamespace()

    result.test_db_name : str = 'test_params.db'

    # HINT open test params database
    try:
        result.conn = sqlite3.connect(result.test_db_name)
        result.cur = result.conn.cursor()

    except sqlite3.Error as exc:
        print(f'{sys.argv[0]}: ERROR {type(exc).__name__}: str(exc)')

        if result.conn:
            result.conn.close()

        # Return to indicate failure
        return None

    # HINT get library id
    result.library = args.library

    qry : str = """
        SELECT library_id FROM libraries
            WHERE name = ?
    """
    rv = result.cur.execute(qry, (result.library,)).fetchone()
    if rv is None:
        print(f'{sys.argv[0]}: ERROR Library \'{result.library}\' not found')

        # Return to indicate failure
        return None

    result.library_id = rv[0]

    # HINT get model id
    result.model = args.model
    qry = """
        SELECT model_id FROM models
            WHERE name = ?
    """
    rv = result.cur.execute(qry, (result.model,)).fetchone()
    if rv is None:
        print(f'{sys.argv[0]}: ERROR Model \'{result.model}\' not found')

        # Return to indicate failure
        return None

    result.model_id = rv[0]

    # HINT get capability id
    result.model = args.model
    qry = """
        SELECT capability_id FROM capabilities
            WHERE model_id = ? AND library_id = ?
    """
    params : Tuple[int, int] = (result.model_id, result.library_id)
    rv = result.cur.execute(qry, params).fetchone()
    if rv is None:
        print(f'{sys.argv[0]}: ERROR Capability not found ' +
              'for model {result.model} and library (result.library}')

        # Return to indicate failure
        return None

    result.capability_id = rv[0]

    # HINT getting template list
    qry = """
        SELECT template_id, description FROM templates
            WHERE capability_id = ?
            ORDER BY template_id ASC
    """
    rv = result.cur.execute(qry, (result.capability_id,)).fetchall()
    if (rv is None) or (not isinstance(rv, (list, tuple))) or (len(rv) == 0):
        print(f'{sys.argv[0]}: ERROR Unexpected error in template query. ' +
              f'It returned {rv}')

        # Return to indicate failure
        return None

    result.template_ord = args.template
    if len(rv) < result.template_ord:
        print(f'{sys.argv[0]}: ERROR Ordinal {result.template_ord} ' +
              'is too large. Only {len(rv)} are available')

        # Return to indicate failure
        return None

    ind : int = result.template_ord - 1
    result.template_id = rv[ind][0]
    result.templ_desc = rv[ind][1]

    # print(type(result.template_id))
    # print(result)

    # HINT getting parameter list
    qry = """
        SELECT param_id, [description], value FROM params
            WHERE template_id = (?)
        ORDER BY param_id
    """
    rv = result.cur.execute(qry, (result.template_id,)).fetchall()
    if (rv is None) or (not isinstance(rv, (list, tuple))) or (len(rv) == 0):
        print(f'{sys.argv[0]}: ERROR Unexpected error in template query. ' +
              f'It returned {rv}')

        # Return to indicate failure
        return None

    result.param_ord = args.parameter
    if len(rv) < result.param_ord:
        print(f'{sys.argv[0]}: ERROR Ordinal {result.param_ord} ' +
              'is too large. Only {len(rv)} are available')

        # Return to indicate failure
        return None

    ind : int = result.param_ord - 1
    result.param_id = rv[ind][0]
    result.param_desc = rv[ind][1]
    result.param_value = rv[ind][2]

    result.data_first, result.data_last = \
        args.data_first, args.data_last

    result.datafile_range : range = \
        bld_range(result.data_first, result.data_last)

    # Normal function termination
    return result

def main(argv : List[str]) -> int:
    """
    Main function for code generation.

    Parameters
    ----------
    argv : List[str]
        Command line arguments.

    Returns
    -------
    int
        0 if no problems found, an error code otherwise.

    """
    args : argparse.Namespace = parse_cli(argv)
    print(f'args\n\t{args}')

    if args is None:
        print(f'{argv[0]}: ERROR Could not parse the comand line')

        # Return to indicate failure
        return 1

    params : SimpleNamespace = interpret_args(args)
    print(f'params\n\t{params}')

    if params is None:
        print(f'{argv[0]}: ERROR Could not interpret the program parameters')

        # Return to indicate failure
        return 2
    
    # TODO loop over the given data files to create the code files    

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
