'''
Module containing Fitter class
'''

from zfit.core.basepdf import BasePDF

import pandas as pnd

from dmu.logging.log_store import LogStore

log=LogStore.add_logger('tnpcal:fitter')
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
    def _get_dset(self, df):
        '''
        Takes dataframe and returns tuple of df_pas, df_fal
        with the rows that pas and fail the probe cut
        '''

        cut_pas = self._cfg['selection']['probe']
        cut_fal = f'~({cut_pas})'

        df_pas = df.query(cut_pas)
        df_fal = df.query(cut_fal)

        return df_pas, df_fal
    # ----------------------------------
    def _fit(self, df):
        nentries = len(df)
        log.info(f'Fitting {nentries} entries')

        return 1, 1
    # ----------------------------------
    def run(self):
        '''
        Will start calculation of efficiencies
        '''

        for cut in self._cfg['binning']:
            log.info(f'Fitting for: {cut}')

            df_bin         = self._df.query(cut)
            df_pas, df_fal = self._get_dset(df_bin)

            vpas, epas = self._fit(df_pas)
            vfal, efal = self._fit(df_fal)
#--------------------------------------------
