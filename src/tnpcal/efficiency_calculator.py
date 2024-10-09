'''
Module containing EfficiencyCalculator class
'''

from dmu.logging.log_store import LogStore

log = LogStore.add_logger('tnpcal:efficiency_calculator')
# -----------------------------------------
class EfficiencyCalculator:
    '''
    Class intended to 
    - Hold yields from fits for different bins
    - Serialize this information
    - Offer interface to access efficiencies
    '''
    #--------------------------------------------
    def __init__(self):
        pass
    #--------------------------------------------
    def __setitem__(self, cut : str, d_val : dict):
        '''
        Takes 

        cut (str): String defining bin and 
        d_val (dict): Dictionary with {'pas' : (val, err), 'fal' : (val, err)} info
        '''
    #--------------------------------------------
    def save(self, path : str):
        '''
        Will save yields to JSON
        '''

        log.info(f'Saving to: {path}')
# -----------------------------------------
