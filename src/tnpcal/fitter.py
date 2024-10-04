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
    def _get_tagged_df(self):
        '''
        Will apply tagging cut and return dataframe
        '''

        ntot = len(self._df)
        cut_tag = self._cfg['selection']['tag']
        df_tag  = self._df.query(cut_tag)
        ntag = len(df_tag)

        log.info(f'Tagging cut {cut_tag}')
        log.info(f'{ntot:<30}{"--->":<30}{ntag:<30}')

        return df_tag
    # ----------------------------------
    def run(self):
        '''
        Will start calculation of efficiencies
        '''

        df_tag = self._get_tagged_df()
        for cut in self._cfg['binning']:
            df_bin = df_tag.query(cut)
            nbin   = len(df_bin)

            log.info(f'Fitting {nbin} entries for: {cut}')

            df_pas, df_fal = self._get_dset(df_bin)

            vpas, epas = self._fit(df_pas)
            vfal, efal = self._fit(df_fal)
#--------------------------------------------
