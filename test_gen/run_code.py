#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an automatically generated test
Created on Mon Feb 10 20:06:16 2025

@author: hilton
"""

import sys      # argv, exit()
import json     # loads()
import signal   # Signal
import sqlite3  # connect(), cursor(), execute()
# import os.path  # exists()
import argparse # class ArgumentParser, class Namespace
import subprocess # class CalledProcessError, run()

# from typing import Any, Dict, List, Tuple
from typing import Any, Dict, List
from types  import SimpleNamespace

from cpuinfo import get_cpu_info

from support_lib import get_executable_folder, get_out_prefix, bld_range, \
    bld_code_name, bld_executable_path, open_db, set_library_info, \
    fetchall_and_tell, fetchone_and_tell

def get_hardware_info() -> Dict[str, str]:
    """
    Get the most relevant hardware information

    Returns
    -------
    Dict[str, Any]
        Information about the processor.

    """
    info : Dict[str, Any] = get_cpu_info()
    result : Dict[str, str] = {}

    for key in ['arch', 'arch_string_raw', 'bits', 'brand_raw', 'count',
                'hz_actual_friendly', 'vendor_id_raw']:
        result[key] = info[key]

    # Normal function termination
    return result


def get_execution_info(params : SimpleNamespace) -> Dict[str, Any]:
    """
    Upload JSON results from executable files, and add them to 
    parameter JSON, to have `execs` value `field`

    Parameters
    ----------
    params : SimpleNamespace
        Program parameters.

    Returns
    -------
    Dict[str, Any]
        DESCRIPTION.

    """



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

    help_str = 'Parameter number'
    parser.add_argument('-p', '--parameter', type=int, required=True,
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
    result.library_ord = args.library_ordinal
    
    # HINT open test params database
    try:
        # HINT find library version string and library id from library ordinal
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
        
        # HINT getting parameter id
        result.param_ord = args.parameter
        target = 'param_id'
        query = """
            SELECT param_id, [description], value FROM params
                WHERE capability_id = (?)
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
        
        # TODO get the exec_id from the database
        result.model = args.model
        target : str = 'exec_id'
        query = """
            SELECT MAX(exec_id FROM execs
        """
        rv = fetchone_and_tell(result, target, query, (result.model,))
        result.model_id = rv[0]

    except sqlite3.Error as exc:
        print(f'{sys.argv[0]}: ERROR {type(exc).__name__}: {str(exc)}')

        # Return to indicate failure
        return None

    except ValueError as exc:
        print(f'{sys.argv[0]}: {type(exc).__name__}: {str(exc)}')

        # Return to indicate failure
        return None

    result.data_range = bld_range(args.data_first, args.data_last)
    result.data_first, result.data_last = \
        result.data_range.start, result.data_range.stop - 1
        
    # TODO adjust datafile range
        
    # TODO create model folder if not available
        
    # TODO create execution output folder if not available
        
    # TODO create execution error folder if not available
        
    # TODO create execution JSON folder if not available

    # Normal function termination
    return result


# TODO get executable id from database
# TODO save json result in the database
# TODO generate log and error msgs for this execution
# TODO save execution results in the database

def save_output(exec_id : int, out_prefix : str, o_type : str, o_buf : bytes) \
    -> None:
    """
    Save program output with proper name in the proper folder

    Parameters
    ----------
    exec_id : int
        Id of the execution.
    out_prefix : str
        Prefix path of the output folder.
    o_type : str
        Output type as a string. Valid values are "log" and "err".
        To be replaced as an enum
    o_buf : bytes
        Contents of the output as a byte array.

    Returns
    -------
    None

    Raises
    -------
    ValueError
        In case of invalid o_type

    OSError
        In case of problem writing the output

    """
    valid_o_type : List[str] = ['err', 'log']
    if o_type not in valid_o_type:
        raise ValueError(f'Invalid o_type \'{o_type}\'. Should be one of ' +
                         valid_o_type)

    if len(o_buf) > 0:
        out_str : str = o_buf.decode(encoding='utf-8')
        out_pre : str = out_prefix + '/exec_' + o_type + 's' + '/'
        out_ext : str = '.' + o_type
        out_name : str = out_pre + f'{exec_id:04d}' + out_ext
        with open(out_name, 'w', encoding='utf-8') as out_f:
            out_f.write(out_str)

        # HINT let the caller handle the exception


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

    # print(args)

    params : SimpleNamespace = interpret_args(args)
    if params is None:
        print(f'{argv[0]}: ERROR Could not interpret command line')

        # Return to indicate failure
        return 2

    # print(params)

    # TODO get processor hardware parameters
    hw_info : Dict[str, str] = get_hardware_info()

    msg : str = ''
    exec_id :int = 1
    for param_id in params.param_range:
        for data_id in params.data_range:
            code_name : str = \
                bld_code_name(params.library, params.model, param_id, data_id)
            # print(code_name)

            executable_name : str = './' + code_name
            executable_folder : str = \
                get_executable_folder(params.library, params.version)
                
            executable_name =\
                bld_executable_path(params.library, params.version, code_name)

            out_prefix : str = \
                get_out_prefix(params.librry, params.version, params.model)

            try:
                print([executable_name, str(exec_id)])
                proc = subprocess.run([executable_name, str(exec_id)],
                # proc = subprocess.run(['ls', '-l'],
                                    cwd=executable_folder,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    check=True
                                   )

                save_output(exec_id, out_prefix, 'log', proc.stdout)

                save_output(exec_id, out_prefix, 'err', proc.stderr)

                # TODO get the process JSON output

                # TODO add the hardware descriptioon to the JSON output

                # TODO save the JSON output in the database

            except FileNotFoundError as exc:
                print(f'{type(exc).__name__}: {str(exc)}')

                msg = f'{type(exc).__name__}: {str(exc)}'
                save_output(exec_id, out_prefix, 'err', msg.encode('utf-8'))

                print(msg)

            except subprocess.CalledProcessError as exc:
                msg = ''
                msg += f'{type(exc).__name__}: {str(exc)}\n'
                msg += f'\tReturn code {exc.returncode}\n'
                if exc.returncode < 0:
                    msg += f'\tSignal: {signal.Signals(-exc.returncode).name})'
                    msg += '\n'

                print(type(exc.output))
                msg += '\n' + 40*'-' + '\n\n'
                msg += exc.output.decode(encoding='utf-8') + '\n'
                print(msg)

                save_output(exec_id, out_prefix, 'err',
                            msg.encode(encoding='utf-8'))

            except ValueError as exc:
                msg += f'{type(exc).__name__}: {str(exc)}\n'
                print(f'{argv[0]}: INTERNAL ERROR {msg}')

            except OSError as exc:
                msg += f'{type(exc).__name__}: {str(exc)}\n'
                print(f'{argv[0]}: ERROR Could not write output')
                print(f'\t{msg}')

            finally:
                exec_id += 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
