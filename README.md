# Thermo-OV (thermov) - physico-chemical properties of water and solutions


## General information
----------------------

This package computes useful thermodynamic quantities for water and aqueous solutions. Is is divided in two modules: **water** (properties of pure water) and **solutions** (properties of aqueous solutions). There is also a list of useful constants in the *constants.py* module.

The package provides various functions that return properties of water and solutions, but it is also possible to just see plots of the properties by running the package directly from a shell console with
`python -m thermov`.

Below is some basic information for a quick overview of the package's contents. For detailed information, see documentation in docstrings.

## Water
--------

The *water* module has the following functions, which return the respective properties of interest as a function of temperature:
- `vapor_pressure` for saturation vapor pressure of pure water (Pa),
- `surface_tension` for surface tension of pure water (N/m).

The package's functions take temperature (in °C or K) as a parameter. It can be input as a scalar or as an array (or tuple, list, etc.).


## Solutions
------------

The *solutions* module has the following functions, which return the respective properties of interest as a function of solute concentration and temperature (when available) of an aqueous solution.
- `density` for absolute (kg / m^3) or relative density,
- `water_activity` for solvent activity (dimensionless, range 0-1),
- `surface_tension` for absolute surface tension (N/m) or relative (normalized by that of pure water at the same temperature).

The package's functions take temperature (in °C or K) and concentration (in various units, e.g. molarity, molality, mole fraction, etc., see units in `convert` below) as parameters. They can be input as scalars or as an arrays (or tuple, list, etc.), but if one of the (concentration, temperature) parameters is an array, the other one has to be a scalar.

The *solutions* module also has a function to convert between concentration units:
`convert(value, unit_in, unit_out, solute)`
where unit_in and unit_out can be in the following list:
- *'m'* (molality, mol/kg)
- *'c'* (molarity, mol/L)
- *'x'* (mole fraction)
- *'w'* (weight fraction)
- *'mass_ratio'* (ratio solute mass to solvent mass).
All these units are acceptable as kwargs in the functions above, e.g. `density(m=5.3)` or `water_activity(x=0.25)`.

When the solute is not specified, it is assumed to be **NaCl** by default. To specify a solute, input it as a kwarg in the functions, e.g. `density(solute='LiCl', x=0.1)`. Most of the time, *solute* is also the first positional argument. See list of available solutes below.

Finally, one can access more elaborate quantities with the following functions:
- `ionic_strength` for ionic strength, which can be expressed in terms of molarity, molality or mole fraction. Which version is chosen among these three possibilities depend on the input parameters, e.g. *m=5.3* for molality, *x=0.08* for mole fraction, *c=5000* for molarity.
- `ion_quantities`, which calculate quantities of individual ions within the solution instead of considering the solute as a whole. Similarly, the result depends on the input unit, which can also be only among `m`, `c` or `x`.

### Available Solutes

Sorted by alphabetical order.

| Solute | Activity | Density | Surface Tension | Convert (+) | 
|:------:|:--------:|:-------:|:---------------:|:-----------:|
| CaCl2  |          |         |        X        |     *x*     |
| KCl    |          |         |                 |     *x*     |
| LiCl   |          |         |        X        |     *x*     |
| NaCl   |    X     |    X    |        X        |      X      |

(+) Solutes with no density data cannot use conversion to/from molarity ('c') but all other conversions work. They are noted with *x* instead of X.

## Constants
------------

The *constants.py* file includes useful values including critical point data, molecular weights of species, dissociation numbers etc. Use the function `molar_mass` to get the molar mass (in kg/mol) of a specific solute from the *solute_list*.


## Module requirements
----------------------
- numpy
- matplotlib (only if running the package directly as a main file to plot the properties)

## Python requirements
Python : >= 3.6 (because of f-strings)

## Author
Olivier Vincent
(olivier.a-vincent@wanadoo.fr)

## Contributors
Marine Poizat (2019), Léo Martin (2020)
