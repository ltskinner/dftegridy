
from . import DateDataUnit


DATE_DAY = 'date_day'

class DateDay(DateDataUnit):
    def profile(self, data):
        '''Only care its within bounds'''
        return {}

    def verify(self, data, profile):
        error_reports = []
        
        range_min, range_max = 1, 31
        range_report = self._verify_range(data, range_min, range_max)
        error_reports.extend(range_report)

        return error_reports
