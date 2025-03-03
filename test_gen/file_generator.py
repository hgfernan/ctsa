#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class `FileGenerator`, to create a code from a template name, and a dictionary
of fillings
Created on Sun Mar  2 13:29:52 2025

@author: hilton
"""

import io # TextIOWrapper
import sys # argv, exit()

from typing import Dict, List

from dh_subs import DoubleHashSubs

class FileGenerator:
    """
    A class that will read a template file with blanks to be filled in, and
    each time it is fed with     a list of fillings, it will generate a file
    with the blanks filled.
    """
    def __init__(self, template_name : str):
        """
        Initialize a file generator, from a file template name

        Parameters
        ----------
        template_name : str
            File template used as input.

        Returns
        -------
        None.

        """
        self.lines : List[List[str]] = [[]]
        self.to_fill : List[int] = []
        self.fill_bkp : Dict[int : List[str]] = {}
        self.being_filled : bool = False

        inp_f : io.TextIOWrapper = io.TextIOWrapper

        # HINT open file, or die trying
        try:
            with open(template_name, "r", encoding='utf-8') as inp_f:
                # HINT input all lines to a string list
                self.lines = inp_f.readlines()

        except FileNotFoundError as exc:
            print(f'{type(exc).__name__}: str(exc))')

            raise

        except IOError as exc:
            print(f'{type(exc).__name__}: str(exc))')

            raise

        finally:
            if not inp_f.closed:
                inp_f.close()

        # HINT for every line in the string list
        for index, line in enumerate(self.lines):
            fields = line.split('##')

            # HINT if a line has double hash pairs
            if (len(fields) % 2) == 1:
                # HINT copy the index to an index list
                self.to_fill.append(index)

                # HINT copy the contents of the line to a backup list
                self.fill_bkp[index] = line

    def fill_in(self, fill_dict : Dict[str, str]) -> int:
        """
        Apply a filling dict to the templates uploaded

        Parameters
        ----------
        fill_dict : Dict[str, str]
            A dictionary containing the names of the blank fields and the
            value to be applied for them.

        Returns
        -------
        int
            Number of lines that had a blank item filled in.

        """
        result : int = 0

        # HINT used as a warning signal
        self.being_filled = True

        for index in self.to_fill:
            line = self.lines[index]

            dhs = DoubleHashSubs(line)
            blanks = dhs.get_blanks()

            for ind, value in enumerate(blanks):
                if value not in fill_dict:
                    msg : str = f'Blank field \'{value}\' from template file '
                    msg += 'in line {index} was not found in fill dictionary.'
                    raise ValueError(msg)

                dhs.fill_in(ind, fill_dict[value])

            self.lines[index] = dhs.rebuild()
            result += 1

        # Normal function termination
        return result

    def save_to_file(self, out_filename : str) -> bool:
        """
        Save the file generator lines in file, provided they were filled in.
        Restores the original values to the lines that were filled in.

        Parameters
        ----------
        out_filename : str
            Filename to be used to save the contents.

        Returns
        -------
        bool
            True if the contents were saved, False otherwise.

        """
        out_f : io.TextIOWrapper

        try:
            with open(out_filename, 'w', encoding='utf-8') as out_f:
                out_f.writelines(self.lines)

        except PermissionError as exc:
            print(f'{type(exc).__name__}: str(exc))')

            raise

        except OSError as exc:
            print(f'{type(exc).__name__}: str(exc))')

            raise

        # HINT restore the original lines
        for ind, value in enumerate(self.to_fill):
            # print(ind, value)
            self.lines[value] = self.fill_bkp[value]

        # HINT revert object to original state
        self.being_filled = False

        # Normal function termination
        return True

def main(argv : List[str]) -> int:
    """
    A simple testbed fro class FileGenerator

    Parameters
    ----------
    argv : List[str]
        Command line parameters.

    Returns
    -------
    int
        0 if no error found, an erro code otherwise.

    """
    rv : bool = False
    n_lines : int = 0
    out_f : io.TextIOWrapper
    out_name : str = 'test.dh'
    fill_dict : Dict[str, str] = {'b' : 122, 'x' : 'Hjelsberg'}
    test_lines : List[List[str]] = ['##b\n','##b##\n', 'aaaa##b##aba\n',
                  'aaaa##b##aba##x##\n', 'aaaa##b##aba##x##\n']

    try:
        with open(out_name, 'w', encoding='utf-8') as out_f:
            out_f.writelines(test_lines)

    except OSError as exc:
        print(f'{argv[0]} ERROR Could not open file for output')
        print(f'\t{type(exc).__name__}: str(exc)')

        # Return to indicate failure
        return 1

    generator : FileGenerator = FileGenerator(out_name)

    n_lines = generator.fill_in(fill_dict)

    print(f'Lines filled: {n_lines}')

    rv = generator.save_to_file('test.filled')

    print(f'Saving done {rv}')

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
