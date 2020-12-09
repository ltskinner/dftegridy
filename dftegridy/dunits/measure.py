
import numpy as np
import pandas as pd

from . import NumericDataUnit


MEASURE = 'measure'

class Measure(NumericDataUnit):
    '''Numeric values with some expected range
    '''
    def profile(self, data):
        # 5 number summary
        data_min = data.min()
        q1 = data.quantile(0.25)
        q2 = data.quantile(0.50)
        q3 = data.quantile(0.75)
        data_max = data.max()

        # fences
        iqr = q3 - q1
        lower_fence_boundary = q1 - (1.5 * iqr)
        upper_fence_boundary = q3 + (1.5 * iqr)

        # others
        #data_mean = data.mean()
        #data_std = np.std(data)

        profile = {
            'min': data_min,
            'lower_fence_boundary': lower_fence_boundary,
            'q1': q1,
            'q2': q2,
            'q3': q3,
            'upper_fence_boundary': upper_fence_boundary,
            'max': data_max,
            #'mean': data_mean,
            #'std': data_std,
        }
        return profile

    @staticmethod
    def verify_fences(data, profile):
        data_min = data.min()
        data_max = data.max()

        error_reports = []
        if data_min < profile['lower_fence_boundary']:
            msg = 'New data contains lower boundary outliers'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)

        if data_max > profile['upper_fence_boundary']:
            msg = 'New data contains upper boundary outliers'
            error = {
                'level': 'info',
                'msg': msg
            }
            error_reports.append(error)

        return error_reports

    def verify(self, data, profile):
        # tested
        error_reports = []

        # self.________(actual_X,   expected_X)
        min_report_min = self.verify_min(data.min(), profile['min'])
        max_report_max = self.verify_max(data.max(), profile['max'])
        error_reports.extend(min_report_min)
        error_reports.extend(max_report_max)

        fence_report = self.verify_fences(data, profile)
        error_reports.extend(fence_report)

        '''
        # 12/8/2020 LTS - dont love these, not sure how actually useful they are
        mean_report_min = self.verify_min(data.mean(), profile['mean'], display_name='mean')
        mean_report_max = self.verify_max(data.mean(), profile['mean'], display_name='mean')
        error_reports.extend(mean_report_min)
        error_reports.extend(mean_report_max)
        
        std_report_min = self.verify_min(np.std(data), profile['std'], display_name='std')
        std_report_max = self.verify_max(np.std(data), profile['std'], display_name='std')
        error_reports.extend(std_report_min)
        error_reports.extend(std_report_max)
        '''
        return error_reports
