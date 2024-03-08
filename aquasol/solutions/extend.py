"""Extension of formulas from the properties of aqueous solutions.

e.g., osmotic_pressure instead of water_activity, etc.
"""

import numpy as np

from ..constants import R, Mw, dissociation_numbers
from ..format import format_temperature, format_output_type, format_concentration
from ..water import molar_volume

from .convert import convert
from .properties import water_activity


def osmotic_pressure(solute='NaCl', T=25, unit='C', source=None, **concentration):
    """Return osmotic pressure of an aqueous solution at a given concentration.

    Basically the same as water_activity, but expressed as -RT/vm * log(a_w)

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
        - r= : mass ratio (unitless)

    Output
    ------
    - Osmotic pressure (Π) in Pa

    Solutes and Sources
    -------------------
    (* = default)
    CaCl2: 'Conde'(*)
    KCl: 'Steiger 2008'(*), 'Tang'
    LiCl: 'Conde'(*)
    Na2SO4: 'Clegg', 'Steiger 2005', 'Steiger 2008'(*)
    NaCl (default solute): 'Clegg' (*), 'Tang', 'Steiger 2005', 'Steiger 2008'

    See details about the sources in the submodules and Readme file.

    Examples
    --------
    - osmotic_pressure(x=0.1) returns Π for a mole fraction of 0.1 of NaCl
    - osmotic_pressure(w=0.2) returns Π for a mass fraction of 0.2 of NaCl
    - osmotic_pressure(c=5000) returns Π for a molality of 5 mol/L of NaCl
    - osmotic_pressure(m=6) returns Π for a molality of 6 mol/kg of NaCl
    - osmotic_pressure('LiCl', m=6): same for LiCl
    - osmotic_pressure('LiCl', m=6, T=30): same for LiCl at 30°C
    - osmotic_pressure('LiCl', 293, 'K', m=6): same for LiCl at 293K.
    - osmotic_pressure(solute='CaCl2', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    a_w = water_activity(
        solute=solute,
        T=T,
        unit=unit,
        source=source,
        **concentration,
    )
    T_kelvin = format_temperature(T=T, unit_in=unit, unit_out='K')
    pi = - R * T_kelvin / molar_volume(T=T_kelvin, unit='K') * np.log(a_w)
    return format_output_type(pi)


def osmotic_coefficient(solute='NaCl', T=25, unit='C', source=None, **concentration):
    """Return osmotic coefficient (Φ) of an aqueous solution at a given concentration.

    Basically the same as water_activity, but expressed as Φ

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
        - r= : mass ratio (unitless)

    Output
    ------
    - Osmotic coefficient (Φ), dimensionless

    Solutes and Sources
    -------------------
    (* = default)
    CaCl2: 'Conde'(*)
    KCl: 'Steiger 2008'(*), 'Tang'
    LiCl: 'Conde'(*)
    Na2SO4: 'Clegg', 'Steiger 2005', 'Steiger 2008'(*)
    NaCl (default solute): 'Clegg' (*), 'Tang', 'Steiger 2005', 'Steiger 2008'

    See details about the sources in the submodules and Readme file.

    Examples
    --------
    - osmotic_coefficient(x=0.1) returns Φ for a mole fraction of 0.1 of NaCl
    - osmotic_coefficient(w=0.2) returns Φ for a mass fraction of 0.2 of NaCl
    - osmotic_coefficient(c=5000) returns Φ for a molality of 5 mol/L of NaCl
    - osmotic_coefficient(m=6) returns Φ for a molality of 6 mol/kg of NaCl
    - osmotic_coefficient('LiCl', m=6): same for LiCl
    - osmotic_coefficient('LiCl', m=6, T=30): same for LiCl at 30°C
    - osmotic_coefficient('LiCl', 293, 'K', m=6): same for LiCl at 293K.
    - osmotic_coefficient(solute='CaCl2', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    a_w = water_activity(
        solute=solute,
        T=T,
        unit=unit,
        source=source,
        **concentration,
    )
    m = format_concentration(
        concentration=concentration,
        unit_out='m',
        solute=solute,
        converter=convert,
    )
    nu_mx = sum(dissociation_numbers[solute])
    phi = - np.log(a_w) / (Mw * nu_mx * m)
    return format_output_type(phi)
