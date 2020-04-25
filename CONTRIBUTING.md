# How to add data


## Create a new property (*water*, *solutions*)

**Note:** The property must depend on the exact same parameters as existing properties (i.e. temperature for *water, temperature and concentration for *solutions*). At this stage, adding more complex dependencies requires modification of the factored code in *general.py*.

- Create a file for the property in the directory **water.formulas** or a folder for the property in the **solutions.formulas** directory.

- Add a function corresponding to the property in the **properties.py** file of the water or solutions module, mimicking the structure of other properties defined within this file.

- For solutions, follow the steps described below to add sources / solutes data in the created folder. For water, add the function to the created file, mimicking the structures of other property files in the formulas directory.

- Update the local module (water or solutions) **\__init\__.py** (*not* the main packagge init file) to import the new function upon init in addition to the existing ones.

- Update **README.md** with descriptions, examples, and adequate crosses in the *Available Solutes* table.

- Add a plot of the new property data in the **\__main\__.py** file.

- *Soon: add tests*


## Add solute to an existing property (*solutions*)

- Create a file with the name of the solute in the folder of the property in the directory **solutions.formulas** (e.g. *licl.py* in  *density* ).

- Follow the same file structure as for other solutes in the same folder. In particular, the `default_source` must be defined, as well at the dictionaries `concentration_types`, `concentration_ranges`, `temperature_units`, `temperature_ranges` at the beginning of the file, and dictionary `formulas` and list `sources` at the end of the file.

- Add a function calculating the property in the file. It must have the same inputs/outputs as functions of other solutes of the same property (e.g. rho0, rho = f (concentration_value, T) for density).

- In **properties.py**, in the function corresponding to the property, add the name of the new solute file in the `modules` dictionary.

- **If the property is density**, also modify the function `basic_density` accordingly in **convert.py**.

- If the solute is not listed in the **constants.py** file, add it in the *solute_list* and add its data in relevant dictionaries in the file.

- In **README.md**, add a cross in the adequate spot in the *Available Solutes* table.

- Add the info on the solute in the docstring of the property's function in the **properties.py** file of the module.

- Add a plot of the new solute data in the **\__main\__.py** file.

- *Soon: add tests*


## Add a source to an existing property (*water*, *solutions*)

- Go into the file/folder for the property in the directory **water.formulas** or **solutions.formulas** and open the *.py* file corresponding to that property and/or solute.

- Add function within that file, and update the `default_source` (if necessary), as well at the dictionaries `concentration_types` (for solutions only), `concentration_ranges` (for solutions only), `temperature_units`, `temperature_ranges` at the beginning of the file, and dictionary `formulas` and list `sources` at the end of the file.

- Add the info on the source in **1)** the docstring of the formula file, **2)** the docstring of the property's function in the **properties.py** file of the module, **3)** in adequate places in **README.md**.

- Add a plot of the new source data in the **\__main\__.py** file.

- *Soon: add tests*


# Structure of code

All user functions calculating the properties of water or solutions (e.g. surface tension, density) are in the **properties.py** file of each module. For solutions, additional functions are in the **convert.py** file. All other files are support files for these main files.

In particular, the **general.py** files of each module contains factored code that takes advantage of the similarity of formatting of all property files (see *How to add data* above) to load and calculate properties through a unique function (`water_calculation` or `solution_calculation` depending on the module). This function also manages formatting / conversion of values of temperature or concentration between those asked by the user and those actually used by the basic functions located in the **formulas** directory.

At the root of the package are also useful files: 
- **constants.py** with data of physical constants used throughout the package and a `molar_mass()` function that returns molar mass of solutes,
- **check.py** and **format.py** that gather useful tools for checking (e.g. validity range, correct units etc.) and formatting (e.g. data in the right units).

An important thing to do is **avoiding circular imports**. For example, if one wants to calculate solution density for a certain molarity, one needs to convert molarity to weight fraction, and this requires the knowledge of density itself. For this reason:
- the `convert` function calls a reduced version of `density`, called `basic_density`, defined in the **convert.py** file itself, and which is used in the molarity functions,
- there is also a reduced version of the `convert` function, named `basic_convert`, which is located in **formulas.basic_conversions**,
- this reduced converter does not use density/molarity data and can be passed as the `converter` argument in the `solution_calculation` and `format_concentration` functions instead of the regular, more general `convert`. This is exactly what is done in the definition of `basic_density` compared to the regular `density`.



