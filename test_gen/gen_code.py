#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generation of code from the databases and templates
Created on Mon Feb 24 19:51:18 2025

@author: hilton
"""

import os       # listdir(), path.exists()
import sys      # argv, exit()
import json     # loads()
import sqlite3  # connect(), cursor(), execute()
import datetime # class datetime
import argparse # class ArgumentParser, class Namespace

from typing import Any, List, Set, Tuple
from types  import SimpleNamespace

# from dh_subs import DoubleHashSubs, NoneType, ItemType
from file_generator import FileGenerator
from support_lib import bld_range, bld_code_name, \
    get_source_folder, bld_source_path, mk_source_folder, \
    version_to_int, open_db


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

    def_int : int = 1
    help_str = 'Library version ordinal from newest to oldest -- 1 is the '
    help_str += f'current, 2 is the previous. Default: {def_int}'
    parser.add_argument('-v', '--version_ordinal',
                        default=def_int,
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

    help_str = 'First of a range of data identification numbers, starting '
    help_str += 'with 1'
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


# def version_to_int(version : str) -> int:
#     """
#     Map the usual version triplet 'major.minor.patch' (where to all three
#     numbers are integers) an integer number

#     To be used in SQLite `ORDER BY` clauses.

#     OBS: Contributed by ChatGPT

#     Parameters
#     ----------
#     version : str
#         A triplet 'major.minor.patch'.

#     Returns
#     -------
#     int
#         A single integer number mapping the version triplet.

#     """
#     # HINT Ensure 3 parts
#     parts = list(map(int, (version.split('.') + ['0', '0'])[:3]))
#     return 1 + 1000 * (parts[1] + 1000 * parts[0]) + parts[2]


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

def insert_code_info(params : SimpleNamespace,
                     code_name : str,
                     datafile_id) -> None:
    """
    Insert code information in the database

    Parameters
    ----------
    params : SimpleNamespace
        Program parameters.

    Returns
    -------
    NoneType
        DESCRIPTION.

    Raises
    ------
    sqlite3.Error
    """
    found : bool = True

    select_qry : str = """
        SELECT * FROM codes
            WHERE filename = (?)
            ORDER BY timestamp DESC
    """

    insert_qry : str = """
        INSERT INTO codes
            (filename,datafile_id,param_id,template_id)
        VALUES (?,?,?,?)
    """
    insert_qry_params : Tuple[Any] = \
        (code_name, datafile_id, params.param_id, params.template_id)

    try:
        rv : List[Tuple[Any]] = \
            params.cur.execute(select_qry, (code_name,)).fetchall()

        if len(rv) > 0:
            found = True
            code_id : int = rv[0][0]
            prior : SimpleNamespace = SimpleNamespace()
            prior.filename = rv[0][2]
            prior.datafile_id = rv[0][3]
            prior.param_id = rv[0][4]
            prior.template_id = rv[0][5]

            if (prior.filename != code_name) or \
               (prior.datafile_id != datafile_id) or \
               (prior.param_id != params.param_id) or \
               (prior.template_id != params.template_id):
                msg : str = 'Existing record (code_id {code_id}) has divergent '
                msg += 'parameters. Please check'

                raise ValueError(msg)

            dt : datetime.datetime = \
                datetime.datetime.now(tz=datetime.timezone.utc)
            new_timestamp : str = dt.strftime('%Y-%m-%d %H:%M:%S')
            update_qry : str = """
            UPDATE codes
                SET timestamp = (?)
            WHERE code_id = (?)
            """
            params.cur.execute(update_qry, (code_id, new_timestamp))

            print(f'*** Adjusted {code_id} to {new_timestamp}')

            # Normal function termination
            return

    except sqlite3.Error as exc:
        print(f'{type(exc).__name__}: {str(exc)}')

        msg : str = ''
        if not found:
            msg = 'Could not select \'{code_name}\''
        else:
            msg = 'Could not update \'{code_name}\''

        # HINT used `from` based on a pylint warning
        raise ValueError(msg) from exc

    try:
        params.cur.execute(insert_qry, insert_qry_params)
        params.conn.commit()

    except sqlite3.Error as exc:
        print(f'{type(exc).__name__}: {str(exc)}')

        msg : str = 'Could not insert info about \'{code_name}\''

        # HINT used `from` based on a pylint warning
        raise ValueError(msg) from exc


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

    # HINT build the datafile range
    result.data_first, result.data_last = \
        args.data_first, args.data_last

    result.datafile_range : range = \
        bld_range(result.data_first, result.data_last)

    # HINT make sure that data_last is updated
    result.data_last = max(result.datafile_range)

    # HINT adjusts the datafile range to the available files in `testdata`
    adjust_datafile_range(result)

    # HINT database name
    result.test_db_name : str = 'test_params.db'

    # HINT library parameters
    result.library = args.library.lower()
    result.library_ord = args.version_ordinal

    # HINT open test params database
    try:
        result.conn, result.cur = \
            open_db(result.test_db_name)

        # HINT get library id using name and version
        set_library_info(result)

        # HINT get model id
        result.model = args.model
        target : str = 'model_id'
        query = """
            SELECT model_id FROM models
                WHERE name = ?
        """
        rv = fetchone_and_tell(result, target, query, (result.model,))
        result.model_id = rv[0]

        # HINT get capability id
        target = 'capability_id'
        query = """
            SELECT capability_id FROM capabilities
                WHERE model_id = ? AND library_id = ?
        """
        rv = fetchone_and_tell(result,
                               target,
                               query,
                               (result.model_id, result.library_id))
        result.capability_id = rv[0]

        # HINT getting template id
        result.template_ord = args.template
        target = 'template_id'
        query = """
            SELECT template_id, description FROM templates
                WHERE capability_id = ?
                ORDER BY template_id ASC
        """
        rv = fetchall_and_tell(result,
                               target,
                               query,
                               (result.capability_id, ),
                               result.template_ord)

        ind : int = result.template_ord - 1
        result.template_id = rv[ind][0]
        result.templ_desc = rv[ind][1]

        # HINT getting parameter id
        result.param_ord = args.parameter
        target = 'parameter_id'
        query = """
            SELECT param_id, [description], value FROM params
                WHERE template_id = (?)
            ORDER BY param_id
        """
        rv = fetchall_and_tell(result,
                               target,
                               query,
                               (result.template_id, ),
                               result.template_ord)

        ind = result.param_ord - 1
        result.param_id = rv[ind][0]
        result.param_desc = rv[ind][1]
        result.param_value = json.loads(rv[ind][2])

    except sqlite3.Error as exc:
        print(f'{sys.argv[0]}: ERROR {type(exc).__name__}: {str(exc)}')

        # Return to indicate failure
        return None

    except ValueError as exc:
        print(f'{sys.argv[0]}: {type(exc).__name__}: {str(exc)}')

        # Return to indicate failure
        return None

    # result.template_ord = args.template
    # if len(rv) < result.template_ord:
    #     print(f'{sys.argv[0]}: ERROR Ordinal {result.template_ord} ' +
    #           'is too large. Only {len(rv)} are available')

    #     # Return to indicate failure
    #     return None

    # ind : int = result.template_ord - 1
    # result.template_id = rv[ind][0]
    # result.templ_desc = rv[ind][1]

    # print(type(result.template_id))
    # print(result)

    # # HINT getting parameter list
    # qry = """
    #     SELECT param_id, [description], value FROM params
    #         WHERE template_id = (?)
    #     ORDER BY param_id
    # """
    # rv = result.cur.execute(qry, (result.template_id,)).fetchall()
    # if (rv is None) or (not isinstance(rv, (list, tuple))) or (len(rv) == 0):
    #     print(f'{sys.argv[0]}: ERROR Unexpected error in template query. ' +
    #           f'It returned {rv}')

    #     # Return to indicate failure
    #     return None

    # result.param_ord = args.parameter
    # if len(rv) < result.param_ord:
    #     print(f'{sys.argv[0]}: ERROR Ordinal {result.param_ord} ' +
    #           'is too large. Only {len(rv)} are available')

    #     # Return to indicate failure
    #     return None

    # ind : int = result.param_ord - 1
    # result.param_id = rv[ind][0]
    # result.param_desc = rv[ind][1]
    # result.param_value = json.loads(rv[ind][2])
    
    if mk_source_folder(result.library, result.library_version):
        msg : str = 'The folder ' + \
            f'{get_source_folder(result.library, result.library_version)} ' +\
            'was created'
        print(f'{sys.argv[0]} WARNING {msg}')

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

    template_name : str = 'templates/' + params.library + '/' + \
        params.library + '_' + params.model.lower() + \
            f'_dh{params.template_id:04d}.c'

    generator : FileGenerator = FileGenerator(template_name)

    # HINT loop over the given data files to create the code files
    for datafile_id in params.datafile_range:
        code_name = \
            bld_code_name(params.library, params.model,
                          params.param_id, datafile_id)

        print(f'{datafile_id:4d} {code_name}')

        source_path = \
            bld_source_path(params.library, params.library_version, code_name)

        datafile_prefix = f'{datafile_id:04d}'

        # HINT confirm there's a file with this name in the folder
        if not os.path.exists('../testdata/' + datafile_prefix + '.csv'):
            print(f'{argv[0]} WARNING: Missing file {datafile_id}')

            # Refuse file name
            continue

        fill_dict = params.param_value['parameters']['init']
        fill_dict['datafile_prefix'] = datafile_prefix
        print(fill_dict)

        # HINT generate the test code, thru the double hash annotation template
        n_lines = generator.fill_in(fill_dict)

        print(f'Lines filled: {n_lines}')

        # HINT write the generated code in the right directory
        rv = generator.save_to_file(source_path)

        print(f'Saving done {rv}')

        # HINT update the database with the code generated
        insert_code_info(params, code_name, datafile_id)

        print(f'Updated database with {code_name}')

    if params.conn:
        params.conn.close()

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
