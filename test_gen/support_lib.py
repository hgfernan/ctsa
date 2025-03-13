#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`test_gen` project support library
Created on Tue Mar  4 18:53:09 2025

@author: hilton
"""

import os # path.exists()
import sys # argv
import sqlite3 # connect(), class Connection

from typing import Any, List, Set, Tuple
from types import SimpleNamespace

def version_to_int(version : str) -> int:
    """
    Map the usual version triplet 'major.minor.patch' (where to all three
    numbers are integers) an integer number

    To be used in SQLite `ORDER BY` clauses.

    OBS: Contributed by ChatGPT

    Parameters
    ----------
    version : str
        The library version. Usually a triplet of three integers 
        'major.minor.patch'.
        
    Returns
    -------
    int
        A single integer number mapping the version triplet.

    """
    # HINT Ensure 3 parts
    parts = list(map(int, (version.split('.') + ['0', '0'])[:3]))
    return 1 + 1000 * (parts[1] + 1000 * parts[0]) + parts[2]

def bld_library_fullname(library : str, version : str) -> str:
    """
    Build the composite of library and version

    Parameters
    ----------
    library : str
        Library name. Will be lowercased.
    version : str
        The library version. Usually a triplet of three integers 
        'major.minor.patch'.

    Returns
    -------
    str
        The concatenation f'{library}_v{version}'.

    """
    result : str = library.lower() + '_v' + version
    
    # Normal function termination
    return result

def get_database_name() -> str:
    return 'test_params.db'

def get_executable_folder(library : str, version : str) -> str:
    """
    Return the executable path

    Returns
    -------
    str
        The binary executable path.

    """
    # TODO how to recover the compilation model (debug, release, etc.) ?
    library_version : str = bld_library_fullname(library, version)
    return '../Bin/DEBUG/' + library_version


def get_source_folder(library : str, version : str) -> str:
    """
    Return the repo-based path to the source folder

    Returns
    -------
    str
        The source code path.

    """
    return '../test/' + library.lower() + '_v' + version


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


def bld_code_name(library : str, model : str,
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
    folder : str = get_executable_folder(library.lower, version)

    if not os.path.exists(folder):
        try:
            os.mkdir(folder)

            return True

        except FileExistsError as exc:
            msg : str = 'OS ERROR ? Executable folder {folder} already exists'

            raise ValueError(msg) from exc

        except FileNotFoundError as exc:
            msg : str = 'Parent folder to executable {folder} doesn\'t exist'

            raise ValueError(msg) from exc

    # Normal function termination
    return False


def mk_source_folder(library : str, version : str) -> bool:
    """
    Create source folder if it's is not available

    Parameters
    ----------
    library : str
        The library in use. Will be lowercased.
    version : str
        The version. Usually a triplet of three integers
        'major.minor.patch'.

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
    folder : str = get_source_folder(library.lower(), version)

    if not os.path.exists(folder):
        try:
            os.mkdir(folder)

            return True

        except FileExistsError as exc:
            msg : str = 'OS ERROR ? Executable folder {folder} already exists'

            raise ValueError(msg) from exc

        except FileNotFoundError as exc:
            msg : str = 'Parent folder to executable folder {folder} '
            msg += 'doesn\'t exist'

            raise ValueError(msg) from exc

    # Normal function termination
    return False


def open_db(db_name : str) -> \
    Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Open the database, catches exception and raises it again

    Parameters
    ----------
    db_name : str
        Database file name.

    Returns
    -------
    None

    Raises
    ------
    sqlite3.Error
        Could not open the database.

        Raises again catched exception.

    """
    conn : sqlite3.Connection = None
    cur : sqlite3.Cursor = None
    
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

    except sqlite3.Error as exc:
        print(f'{sys.argv[0]}: ERROR {type(exc).__name__}: {str(exc)}')

        if conn:
            conn.close()

        # Raise to indicate failure
        msg : str = f'Could not open the database \'{db_name}\''
        raise sqlite3.Error(msg)

    result : Tuple[sqlite3.Connection, sqlite3.Cursor] = conn, cur
    
    # Normal function termination
    return result


def set_library_info(params : SimpleNamespace) -> None:
    """
    Set the version of a library, given its ordinal number, where
    1 is the latest version, 2 is the prior version, etc. in the
    program parameter.

    Set also the unique identifier `library_id` of the pair library
    and version in the program parameter.

    Parameters
    ----------
    params : SimpleNamespace
        An object containing .

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the information sought is not found.

    """
    # HINT registers the function in SQLite database
    params.conn.create_function("version_to_int", 1,
                                version_to_int,
                                deterministic=True)
    query : str = """
    SELECT library_id, name, version FROM libraries
        WHERE name = (?)
        ORDER BY name ASC,
            version_to_int(version) DESC
    """
    target : str = 'library_id'
    rv : List[Tuple[Any]] = params.cur.execute(query,
                                               (params.library.lower(),)
                                               ).fetchall()

    if (rv is None) or (not isinstance(rv, (list, tuple))) or \
        (len(rv) == 0):
        msg : str = f'Query for \'{target}\' returned {rv}'
        print(f'{sys.argv[0]}: ERROR {msg}')

        # Raise exception to indicate failure
        raise ValueError(msg)

    if len(rv) < params.library_ord:
        msg : str = 'Ordinal {params.library_ord} is too large. Only '
        msg += f'{len(rv)} values are available for \'{target}\''
        print(f'{sys.argv[0]}: ERROR {msg}')

        # Raise exception to indicate failure
        raise ValueError(msg)

    ind : int = params.library_ord - 1
    params.library_id = rv[ind][0]
    params.library_version = rv[ind][2]
    

def fetchone_and_tell(params : SimpleNamespace,
                      target : str,
                      query : str,
                      query_params : Tuple[Any, Any]) -> Tuple[Any]:
    """
    Query the database, fetch one row for the answer and raises exception
    if something was wrong

    Parameters
    ----------
    params : SimpleNamespace
        An object with program parameters.
    query : str
        The query to be applied to the database.
    qry_params : Tuple[Any, Any]
        The parameters to the query.

    Returns
    -------
    Tuple[Any]
        The answer, as a tuple.

    Raises
    ------
    ValueError
        If the information sought is not found.

    """
    result = params.cur.execute(query, query_params).fetchone()
    if result is None:
        msg : str = f'Query for \'{target}\' returned empty'
        print(f'{sys.argv[0]}: ERROR {msg}')

        # Raise exception to indicate failure
        raise ValueError(msg)

    # Normal function termination
    return result


def fetchall_and_tell(params : SimpleNamespace,
                      target : str,
                      query : str,
                      query_params : Tuple[Any, Any],
                      ordinal : int) -> List[Tuple[Any]]:
    """
    Query the database, fetch all row of the answer and raises exception
    if something was wrong

    Parameters
    ----------
    params : SimpleNamespace
        An object with program parameters.
    query : str
        The query to be applied to the database.
    query_params : Tuple[Any, Any]
        The parameters to the query.
    ordinal : int
        The position of the expected answer in the list

    Returns
    -------
    List[Tuple[Any]]
        The answer, as a list of tuples.

    Raises
    ------
    ValueError
        If the information sought is not found.

    """
    result = params.cur.execute(query, query_params).fetchall()
    if (result is None) or (not isinstance(result, (list, tuple))) or \
        (len(result) == 0):
        msg : str = f'Query for \'{target}\' returned {result}'
        print(f'{sys.argv[0]}: ERROR {msg}')

        # Raise exception to indicate failure
        raise ValueError(msg)

    if len(result) < ordinal:
        msg : str = 'Ordinal {ordinal} is too large. Only '
        msg += f'{len(result)} values are available for \'{target}\''
        print(f'{sys.argv[0]}: ERROR {msg}')

        # Raise exception to indicate failure
        raise ValueError(msg)

    # Normal function termination
    return result


def adjust_datafile_range(params : SimpleNamespace) -> None:
    """
    Adjust given data file range of numbers to their real limits.
    Raises exception if not possible.

    Parameters
    ----------
    params : SimpleNamespace
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    Raises
    ------
    ValueError
        If the real and the given range sets have no intersection.

    """
    # HINT get the real  file limits in testdata folder
    files : List[str] = sorted(os.listdir('../testdata'))
    datafiles : List[dir] = list(filter(lambda x : x[-4 : ] == '.csv', files))
    data_first = int(datafiles[0].split('.')[0])
    data_last = int(datafiles[-1].split('.')[0])

    real_set : Set[int] = set(range(data_first, data_last + 1))
    print(f'real_set {real_set}')

    # HINT the set given in the command line
    given_set : Set[int] = set(params.datafile_range)
    print(f'given_set {given_set}')

    # HINT the intersection between given and real
    inter = real_set.intersection(given_set)
    print(f'intersection {inter}')

    if len(inter) == 0:
        msg : str = 'Wrong datafile limits. The available range is '
        msg += 'between {data_first} and {data_last}, including'

        raise ValueError(msg)

    inter_min = min(inter)
    inter_max = max(inter)

    if (inter_min != params.data_first) or (inter_max != params.data_last):
        msg : str = 'The given datafile limits will be adjusted to '
        msg += f'[{inter_min}, {inter_max}]'

        print(f'{sys.argv[0]} WARNING: {msg}')

    params.data_first, params.data_last = inter_min, inter_max
    params.datafile_range = range(params.data_first, params.data_last + 1)
    
