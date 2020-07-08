General information
===================

This package computes useful thermodynamic quantities for water and aqueous solutions. Is is divided in two modules: **water** (properties of pure water) and **solutions** (properties of aqueous solutions), which provide various functions to calculate properties of interest. There is also a list of useful constants in the *constants.py* module.

It is also possible to just see plots of the properties by running the package directly from a shell console with
```bash
python -m aquasol
```


WATER
=====

Properties
----------

The *water* module has the following functions, which return the respective properties of interest as a function of temperature:
- `vapor_pressure` for saturation vapor pressure of pure water (Pa),
- `surface_tension` for surface tension of pure water (N/m).
- `density_sat` for density on the liquid-vapor coexistence line (kg/m^3)
- `density_atm` for density at ambient pressure 0.1 MPa (kg/m^3)

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


Sources
-------

Below are the sources for water vapor pressure (1, 2, 3), density (1, 4, 5), surface tension (6).

(1) Wagner, W. & Pruß, A. *The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use.* Journal of Physical and Chemical Reference Data 31, 387–535 (2002).

(2) Wexler, A. & Greenspan, L. *Vapor Pressure Equation for Water in the Range 0 to 100°C.* Journal of Research of the National Bureau of Standards - A. Physics and Chemistry 75A, 213–245 (1971).

(3) Bridgeman, O. C. & Aldrich, E. W. *Vapor Pressure Tables for Water.* Journal of Heat Transfer 86, 279–286 (1964).

(4) Pátek, J., Hrubý, J., Klomfar, J., Součková, M. & Harvey, A. H. *Reference Correlations for Thermophysical Properties of Liquid Water at 0.1MPa.* Journal of Physical and Chemical Reference Data 38, 21–29 (2009).*

(5) Kell, G. S. Density, thermal expansivity, and compressibility of liquid water from 0.deg. to 150.deg.. *Correlations and tables for atmospheric pressure and saturation reviewed and expressed on 1968 temperature scale.* J. Chem. Eng. Data 20, 97–105 (1975).

(6) IAPWS *Revised Release on Surface Tension of Ordinary Water Substance.* Moscow, Russia, June 2014.

* recommended by IAPWS.


SOLUTIONS
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

Inverse property functions
--------------------------

The `aw_to_conc` calculates what concentration of solute is necessary to reach a specific water activity:
```python
aw_to_conc(a, out='w', solute='NaCl', T=25, unit='C', source=None):
```
For example:
```python
aw_to_conc(0.39)
>>> 0.4902761745068064  # in terms of weight fraction
aw_to_conc([0.39, 0.75], out='m')
>>> array([16.45785963,  6.21127029])  # in terms of molality
aw_to_conc(0.11, 'mass_ratio', 'LiCl', T=50)
>>> 0.9167650291014361  # in terms of mass ratio, for LiCl, at 50°C
```

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

Sorted by alphabetical order. When available, the sources are written in parentheses. For convert, an X means available.

| Solute | Activity | Density | Surface Tension | Convert (*) | 
|:------:|:--------:|:-------:|:---------------:|:-----------:|
| CaCl2  |   (1)    |  (1,3)  |      (1,6)      |      X      |
| KCl    |          |   (3)   |       (6)       |      X      |
| KI     |          |   (3)   |                 |      X      |
| LiCl   |   (1)    |   (1)   |       (1)       |      X      |
| MgCl2  |          |   (3)   |       (6)       |      X      |
| Na2SO4 |   (2)    |         |       (6)       |      -      |
| NaCl   |   (2)    | (1,4,5) |       (6)       |      X      |

(*) Solutes with no density data cannot use conversion to/from molarity ('c') but all other conversions work. They are noted with - instead of X.

Sources
-------

(1) Conde, M. R., *Properties of aqueous solutions of lithium and calcium chlorides: formulations for use in air conditioning equipment design.*
International Journal of Thermal Sciences 43, 367–382 (2004).

(2) Clegg, S. L., Brimblecombe, P., Liang, Z. & Chan, C. K., *Thermodynamic Properties of Aqueous Aerosols to High Supersaturation: II — A Model of the System Na+ Cl− NO3- SO42- H2O at 298.15 K.* Aerosol Science and Technology 27, 345–366 (1997).

(3) Al Ghafri, S., Maitland, G. C. & Trusler, J. P. M., *Densities of Aqueous MgCl 2 (aq), CaCl 2 (aq), KI(aq), NaCl(aq), KCl(aq), AlCl 3 (aq), and (0.964 NaCl + 0.136 KCl)(aq) at Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and Molalities up to 6 mol·kg –1.* Journal of Chemical & Engineering Data 57, 1288–1304 (2012).

(4) Tang, I. N., *Chemical and size effects of hygroscopic aerosols on light scattering coefficients.* Journal of Geophysical Research: Atmospheres 101, 19245–19250 (1996).

(5) Simion, A. I., Grigoras, C., Rosu, A.-M. & Gavrilă, L. *Mathematical modelling of density and viscosity of NaCl aqueous solutions.* Journal of Agroalimentary Processing and Technologies 21, 41–52 (2015).

(6) Dutcher, C. S., Wexler, A. S. & Clegg, S. L. *Surface Tensions of Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.* J. Phys. Chem. A 114, 12216–12230 (2010).


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
