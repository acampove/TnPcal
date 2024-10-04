'''
Module containing tests for the Fitter class
'''

import tnpcal.test_utilities as tut 

from tnpcal.fitter         import Fitter

def test_simple():
    mod = tut.get_model()
    df  = tut.get_data()

    obj = TnPFitter(data=df, model=mod, cfg=cfg)
    obj.run()

