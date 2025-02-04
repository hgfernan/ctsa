#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 18:35:36 2025

@author: hilton
"""

import sys  # exit()
import json # loads(), dumps()

from types  import SimpleNamespace
from typing import List

#   int L; // Number of values to extrapolate
# 	int N; // length of time series
# 	int method;
# 	int optmethod;// Valid only for MLE estimation

class Model:
    pass 

class Ar(Model): 
    def __init__(self, value : str) -> None:
        jobj = json.loads(value)
        
        if 'params' not in jobj:
            raise KeyError('\'params\' was not found in AR JSON value')
        
        self.jobj = jobj
        self.base = SimpleNamespace()
        
        params = self.jobj['params']
        self.base.params = SimpleNamespace()
        
        err_msg : str = ''
        should_raise : bool = False
        expecteds : List[str] = ['L', 'N', 'method', 'optmethod']
        for expected in expecteds:
            if expected not in params:
                should_raise = True
                err_msg += '\'' + expected + '\', '
            else:
                self.base.params.__dict__[expected] = params[expected]
        
        if should_raise: 
            err_msg = err_msg[0 : -2 ] + ' were not found in the AR params'
            raise KeyError(err_msg)
            
        if 'results' not in self.jobj:
            return 
        
        results = self.jobj['results']
        self.base.results = SimpleNamespace()
        
        err_msg : str = ''
        should_raise : bool = False
        expecteds = ['p', 'mean', 'var', 'phi']
        for expected in expecteds:
            if expected not in results:
                should_raise = True
                err_msg += '\'' + expected + '\', '
            else:
                self.base.results.__dict__[expected] = results[expected]
            
        if should_raise: 
            err_msg = err_msg[0 : -2] + ' were not found in AR results.' 
            raise KeyError(err_msg)
    
    def get_constructor_names(self) -> List[str]:
        """
        Get parameter names for model construction as a list

        Returns
        -------
        None.

        """
    
    def get_constructor_values(self) -> List[str]:
        """
        Get parameter values for model construction as a list

        Returns
        -------
        None.

        """
    
    def get_fitting_names(self) -> List[str]:
        """
        Get parameter names for model fitting as a list

        Returns
        -------
        None.

        """
    
    def get_fitting_values(self) -> List[str]:
        """
        Get parameter values for model fitting as a list

        Returns
        -------
        None.

        """
    
    def get_prediction_names(self) -> List[str]:
        """
        Get parameter names for model predictions as a list

        Returns
        -------
        None.

        """
    
    def get_prediction_values(self) -> List[str]:
        """
        Get parameter values for model fitting as a list

        Returns
        -------
        None.

        """
        
        # TODO call class _exec()
        # TODO call class _predict()

    
    def __str__(self): 
        return str(self.jobj)

        
class Arima(Model):
    pass 

class AutoArima(Model):
    pass 

class Sarima(Model):
    pass 

class Sarimax(Model):
    pass 

def main() -> int:
    # json_str = '{ "params" : {"L" : 5, "N" : 10, "method" : 2, "optmethod" : 4}}'
    json_str = '{ "params" : {"N" : 10, "method" : 2, "optmethod" : 4}}'
    ar = Ar(json_str)
    
    print(str(ar))
    
    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit(main())