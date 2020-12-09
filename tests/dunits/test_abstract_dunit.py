
import pytest

import numpy as np
import pandas as pd
from datetime import datetime

from dftegridy.dunits.abstract_dunit import (
    DataUnit,
    NumericDataUnit,
    DateDataUnit
)


def test_verify_dtype():
    dunit = DataUnit('column')
    cases = [
        (pd.Series([1]), {'dtype': 'int64'}, 0),
        (pd.Series(['test']), {'dtype': 'object'}, 0),
        (pd.Series([1.0]), {'dtype': 'float64'}, 0),
        (pd.Series(['1']), {'dtype': 'float64'}, 1),
    ]
    for data, profile, num_errors in cases:
        result = dunit.verify_dtype(data, profile)
        assert len(result) == num_errors


def test_verify_na():
    dunit = DataUnit('column')
    cases = [
        (pd.Series([1]), {'hasna': False}, 0),
        (pd.Series([np.nan]), {'hasna': False}, 1),
        (pd.Series([np.nan]), {'hasna': True}, 0),
    ]
    for data, profile, num_errors in cases:
        result = dunit.verify_na(data, profile)
        assert len(result) == num_errors


def test_verify_min():
    dunit = NumericDataUnit('column')
    cases = [
        (9, 10, 0),
        (0, 10, 1),
    ]
    for actual_min, expected_min, num_errors in cases:
        result = dunit.verify_min(actual_min, expected_min)
        assert len(result) == num_errors

def test_verify_max():
    dunit = NumericDataUnit('column')
    cases = [
        (11, 10, 0),
        (200, 10, 1),
    ]
    for actual_max, expected_max, num_errors in cases:
        result = dunit.verify_max(actual_max, expected_max)
        assert len(result) == num_errors


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


def test__verify_range_pass():
    dunit = DateDataUnit('column')
    
    data = pd.Series([1, 2, 3, 4])
    range_min, range_max = 1, 4

    expected = []
    result = dunit._verify_range(data, range_min, range_max)
    assert result == expected

def test__verify_range_fail():
    dunit = DateDataUnit('column')
    
    data = pd.Series([0, 1, 2, 3, 4])
    range_min, range_max = 1, 4

    result = dunit._verify_range(data, range_min, range_max)
    assert len(result) == 1
