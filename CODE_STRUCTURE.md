# Structure of code


### Module structure

The code contains low-level modules:

- `aquasol.constants` contains data of physical constants used throughout the package, useful functions such as `molar_mass()` and other dicts of charge, dissociation data etc.

- `aquasol.format` gather useful tools for checking (e.g. validity range, correct units etc.) and formatting (e.g. data in the right units).

- `aquasol.formulas` with all raw formulas for the properties of water and solutions

The main modules rely on the above ones to provide higher-level interfaces and user-friendly functions:

- `aquasol.water`

- `aquasol.solutions`

(and to some extent `aquasol.humidity` which has been separated from `aquasol.format` to prevent circular import problems).

The separation of raw formulas into a separate module outside of `aquasol.water` and `aquasol.solutions` serves the purpose of having clear separation between formulas and user interface, and this helps in particular avoiding circular import problems. We explain these potential problems below.

Note also that the `aquasol.properties` module, which defines base classes for `WaterProperty` and `SolutionsProperty` etc., also shouldn't import from `aquasol.solutions` or `aquasol.water`. This is why the converter of the `SolutionsProperty` class is defined to `None` in the base class, and the converter is defined later during subclassing in the `aquasol.water` and `aquasol.solutions` modules.


### Avoiding circular import issues

Since all thermodynamic data are interdependent, it is easy to run into circular import problems. For example, if one wants to calculate solution density for a certain molarity, one needs to convert molarity to weight fraction, and this requires the knowledge of density itself. For this reason:

- The `solutions.convert()` function, when asked to use molarity, does not call `solutions.density()` but a locally-defined density function `density_basic()` (in **convert.py**) that imports a density formula from the `aquasol.formulas` module directly, which itself uses a reduced conversion function named `basic_convert()`, located in `aquasol.formulas.solutions.basic_conversions`

- The reduced converter `basic_convert()` does not use density/molarity data (as would the main `convert` function) to avoid another circular import.

The pattern of calls and imports in `aquasol.solutions` is summarized below.

`density` (or any user property in **solutions.properties**), inherits from `SolutionsProperty` (**aquasol.properties**) with *convert()* as unit converter

&darr;

`convert` (**aquasol.solutions.convert**)

&darr;

`density_basic` (**aquasol.solutions.convert**), inherits from `SolutionsProperty` (**aquasol.properties**) with *basic_convert()* as converter

&darr;

`basic_convert()` (**formulas.solutions.basic_conversions**)

For the same reason, the `aquasol.properties` module, which defines base classes for properties, cannot import `convert()` directly (see above).

For now, such a problem only arises with density-related parameters such as molarity, but be vigilant for possible circular import problems when adding new properties.
