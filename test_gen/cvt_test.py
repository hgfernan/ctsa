#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptation of files to new testing standard
Created on Wed Feb  5 15:15:16 2025

@author: hilton
"""

import sys # argv, exit()

from typing import List

import pandas as pd 

# TODO open file db
# TODO for each line of file db
    # TODO get data file, skipping rows 
    # TODO if file has index, select column 0 as index
    # TODO create a data frame with index named 'index' and value as 'value'
    # TODO save file as <file number>.csv
    
def main(argv : List[str]) -> int:
    file_db_name : str = 'file_db.csv'
    try:
        file_db = pd.read_csv(file_db_name)
    
    except (FileNotFoundError, IOError) as exc:
        print(f'{argv[0]}: Could not open file \'{file_db_name}\'')
        print(f'\t{type(exc).__name__}: {str(exc)}')
        
        # Return to indicate error
        return 1
    
    file_no : int = 1
    value_ind : int = -1
    for index, row in file_db.iterrows():
        if row['Separator'] == ' ':
            original : pd.DataFrame = \
                pd.read_csv(row['Original'], 
                            skiprows=row['Skip'], 
                            delim_whitespace=True)
        else:
            original : pd.DataFrame = \
                pd.read_csv(row['Original'], skiprows=row['Skip'])
            
        print(index, row)

        value_ind = row['Selected'] - 1
        
        if row['Index'] != 0:
            original.reset_index()
            index = original.iloc[:, row['Index'] - 1]
        else:
            index = [ind for ind in range(len(original))]

        value = original.iloc[:, value_ind]
        
        file_df = pd.DataFrame({'index': index, 'value' : value})
        
        file_df_name : str = f'{file_no:04d}.csv'
        file_df.to_csv(file_df_name, index=False)
        
        # HINT Go next file
        file_no += 1 
    
    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
