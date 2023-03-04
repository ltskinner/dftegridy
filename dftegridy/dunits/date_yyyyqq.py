from . import DateYYYYXXDataUnit
from .date_quarter import DateQuarter


DATE_YYYYQQ = 'date_yyyyqq'

class DateYYYYQQ(DateYYYYXXDataUnit, DateQuarter):
    def profile(self, data):
        yyyy_series, qq_series = self._split_yyyy_xx(data)

        yyyy_profile = self._profile_yyyy(yyyy_series)
        qq_profile = self._profile_qq(qq_series)
        combined_profile = {**yyyy_profile, **qq_profile}
        return combined_profile

    def verify(self, data, profile):
        # TODO: may want to split and profile on year and month separately...
        error_reports = []

        yyyy_series, qq_series = self._split_yyyy_xx(data)

        yyyy_report = self._verify_yyyy(yyyy_series, profile)
        qq_report = self._verify_qq(qq_series, profile)
        error_reports.extend(yyyy_report)
        error_reports.extend(qq_report)

        return error_reports
