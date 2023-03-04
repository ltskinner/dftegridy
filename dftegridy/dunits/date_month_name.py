
import pandas as pd

from . import Categorical


DATE_MONTH_NAME = 'date_month_name'

class DateMonthName(Categorical):
    @staticmethod
    def _get_month_base_values():
        values = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]
        return values

    def _get_month_Month(self):
        base_values = self._get_month_base_values()
        values = base_values  # keep form
        return values

    def _get_month_Mon(self):
        base_values = self._get_month_base_values()
        values = [
            month[:3] for month in base_values
        ]
        return values

    def _get_month_month(self):
        base_values = self._get_month_base_values()
        values = [
            month.lower() for month in base_values
        ]
        return values

    def _get_month_mon(self):
        base_values = self._get_month_base_values()
        values = [
            month.lower()[:3] for month in base_values
        ]
        return values

    def _get_month_values(self, data):
        values = data.unique().tolist()

        month_Month = self._get_month_Month()
        month_Mon = self._get_month_Mon()

        month_month = self._get_month_month()
        month_mon =  self._get_month_mon()

        match_dict = {
            'Month': {
                'count': 0,
                'values': month_Month,
            },
            'Mon': {
                'count': 0,
                'values': month_Mon,
            },
            'month': {
                'count': 0,
                'values': month_month,
            },
            'mon': {
                'count': 0,
                'values': month_mon,
            },
        }
        for value in values:
            if value.lower() == 'may':
                # not checking bc multi match
                continue

            if value in month_Month:
                match_dict['Month']['count'] += 1

            if value in month_Mon:
                match_dict['Mon']['count'] += 1

            if value in month_month:
                match_dict['month']['count'] += 1

            if value in month_mon:
                match_dict['mon']['count'] += 1

        max_match = 0
        max_convention = None

        for key, value in match_dict.items():
            count = value['count']
            if count > max_match:
                max_match = count
                max_convention = key

        if max_convention is None:
            month_values = None
        else:
            month_values = pd.Series(match_dict[max_convention]['values'])

        return month_values

    def profile(self, data):
        conventions = '''
        Accepted conventions include:
            ['jan', ..., 'mar', ...],        # short, lower
            ['january', ..., 'march', ...],  # full name, lowercase
            ['Jan', 'Feb', ...],             # short, upper
            ['January', ..., 'December'],    # full, upper
        
        If data not in one of these recognized formats, please:
            - convert to recognized format (str or numeric)
            or
            - set column dunit to `UNVERIFIED`
        '''

        month_values = self._get_month_values(data)
        if month_values is None:
            msg = f'Unable to match month naming convention\n{conventions}'
            raise ValueError(msg)

        # asymetric non-categorical to keep month order for
        # human readbility in the tegridy.yaml file
        values = month_values.dropna().unique().tolist()
        profile = {
            'values': values
        }
        return profile
