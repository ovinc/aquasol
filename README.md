# Thermo-OV (thermov) - thermodynamic relations for water and solutions

## General information
----------------------

This package computes useful thermodynamic quantities for water and aqueous solutions.

### `activity`

- `a_w` compute water activity in Sodium Chloride solutions in function of salt concentration

### `density`

- `density` return the solution density as a function of salt concentration and temperature

### `vapor_pressure`

- `psat` can use several formulas to compute water vapor pressure in function of temperature

See `documentation` to plot these functions

### `surface_tension`

- `surface_tension` returns water surface tension as a function of temperature

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
