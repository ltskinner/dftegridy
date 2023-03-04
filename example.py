
import numpy as np
import pandas as pd

from datetime import datetime

import dftegridy


def build_profile(dfid_profile_path):
    datetime_now = datetime.now()
    original_df = pd.DataFrame({
        'record_id': [1, 2, 3, 4, 5],
        'name': ['Joe', 'John', 'David', 'Brett', 'Richard'],
        'occupation': ['Carpenter', 'Carpenter', 'Surveyor', 'Driver', 'Mechanic'],
        'work_hours_per_week': [25, 60, 100, 70, 65],
        
        'yyyymm': [202001, 202005, 202002, 202004, 202009],
        'yyyyqq': [202001, 202002, 202001, 202002, 202003],
        'yyyyqq2': ['2020q1', '2020q2', '2020q1', '2020q2', '2020q3'],

        'year': [2020, 2020, 2020, 2020, 2020],
        'description': ['Excellent carpenter', '', '', 'Drives fast', ''],
        'quarter': ['Quarter 1', 'Quarter 2', 'Quarter 1', 'Quarter 2', 'Quarter 3'],
        'month_numeric': ['1', '5', '2', '4', '9'],
        'Month': ['January', 'May', 'February', 'April', 'September'],
        'Mon': ['Jan', 'May', 'Feb', 'Apr', 'Sep'],
        'month': ['january', 'may', 'february', 'april', 'september'],
        'mon': ['jan', 'may', 'feb', 'apr', 'sep'],
        'datetime': [datetime_now, datetime_now, datetime_now, datetime_now, datetime_now],
        'pattern': ['2020-01-01', '2020-05-01', '2020-02-01', '2020-04-01', '2020-09-01'],
        'week0': [1, 35, 6, 20, 42],
        'week1': ['1', '35', '6', '20', '42'],
        'day': [1, 1, 1, 1, 1],
    })

    # cant save this as json, better to have as str
    dunit_config = {
        'record_id': dftegridy.dunits.ID_UNIQUE,
        'name': dftegridy.dunits.LABEL,
        'occupation': dftegridy.dunits.CATEGORICAL,
        'work_hours_per_week': dftegridy.dunits.MEASURE,

        'yyyymm': dftegridy.dunits.DATE_YYYYMM,
        'yyyyqq': dftegridy.dunits.DATE_YYYYQQ,
        'yyyyqq2': dftegridy.dunits.DATE_YYYYQQ,

        'year': dftegridy.dunits.DATE_YEAR,
        'description': dftegridy.dunits.FREE_TEXT,
        'quarter': dftegridy.dunits.DATE_QUARTER,
        'month_numeric': dftegridy.dunits.DATE_MONTH_NUMERIC,
        'Month': dftegridy.dunits.DATE_MONTH_NAME,
        'Mon': dftegridy.dunits.DATE_MONTH_NAME,
        'month': dftegridy.dunits.DATE_MONTH_NAME,
        'mon': dftegridy.dunits.DATE_MONTH_NAME,
        'datetime': dftegridy.dunits.DATE_DATETIME,
        'pattern': dftegridy.dunits.DATE_PATTERN,
        'week0': dftegridy.dunits.DATE_WEEK_0_START,
        'week1': dftegridy.dunits.DATE_WEEK_1_START,
        'day': dftegridy.dunits.DATE_DAY,
    }

    dfid = dftegridy.DFID(dunit_config=dunit_config)
    dfid.profile(original_df)
    dfid.print_profile()
    dfid.save_profile(dfid_profile_path)


def verify_profile(dfid_profile_path):

    datetime_now = datetime.now()
    compare_df = pd.DataFrame({
        'random_new_col': ['something', 'anotherthing'],
        'record_id': [6, 7],
        'name': ['Paul', 'Jacob'],
        'occupation': ['Driver', 'Technician'],
        'work_hours_per_week': [168, 45],

        'yyyymm': [302104, 202012],
        'yyyyqq': [302102, 202005],
        'yyyyqq2': ['3021q2', '2020Q5'],

        'year': [2021, np.nan],
        'quarter': ['Quarter 4', 'Q4'],
        'month_numeric': ['4', '12'],
        'Month': ['April', 'December'],
        'Mon': ['Apr', 'Dec'],
        'month': ['april', 'december'],
        'mon': ['apr', 'dec'],
        'datetime': [datetime_now, datetime_now],
        'pattern': ['2020-04-01', '1/12/2020'],
        'week0': [20, 55],
        'week1': ['20', '55'],
        'day': [1, 1],
    })


    dfid = dftegridy.DFID()
    dfid.load_profile(dfid_profile_path)
    dfid.print_profile()

    dfid.verify(compare_df, skip_unverified=False)
    print('\n')
    dfid.print_verification_report()


if __name__ == '__main__':

    dfid_profile_path = './example_dfid_profile.yaml'
    build_profile(dfid_profile_path)

    print('\n\nVerifying new DF\n\n')

    verify_profile(dfid_profile_path)
