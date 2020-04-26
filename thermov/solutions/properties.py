"""Main module to calculate the properties of aqueous solutions.

NOTE: when modifying density, make sure to also change basic_density in convert.
"""

# TODO: add other salts (LiCl as priority, then KCl, CaCl2, Na2S04)
# TODO - add expression of Clegg & Wexler 2011 (eq. 24)
# TODO - add expression of Pitzer 1982 (source of CRC Handbook)
# TODO - Add tests (unittests)
# TODO - write more comprehensive examples
# TODO: other temperatures than 25°C



from .general import calculation
from .convert import convert as converter


# ================================== ACTIVITY ================================

def water_activity(solute='NaCl', T=25, unit='C', source=None, **concentration):
    """Return water activity of an aqueous solution at a given concentration.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature (default 25)
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin

    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    - **concentration: kwargs with any unit that is allowed by convert(), e.g.
        - m= : molality (mol/kg)
        - w= : mass fraction
        - x= : mole fraction
        - c= : molarity (mol/m^3)
        - mass_ratio= : mass ratio (unitless)

    Output
    ------
    - Water activity (range 0-1)

    Sources
    -------
    NaCl: 'Clegg' (default)
    See details about the sources in the submodules.

    Examples
    --------
    - water_activity(x=0.1) returns a_w for a mole fraction of 0.1 of NaCl
    - water_activity(w=0.2) returns a_w for a mass fraction of 0.2 of NaCl
    - water_activity(c=5000) returns a_w for a molality of 5 mol/L of NaCl
    - water_activity(m=6) returns a_w for a molality of 6 mol/kg of NaCl
    - water_activity('LiCl', m=6): same for LiCl
    - water_activity('LiCl', m=6, T=30): same for LiCl at 30°C
    - water_activity('LiCl', 293, 'K', m=6): same for LiCl at 293K.
    """

    parameters = T, unit, concentration
    a_w = calculation('water activity', solute, source, parameters, converter)

    return a_w


# =================================== DENSITY ================================

def density(solute='NaCl', T=25, unit='C', relative=False, source=None, **concentration):
    """Return the density of an aqueous solution at a given concentration.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature (default 25)
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - relative (bool, default False): True for relative density

    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    - **concentration: kwargs with any unit that is allowed by convert(), e.g.
        - m= : molality (mol/kg)
        - w= : mass fraction
        - x= : mole fraction
        - c= : molarity (mol/m^3)
        - mass_ratio= : mass ratio (unitless)

    Output
    ------
    - density (kg/m^3) or relative density (dimensionless) if relative is True

    Sources
    -------
    NaCl: 'Simion' (default), 'Tang'
    See details about the sources in the submodules.

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

    parameters = T, unit, concentration
    rho0, rho = calculation('density', solute, source, parameters, converter)

    if relative:
        return rho / rho0
    else:
        return rho


# ============================== SURFACE TENSION =============================

def surface_tension(solute='NaCl', T=25, unit='C', relative=False, source=None, **concentration):
    """Surface tension of a solution as a function of concentration and temperature

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature (default 25)
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - relative (bool, default False): True to normalize with pure water at T.

    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    - **concentration: kwargs with any unit that is allowed by convert(), e.g.
        - m= : molality (mol/kg)
        - w= : mass fraction
        - x= : mole fraction
        - c= : molarity (mol/m^3)
        - mass_ratio= : mass ratio (unitless)

    Output
    ------
    - sigma (float): surface tension (absolute in N/m or relative).

    Sources
    -------
    NaCl: 'Dutcher' (default)
    CaCl2: 'Dutcher' (default), 'Conde'
    LiCl: 'Conde' (default)
    See details about the sources in the submodules.

    Examples
    --------
    - surface_tension(x=0.05) the returns surface tension of an aqueous NaCl
    solution at 25°C and a mole fraction of 5%
    - surface_tension('LiCl', w=0.1) returns the surface tension of a LiCl
    solution at 25°C and weight fraction of 10%
    - surface_tension('CaCl2', 20, m=6) returns the surface tension of
    a CaCl2 solution at 20°C and molality 6 mol/kg
    - surface_tension('CaCl2', 300, 'K', c=5e3) returns the surface tension of
    a CaCl2 solution at 300K and molarity of 5 mol/L
    """

    parameters = T, unit, concentration
    s0, s = calculation('surface tension', solute, source, parameters, converter)

    if relative:
        return s / s0
    else:
        return s
