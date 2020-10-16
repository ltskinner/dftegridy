# Design Decisions

## Why is there no dedicated BOOLEAN value

Boolean values can come in many forms:

* 0,1
* T,F
* True,False

CATEGORICAL will cover these just fine

## Why do YYYYMM and YYYYQQ lead with year

For YYYYMM, when the string or int value is sorted, it gets sorted first by year and then by month

For YYYYQQ, the YYYYqX format is standard in the business world. I dont see any value in leading with the quarter values like Q4YYYY or 4QYYYY for the same sorting reason listed above

**If you feel strongly about having the year trail, please feel free to make a custom `DataUnit`to meet your needs**

## Why dftegrity.dunits.__init__.py uses 'global' variables

The import convention of:

```python
from .module import CLASSNAME_UNIQUE_KEY, ClassName
```

with module.py declarations defined as:

```python
CLASSNAME_UNIQUE_KEY = 'categorical'

class ClassName(DataUnit):
```

Was decided upon for one key reason:

* When saving the `dunit_config`, **string** values can be saved literally into json or yaml files
* This allows a human to:
  * Configure these files manually, and be able to read them
  * Save a pythonically defined `dunit_config`, and be able to interpret what those values are

Furthermore, declaring `CLASSNAME_UNIQUE_KEY` as a top level object, or "first-class object" is no different from the way:

* A module is:
  * imported as `import module`
  * used by `module.XXX`
* A class is:
  * defined as `class Class(object):`
  * accessed by `module.Class`
* A function is:
  * defined as `def function():`
  * accessed by `module.function`

Because these have no expectation of their **definitions being overwritten or updated**, a static variable defined the same way can be used **identically**
