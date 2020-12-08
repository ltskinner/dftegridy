
import pytest

import numpy as np
import pandas as pd

from dftegridy.dunits.categorical import (
    CATEGORICAL, Categorical
)


def test_ensure_correct_names():
    assert CATEGORICAL == 'categorical'


def test__profile_categorical():
    dunit = Categorical('column')

    data = pd.Series(['hammer', 'nail', 'saw', 'hammer', np.nan])
    expected = {
        'values': ['hammer', 'nail', 'saw']
    }
    
    result = dunit._profile_categorical(data)
    assert result == expected

def test__verify_categorical_pass():
    dunit = Categorical('column')
    data = pd.Series(['hammer', 'nail', 'saw', 'saw'])
    
    profile = {
        'values': ['hammer', 'nail', 'saw'],
        'hasna': False
    }

    expected = []
    result = dunit._verify_categorical(data, profile)
    assert result == expected


def test__verify_categorical_fail():
    dunit = Categorical('column')
    data = pd.Series(['hammer', 'nail', 'drill', np.nan])
    
    profile = {
        'values': ['hammer', 'nail', 'saw'],
        'hasna': False
    }

    result = dunit._verify_categorical(data, profile)
    assert len(result) == 2
