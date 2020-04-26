General information
===================

This package computes useful thermodynamic quantities for water and aqueous solutions. Is is divided in two modules: **water** (properties of pure water) and **solutions** (properties of aqueous solutions), which provide various functions to calculate properties of interest. There is also a list of useful constants in the *constants.py* module.

It is also possible to just see plots of the properties by running the package directly from a shell console with
`python -m thermov`.

Water
=====

Properties
----------

The *water* module has the following functions, which return the respective properties of interest as a function of temperature:
- `vapor_pressure` for saturation vapor pressure of pure water (Pa),
- `surface_tension` for surface tension of pure water (N/m).

The structure of the call for any property (replace *property* below by one of the function names above) is
```python
data = property(T=25, unit='C', source=None)
```
*Inputs*

- `T` (int, float, array, list, or tuple): temperature
- `unit` (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
- `source` (str, default None) : Source for the used equation, if *None* then the default source for the particular property is used.

*Output*

- Property in SI units, returned as numpy array if input is not a scalar.

*See docstrings for more details.*

Solutions
=========

Properties
----------

The *solutions* module has the following functions, which return the respective properties of interest as a function of solute concentration and temperature (when available) of an aqueous solution.
- `density` for absolute (kg / m^3) or relative density,
- `water_activity` for solvent activity (dimensionless, range 0-1),
- `surface_tension` for absolute surface tension (N/m) or relative (normalized by that of pure water at the same temperature).

The structure of the call for any property (replace *property* below by one of the function names above) is
```python
data = property(solute='NaCl', T=25, unit='C', source=None, **concentration)
```
with an additional parameter `relative=False` where applicable.

*Inputs*

- `solute` (str): solute name, default 'NaCl'
- `T` (float): temperature (default 25)
- `unit` (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
- `source` (str, default None) : Source for the used equation, if None then
gets the default source for the particular solute (defined in submodules).
- `**concentration`: kwargs with any unit that is allowed by `convert` (see below), e.g. `property(m=5.3)` for molality.
- when applicable: `relative` (bool, default False): True for relative density

*Output*

- Property in SI units, returned as numpy array if input is not a scalar.

Note: similarly to temperature, the values in `**concentration` can be an array, list or tuple, however if it's the case, temperature needs to be a scalar.

Other functions
---------------

The *solutions* module also has a function to convert between concentration units:
```python
value_out = convert(value, unit_in, unit_out, solute)
```
where unit_in and unit_out can be in the following list:
- *'m'* (molality, mol/kg)
- *'c'* (molarity, mol/m^3)
- *'x'* (mole fraction)
- *'w'* (weight fraction)
- *'mass_ratio'* (ratio solute mass to solvent mass).

By default, solute is `NaCl`.

One can access more elaborate quantities with the following functions:

```python
Iy = ionic_strength(solute, **concentration)
```
for ionic strength, which can be expressed in terms of molarity, molality or mole fraction. Which version is chosen among these three possibilities depend on the input parameters, e.g. *m=5.3* for molality, *x=0.08* for mole fraction, *c=5000* for molarity.

```python
y1, y2 = ion_quantities(solute, **concentration)
```
which calculate quantities of individual ions within the solution instead of considering the solute as a whole. Similarly, the result depends on the input unit, which can also be only among `m`, `c` or `x`.

*See docstrings for more details.*

Available Solutes
-----------------

Sorted by alphabetical order.

| Solute | Activity | Density | Surface Tension | Convert (+) | 
|:------:|:--------:|:-------:|:---------------:|:-----------:|
| CaCl2  |    X     |         |        X        |     *x*     |
| KCl    |          |         |                 |     *x*     |
| LiCl   |    X     |         |        X        |     *x*     |
| NaCl   |    X     |    X    |        X        |      X      |

(+) Solutes with no density data cannot use conversion to/from molarity ('c') but all other conversions work. They are noted with *x* instead of X.

Constants
=========

The *constants.py* file includes useful values including critical point data, molecular weights of species, dissociation numbers etc. Use the function `molar_mass` to get the molar mass (in kg/mol) of a specific solute from the *solute_list*.


Misc. info
==========

Module requirements
-------------------
- numpy
- matplotlib (only if running the package directly as a main file to plot the properties)

Python requirements
-------------------
Python : >= 3.6 (because of f-strings)

Author
------
Olivier Vincent
(olivier.a-vincent@wanadoo.fr)

Contributors
------------
Marine Poizat (2019), Léo Martin (2020)
