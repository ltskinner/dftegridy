
import pytest

import numpy as np
import pandas as pd
from datetime import datetime

from dftegrity.dunits.abstract_dunit import (
    DataUnit,
    NumericDataUnit,
    DateDataUnit
)

'''
def test_verify_dtype():
    pass

def test_verify_na():
    pass

def test_verify_min():
    pass

def test_verify_max():
    pass
'''

def test__convert_str_to_int_str():
    dunit = DateDataUnit('column')

    data = pd.Series(['1', '2', '3'])
    expected = pd.Series([1, 2, 3])

    result = dunit._convert_str_to_int(data)
    assert expected.tolist() == result.tolist()

def test__convert_str_to_int_int():
    dunit = DateDataUnit('column')

    data = pd.Series([1, 2, 3])
    expected = pd.Series([1, 2, 3])

    result = dunit._convert_str_to_int(data)
    assert expected.tolist() == result.tolist()

def test__convert_str_to_int_float():
    dunit = DateDataUnit('column')

    data = pd.Series([1, 2, 3, np.nan])
    expected = pd.Series([1, 2, 3])

    result = dunit._convert_str_to_int(data)
    assert expected.tolist() == result.tolist()


def test__convert_str_to_int_fail():
    dunit = DateDataUnit('column')


    data = pd.Series([datetime.now(), {}, []])
    with pytest.raises(Exception):
        _ = dunit._convert_str_to_int(data)


'''
def test__verify_range():
    pass
'''
