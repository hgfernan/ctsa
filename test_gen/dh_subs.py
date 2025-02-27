#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation and some testing of double hash annotations in code
templates
Created on Wed Feb 26 13:19:42 2025

@author: hilton
"""

import re  # compile(), search()
import sys # argv, exit

from typing import Any, List, Union

NoneType = type(None)
ItemType = Union[str, int, float, NoneType]

class DoubleHashSubs:
    """
    Will parse a string with double hash markings
    """
    re_int : str = r'[\-\+]{0,1}(\d)+'
    re_fixed : str = r'[\-\+]{0,1}(\d)+\.{0,1}(\d)+'
    re_sci : str = r'[\-\+]{0,1}(\d)+\.{0,1}(\d)+[eE][\-\+]{0,1}(\d){1,4}'

    p_int = re.compile(re_int)
    p_fixed = re.compile(re_fixed)
    p_sci = re.compile(re_sci)

    def __init__(self,  line : str, dbl_quote : bool = True) -> None:
        """
        Creates an instance of a double hash parser and substituter

        Parameters
        ----------
        line : str
            The double hash string to be parsed and eventually filled in.
        dbl_quote : bool, optional
            Should strings be delimited with double quotes, aka ". 
            The default is True.

        Returns
        -------
        None
            A Python constructor returns nothing.

        """
        self.items : List[ItemType] = line.split('##')
        self.n_blanks = len(self.items) // 2

        self.blanks : List[int] = []
        for ind in range(self.n_blanks):
            self.blanks.append(2*ind + 1)

        self.dbl_quote = dbl_quote
        self.quotechar = '\''
        if self.dbl_quote:
            self.quotechar = '"'

    def get_n_blanks(self) -> int:
        """
        Obtain the number of fields that can be replaced

        Returns
        -------
        int
            Number of fields open to blank.

        """
        return self.n_blanks

    def get_blank_indices(self) -> List[int]:
        """
        Get the position in the item list, of all blank items

        Returns
        -------
        List[int]
            DESCRIPTION.

        """
        return self.blanks

    def get_blanks(self) -> List[ItemType]:
        """
        Return the list of all blank items, filled in or not, in the 
        item list

        Returns
        -------
        List[ItemType]
            A list of all blank items, filled in or not.

        """
        result : List[Union[str, int, float]] = []

        for _, value in enumerate(self.blanks):
            result.append(self.items[value])

        return result

    def get_blank(self, ind : int) -> ItemType:
        """
        Return the item of the ind-th blank in the item list, or None if the 
        index is invalid

        Parameters
        ----------
        ind : int
            The position of the ind-th blank in the item list.

        Returns
        -------
        ItemType
            The value of the given blank in the item list, or None
            if the index is invalid.

        """
        if (ind < 0) or (ind >= self.n_blanks):
            return None

        return self.items[self.blanks[ind]]

    def get_n_items(self) -> int:
        """
        Obtain the count of items available

        Returns
        -------
        int
            The count of items avaliable.

        """
        return len(self.items)

    def get_items(self) -> List[Union[str, int, float]]:
        """
        Return the whole list of items

        Returns
        -------
        List[Union[str, int, float]]
            The list of available items.

        """
        return self.items

    def get_item(self, ind) -> Union[str, float, int, NoneType]:
        """
        Return the item with the given index, or None if invalid index.

        Parameters
        ----------
        ind : int
            The index to the element list.

        Returns
        -------
        Union[str, float, int, NoneType]
            The item in the given index, or None if not available.

        """
        if (ind < 0) or (ind >= self.get_n_items()):
            return None

        return self.items[ind]

    def fill_in(self, ind : int, elmt : Union[float, str]) -> Any:
        """
        Fill some blank with a provided element, if the index to it
        is valid.

        Parameters
        ----------
        ind : int
            Index to blank to be filled in.
        elmt : Union[float, str]
            The element to fill in the blank.

        Returns
        -------
        Any
            The previous value in the line, or None if the index is
            invalid.

        """
        if (ind < 0) or (ind >= self.n_blanks):
            return None

        abs_ind = self.blanks[ind]
        result : Union[float, str] = self.items[abs_ind]

        if isinstance(elmt, str):
            self.items[abs_ind] = elmt

            # Normal function termination
            return result

        rv = __class__.p_int.search(elmt)
        if rv:
            span : List[int] = rv.span()
            frag : str = elmt[span[0] : span[1]]
            # print(self.blanks)
            # print(self.blanks, ind, int(frag))
            self.items[abs_ind] = int(frag)

            # Normal function termination
            return result

        rv = __class__.p_sci.search(elmt)
        if rv:
            rv = __class__.p_fixed.search(elmt)

        if rv:
            span = rv.span()
            frag : str = elmt[span[0] : span[1]]
            self.items[abs_ind] = float(frag)

            # Normal function termination
            return result

        # HINT it's not a numeric value, let's quote it
        self.items[abs_ind] = self.quotechar + elmt + self.quotechar

        # Normal function termination
        return result

    def rebuild(self) -> str:
        """
        Generate a string from the splitted elements, possibly after
        filling ins.

        Returns
        -------
        str
            A string with the splitted items joined.

        """
        result : str = ''

        # HINT to keep pylint happy
        for ind, _ in enumerate(self.items):
            result += str(self.items[ind])

        # Normal function termination
        return result


def test_doublehashsubs(line : str, fillings : List[str]) -> str:
    """
    Test class DoubleHashSubs

    Parameters
    ----------
    base : str
        DESCRIPTION.
    fillings : List[str]
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    print(f'Will fill in the blanks in \n\t\'{line}\'')
    dh_parser = DoubleHashSubs(line)

    print(f'With the fillings\n\t{fillings}')

    n_items : int = dh_parser.get_n_items()
    print(f'n_items {n_items}')

    for ind in range(n_items):
        print(f'\t{ind:3} \'{dh_parser.get_item(ind)}\'')

    n_blanks : int = dh_parser.get_n_blanks()
    print(f'n_blanks {n_blanks}')

    for ind in range(n_blanks):
        print(f'\t{ind:3} \'{dh_parser.get_blank(ind)}\'')

    print('Will replace')

    for ind, value in enumerate(fillings):
        old = dh_parser.fill_in(ind, value)
        new = dh_parser.get_blank(ind)
        print(f'\t{ind} Replaced \'{old}\' with {new}')

    print('After replacement, the fillings are')
    for ind in range(min(len(fillings), dh_parser.get_n_blanks()) ):
        rv = dh_parser.get_blank(ind)
        print(f'\t{ind} {rv}')

    print('Will rebuild the replaced string')
    print(f'\t{dh_parser.rebuild()}')
    print()


def main(argv : List[str]) -> int:
    """
    The main program, tiny test of class DoubleHashSubs

    Parameters
    ----------
    argv : List[str]
        Command line parameters.

    Returns
    -------
    int
        0 if everything fine, an error code otherwise.

    """
    print(f'{argv[0]} Testing class DoubleHashSubs...\n')

    test_doublehashsubs('aaaa##b##aba', ['122'])
    test_doublehashsubs('aaaa##b##aba##x##', ['122', 'hjelsberg'])
    test_doublehashsubs('aaaa##b##aba##x##', ['122', 'hjelsberg', 'karma'])

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
