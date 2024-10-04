'''
Module containing tests for the Fitter class
'''

import tnpcal.test_utilities as tut

from tnpcal.fitter         import Fitter

def test_simple():
    '''
    Simplest test of Fitter class
    '''
    df  = tut.get_data()
    mod = tut.get_model()
    cfg = tut.get_config() 

    obj = Fitter(data=df, model=mod, cfg=cfg)
    obj.run()
