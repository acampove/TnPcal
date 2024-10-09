'''
Module used to hold tests for EfficiencyCalculator
'''
import os
from tnpcal.efficiency_calculator import EfficiencyCalculator

# ------------------------------------------------------
def  _make_out_dir(name : str):
    '''
    Will make directory where output of test goes
    '''

    out_dir = f'tests/efficiency_calculator/{name}'
    os.makedirs(out_dir, exist_ok=True)
# ------------------------------------------------------
def test_simple():
    '''
    Simple test for inteface
    '''
    eff_cal          = EfficiencyCalculator()
    eff_cal['x > 0'] = {'pas' : (100, 3), 'fal' : (100, 3)}

    out_dir = _make_out_dir('simple')
    eff_cal.save(path = f'{out_dir}/efficiencies.json')
# ------------------------------------------------------
