
import pandas as pd

from .categorical import Categorical


DATE_MONTH_NUMERIC = 'date_month_numeric'

class DateMonthNumeric(Categorical):
    def _profile_mm(self, data):
        '''options:
            [1, 2, 3, ..., 12],
            ['1', '2', ..., '12'],
        '''

        try:
            data.dropna().astype(int)
        except ValueError:
            print(data.value_counts())
            msg = '\n'.join([
                'Unable to convert data into int format',
                'If your data uses month names, like `Jan` or `August`, please use the `DATE_MONTH_NAME` dunit'
            ])
            raise ValueError(msg)

        start_month = 1
        num_months = 12
        end_month = start_month + num_months
        values = pd.Series([i for i in range(start_month, end_month)])
        values = values.astype(data.dtype)
        return self._profile_categorical(values)
    
    def profile(self, data):
        # wrapper to multi-inheritance exposed self._profile_mm()
        return self._profile_mm(data)

    def _verify_mm(self, data, profile):
        # Need to convert to int b/c thats what `DATE_MONTH_NUMERIC`
        # saves the values as
        data = data.dropna().astype(int)
        return self._verify_categorical(data, profile)

    def verify(self, data, profile):
        # wrapper to multi-inheritance exposed self._verify_mm()
        return self._verify_mm(data, profile)
