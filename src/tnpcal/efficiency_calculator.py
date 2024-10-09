'''
Module containing EfficiencyCalculator class
'''

import os
import json

from dmu.logging.log_store import LogStore

log = LogStore.add_logger('tnpcal:efficiency_calculator')
# -----------------------------------------
class EfficiencyCalculator:
    '''
    Class intended to
    - Hold yields from fits for different bins
    - Serialize this information
    - Offer interface to access efficiencies
    '''
    #--------------------------------------------
    def __init__(self):
        self._d_data : dict = {}
    #--------------------------------------------
    def __setitem__(self, cut : str, d_val : dict):
        '''
        Takes

        cut (str): String defining bin and
        d_val (dict): Dictionary with {'pas' : (val, err), 'fal' : (val, err)} info
        '''

        self._d_data[cut] = d_val
    #--------------------------------------------
    def __eq__(self, other):
        '''
        Two efficiency calculators are equal if their cut - yield dictionaries are equal
        '''
        return self._d_data == other._d_data
    #--------------------------------------------
    @staticmethod
    def from_json(path : str):
        '''
        Will pick path to JSON file and return instance of EfficiencyCalculator
        '''

        if not os.path.isfile(path):
            raise FileNotFoundError(f'Cannot find: {path}')

        with open(path, encoding='utf-8') as ifile:
            d_data = json.loads(ifile.read())

        obj = EfficiencyCalculator()
        for cut, d_yld in d_data.items():
            obj[cut] = d_yld

        return obj
    #--------------------------------------------
    def save(self, path : str):
        '''
        Will save yields to JSON
        '''

        with open(path, 'w', encoding='utf-8') as ofile:
            json.dump(self._d_data, ofile, indent=4)

        log.info(f'Saving to: {path}')
# -----------------------------------------
