# How to add data

**Note:** For a quick and clean additions, new properties must depend on the exact same parameters as existing properties (i.e. temperature for *water*, temperature and concentration for *solutions*). Adding more complex dependencies is possible but requires modification of the factored code in *general.py* or specific, non-factored definitions in *properties.py* (not recommended).

## Create a new property (*water*, *solutions*)

- Choose a common name *[cmn_name]* and a module name *[mod_name]* for the new property. Then:

    + For *water*, create a **[mod_name].py** file in the **water.formulas** directory. 
    + For *solutions*, create a folder named **[mod_name]** in the **solutions.formulas** directory.

- In the **general.py** file of the water or solutions module, add the new property *[cmn_name]* and its corresponding *[mod_name]* in the `property_modules` dictionary.

- Add the formulas for calculating the new property, mimicking the structure of other properties already defined:
    + For *water*, in **[mod_name].py**, 
    + For *solutions*, create one file **[solute_name].py** per solute in the **[mod_name]** directory (see below *Add solute* for details).

In particular, the `default_source` must be defined, as well at the dictionaries `temperature_units`, `temperature_ranges`, `concentration_types` (only for solutions), `concentration_ranges` (only for solutions) at the beginning of the file, and dictionary `formulas` and list `sources` at the end of the file. The function coding the formula can have any output, but must have the same inputs as other existing properties (see *Note* above).

- Add a function corresponding to the property in the **properties.py** file of the water or solutions module, mimicking the structure of other properties defined within this file. Write a detailed docstring, as this is the function that will be publicly available to the user.

- Update the local module (water or solutions) **\__init\__.py** (*not* the main package init file) to import the new function upon init.

- Update **README.md** with descriptions, examples, and adequate crosses in the *Available Solutes* table.

- Add a plot of the new property data in the **\__main\__.py** file.

- *Soon: add tests*


## Add solute to an existing property (*solutions*)

- Create a file with the chemical name of the solute in the folder of the property in the directory **solutions.formulas** (e.g. *LiCl.py* or *Na2SO4.py* in  *solutions.formulas.density* ). Follow the same file structure as for other solutes in the same folder (see dictionaries to define in *Create a new property* above).

- Add a function calculating the property in the file. It must have the same inputs and outputs as functions of other solutes of the same property. Do not hesitate to write functions common to several solutes in a *misc.py* file, and call it from the solute file.

- **If the property is density**, also modify the function `basic_density` accordingly in **convert.py** (see *Structure of code* below for an explanation of why there are two density functions).

- If the solute is not listed in the **constants.py** file, add it in the *solute_list* and add its data in relevant dictionaries in the file.

- In **README.md**, add a cross in the adequate spot in the *Available Solutes* table.

- Add the info on the solute in the docstring of the property's function in the **properties.py** file of the module.

- Add a plot of the new solute data in the **\__main\__.py** file.

- *Soon: add tests*


## Add a formula / source to an existing property (*water*, *solutions*)

- Go into the file/folder for the property in the directory **water.formulas** or **solutions.formulas** and open the *.py* file corresponding to that property and/or solute.

- Add the formula as a function within that file, and update the `default_source` (if necessary), as well at the dictionaries mentioned in *Create a new property* above. Note that changing the default source for solution densities will change the way molarities are calculated / converted.

- Add the info on the source in **1)** the docstring of the formula *.py* file (detailed info), **2)** the docstring of the property's function in the **properties.py** file of the module (brief info), **3)** in adequate places in **README.md**.

- Add a plot of the new source data in the **\__main\__.py** file.

- *Soon: add tests*


# Structure of code

### Main user files

All public user functions calculating the properties of water or solutions (e.g. surface tension, density) are in the **properties.py** file of each module (*water* or *solution*). For solutions, additional functions are in the **convert.py** file. 

### Support files

All other files are support files for these main files. In particular:

- **general.py** in each module contains factored code that takes advantage of the similarity of formatting of all property files (see *How to add data* above) to load and calculate properties through a unique function (`calculation`). This function also manages formatting / conversion of values of temperature or concentration between those asked by the user and those actually used by the basic functions located in the **formulas** directories. **general.py** also contains a useful `get_infos` function that gets information about formulas and sources available for a given property and/or solute.

- **constants.py** has data of physical constants used throughout the package and a `molar_mass()` function that returns molar mass of solutes.

- **check.py** and **format.py** gather useful tools for checking (e.g. validity range, correct units etc.) and formatting (e.g. data in the right units).

### "Basic" functions to avoid circular imports

Since all thermodynamic data are interdependent, it is easy to run into circular import problems. For example, if one wants to calculate solution density for a certain molarity, one needs to convert molarity to weight fraction, and this requires the knowledge of density itself. For this reason:

- The `convert` function, when asked to use molarity, calls a reduced version of `density` called `basic_density`, which is defined in the **convert.py** file itself.

- `basic_density`, when called, does not use `convert` to manage possible unit conversions (which would cause a circular import), but a reduced version named `basic_convert`, located in **formulas.basic_conversions**

- The reduced converter `basic_convert` does not use density/molarity data (as would the main `convert` function) to avoid another circular import. 

Note that both `basic_convert` and `convert` rely on the same `calculation` function to calculate density, but only use a different converter. The pattern of calls and imports in **solutions** is summarized below.

---

`density` (or any user property in **properties.py**) 

&darr;  

`calculation` (**solutions.general**) called with *convert* as converter

&darr;

`convert` (**solutions.convert**)

&darr;

`basic_density` (**solutions.convert**)

&darr;  

`calculation` (**solutions.general**) called with *basic_convert* as converter

&darr;

`basic_convert` (**solutions.formulas**)

(some intermediaries such as *format_concentration* and molarity calculation functions were omitted for clarity)

---

For now, such a problem only arises with density-related parameters such as molarity, but be vigilant for possible circular import problems when adding new properties.


