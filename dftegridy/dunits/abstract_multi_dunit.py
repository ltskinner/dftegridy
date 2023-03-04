# module required to deal with import order

import pandas as pd

from .abstract_dunit import DateDataUnit
from .categorical import Categorical


class DateYYYYXXDataUnit(DateDataUnit, Categorical):
    '''Gives access to:
        - DateDataUnit._convert_str_to_int(data)
        - Categorical._verify_categorical(data, profile)
    '''

    def _profile_yyyy(self, data):
        numeric_data = self._convert_str_to_int(data)

        data_min = numeric_data.min()
        data_max = numeric_data.max()
        
        profile = {
            'min': data_min,
            'max': data_max,
        }
        return profile

    @staticmethod
    def _split_yyyy_xx(data):
        str_data = data.unique().astype(str)

        yyyy_list = []
        xx_list = []
        MIN_LEN_OF_YYYY_XX = 5
        for value in str_data:
            num_chars = len(value)
            if num_chars < MIN_LEN_OF_YYYY_XX:
                raise ValueError(f'`{value}` doesnt match `YYYYXX` pattern')

            yyyy = value[:4]
            yyyy_list.append(yyyy)

            xx = value[4:]
            xx_list.append(xx)

        yyyy_series = pd.Series(yyyy_list)
        xx_series = pd.Series(xx_list)

        return yyyy_series, xx_series

    def _verify_yyyy(self, data, profile):
        error_reports = []

        numeric_data = self._convert_str_to_int(data)
        # self.________(actual_X,   expected_X)
        min_report_min = self.verify_min(numeric_data.min(), profile['min'], display_name='yyyy')
        max_report_max = self.verify_max(numeric_data.max(), profile['max'], display_name='yyyy')
        error_reports.extend(min_report_min)
        error_reports.extend(max_report_max)

        return error_reports
