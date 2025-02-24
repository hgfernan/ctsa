#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptation of files to new testing standard
Created on Wed Feb  5 15:15:16 2025

@author: hilton
"""

import sys     # argv, exit()
import csv     # QUOTE_NONNUMERIC
import sqlite3 # class Connection, class Cursor, connect()

from typing import Any, Dict, List, Tuple

import pandas as pd

def main(argv : List[str]) -> int:
    """
    Main program

    Parameters
    ----------
    argv : List[str]
        Command line parameters. Used only to get script name

    Returns
    -------
    int
        DESCRIPTION.

    """
    file_db_name : str = 'file_db.csv'
    test_db_name : str = 'test_params.db'

    # HINT open file db
    try:
        file_db = pd.read_csv(file_db_name)

    except (FileNotFoundError, IOError) as exc:
        print(f'{argv[0]}: Could not open file \'{file_db_name}\'')
        print(f'\t{type(exc).__name__}: {str(exc)}')

        # Return to indicate error
        return 1

    # HINT open test params database
    try:
        conn = sqlite3.connect(test_db_name)
        cur = conn.cursor()

    except sqlite3.Error as exc:
        print(f'{argv[0]}: ERROR {type(exc).__name__}: str(exc)')

        # Return to indicaate failure
        return 2

    except FileNotFoundError as exc:
        print(f'{argv[0]}: ERROR Could not find file \'{test_db_name}\'')
        print(f'\t{type(exc).__name__}: {str(exc)}')

        # Return to indicate error
        return 3

    except IOError as exc:
        print(f'{argv[0]}: Could not open file \'{test_db_name}\'')
        print(f'\t{type(exc).__name__}: {str(exc)}')

        # Return to indicate error
        return 4

    # HINT line separator mapping
    terminator_dict : Dict[str, str] = \
        {'newline' : '\n', 'carriage_return' : '\r'}

    # HINT obtain next file number value
    query : str = 'SELECT MAX(datafile_id) FROM datafiles;'
    rv : List[Tuple[Any]] = cur.execute(query).fetchall()

    file_no : int = 1
    if (len(rv) >= 1) and (rv[0][0] is not None):
        file_no = rv[0][0] + 1

    # HINT for each line of file db
    value_ind : int = -1
    for index, row in file_db.iterrows():
        # HINT chose a terminator
        terminator : str = terminator_dict[row['Terminator']]

        header : int = None
        if row['Header'] == 1:
            header = 0

        index_col = False
        if row['Index'] != 0:
            index_col = row['Index'] - 1

        parse_dates = False
        if row['Date indx'] != 0:
            parse_dates = True

        # HINT get data file, skipping rows
        if row['Separator'] == ' ':
            # HINT handle file with blank space separators
            original : pd.DataFrame = \
                pd.read_csv(row['Original'],
                            header=header,
                            quoting=csv.QUOTE_NONNUMERIC,
                            parse_dates=parse_dates,
                            index_col=index_col,
                            skiprows=row['Skip'],
                            sep='\\s+',
                            lineterminator=terminator)
        else:
            original : pd.DataFrame = \
                pd.read_csv(row['Original'],
                            header=header,
                            quoting=csv.QUOTE_NONNUMERIC,
                            index_col=index_col,
                            parse_dates=parse_dates,
                            skiprows=row['Skip'],
                            lineterminator=terminator)

        print(index, row)


        # HINT if file has index, select column 0 as index
        if row['Index'] != 0:
            original = original.reset_index()
            index = original.iloc[:, row['Index'] - 1]
            value_ind = row['Selected']
        else:
            index = list( range(len(original)) )
            value_ind = row['Selected'] - 1

        # print(f'value_ind {value_ind}')
        # print(original.head())
        value = original.iloc[:, value_ind]

        # HINT create a data frame with 'index' and 'value'
        file_df = pd.DataFrame({'index': index, 'value' : value})

        # HINT save file as <file number>.csv
        file_df_name : str = f'../testdata/{file_no:04d}.csv'
        file_df.to_csv(file_df_name, index=False)

        # HINT create a database entry with the information obtained
        query  = 'INSERT INTO datafiles (from_name, total_recs, description)'
        query += 'VALUES (?, ?, ?)'

        param_tuple = (row['Original'], len(file_df), file_df_name)
        rv = cur.execute(query, param_tuple)

        # HINT commit the changes
        conn.commit()

        # HINT Go next file
        file_no += 1

    # HINT close the test params database
    cur.close()
    conn.close()

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
