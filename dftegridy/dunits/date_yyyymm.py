
from . import DateYYYYXXDataUnit
from .date_month_numeric import DateMonthNumeric


DATE_YYYYMM = 'date_yyyymm'

class DateYYYYMM(DateYYYYXXDataUnit, DateMonthNumeric):
    def profile(self, data):
        yyyy_series, mm_series = self._split_yyyy_xx(data)

        yyyy_profile = self._profile_yyyy(yyyy_series)
        mm_profile = self._profile_mm(mm_series)
        combined_profile = {**yyyy_profile, **mm_profile}
        return combined_profile

    def verify(self, data, profile):
        # TODO: may want to split and profile on year and month separately...
        error_reports = []

        yyyy_series, mm_series = self._split_yyyy_xx(data)

        yyyy_report = self._verify_yyyy(yyyy_series, profile)
        mm_report = self._verify_mm(mm_series, profile)
        error_reports.extend(yyyy_report)
        error_reports.extend(mm_report)

        return error_reports
