
import numpy as np

from . import DataUnit


class ID(DataUnit):
    '''For the ids, expecting to be a lot of values.
        Main value of this is on .verify()
        b/c of this, only saving metadata
    '''
    @staticmethod
    def _check_na(data):
        msg = '\n'.join([
            'ID series includes na values',
            'dtype ID_XXXXX assumes there are no records with na ID values'
        ])
        assert np.isnan(data).any() == False, msg

    def profile(self, data):
        self._check_na(data)

        count = data.unique().shape[0]
        profile = {
            'count': count
        }
        return profile
    
    def verify(self, data, profile):
        previous_id_count = profile['count']
        current_id_count = data.unique().shape[0]

        # TODO: make settable by the user on init
        GROWTH_THRESHOLD = .2  # 20%
        expected_max_num_ids = previous_id_count + (previous_id_count * GROWTH_THRESHOLD)
        error_reports = []
        if current_id_count > expected_max_num_ids:
            clean_growth_threshold = GROWTH_THRESHOLD * 100
            error = {
                'level': 'info',
                'msg': f'Number of ids has grown more than {clean_growth_threshold}%'
            }
            error_reports.append(error)

        return error_reports


ID_UNIQUE = 'id_unique'

class IdUnique(ID):
    @staticmethod
    def _check_unique(data):
        total_id_count = data.shape[0]
        unique_id_count = data.unique().shape[0]

        msg = '\n'.join([
            f'total_id_count `{total_id_count}` != unique_id_count `{unique_id_count}`',
            f'If this should not be the case, please inspect your data.',
            f'However, if your ids are reused by multiple rows, convert dunit:',
            f'    from `ID_UNIQUE`',
            f'    to `ID_REUSED',
        ])
        assert total_id_count == unique_id_count, msg

    def profile(self, data):
        self._check_unique(data)
        return super().profile(data)

    def verify(self, data, profile):
        error_reports = []
    
        total_id_count = data.shape[0]
        unique_id_count = data.unique().shape[0]
        if total_id_count != unique_id_count:
            error = {
                'level': 'critical',
                'msg': f'Not all IDs are unique'
            }
            error_reports.append(error)
        
        baseline_report = super().verify(data, profile)
        error_reports.extend(baseline_report)

        return error_reports


ID_REUSED = 'id_reused'

class IdReused(ID):
    pass
