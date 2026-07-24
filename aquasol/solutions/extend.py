"""Extension of formulas from the properties of aqueous solutions.

e.g., osmotic_pressure instead of water_activity, etc.
"""

import numpy as np

from ..constants import R, Mw, Na, k, e, epsilon0, get_solute
from ..format import format_temperature, format_output_type, format_concentration
from ..water import molar_volume, dielectric_constant
from ..formulas.solutions.ionic import ionic_strength

from .convert import convert
from .properties import water_activity, solubility


def osmotic_pressure(solute='NaCl', T=25, unit='C', source=None, density_source=None, **concentration):
    """Return osmotic pressure of an aqueous solution at a given concentration.

    Basically the same as water_activity, but expressed as -RT/vm * log(a_w).

    Parameters
    ----------
    solute : str, optional
        Solute name. Default is 'NaCl'.
    T : float, optional
        Temperature. Default is 25.
    unit : str, optional
        Temperature unit ('C' or 'K'). Default is 'C'.
    source : str, optional
        Source for the used equation. If None, the default source for the
        particular solute is used. See summary of available sources below.
    density_source : str, optional
        Source for density in case the concentration involves molarities ('c').
    **concentration : kwargs
        Concentration in any unit allowed by `convert()`, e.g.:
        - `m`: molality (mol/kg)
        - `w`: mass fraction
        - `x`: mole fraction
        - `c`: molarity (mol/m^3)
        - `r`: mass ratio (unitless)

    Returns
    -------
    float or array-like
        Osmotic pressure (Π) in Pa.

    Solutes and Sources
    -------------------
    See `water_activity.solutes`, `water_activity.sources`,
    `water_activity.default_sources`, and README.md.

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
        density_source=density_source,
        **concentration,
    )
    T_kelvin = format_temperature(T=T, unit_in=unit, unit_out='K')
    pi = - R * T_kelvin / molar_volume(T=T_kelvin, unit='K') * np.log(a_w)
    return format_output_type(pi)


def osmotic_coefficient(solute='NaCl', T=25, unit='C', source=None, density_source=None, **concentration):
    """Return osmotic coefficient (Φ) of an aqueous solution at a given concentration.

    Basically the same as water_activity, but expressed as Φ.

    Parameters
    ----------
    solute : str, optional
        Solute name. Default is 'NaCl'.
    T : float, optional
        Temperature. Default is 25.
    unit : str, optional
        Temperature unit ('C' or 'K'). Default is 'C'.
    source : str, optional
        Source for the used equation. If None, the default source for the
        particular solute is used. See summary of available sources below.
    density_source : str, optional
        Source for density in case the concentration involves molarities ('c').
    **concentration : kwargs
        Concentration in any unit allowed by `convert()`, e.g.:
        - `m`: molality (mol/kg)
        - `w`: mass fraction
        - `x`: mole fraction
        - `c`: molarity (mol/m^3)
        - `r`: mass ratio (unitless)

    Returns
    -------
    float or array-like
        Osmotic coefficient (Φ), dimensionless.

    Solutes and Sources
    -------------------
    See `water_activity.solutes`, `water_activity.sources`,
    `water_activity.default_sources`, and README.md.

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
        density_source=density_source,
        **concentration,
    )
    m = format_concentration(
        concentration=concentration,
        unit_out='m',
        solute=solute,
        converter=convert,
        density_source=density_source,
    )
    salt = get_solute(formula=solute)
    nu_mx = sum(salt.stoichiometry)
    phi = - np.log(a_w) / (Mw * nu_mx * m)
    return format_output_type(phi)


def aw_saturated(
    crystal='NaCl',
    T=25,
    unit='C',
    activity_source=None,
    solubility_source=None,
):
    """Return water activity of the saturated solution.

    Basically the same as solubility, but expressed as a_w.

    Parameters
    ----------
    crystal : str, optional
        Crystal name. Default is 'NaCl'.
    T : float, optional
        Temperature. Default is 25.
    unit : str, optional
        Temperature unit ('C' or 'K'). Default is 'C'.
    activity_source : str, optional
        Source for the water activity equation. If None, the default source is used.
    solubility_source : str, optional
        Source for the solubility equation. If None, the default source is used.

    Returns
    -------
    float
        Water activity, dimensionless.

    Solutes and Sources
    -------------------
    See `solubility.solutes`, `solubility.sources`,
    `solubility.default_sources`, and README.md.

    Examples
    --------
    - aw_saturated()               # of NaCl at 25°C
    - aw_saturated('LiCl', T=15)   # of LiCl at 15°C
    """
    m_sat = solubility(
        crystal=crystal,
        T=T,
        unit=unit,
        source=solubility_source,
        out='m',
    )

    formula = solubility.get_formula(
        crystal=crystal,
        source=solubility_source,
    )

    a_w = water_activity(  # no need for density_source because m is used
        solute=formula.solute,
        T=T,
        unit=unit,
        source=activity_source,
        m=m_sat,
    )
    return a_w


def debye_length(solute='NaCl', T=25, unit='C', density_source=None, **concentration):
    """Return Debye length of an aqueous solution at a given concentration.

    NOTE: the dependence of water dielectric constant (epsilon) as a function
    of temperature is taken into account, but not as a function of concentration.
    TODO: Add concentration dependence.

    Parameters
    ----------
    solute : str, optional
        Solute name. Default is 'NaCl'.
    T : float, optional
        Temperature. Default is 25.
    unit : str, optional
        Temperature unit ('C' or 'K'). Default is 'C'.
    density_source : str, optional
        Source for density in case the concentration involves molarities ('c').
    **concentration : kwargs
        Concentration in any unit allowed by `convert()`, e.g.:
        - `m`: molality (mol/kg)
        - `w`: mass fraction
        - `x`: mole fraction
        - `c`: molarity (mol/m^3)
        - `r`: mass ratio (unitless)

    Returns
    -------
    float or array-like
        Debye length in meters.

    Solutes and Sources
    -------------------
    See `water_activity.solutes`, `water_activity.sources`,
    `water_activity.default_sources`, and README.md.

    Examples
    --------
    - debye_length(w=0.26)        # Debye length in saturated NaCl
    - debye_length(c=2.5, T=20)   # Debye length at 2.5 mM, 20°C
    """
    c = format_concentration(
        concentration=concentration,
        unit_out='c',
        solute=solute,
        converter=convert,
        density_source=density_source,
    )
    Ic = ionic_strength(solute=solute, c=c)
    epsilon = epsilon0 * dielectric_constant(T=T, unit=unit)
    T_kelvin = format_temperature(T=T, unit_in=unit, unit_out='K')
    l_squared = epsilon * k * T_kelvin / (2 * e**2 * Ic * Na)
    return l_squared**(1 / 2)
