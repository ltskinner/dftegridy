
from . import DateDataUnit


DATE_WEEK_0_START = 'date_week_0_start'

class DateWeek0Start(DateDataUnit):
    def profile(self, data):
        '''Only care its within bounds'''
        return {}

    def verify(self, data, profile):
        error_reports = []
        
        range_min, range_max = 0, 51
        range_report = self._verify_range(data, range_min, range_max)
        error_reports.extend(range_report)
        
        return error_reports
