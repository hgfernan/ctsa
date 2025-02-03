#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datafile is a class to hold all information in a `datafiles` row
Created on Sun Feb  2 00:25:00 2025

@author: hilton
"""

import sys # argv, exit()
import logging # logger

logger = logging.getLogger(__name__)

from typing import List

import pandas # DataFrame

class DataFile:
    def __init__(self, 
                 file_id : int, filename : str, 
                 expected_recs: int, description : str) \
        -> None:
        """
        Open a data file, set associated information

        Parameters
        ----------
        file_id : int
            DESCRIPTION.
        filename : str
            DESCRIPTION.
        expected_recs : int
            Expected number of records.
        description : str
            DESCRIPTION.

        Raises
        -------
        ValueError
            In case file can't be opened or integer values are negative

        """
        
        self.file_id = file_id
        self.filename = filename
        self.expected_recs = expected_recs
        self.description   = description
        self.data = None
        
        try:
            self.data = pandas.read_csv('data/' + self.filename)
        except FileNotFoundError as exc:
            msg : str = f'{sys.argv[0]}: Could not open file '
            msg += '\'{self.filename}\' for input'
            print(msg)
            print(f'\t{type(exc).__name__}: {str(exc)}')
            
            raise ValueError(msg)
            
        # TODO handle other exceptions 
        
        real_n_recs : int = len(self.data)
        if real_n_recs != self.expected_recs:
            msg : str = f'{sys.argv[0]} Expected number of records '
            msg += f'({self.expected_recs}) differs from the real number '
            msg += f'({real_n_recs}).\n\tIt will be adjusted'
            logger.warning(msg)
            
            self.expected_recs = real_n_recs
        
    def get_file_id(self) -> int:
        return self.file_id
    
    def get_filename(self) -> str:
        return self.filename
    
    def get_expected_recs(self) -> str:
        return self.expected_recs
        
    def get_description(self) -> str:
        return self.description
    
def main(argv : List[str]) -> int:    
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        level=logging.DEBUG)
    
    fmt = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s',
                            '%Y-%m-%d %H:%M:%S')
    file_log = logging.FileHandler('logs/datafiles.log')
    file_log.setFormatter(fmt)
    file_log.setLevel(logging.DEBUG)
    
    logger.addHandler(file_log)

    test_f = open('data/test.csv', 'w', encoding='utf-8')
    test_f.write('"Timestamp","Value"\n')
    test_f.flush()
    
    for recno in range(10):
        value = 10*recno*(10*recno + 5) + 12 
        value = (recno % 200) / 200
        test_f.write(f'{recno},{value}\n')
        test_f.flush()
    
    test_f.close()

    data = DataFile(1, 'test.csv', 20, 'A simple test file')
    
    msg : str = f'Read file \'{data.get_filename()}\''
    logger.info(msg)
    
    msg : str = f'File id {data.get_file_id()}'
    logger.info(msg)
    
    msg : str = f'Total records {data.get_expected_recs()}'
    logger.info(msg)
    
    msg : str = f'Description \'{data.get_description()}\''
    logger.info(msg)
    
    # Normal function termination
    return 0
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
