'''
Module used to hold tests for EfficiencyCalculator
'''
import os
from importlib.resources import files

import yaml
import numpy
import pytest

from dmu.logging.log_store        import LogStore
from ROOT                         import RDF
from tnpcal.efficiency_calculator import EfficiencyCalculator

# ------------------------------------------------------
@pytest.fixture
def _initialize():
    LogStore.set_level('tnpcal:efficiency_calculator', 10)
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
def test_set_yields():
    '''
    Simple test passing yields
    '''
    d_fit   = _load_yaml('tests/efficiency_calculator_simple.yaml')
    eff_cal = EfficiencyCalculator()

    for cut, d_yld in d_fit.items():
        eff_cal[cut] = d_yld
# ------------------------------------------------------
def test_serialize():
    '''
    Test serialization
    '''
    d_fit   = _load_yaml('tests/efficiency_calculator_simple.yaml')
    eff_cal = EfficiencyCalculator()

    for cut, d_yld in d_fit.items():
        eff_cal[cut] = d_yld

    out_dir = _make_out_dir('serialize')
    eff_cal.save(path = f'{out_dir}/efficiencies.json')
# ------------------------------------------------------
def test_load():
    '''
    Will test creating an EfficiencyCalculator object from JSON
    '''
    d_fit     = _load_yaml('tests/efficiency_calculator_simple.yaml')
    eff_cal_1 = EfficiencyCalculator()

    for cut, d_yld in d_fit.items():
        eff_cal_1[cut] = d_yld

    out_dir   = _make_out_dir('load')
    json_path = f'{out_dir}/efficiencies.json'

    eff_cal_1.save(path = json_path)

    eff_cal_2 = EfficiencyCalculator.from_json(json_path)

    assert eff_cal_1 == eff_cal_2
# ------------------------------------------------------
def test_read():
    '''
    Will test reading of efficiencies
    '''

    d_fit   = _load_yaml('tests/efficiency_calculator_simple.yaml')
    eff_cal = EfficiencyCalculator()

    for cut, d_yld in d_fit.items():
        eff_cal[cut] = d_yld

    d_data = {'x' : numpy.random.uniform(0, 5, 1000)}

    rdf     = RDF.FromNumpy(d_data)
    arr_eff = eff_cal.read_eff(rdf)
# ------------------------------------------------------
