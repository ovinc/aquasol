# Instructions for contributing

Contributing to *aquasol* is possible in several ways. Here we show how to add **formulas** (i.e., sources) to a given property, and how to add a new **property** for water or solutions.

## Add formula (to existing property)

Formulas are managed by the `aquasol.formulas` module.
All formulas are described by classes that inherit from `Formula`, defined in `aquasol.formulas.general`.

- Formulas for water are present in the `aquasol.formulas.water` module and inherit from `WaterFormula`; they depend only on temperature (*T*)

- Formulas for solutions are present in the `aquasol.formulas.solutions` module and inherit from `SolutionFormula` (dependence on *T* and concentration), or `SaturatedSolutionFormula` (dependence on *T* only)

**Important NOTE**: If the formula uses other formulas (e.g. solution formula using water quantity as reference), or conversions between concentration units (including `ionic_strength()`), please only import functions, classes etc. that are contained in the `aquasol.formulas` module (including `basic_conversions` or `ionic` in `aquasol.formulas.solutions`), or in the `aquasol.constants` module; **DO NOT** import from `aquasol`, `aquasol.water` or `aquasol.solutions`. This is to keep modules as independent from each other and prevent circular imports problems.

- **OK Examples**:
    ```python
    from aquasol.constants import R, Mw, Patm, Pc, Tc
    from aquasol.formulas.water.vapor_pressure import VaporPressure_IAPWS
    from aquasol.formulas.solutions.ionic import ionic strength
    from aquasol.formulas.solutions.basic_conversions import basic_convert
    ```

- **NOT OK Examples**:
    ```python
    from aquasol import ps, dp, cv
    from aquasol.water import vapor_pressure
    from aquasol.solutions import ionic strength
    from aquasol.solutions import convert
    ```

### *Water* formula

- Go to the module of the specific property where you want to add a formula (e.g. `aquasol/formulas/water/surface_tension.py`).

- Add class for the formula, inheriting from `WaterFormula`, with the following characteristics :

    - **Class attributes**:
        - `source` [str]: short name describing the source for the formula
        - `temperature_range` [tuple of floats]: validity Tmin, Tmax for the formula)
        - `temperature_unit` [str]: `'C'` or `'K'`

    - **Method** `calculate(self, T)`, which takes temperature as an input (in the units defined above) and returns the calculated property in SI units.

- Add the class to the tuple gathering all formulas at the end of file of the property module (e.g. `aquasol/formulas/water/surface_tension.py`)


### *Solutions* formula

The strategy is similar to that for water, but with a few extra steps.

- Go to the module of the specific property where you want to add a formula (e.g. `aquasol/formulas/solutions/surface_tension`).

- Decide where to add the formula:

    - If the formula is for just one specific solute, add it directly to the file bearing the name of the solute (e.g., `aquasol/formulas/solutions/surface_tension/NaCl.py`)

    - If the solute file does not exist (solute not documented before), add it and use the file for *NaCl* as a template.

    - If the formula can describe different solutes (e.g. same equation with different coefficients), it is preferrable to create a new, single file gathering all formulas for different solutes, then import the formulas in each solute file (see e.g. how it is done for *LiCl* and *CaCl2* in the `conde.py`, `LiCl.py` and `CaCl2.py` files in `aquasol/formulas/solutions/surface_tension/`)

- Add class for the formula, inheriting from `SolutionFormula` or `SaturatedSolutionFormula`, with the following characteristics :

    - **Class attributes**:
        - `source`, `temperature_range`, `temperature_unit` (same as for water)
        - `concentration_range` [tuple of floats]: validity c_min, c_max for the formula
        - `concentration_unit`: [str], any concentration type accepted by `aquasol.convert()`, e.g. molality (`'m'`), weight fraction (`'w'`), etc.)
        - if formula returns both the value and a reference value (value at zero concentration), set `with_water_reference = True`.

    - **Method** `calculate(self, c, T)`, which takes concentration and temperature as an input (in the units defined above) and returns the calculated property in SI units; if `with_water_reference`, the method should return a tuple `(v0, v)` with `v0` the value of the property at zero concentration.

- Add the class to the tuple gathering all formulas at the end of file of each solute file (e.g. `aquasol/formulas/solutions/surface_tension/NaCl.py`)

- If adding solutes that were not documented before for the considered property, also add the tuple to the init file of the property module (e.g. `aquasol/formulas/solutions/surface_tension/__init__.py`), similarly to other existing solutes.


### Final steps for both *water* and *solutions* formulas

- Update **README.md** with new entry in the *Sources* reference list, and for solutions with adequate crosses in the *Available Solutes* table.

- Add tests in **tests** folder and run all tests of aquasol to make sure nothing is broken (type `pytest` in console while being in the root folder of the *aquasol* project).


## Create new property

### Water property

#### 1. Define new formulas in `aquasol.formulas`

- Create new file in `aquasol.formulas.water`, which will contain the formulas for the new property.

- Add formulas in that file (see *Add formula (to existing property)* section above)

- One of the formulas has to be designed as the default formula to use for the particular property. This is achieved by setting the class attribute `default=True` in the formula class.

- Create a tuple containing all formula classes at the end of the file (see other property files for examples), e.g. in `vapor_pressure` module:
    ```python
    VaporPressureFormulas = (
        VaporPressure_IAPWS,
        VaporPressure_Wexler,
        VaporPressure_Bridgeman,
    )
    ```

#### 2. Define new property in `aquasol.water`

- Create new class inheriting from `WaterProperty` in `aquasol/water/properties.py`, which will describe the new property and gather all available formulas. Then, go to *Final steps* section below.


### Solution property

#### 1. Define new formulas in `aquasol.formulas`

- Create new folder in `aquasol.formulas.water` with an ``__init__.py`` empty file. This module will contain all formulas for the new property.

- In that new folder, also create one python file per solute (e.g. `NaCl.py`) that will be

- Add formulas in the module (see *Add formula (to existing property)* section above)

- One of the formulas in each solute file has to be designed as the default formula to use for the particular property and given solute. This is achieved by setting the class attribute `default=True` in the formula class.

- Create a tuple containing all formula classes at the end of each solute file (see other property files for examples), e.g. in `aquasol/formulas/solutions/density/NaCl.py`:
    ```python
    Density_NaCl_Formulas = (
        Density_NaCl_Simion,
        Density_NaCl_Tang,
        Density_NaCl_AlGhafri,
    )
    ```

- In the empty `__init__.py` file previously created in the property module, import all solute formulas and create a new tuple with all formulas for all solutes, e.g. in `aquasol/formulas/solutions/density/__init__.py`:
    ```python
    from .KCl import Density_KCl_Formulas
    from .LiCl import Density_LiCl_Formulas
    from .NaCl import Density_NaCl_Formulas

    DensityFormulas = (
        Density_KCl_Formulas +
        Density_LiCl_Formulas +
        Density_NaCl_Formulas
    )
    ```

#### 2. Define new property in `aquasol.water`

- Create new class inheriting from `SolutionProperty` (or equivalent, e.g. `SolubilityProperty`) in `aquasol/solution/properties.py`, which will describe the new property and gather all available formulas. Then, go to *Final steps* section below.

#### 2. Define new property in `aquasol.water`

- Create new class inheriting from `WaterProperty` in `aquasol/water/properties.py`, which will describe the new property and gather all available formulas. Then, go to *Final steps* section below.


### Final steps for both *water* and *solutions* properties

- In the new property class, define the following class attributes:
    - `quantity` [str]: short title for the property
    - `unit` [str]: what is the physical unit (SI) of the quantity
    - `Formulas` [tuple]: put here the tuple of formulas defined above, e.g.
        ```python
        Formulas = VaporPressureFormulas
        ```
        or
        ```python
        Formulas = DensityFormulas
        ```
        with the examples above

- Also include a docstring in that new class, with a one-liner describing the property and some examples; a more general docstring describing possible inputs etc. is automatically added by `Property` base classes.

- At the end of the `properties.py` file, instantiate an object of the class; this object will be the function accessible to the user for the specific property(*).

- Import that object in the `__init__.py` file of the module (`water` or `solutions`) so that it is accessible to the user by calling `from aquasol.water import ...` or `from aquasol.solutions import ...`

- Update **README.md** with descriptions of the new property and some examples.

- Add a plot of the new property data in the **\__main\__.py** file in `aquasol`.

- Go to the root folder of `aquasol` and run the two following commands to make sure nothing is broken:
    - Run tests [requires pytest installed]
        ```bash
        pytest
        ```
    - Check graphs [requires matplotlib installed]
        ```bash
        python -m aquasol
        ```

(*) These objects are not true python functions but objects from callable classes, which act as functions but with extra attributes, e.g. all sources available can be accessed with `.sources` attribute.

