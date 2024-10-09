'''
Module containing utility functions needed by unit tests
'''

import os
from dataclasses import dataclass
from importlib.resources import files

import yaml
import numpy
import ROOT
import zfit
import pandas as pnd

from dmu.logging.log_store import LogStore

log = LogStore.add_logger('tnpcal:test_utilities')
#------------------------------------------------------
@dataclass
class Data:
    '''
    Class used to hold shared data
    '''
    obs = zfit.Space('mass', limits=(5000, 6000))
#------------------------------------------------------
def get_model(kind = 'simple', obs : zfit.Space | None = None):
    '''
    kind (str) : type of model, by default simple = signal (gauss) + background (exp)

    Returns zfit model
    '''

    nsg = zfit.Parameter('nsg', 1000, 0, 1000000)
    nbk = zfit.Parameter('nbk', 1000, 0, 1000000)
    obs = Data.obs if obs is None else obs
    pdf = None

    if kind == 'simple':
        mu  = zfit.Parameter('mu',  5280, 5000, 5400)
        sg  = zfit.Parameter('sg',    30,   20,   50)
        sig = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg)
        sig = sig.create_extended(nsg, name = 'Signal')

        lam = zfit.Parameter('lam', -0.001, -0.1, 0.0)
        bkg = zfit.pdf.Exponential(lam=lam, obs=obs)
        bkg = bkg.create_extended(nbk, name = 'Background')

        pdf = zfit.pdf.SumPDF([sig, bkg])
    else:
        log.error(f'Invalid kind: {kind}')
        raise ValueError

    return pdf
#------------------------------------------------------
def _get_purities(arr_sig, arr_bkg):
    '''
    Will return tuple of arrays with
    signal  (close to 1)
    and
    background (close to 0)
    purities
    '''

    arr_prs = numpy.random.normal(loc=1, scale=0.3, size=arr_sig.size)
    arr_prb = numpy.random.normal(loc=0, scale=0.3, size=arr_bkg.size)

    return arr_prs, arr_prb
#------------------------------------------------------
def _get_targets(arr_sig, arr_bkg):
    '''
    Returns touple of arrays with

    signal (uniform between 0 and 1)
    and
    background (non-uniform, shape does not matter)

    distributions of target variable whose efficiency will need to be calculated
    '''

    arr_tgs = numpy.random.uniform(low=0, high=1, size=arr_sig.size)
    arr_tgb = numpy.random.normal(loc=0, scale=0.8, size=arr_bkg.size)

    return arr_tgs, arr_tgb
#------------------------------------------------------
def get_data(kind = 'simple', obs : zfit.Space | None = None):
    '''
    kind (str) : Type of model used to build this dataset, default simple
    obs  (zfi.Space) : Observable, if not passed, will pick default

    Returns pandas dataframe with "mass, purity, quantity" columns
    '''
    # pylint: disable=too-many-locals

    model = get_model(kind=kind, obs=obs)

    [pdf_sig, pdf_bkg] = model.pdfs

    sam_sig = pdf_sig.create_sampler(n=20_000)
    sam_bkg = pdf_bkg.create_sampler(n=80_000)

    arr_sig = sam_sig.numpy().flatten()
    arr_bkg = sam_bkg.numpy().flatten()

    arr_prs, arr_prb = _get_purities(arr_sig, arr_bkg)
    arr_trs, arr_trb = _get_targets(arr_sig, arr_bkg)
    arr_bns, arr_bnb = _get_targets(arr_sig, arr_bkg)

    arr_mas = numpy.concatenate([arr_sig, arr_bkg])
    arr_pur = numpy.concatenate([arr_prs, arr_prb])
    arr_tgt = numpy.concatenate([arr_trs, arr_trb])
    arr_bin = numpy.concatenate([arr_bns, arr_bnb])

    d_data  = {'mass' : arr_mas, 'purity' : arr_pur, 'target' : arr_tgt, 'var_bin' : arr_bin}

    return pnd.DataFrame(d_data)
#------------------------------------------------------
def get_config():
    '''
    Will load config from YAML file and return dictionary
    '''
    cfg_path = files('tnpcal_data').joinpath('tests/fitter_simple.yaml')
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f'Cannot find: {cfg_path}')

    with open(cfg_path, encoding='utf-8') as ifile:
        cfg = yaml.safe_load(ifile)

        return cfg
#------------------------------------------------------
