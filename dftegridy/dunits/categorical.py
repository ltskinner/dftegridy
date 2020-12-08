
import pandas as pd

from . import DataUnit


CATEGORICAL = 'categorical'

class Categorical(DataUnit):
    '''Discrete set of values

    Use for Boolean values as well
        - Not worth dealing with permutations
            - T/F
            - True/False
            - true/false
            - 0/1
    '''
    @staticmethod
    def _profile_categorical(data):
        # tested
        values = sorted(data.dropna().unique().tolist())
        profile = {
            'values': values
        }
        return profile
    
    def profile(self, data):
        # wrapper to multi-inheritance exposed self._profile_categorical()
        return self._profile_categorical(data)

    
    @staticmethod
    def _verify_categorical(data, profile):
        # tested
        expected_values = profile['values']
        actual_values = data.unique().tolist()
        unexpected_values = []
        has_unexpected_na = False
        for value in actual_values:
            if pd.isna(value) and not profile['hasna']:
                has_unexpected_na = True

            if value not in expected_values:
                unexpected_values.append(value)

        unexpected_values = sorted([repr(i) for i in unexpected_values])

        error_reports = []

        if has_unexpected_na:
            msg = f'Found unexpected NaN value'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)

        if len(unexpected_values) > 0:
            list_values = ',\n    '.join(unexpected_values)
            list_msg = f'[\n    {list_values}\n]'
            msg = f'Unexpected categorical values:\n{list_msg}'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)
        
        return error_reports

    def verify(self, data, profile):
        # wrapper to multi-inheritance exposed self._verify_categorical()
        return self._verify_categorical(data, profile)
