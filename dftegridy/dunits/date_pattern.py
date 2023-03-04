
from . import DataUnit
from . import dateinfer


DATE_PATTERN = 'date_pattern'

class DatePattern(DataUnit):
    def profile(self, data):
        try:
            pattern = dateinfer.infer(data)
        except TypeError:
            msg = '\n'.join([
                f'Date format appears to be `datetime` aka `{data.dtype}`',
                f'--> Please use the `DATE_DATETIME` dunit instead',
                f'or',
                f'If you do intend to use a string pattern, please convert the data into something like',
                f"- ['2020-01-02', ...]",
                f"- ['1/2/2020', ...]",
                f"- etc...",
            ])
            raise TypeError(msg)
        
        profile = {
            'pattern': pattern
        }
        return profile

    def verify(self, data, profile):
        expected_pattern = profile['pattern']

        broken_patterns = []
        dates_to_check = data.unique()  # unique to speedup
        for date in dates_to_check:
            actual_pattern =  dateinfer.infer([date])
            if actual_pattern != expected_pattern:
                broken_patterns.append(actual_pattern)

        error_reports = []
        if len(broken_patterns) > 0:
            broken_msg = ''
            for broken in broken_patterns:
                broken_msg = f'    - {broken}\n'
            msg = '\n'.join([
                f'Date patterns not matching expected `{expected_pattern}`',
                broken_msg
            ])
            error = {
                'level': 'critical',
                'msg': msg
            }
            error_reports.append(error)

        return error_reports
