
import numpy as np


DATA_UNIT = 'data_unit'

class DataUnit(object):
    def __init__(self, column):
        self.column = column

    def profile(self, df):
        raise NotImplementedError

    def verify(self, df):
        raise NotImplementedError

    @staticmethod
    def verify_dtype(data, profile):
        expected = profile['dtype']
        actual = data.dtype

        error_reports = []
        if expected != actual:
            error = {
                'level': 'critical',
                'msg': f'dtype error --> actual `{actual}` != expected `{expected}`'
            }
            error_reports.append(error)

        return error_reports

    @staticmethod
    def verify_na(data, profile):
        error_reports = []
        if data.hasnans:
            if not profile['hasna']:
                error = {
                    'level': 'warning',
                    'msg': f'NaN error --> contains unexpected nan values'
                }
                error_reports.append(error)

        return error_reports


class NumericDataUnit(DataUnit):
    @staticmethod
    def verify_min(actual_min, expected_min, display_name='min'):
        CHANGE_THRESHOLD = .2
        expected_min_threshold = expected_min - (expected_min * CHANGE_THRESHOLD)

        error_reports = []
        if actual_min < expected_min_threshold:
            clean_min_threshold = CHANGE_THRESHOLD * 100
            msg = f'new {display_name} value `{actual_min}` below tolerable min of `{expected_min_threshold}` at {clean_min_threshold}%'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)
    
        return error_reports

    @staticmethod
    def verify_max(actual_max, expected_max, display_name='max'):
        CHANGE_THRESHOLD = .2
        expected_max_threshold = expected_max + (expected_max * CHANGE_THRESHOLD)

        error_reports = []
        if actual_max > expected_max_threshold:
            clean_max_threshold = CHANGE_THRESHOLD * 100
            msg = f'new {display_name} value `{actual_max}` above tolerable max of `{expected_max_threshold}` at {clean_max_threshold}%'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)

        return error_reports


class DateDataUnit(NumericDataUnit):
    @staticmethod
    def _convert_str_to_int(data):
        # tested
        if data.dtype == np.object:
            #raw_dtype = np.object
            numeric_data = data.astype(np.int64)
        elif data.dtype == np.int64:
            #raw_dtype = np.int64
            numeric_data = data
        elif data.dtype == np.float:
            numeric_data = data.dropna().astype(np.int64)
        else:
            raise ValueError(f'dtype neither object nor int64: `{data.dtype}`')

        return numeric_data

    @staticmethod
    def _verify_range(data, range_min, range_max):
        expected_values = [
            i for i in range(range_min, range_max + 1)
        ]
        out_of_bounds_values = []
        for value in data.dropna().unique():
            if int(value) not in expected_values:
                out_of_bounds_values.append(value)


        error_reports = []
        if len(out_of_bounds_values) > 0:
            list_values = ',\n    '.join([
                repr(i) for i in out_of_bounds_values
            ])
            list_msg = f'[\n    {list_values}\n]'
            msg = f'Out of bounds values:\n{list_msg}'
            error = {
                'level': 'critical',
                'msg': msg
            }
            error_reports.append(error)

        return error_reports
