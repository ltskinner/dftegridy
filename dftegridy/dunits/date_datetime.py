
from . import DataUnit


DATE_DATETIME = 'date_datetime'

class DateDatetime(DataUnit):
    def profile(self, data):
        '''Only thing we really care about is that its datetime dtype
        '''
        return {}

    def verify(self, data, profile):
        error_reports = []
        return error_reports
