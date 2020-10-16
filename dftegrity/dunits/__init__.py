# 
from .abstract_dunit import (
    DataUnit, NumericDataUnit, DateDataUnit
)
from .abstract_multi_dunit import DateYYYYXXDataUnit
from . import dateinfer

# Format is as follows, reference DESIGN.md for justification:
# from .module import CLASSNAME_UNIQUE_KEY, ClassName
from .id import ID_UNIQUE, IdUnique
from .id import ID_REUSED, IdReused

from .label import LABEL, Label
from .free_text import FREE_TEXT, FreeText

from .categorical import CATEGORICAL, Categorical
from .measure import MEASURE, Measure

from .date_datetime import DATE_DATETIME, DateDatetime
from .date_pattern import DATE_PATTERN, DatePattern

from .date_yyyymm import DATE_YYYYMM, DateYYYYMM
from .date_yyyyqq import DATE_YYYYQQ, DateYYYYQQ

from .date_year import DATE_YEAR, DateYear
from .date_quarter import DATE_QUARTER, DateQuarter
from .date_month_numeric import DATE_MONTH_NUMERIC, DateMonthNumeric
from .date_month_name import DATE_MONTH_NAME, DateMonthName

from .date_week_0_start import DATE_WEEK_0_START, DateWeek0Start
from .date_week_1_start import DATE_WEEK_1_START, DateWeek1Start
from .date_day import DATE_DAY, DateDay


UNVERIFIED = 'UNVERIFIED'  # unverified key
registry = {
    ID_UNIQUE: IdUnique,
    ID_REUSED: IdReused,

    LABEL: Label,
    FREE_TEXT: FreeText,

    CATEGORICAL: Categorical,
    MEASURE: Measure,

    DATE_DATETIME: DateDatetime,
    DATE_PATTERN: DatePattern,

    DATE_YYYYMM: DateYYYYMM,
    DATE_YYYYQQ: DateYYYYQQ,

    DATE_YEAR: DateYear,
    DATE_QUARTER: DateQuarter,
    DATE_MONTH_NUMERIC: DateMonthNumeric,
    DATE_MONTH_NAME: DateMonthName,

    DATE_WEEK_0_START: DateWeek0Start,
    DATE_WEEK_1_START: DateWeek1Start,
    DATE_DAY: DateDay,
}


def get_dunit_obj(dunit_name, column_name):
    if dunit_name not in registry.keys():
        msg = f'Specified dunit `{dunit_name}` does not exist - please check name'
        raise ValueError(msg)

    dunit_class = registry[dunit_name]
    dunit_obj = dunit_class(column_name)

    return dunit_obj
