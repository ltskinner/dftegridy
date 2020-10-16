
import pytest

from dftegridy import DFID


def test__confirm_dunit_config_pass():
    dfid = DFID(dunit_config={})

    exepcted = True
    result = dfid._confirm_dunit_config(dfid.dunit_config)
    assert exepcted == result


def test__confirm_dunit_config_fail():
    dfid = DFID()

    with pytest.raises(Exception):
        _ = dfid._confirm_dunit_config(dfid.dunit_config)


'''
def test_save_dunit_config():
    pass

def test_load_dunit_config():
    pass


def test__clean_dict_structure():
    pass

def test_save_profile():
    pass

def test_load_profile():
    pass


# -------- profile
def test_profile():
    pass


# -------- verify

def test__verify_no_extra_cols():
    pass
def test__verify_has_expected_cols():
    pass
def test__verify_cols_present():
    pass
def test__verify_cols_order():
    pass
def test__verify_columns():
    pass
def test_verify():
    pass
'''
