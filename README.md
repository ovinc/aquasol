# Thermo-OV (thermov) - thermodynamic relations for water and solutions

## General information
----------------------
This package is to compute some useful thermodynamic quantities for water and Sodium Chloride solutions :
### `activity_density` contains :
- `a_w` that compute water activity in Sodium Chloride solutions in function of salt concentration
- `rho` and `rho2` that return the solution density in function of salt concentration (rho is temperature-dependent and rho2 is for supersaturated solutions)

### `Psat` contains several formulas to compute water vapor pressure in function of temperature

See `documentation` to plot these functions

### `SaltsSolutionData` is a Matlab code to plot data for salt solutions (density, activity, index of refraction etc.)

## Module requirements
----------------------
- numpy

## Python requirements
----------------------
Python : >= 3.6 (because of f-strings)

## Author
---------
Olivier Vincent, 2020
Marine Poizat, 2019
Léo Martin, 2020
