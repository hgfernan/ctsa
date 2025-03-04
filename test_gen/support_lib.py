#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`test_gen` project support library
Created on Tue Mar  4 18:53:09 2025

@author: hilton
"""

import os # path.exists()

def get_executable_folder(library : str, version : str) -> str:
    """
    Return the executable path

    Returns
    -------
    str
        The binary executable path.

    """
    # TODO how to recover the compilation model (debug, release, etc.) ?
    return '../Bin/DEBUG/' + library.lower() + 'v' + version


def get_source_folder(library : str, version : str) -> str:
    """
    Return the repo-based path to the source folder

    Returns
    -------
    str
        The source code path.

    """
    # TODO how to recover the compilation model (debug, release, etc.)
    return '../test/' + library.lower() + 'v' + version


def get_out_prefix(library : str, version : str, model : str) -> str :
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
    return get_executable_folder(library, version) + '/' + model.lower()


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

    result : str = library.lower() + '_' + model.lower() + '_'
    result += f'p{param_id:04d}_d{data_id:04d}'

    # normal function termination
    return result



def bld_executable_path(library : str, version : str, code_name : str) -> str:
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
    result : str = library + 'v' + version + '/' + code_name

    # Normal function termination
    return result


def bld_source_path(library : str, version : str, code_name : str) -> str:
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
    # TODO in the future, create an OOP solution
    match library.lower():
        case 'ctsa':
            ext = '.c'
        case 'forecast':
            ext = '.R'
        case 'pmdarima':
            ext = '.py'
        case 'pmdarima':
            ext = '.py'
        case 'statsmodels':
            ext = '.py'
        case _:
            msg : str = f'INTERNAL ERROR Unknown library \'{library}\''
            raise ValueError(msg)

    result : str = get_source_folder(library, version) + '/' + code_name + ext

    # Normal function termination
    return result


def mk_executable_folder(library : str, version : str) -> bool:
    """
    Create executable folder if it's not available

    Parameters
    ----------
    library : str
        The library name.
    version : str
        The library name.

    Returns
    -------
    bool
        True if executable folder created successfully, False otherwise.

    Raises
    -------
    ValueError
        If executable folder could not be created or if its parent folder was 
        not available

    """


def mk_source_folder(library : str, version : str) -> bool:
    """
    Create source folder if it's is not available

    Parameters
    ----------
    library : str
        DESCRIPTION.
    version : str
        DESCRIPTION.

    Returns
    -------
    bool
        True if source folder created successfully, False otherwise.

    Raises
    -------
    ValueError
        If source folder could not be created or if its parent folder was not 
        available

    """
    folder : str = get_source_folder(library.lower, version)
    
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
            
            return True
            
        except FileExistsError as exc:
            msg : str = 'OS ERROR ? Folder {folder} already exists'
            
            raise ValueError(msg) from exc
            
        except FileNotFoundError as exc:
            msg : str = 'Parent folder to path {folder} doesn\'t exist'
            
            raise ValueError(msg) from exc
            
    # Normal function termination
    return False    
