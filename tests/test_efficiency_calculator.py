'''
Module used to hold tests for EfficiencyCalculator
'''
import os
from importlib.resources import files

import yaml
from tnpcal.efficiency_calculator import EfficiencyCalculator

# ------------------------------------------------------
class Data:
    '''
    Class storing shared data for tests
    '''

# ------------------------------------------------------
def  _make_out_dir(name : str):
    '''
    Will make directory where output of test goes
    Return path to directory
    '''

    out_dir = f'tests/efficiency_calculator/{name}'
    os.makedirs(out_dir, exist_ok=True)

    return out_dir
# ------------------------------------------------------
def _load_yaml(path : str):
    '''
    Loads data from yaml file and returns it
    '''
    yaml_path = files('tnpcal_data').joinpath(path)
    yaml_path = str(yaml_path)
    if not os.path.isfile(yaml_path):
        raise ValueError(f'Cannot find: {yaml_path}')

    with open(yaml_path, encoding='utf-8') as ifile:
        data = yaml.safe_load(ifile)

    return data
# ------------------------------------------------------
def test_simple():
    '''
    Simple test for inteface
    '''
    d_fit = _load_yaml('tests/efficiency_calculator_simple.yaml')

    eff_cal          = EfficiencyCalculator()

    for cut, d_yld in d_fit.items():
        eff_cal[cut] = d_yld

    out_dir = _make_out_dir('simple')
    eff_cal.save(path = f'{out_dir}/efficiencies.json')
# ------------------------------------------------------
