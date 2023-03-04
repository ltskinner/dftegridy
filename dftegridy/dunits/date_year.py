
from . import DateDataUnit


DATE_YEAR = 'date_year'

class DateYear(DateDataUnit):
    def profile(self, data):
        numeric_data = self._convert_str_to_int(data)

        data_min = numeric_data.min()
        data_max = numeric_data.max()
        
        profile = {
            'min': data_min,
            'max': data_max,
        }
        return profile

    def verify(self, data, profile):
        error_reports = []

        numeric_data = self._convert_str_to_int(data)
        # self.________(actual_X,   expected_X)
        min_report_min = self.verify_min(numeric_data.min(), profile['min'])
        max_report_max = self.verify_max(numeric_data.max(), profile['max'])
        error_reports.extend(min_report_min)
        error_reports.extend(max_report_max)

        return error_reports
