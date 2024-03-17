"""Main module to calculate the properties of aqueous solutions."""

# TODO: add densities expression of Clegg & Wexler 2011 (eq. 24)
# TODO: add expression of Pitzer 1982 (source of CRC Handbook)
# TODO: write more comprehensive examples


from .convert import convert

from ..properties import SolutionProperty, SolutionSolubilityProperty

from ..formulas.solutions.activity_coefficient import ActivityCoefficientFormulas
from ..formulas.solutions.water_activity import WaterActivityFormulas
from ..formulas.solutions.density import DensityFormulas
from ..formulas.solutions.surface_tension import SurfaceTensionFormulas
from ..formulas.solutions.electrical_conductivity import ElectricalConductivityFormulas
from ..formulas.solutions.refractive_index import RefractiveIndexFormulas
from ..formulas.solutions.solubility import SolubilityFormulas


class SolutionProperty_Full(SolutionProperty):
    """Solution property with full converter (including molarity).

    Is used to prevent circular import problems
    (because SolutionProperty is also used to define the density function used
    in convert())
    """
    # See SolutionProperty for explanation of necessity of staticmethod()
    converter = staticmethod(convert)


class ActivityCoefficient(SolutionProperty_Full):
    """Molal activity coefficient (Ɣ) of solute in a solution (a_s = Ɣ * m / mref)

    Examples
    --------
    - activity_coefficient(m=6.1)  # at saturation for NaCl
    - activity_coefficient(solute='KCl', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    Formulas = ActivityCoefficientFormulas
    quantity = 'activity coefficient'
    unit = '[-]'


class WaterActivity(SolutionProperty_Full):
    """Water activity of a solution(aq) at given concentration and temperature

    Examples
    --------
    - water_activity(x=0.1) returns a_w for a mole fraction of 0.1 of NaCl
    - water_activity(w=0.2) returns a_w for a mass fraction of 0.2 of NaCl
    - water_activity(c=5000) returns a_w for a molality of 5 mol/L of NaCl
    - water_activity(m=6) returns a_w for a molality of 6 mol/kg of NaCl
    - water_activity('LiCl', m=6): same for LiCl
    - water_activity('LiCl', m=6, T=30): same for LiCl at 30°C
    - water_activity('LiCl', 293, 'K', m=6): same for LiCl at 293K.
    - water_activity(solute='CaCl2', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    Formulas = WaterActivityFormulas
    quantity = 'water activity'
    unit = '[-]'


class Density(SolutionProperty_Full):
    """Density of a solution(aq) at a given concentration and temperature

    Examples
    --------
    - density(w=0.1) returns the density of a NaCl solution, calculated with
    Simion equation for a mass fraction of 0.1 at a temperature of 25°C.
    - density('LiCl', 300, 'K', m=6) density of a LiCl solution at 300K
    for a molality of 6 mol/kg.
    - density(source='Tang', x=0.1), density of NaCl solution at a mole
    fraction of 0.1, calculated with the equation from Tang.
    - density(c=5000, relative=True), relative density of NaCl solution at
    a concentration of 5 mol/L.
    """
    Formulas = DensityFormulas
    quantity = 'density'
    unit = '[kg/m^3]'


class SurfaceTension(SolutionProperty_Full):
    """Surface tension of a solution(aq) at a given concentration and temperature

    Examples
    --------
    - surface_tension(x=0.05) returns surface tension of an aqueous NaCl
    solution at 25°C and a mole fraction of 5%
    - surface_tension('LiCl', w=0.1) returns the surface tension of a LiCl
    solution at 25°C and weight fraction of 10%
    - surface_tension('CaCl2', 20, m=6) returns the surface tension of
    a CaCl2 solution at 20°C and molality 6 mol/kg
    - surface_tension('CaCl2', 300, 'K', c=5e3) returns the surface tension of
    a CaCl2 solution at 300K and molarity of 5 mol/L
    - surface_tension(x=[0.02, 0.04, 0.08])  # iterable concentration is ok
    """
    Formulas = SurfaceTensionFormulas
    quantity = 'surface tension'
    unit = '[N/m]'


class ElectricalConductivity(SolutionProperty_Full):
    """Electrical conductivity of an aqueous solution at a given concentration.

    Examples
    --------
    - electrical_conductivity(c=1000)  # 1 molar NaCl conductivity
    - electrical_conductivity(solute='KCl', m=0.1)
    - electrical_conductivity(solute='KCl, m=2.2, T=50)  # at 50°C

    (Note: arrays are accepted for concentration and temperature)
    """
    Formulas = ElectricalConductivityFormulas
    quantity = 'electrical conductivity'
    unit = '[S/m]'


class RefractiveIndex(SolutionProperty_Full):
    """Refractive index of a solution as a function of concentration and temperature

    Examples
    --------
    - refractive_index(x=0.1) returns n for a mole fraction of 0.1 of NaCl
    - refractive_index(w=0.2) returns n for a mass fraction of 0.2 of NaCl
    - refractive_index(c=5000) returns n for a molality of 5 mol/L of NaCl
    - refractive_index(m=3) returns n for a molality of 6 mol/kg of NaCl
    - refractive_index('KCl', m=3): same for KCl
    - refractive_index('KCl', m=3, T=30): same for KCl at 30°C
    - refractive_index('KCl', 293, 'K', m=3): same for KCl at 293K.
    """
    Formulas = RefractiveIndexFormulas
    quantity = 'refractive index'
    unit = '[-]'


class Solubility(SolutionSolubilityProperty):
    """Solubility as a function of temperature.

    Examples
    --------
    - solubility()                   # solubility (molality) of NaCl at 25°C
    - solubility(T=40)               # solubility (molality) of NaCl at 40°C
    - solubility(T=40, out='x')      # same, but in terms of mole fraction
    - solubility(T=40, out='c')      # same, but in terms of molarity (mol/m^3)
    - solubility('KCl', T=303.15, unit='K')  # solubility of KCl at 30°C
    - solubility(T=[0, 10, 20, 30])          # iterables accepted too
    - solubility('Na2SO4')           # solubility of Na2SO4 at 25°C
    """
    Formulas = SolubilityFormulas
    quantity = 'solubility'
    converter = staticmethod(convert)


# ================ GENERATE USABLE OBJECTS FROM ABOVE CLASSES ================

activity_coefficient = ActivityCoefficient()
water_activity = WaterActivity()
density = Density()
surface_tension = SurfaceTension()
electrical_conductivity = ElectricalConductivity()
refractive_index = RefractiveIndex()
solubility = Solubility()


# # ================================== ACTIVITY ================================


# def activity_coefficient(solute='NaCl', T=25, unit='C', source=None, **concentration):
#     """Molal activity coefficient (Ɣ) of solute in a solution (a_s = Ɣ * m / mref)

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin

#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - Activity coefficient of solute (dimensionless)

#     Solutes and Sources
#     -------------------
#     (* = default)
#     KCl: 'Steiger 2008'(*), 'Tang'
#     Na2SO4: 'Steiger 2005', 'Steiger 2008'(*)
#     NaCl (default solute): 'Steiger 2005', 'Steiger 2008'(*), 'Tang'

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - activity_coefficient(m=6.1)  # at saturation for NaCl
#     - activity_coefficient(solute='KCl', T=50, m=[2, 4, 6])  # concentration as iterable
#     """
#     gamma = calculation(
#         propty='activity coefficient',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     return format_output_type(gamma)


# def water_activity(solute='NaCl', T=25, unit='C', source=None, **concentration):
#     """Return water activity of an aqueous solution at a given concentration.

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin

#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - Water activity (range 0-1)

#     Solutes and Sources
#     -------------------
#     (* = default)
#     CaCl2: 'Conde'(*)
#     KCl: 'Steiger 2008'(*), 'Tang'
#     LiCl: 'Conde'(*)
#     Na2SO4: 'Clegg', 'Steiger 2005', 'Steiger 2008'(*)
#     NaCl (default solute): 'Clegg' (*), 'Tang', 'Steiger 2005', 'Steiger 2008'

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - water_activity(x=0.1) returns a_w for a mole fraction of 0.1 of NaCl
#     - water_activity(w=0.2) returns a_w for a mass fraction of 0.2 of NaCl
#     - water_activity(c=5000) returns a_w for a molality of 5 mol/L of NaCl
#     - water_activity(m=6) returns a_w for a molality of 6 mol/kg of NaCl
#     - water_activity('LiCl', m=6): same for LiCl
#     - water_activity('LiCl', m=6, T=30): same for LiCl at 30°C
#     - water_activity('LiCl', 293, 'K', m=6): same for LiCl at 293K.
#     - water_activity(solute='CaCl2', T=50, m=[2, 4, 6])  # concentration as iterable
#     """
#     a_w = calculation(
#         propty='water activity',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     return format_output_type(a_w)


# # =================================== DENSITY ================================


# def density(solute='NaCl', T=25, unit='C', relative=False, source=None, **concentration):
#     """Return the density of an aqueous solution at a given concentration.

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
#     - relative (bool, default False): True for relative density

#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - density (kg/m^3) or relative density (dimensionless) if relative is True

#     Solutes and Sources
#     -------------------
#     (* = default)
#     CaCl2: 'Conde'(*), 'Al Ghafri', 'Krumgalz'
#     KCl: 'Al Ghafri'(*), 'Krumgalz'
#     KI: 'Al Ghafri'(*), 'Krumgalz'
#     LiCl: 'Conde'(*), 'Krumgalz'
#     MgCl2: 'Al Ghafri'(*), 'Krumgalz'
#     Na2SO4: 'Tang'(*), 'Clegg', 'Krumgalz'
#     NaCl (default solute): 'Simion'(*), 'Tang', 'Al Ghafri',
#                            'Steiger', 'Krumgalz', 'Clegg'

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - density(w=0.1) returns the density of a NaCl solution, calculated with
#     Simion equation for a mass fraction of 0.1 at a temperature of 25°C.
#     - density('LiCl', 300, 'K', m=6) density of a LiCl solution at 300K
#     for a molality of 6 mol/kg.
#     - density(source='Tang', x=0.1), density of NaCl solution at a mole
#     fraction of 0.1, calculated with the equation from Tang.
#     - density(c=5000, relative=True), relative density of NaCl solution at
#     a concentration of 5 mol/L.
#     """
#     rho0, rho = calculation(
#         propty='density',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     if relative:
#         return format_output_type(rho / rho0)
#     else:
#         return format_output_type(rho)


# # ============================== SURFACE TENSION =============================


# def surface_tension(solute='NaCl', T=25, unit='C', relative=False, source=None, **concentration):
#     """Surface tension of a solution as a function of concentration and temperature

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
#     - relative (bool, default False): True to normalize with pure water at T.

#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - sigma (float): surface tension (absolute in N/m or relative).

#     Solutes and Sources
#     -------------------
#     (* = default)
#     CaCl2: 'Dutcher'(*), 'Conde'
#     KCl: 'Dutcher'(*)
#     LiCl: 'Conde'(*)
#     MgCl2: 'Dutcher'(*)
#     Na2SO4: 'Dutcher'(*)
#     NaCl (default solute): 'Dutcher'(*), 'Steiger'

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - surface_tension(x=0.05) returns surface tension of an aqueous NaCl
#     solution at 25°C and a mole fraction of 5%
#     - surface_tension('LiCl', w=0.1) returns the surface tension of a LiCl
#     solution at 25°C and weight fraction of 10%
#     - surface_tension('CaCl2', 20, m=6) returns the surface tension of
#     a CaCl2 solution at 20°C and molality 6 mol/kg
#     - surface_tension('CaCl2', 300, 'K', c=5e3) returns the surface tension of
#     a CaCl2 solution at 300K and molarity of 5 mol/L
#     - surface_tension(x=[0.02, 0.04, 0.08])  # iterable concentration is ok
#     """
#     s0, s = calculation(
#         propty='surface tension',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     if relative:
#         return format_output_type(s / s0)
#     else:
#         return format_output_type(s)


# # =================================== OPTICS =================================


# def refractive_index(solute='NaCl', T=25, unit='C', source=None, **concentration):
#     """Refractive index of a solution as a function of concentration and temperature

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - n (float): refractive index (dimensionless)

#     Solutes and Sources
#     -------------------
#     (* = default)
#     CaCl2: 'Tan'(*),
#     KCl: 'Tan'(*)
#     NaCl (default solute): 'Tan'(*)

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - refractive_index(x=0.1) returns n for a mole fraction of 0.1 of NaCl
#     - refractive_index(w=0.2) returns n for a mass fraction of 0.2 of NaCl
#     - refractive_index(c=5000) returns n for a molality of 5 mol/L of NaCl
#     - refractive_index(m=3) returns n for a molality of 6 mol/kg of NaCl
#     - refractive_index('KCl', m=3): same for KCl
#     - refractive_index('KCl', m=3, T=30): same for KCl at 30°C
#     - refractive_index('KCl', 293, 'K', m=3): same for KCl at 293K.
#     """
#     n = calculation(
#         propty='refractive index',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     return format_output_type(n)


# # ================================= ELECTRICAL ===============================


# def electrical_conductivity(solute='NaCl', T=25, unit='C', source=None, **concentration):
#     """Return electrical conductivity of an aqueous solution at a given concentration.

#     Parameters
#     ----------
#     - solute (str): solute name, default 'NaCl'
#     - T (float): temperature (default 25)
#     - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin

#     - source (str, default None) : Source for the used equation, if None then
#     gets the default source for the particular solute (defined in submodules).
#     See summary of available sources below.

#     - **concentration: kwargs with any unit that is allowed by convert(), e.g.
#         - m= : molality (mol/kg)
#         - w= : mass fraction
#         - x= : mole fraction
#         - c= : molarity (mol/m^3)
#         - r= : mass ratio (unitless)

#     Output
#     ------
#     - Electrical conductivity (S/m)

#     Solutes and Sources
#     -------------------
#     (* = default)
#     KCl: 'McKee'(*)
#     NaCl (default solute): 'Sinmyo'(*)

#     See details about the sources in the submodules and Readme file.

#     Examples
#     --------
#     - electrical_conductivity(c=1000)  # 1 molar NaCl conductivity
#     - electrical_conductivity(solute='KCl', m=0.1)
#     - electrical_conductivity(solute='KCl, m=2.2, T=50)  # at 50°C

#     (Note: arrays are accepted for concentration and temperature)
#     """
#     sigma = calculation(
#         propty='electrical conductivity',
#         solute=solute,
#         source=source,
#         parameters=(T, unit, concentration),
#         converter=convert,
#     )
#     return format_output_type(sigma)
