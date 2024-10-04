'''
Module containing Fitter class
'''

from zfit.core.basepdf import BasePDF

import pandas as pnd

#--------------------------------------------
class Fitter:
    '''
    Class used to measure efficiency through tag and probe and fits
    '''
    # pylint: disable=too-few-public-methods
    # ----------------------------------
    def __init__(self, data : pnd.DataFrame, model : BasePDF, cfg : dict):
        self._df    = data
        self._model = model
        self._cfg   = cfg
    # ----------------------------------
    def run(self):
        '''
        Will start calculation of efficiencies
        '''

        return
#--------------------------------------------
