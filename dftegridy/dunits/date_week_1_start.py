
from . import DateDataUnit


DATE_WEEK_1_START = 'date_week_1_start'

class DateWeek1Start(DateDataUnit):
    def profile(self, data):
        '''Only care its within bounds'''
        return {}

    def verify(self, data, profile):
        error_reports = []
        
        range_min, range_max = 1, 52
        range_report = self._verify_range(data, range_min, range_max)
        error_reports.extend(range_report)
        
        return error_reports
