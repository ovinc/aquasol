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
- `vapor_pressure()` for saturation vapor pressure of pure water (Pa),
- `surface_tension()` for surface tension of pure water (N/m).
- `density_sat()` for density on the liquid-vapor coexistence line (kg/m^3)
- `density_atm()` for density at ambient pressure 0.1 MPa (kg/m^3)
- `diffusivity_in_air()` for diffusivity of water vapor in air (m^2/s)
- `viscosity_atm` for viscosity of liquid water (Pa.s)

The structure of the call for any property (replace *property* below by one of the function names above) is
```python
from aquasol.water import property
data = property(T=25, unit='C', source=None)
```
*Inputs*

- `T` (int, float, array, list, or tuple): temperature
- `unit` (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
- `source` (str, default None) : Source for the used equation, if *None* then the default source for the particular property is used.

*Output*

- Property in SI units, returned as numpy array if input is not a scalar.


### Examples

(See docstrings for more details)

```python
from aquasol.water import vapor_pressure, surface_tension
from aquasol.water import density_atm, density_sat
from aquasol.water import diffusivity_in_air, viscosity_atm

vapor_pressure()             # Saturation vapor pressure (Pa) at 25°C (3170 Pa)
vapor_pressure(298.15, 'K')        # same thing
vapor_pressure(source='Wexler')    # same thing, but according to Wexler
vapor_pressure(T=[5, 15, 25])          # psat at different temperatures in °C

surface_tension(T=[5, 15, 25])         # same, but for surface tension (N/m)

density_atm(4)               # density of water at atmospheric pressure at 4°C
density_sat(277.15, 'K')     # same thing, but on the coexistence line

diffusivity_in_air(27)  # Diffusivity of water vapor in air at 27°C

viscosity_atm()         # Viscosity of liquid water at 25°C
```

Inverse and other property functions
------------------------------------

Based on the functions above, some inverse and other properties are also provided:

- `dewpoint()`
- `kelvin_pressure()`
- `kelvin_radius()`
- `kelvin_humidity()`

### Examples

(See docstrings for more details)

```python
from aquasol.water import dewpoint, kelvin_radius, kelvin_humidity

dewpoint(p=1000)  # Dew point of a vapor at 1kPa
dewpoint(rh=50)  # Dew point at 50%RH and 25°C (default)
dewpoint('K', 300, rh=50)  # specify temperature
dewpoint(aw=[0.5, 0.7])     # It is possible to input lists, tuples, arrays

kelvin_pressure(rh=80)  # (liquid) Kelvin pressure corresponding to 80%RH
kelvin_pressure(aw=[0.5, 0.7, 0.9], T=20)  # at 20°C for 50%RH, 70%RH, 90%RH

kelvin_radius(aw=0.8)  # Kelvin radius at 80%RH and T=25°C
kelvin_radius(rh=80, ncurv=1)  # assume cylindrical meniscus instead of spherical

kelvin_humidity(r=4.7e-9)  # activity corresponding to Kelvin radius of 4.7 nm at 25°C
kelvin_humidity(r=4.7e-9, out='rh')  # same, but expressed in %RH instead of activity
kelvin_humidity(r=4.7e-9, ncurv=1, out='p')  # cylindrical interface, output as pressure
kelvin_humidity(P=[-30e6, -50e6])  # input can also be liquid pressure
```


Sources
-------

Below are the sources for water vapor pressure (1, 2, 3), density (1, 4, 5), surface tension (6), diffusivity in air (7, 8), viscosity (9)

(1) Wagner, W. & Pruß, A. *The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use.* Journal of Physical and Chemical Reference Data 31, 387–535 (2002).

(2) Wexler, A. & Greenspan, L. *Vapor Pressure Equation for Water in the Range 0 to 100°C.* Journal of Research of the National Bureau of Standards - A. Physics and Chemistry 75A, 213–245 (1971).

(3) Bridgeman, O. C. & Aldrich, E. W. *Vapor Pressure Tables for Water.* Journal of Heat Transfer 86, 279–286 (1964).

(4) Pátek, J., Hrubý, J., Klomfar, J., Součková, M. & Harvey, A. H. *Reference Correlations for Thermophysical Properties of Liquid Water at 0.1MPa.* Journal of Physical and Chemical Reference Data 38, 21–29 (2009).*

(5) Kell, G. S. Density, thermal expansivity, and compressibility of liquid water from 0.deg. to 150.deg.. *Correlations and tables for atmospheric pressure and saturation reviewed and expressed on 1968 temperature scale.* J. Chem. Eng. Data 20, 97–105 (1975).

(6) IAPWS *Revised Release on Surface Tension of Ordinary Water Substance.* Moscow, Russia, June 2014.

(7) Massman, W. J. *A review of the molecular diffusivities of H2O, CO2, CH4, CO, O3, SO2, NH3, N2O, NO, and NO2 in air, O2 and N2 near STP.* Atmospheric Environment 32, 1111-1127 (1998).

(8) Marrero, T. R. and Mason E. A., *Gaseous diffusion coeffcients.* Journal of Physics and Chemistry Reference Data 1, 3-118 (1972)

(9) Huber, M. L. et al. *New International Formulation for the Viscosity of H2O.* Journal of Physical and Chemical Reference Data 38, 101-125 (2009).*

(*) recommended by IAPWS.


SOLUTIONS
=========

Properties
----------

The *solutions* module has the following functions, which return the respective properties of interest as a function of solute concentration and temperature (when available) of an aqueous solution.
- `density()` for absolute (kg / m^3) or relative density,
- `water_activity()` for solvent activity (dimensionless, range 0-1),
- `surface_tension()` for absolute surface tension (N/m) or relative (normalized by that of pure water at the same temperature).
- `refractive_index()` (dimensionless)
- `electrical_conductivity()` (S/m)

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


### Examples

```python
from aquasol.solutions import water_activity, density, surface_tension, refractive_index

# Water activity (dimensionless) ---------------------------------------------
water_activity(x=0.1)            # NaCl solution, mole fraction 10%, 25°C
water_activity(r=0.3)           # solution when mixing 55g NaCl with 100g H2O
water_activity('LiCl', w=0.3, T=70)  # LiCl solution, 30% weight fraction, 70°C
water_activity(solute='CaCl2', m=[2, 4, 6])  # for several molalities (mol/kg)

# Density (absolute, kg / m^3, or relative) ----------------------------------
density(source='Tang', x=0.23)  # supersaturatad NaCl, 25°C, using Tang equation
density(c=5000, relative=True)  # relative density of NaCl, 5 mol/L.
density('LiCl', w=[0.11, 0.22, 0.51])  # for several weight fractions of LiCl

# Surface tension (N / m) ----------------------------------------------------
surface_tension(r=0.55)           # solution when mixing 55g NaCl with 100g H2O
surface_tension(c=5000, relative=True)  # sigma / sigma(H2O) at 5 mol/L of NaCl
surface_tension('CaCl2', 353, 'K', c=5e3)    # CaCl2, 300K, 5 mol/L
surface_tension(x=[0.02, 0.04, 0.08], T=21)  # iterable mole fraction

# Refractive index -----------------------------------------------------------
refractive_index(c=4321)  # concentration of 4.321 mol/L of NaCl, 25°C
refractive_index('KCl', T=22, r=[0.1, 0.175])  # various mass ratios of KCl

# Electrical conductivity ----------------------------------------------------
electrical_conductivity('KCl', m=0.1)  # molality of 0.1 mol/L of KCl, 25°C
electrical_conductivity('KCl', T=50, x=[0.01, 0.02])  # various mole fractions
electrical_conductivity('KCl', T=[0, 25, 50], m=1)  # various mole fractions
```


Inverse property functions
--------------------------

The `aw_to_conc` calculates what concentration of solute is necessary to reach a specific water activity:
```python
aw_to_conc(a, out='w', solute='NaCl', T=25, unit='C', source=None):
```
For example:
```python
aw_to_conc(0.8)  # weight fraction of NaCl to have a humidity of 80%RH
aw_to_conc([0.6, 0.85], out='m')  # molality of NaCl to get 60%RH and 85%RH
aw_to_conc(0.33, 'r', 'LiCl', T=50)  # in terms of mass ratio, for LiCl at 50°C
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
- *'r'* (ratio solute mass to solvent mass).

By default, solute is `'NaCl'`.

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

| Solute | Activity | Density | Surface Tension | Refractive Index | Electrical conductivity | Convert (*) |
|:------:|:--------:|:-------:|:---------------:|:----------------:|:-----------------------:|:-----------:|
| CaCl2  |   (1)    |  (1,3)  |      (1,6)      |       (7)        |                         |      X      |
| KCl    |   (8)    |   (3)   |       (6)       |       (7)        |           (9)           |      X      |
| KI     |          |   (3)   |                 |                  |                         |      X      |
| LiCl   |   (1)    |   (1)   |       (1)       |                  |                         |      X      |
| MgCl2  |          |   (3)   |       (6)       |                  |                         |      X      |
| Na2SO4 |   (2)    |   (10)  |       (6)       |                  |                         |      X      |
| NaCl   |  (2,8)   | (1,4,5) |       (6)       |       (7)        |                         |      X      |

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

(7) Tan, C.-Y. & Huang, Y.-X. *Dependence of Refractive Index on Concentration and Temperature in Electrolyte Solution, Polar Solution, Nonpolar Solution, and Protein Solution.* J. Chem. Eng. Data 60, 2827–2833 (2015).

(8) Tang, I. N., Munkelwitz, H. R. & Wang, N. *Water activity measurements with single suspended droplets: The NaCl-H2O and KCl-H2O systems.* Journal of Colloid and Interface Science 114, 409–415 (1986).

(9) McKee, C. B., *An Accurate Equation for the Electrolytic Conductivity of Potassium Chloride Solutions*. J Solution Chem 38, 1155-1172 (2009).

(10) Tang, I. N. & Munkelwitz, H. R., *Simultaneous Determination of Refractive Index and Density of an Evaporating Aqueous Solution Droplet*. Aerosol Science and Technology 15, 201–207 (1991).

(11) Talreja-Muthreja, T., Linnow, K., Enke, D. & Steiger. *M. Deliquescence of NaCl Confined in Nanoporous Silica*. Langmuir 38, 10963-10974 (2022).


Constants
=========

The *constants.py* file includes useful values including critical point data, molecular weights of species, dissociation numbers etc. Use the function `molar_mass` to get the molar mass (in kg/mol) of a specific solute from the *solute_list*, e.g.:

```python
from aquasol.constants import Mw           # molar mass of water (kg/mol)
from aquasol.constants import molar_mass   # molar mass of specific solute
from aquasol.constants import charge_numbers        # charges z+ / z-
from aquasol.constants import dissociation_numbers  # nu+ / nu-

solute = 'Na2SO4'

molar_mass(solute)  # 0.142 kg/mol
z_m, z_x = charge_numbers[solute]          # (1, 2) for Na(1+), SO4(2-)
nu_m, nu_x = dissociation_numbers[solute]  # (2, 1) for Na(2) SO4(1)
```


Shortcut functions
==================

For rapid calculations without much typing, the following shortcuts are provided:

|       original function       | shortcut |
|:-----------------------------:|:--------:|
| `water.vapor_pressure()`      |  `ps()`  |
| `water.dewpoint()`            |  `dp()`  |
| `water.kelvin_pressure()`     |  `kp()`  |
| `water.kelvin_radius()`       |  `kr()`  |
| `water.kelvin_humidity()`     |  `kh()`  |
| `solutions.water_activity()`  |  `aw()`  |
| `solutions.aw_to_conc()`      |  `ac()`  |
| `solutions.convert()`         |  `cv()`  |

For example, the two following imports are equivalent:
```python
from aquasol.solutions import water_activity as aw
from aquasol import aw
```

Information
===========

Package requirements
--------------------
- numpy
- matplotlib (only if running the package directly as a main file to plot the properties)
- pynverse

Python requirements
-------------------
Python : >= 3.6

Author
------

Olivier Vincent

(ovinc.py@gmail.com)

Contributors
------------
Marine Poizat (2019), Léo Martin (2020)

License
-------
--- TO BE DETERMINED ---
