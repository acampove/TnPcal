'''
Module containing EfficiencyCalculator class
'''

import os
import json

from dmu.dataframe.dataframe import DataFrame
from dmu.logging.log_store   import LogStore

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
    def _get_cut_expr(self):
        '''
        Return string with expression:

        (flg_1) * eff_1 ...

        such that each flg_i is true if the event is in the satistisfies specific cut
        '''

        l_cut = list(self._d_data)
        l_eff = [ self._get_eff(cut) for cut      in            l_cut ]
        l_exp = [ f'({cut}) * {eff}' for cut, eff in zip(l_cut, l_eff)]

        return ' + '.join(l_exp)
    #--------------------------------------------
    def _get_eff(self, cut : str):
        '''
        Will return efficiency for given cut
        '''

        d_yld = self._d_data[cut]

        pas_val, _ = d_yld['pas']
        fal_val, _ = d_yld['fal']

        eff = pas_val / ( pas_val + fal_val )

        return eff
    #--------------------------------------------
    def read_eff(self, df : DataFrame):
        '''
        Take dmu Dataframe, return numpy array of efficiencies
        '''

        eff_name = 'temporary_column_holding_efficiencies'
        log.debug(f'Using {eff_name} to dump efficiencies')

        cut      = self._get_cut_expr()
        df       = df.define(eff_name, cut)
        arr_eff  = df[eff_name].to_numpy()

        return arr_eff
    #--------------------------------------------
    def save(self, path : str):
        '''
        Will save yields to JSON
        '''

        with open(path, 'w', encoding='utf-8') as ofile:
            json.dump(self._d_data, ofile, indent=4)

        log.info(f'Saving to: {path}')
# -----------------------------------------
