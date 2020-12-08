
import pytest

import numpy as np
import pandas as pd

from dftegridy.dunits.id import (
    ID, IdUnique,
    ID_UNIQUE, ID_REUSED
)


def test_ensure_correct_names():
    assert ID_UNIQUE == 'id_unique'
    assert ID_REUSED == 'id_reused'


def test__check_na_pass():
    dunit = ID('column')
    data = pd.Series([1, 2, 3])

    _ = dunit._check_na(data)

def test__check_na_fail():
    dunit = ID('column')
    data = pd.Series([1, 2, np.nan])

    with pytest.raises(Exception):
        _ = dunit._check_na(data)

def test_id_profile():
    dunit = ID('column')
    data = pd.Series([1, 2, 3])

    expected = {
        'count': data.shape[0]
    }
    result = dunit.profile(data)
    assert result == expected

def test_id_verify_pass():
    dunit = ID('column')
    profile = {
        'count': 5,
    }

    data = pd.Series([1, 2, 3, 4, 5, 6])

    expected = []

    result = dunit.verify(data, profile)
    
    assert result == expected

def test_id_verify_fail():
    dunit = ID('column')
    profile = {
        'count': 2,
    }

    data = pd.Series([1, 2, 3, 4, 5, 6])

    result = dunit.verify(data, profile)
    assert len(result) == 1
    

def test__check_unique_pass():
    dunit = IdUnique('column')
    data = pd.Series([1, 2, 3])

    _ = dunit._check_unique(data)

def test__check_unique_fail():
    dunit = IdUnique('column')
    data = pd.Series([1, 2, 2])

    with pytest.raises(Exception):
        _ = dunit._check_unique(data)

def test_id_unique_verify_pass():
    dunit = IdUnique('column')
    data = pd.Series([1, 2, 3, 4, 5, 6])

    profile = {
        'count': 5
    }

    expected = []
    result = dunit.verify(data, profile)
    assert result == expected

def test_id_unique_verify_fail():
    dunit = IdUnique('column')
    data = pd.Series([1, 2, 3, 4, 5, 5])

    profile = {
        'count': 2
    }

    result = dunit.verify(data, profile)
    assert len(result) == 2
