
import pandas as pd

from .categorical import Categorical


DATE_QUARTER = 'date_quarter'

class DateQuarter(Categorical):
    @staticmethod
    def _build_quarter_convention(quarter):
        STANDARD_PREFIX_0Q = '0'  # expected 01, 02, 03, 04 values
        number_index = 0
        corrected_quarter_list = []
        for c, q in enumerate(quarter):
            if q.isdigit() and q != STANDARD_PREFIX_0Q:
                number_index = c
            else:
                corrected_quarter_list.append(q)

        quarter_convention = ''.join(corrected_quarter_list)

        quarter_options = []
        # 10/3/2020 LTS - using [1, 2, 3, 4] bc nontechs dont start counting at
        # 0, they start at 1, so expecting data to be 1-4
        for quarter_num in [1, 2, 3, 4]:
            quarter_char_list = list(quarter_convention)

            quarter_char_list.insert(number_index, str(quarter_num))
            reconstructed_quarter = ''.join(quarter_char_list)

            quarter_options.append(reconstructed_quarter)
        
        # sorting in case end up sorting on .verify()
        values = quarter_options
        return values

    def _profile_qq(self, data):
        '''Because quarter, only options really are:
            [1, 2, 3, 4],
            ['1', '2', '3', '4'],
            ['01', '02', '03', '04'],
            ['Q1', 'Q2', 'Q3', 'Q4'],
            ...other string variants...
        
        Just convert to categorical and call it gucci
        
        9/23/2020 LTS - Executive decision to just use existing quarter values
            despite possibility of there only being 1, 2 or 3.
            Best way to handle would be to project the current pattern
        '''

        raw_quarter_values = data.unique().tolist()

        reconstructed_quarter_convention = []
        for quarter in raw_quarter_values:
            values = self._build_quarter_convention(quarter)
            reconstructed_quarter_convention.append(values)

        x = reconstructed_quarter_convention # renaming to short variable name
        all_conventions_equal = x.count(x[0]) == len(x)
        if not all_conventions_equal:
            msg = 'inconsistent naming convention - unable to verify quarters\n'
            msg = msg + str(raw_quarter_values)
            raise ValueError(msg)

        recon_quarter_data = pd.Series(reconstructed_quarter_convention[0])
        recon_quarter_data = recon_quarter_data.astype(data.dtype)
        
        return super().profile(recon_quarter_data)

    def profile(self, data):
        return self._profile_qq(data)

    def _verify_qq(self, data, profile):
        return super().verify(data, profile)

    def verify(self, data, profile):
        return self._verify_qq(data, profile)
