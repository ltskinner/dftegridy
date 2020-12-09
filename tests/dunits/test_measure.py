
import pandas as pd

from dftegridy.dunits.measure import (
    MEASURE, Measure
)


def test_ensure_correct_names():
    assert MEASURE == 'measure'


def test_profile():
    dunit = Measure('column')

    data = pd.Series([0, 1, 2, 3])
    expected = {
        'min': 0,
        'lower_fence_boundary': -1.5,
        'q1': .75,
        'q2': 1.5,
        'q3': 2.25,
        'upper_fence_boundary': 4.5,
        'max': 3,
    }
    
    result = dunit.profile(data)

    assert result == expected

def test_verify_fences_pass():
    dunit = Measure('column')

    data = pd.Series([1, 2])

    profile = {
        'lower_fence_boundary': 0,
        'upper_fence_boundary': 4,
    }
    expected = []
    
    result = dunit.verify_fences(data, profile)
    assert result == expected

def test_verify_fences_fail():
    dunit = Measure('column')

    data = pd.Series([0, 3])

    profile = {
        'lower_fence_boundary': 1,
        'upper_fence_boundary': 2,
    }

    result = dunit.verify_fences(data, profile)
    # error 1: lower fence out of range
    # error 2: upper fence out of range
    assert len(result) == 2

def test_verify_pass():
    dunit = Measure('column')

    data = pd.Series([0, 1, 2, 3])
    profile = {
        'min': 0,
        'lower_fence_boundary': -1.5,
        'q1': .75,
        'q2': 1.5,
        'q3': 2.25,
        'upper_fence_boundary': 4.5,
        'max': 3,
    }
    expected = []
    result = dunit.verify(data, profile)
    assert result == expected

def test_verify_fail():
    dunit = Measure('column')

    data = pd.Series([-10, 10])
    profile = {
        'min': 0,
        'lower_fence_boundary': -1.5,
        'q1': .75,
        'q2': 1.5,
        'q3': 2.25,
        'upper_fence_boundary': 4.5,
        'max': 3,
    }

    result = dunit.verify(data, profile)
    # error 1: lower past previous min
    # error 2: upper past previous max
    # error 3: lower outside of fence
    # error 4: upper outside of fence
    assert len(result) == 4
