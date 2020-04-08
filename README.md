# Thermo-OV (thermov) - thermodynamic relations for water and solutions

## General information
----------------------

This package computes useful thermodynamic quantities for water and aqueous solutions.

### `activity_density`

- `a_w` that compute water activity in Sodium Chloride solutions in function of salt concentration
- `rho` and `rho2` that return the solution density in function of salt concentration (rho is temperature-dependent and rho2 is for supersaturated solutions)

### `Psat`

Contains several formulas to compute water vapor pressure in function of temperature

See `documentation` to plot these functions

### `SaltsSolutionData`

Old Matlab code to plot data for salt solutions (density, activity, index of refraction etc.)

## Module requirements
----------------------
- numpy

## Python requirements
----------------------
Python : >= 3.6 (because of f-strings)

## Authors
----------
Olivier Vincent, 2019-2020
Marine Poizat, 2019
Léo Martin, 2020
