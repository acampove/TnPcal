'''
Module containing Fitter class
'''
import os

import zfit
import numpy
import matplotlib.pyplot as plt

from zfit.core.basepdf import BasePDF
from zfit.result       import FitResult

import pandas as pnd

from zutils.plot           import plot      as zfp
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

        self._min   = zfit.minimize.Minuit()
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
    def _fit(self, df, label : str, index : int):
        '''
        Take dataframe with dataset after full selection
        Extract column with observable
        Fit model and plot fit
        Return tuple with fit yield and error
        '''
        nentries = len(df)
        log.info(f'Fitting {nentries} entries')

        obs_name= self._cfg['observable']['name']
        arr_obs = df[obs_name].to_numpy()
        nll     = zfit.loss.ExtendedUnbinnedNLL(model=self._model, data=arr_obs)
        res     = self._min.minimize(nll)

        error_method = self._cfg['fitting']['error_method']

        self._plot_fit(data=arr_obs, res=res, label=label, index=index)
        res.hesse(method=error_method)
        res.freeze()
        yld = self._get_fit_yield(res = res)

        return yld
    # ----------------------------------
    def _plot_fit(self, data : numpy.ndarray, res : FitResult, label : str, index : int):
        '''
        Will take the data as an arry of observables and the result of the fit
        Will plot and save the result of the fit
        '''
        out_dir = self._cfg['plotting']['out_dir']
        nbins   = self._cfg['plotting']['nbins'  ]
        min_x   = self._cfg['plotting']['min_x'  ]
        max_x   = self._cfg['plotting']['max_x'  ]

        os.makedirs(out_dir, exist_ok=True)

        obj= zfp(data=data, model=self._model, result=res)
        obj.plot(nbins=nbins, plot_range=(min_x, max_x), ext_text=label)

        plt.savefig(f'{out_dir}/fit_{index:03}.png')
    # ----------------------------------
    def _get_tagged_df(self):
        '''
        Will apply tagging cut and return dataframe
        '''

        ntot    = len(self._df)
        cut_tag = self._cfg['selection']['tag']
        df_tag  = self._df.query(cut_tag)
        ntag    = len(df_tag)

        log.info(f'Tagging cut {cut_tag}')
        log.info(f'{ntot:<30}{"--->":<30}{ntag:<30}')

        return df_tag
    # ----------------------------------
    def _get_fit_yield(self, res : FitResult):
        '''
        Takes zfit Fit Result object

        Returns tuple with signal yield and error
        '''
        sig_name = self._cfg['maps']['signal_name']
        d_nsig   = res.params[sig_name]

        val = d_nsig['value']
        err = d_nsig['hesse']['error']

        return val, err
    # ----------------------------------
    def run(self):
        '''
        Will start calculation of efficiencies
        '''
        df_tag = self._get_tagged_df()

        i_fit = 1

        #eff_cal = EffCalculator()
        for cut in self._cfg['binning']:
            df_bin = df_tag.query(cut)
            nbin   = len(df_bin)

            log.info(f'Fitting {nbin} entries for: {cut}')

            df_pas, df_fal = self._get_dset(df_bin)

            pas = self._fit(df_pas, label=f'Pass: {cut}', index=i_fit)
            fal = self._fit(df_fal, label=f'Fail: {cut}', index=i_fit)

            #eff_cal[cut] = {'pas' : pas, 'fal' : fal}

            i_fit     += 1

        #out_dir = self._cfg['maps']['out_dir']
        #eff_cal.save(path = f'{out_dir}/efficiencies.json')
#--------------------------------------------
