# dftegrity

Ensure your dataframes have some 'tegrity

## 🚧 UNDER CONSTRUCTION 🚧

There are likely some debug print statements as well as unfinalized data structures, so if any bugs arise please be understanding

## Contributions

* Please extend the abstract `DataUnit` class for any new data types
* For data unit types that dont fall into a grouping of the existing dunit modules, please make a new file. Organization is important and minimizes merge conflicts

## Tests

## License

Inside `dftegrity.dunits` there is a subpackage called `dateinfer`

**This package was not created by me**, it was created by **@jeffreystar** and source can be found at [https://github.com/jeffreystarr/dateinfer](https://github.com/jeffreystarr/dateinfer)

The reason this package is embedded as source instead of being sourced from PyPi is because there are early version python relative imports that make the package **unusable in its distributed state**

**The only modifications to the version here are the relative imports have been updated - all credit for the package goes to @jeffreystar**
