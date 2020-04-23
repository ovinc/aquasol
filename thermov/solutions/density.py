""" Density of pure water and aqueous solutions."""

# TODO - add expression of Clegg & Wexler 2011 (eq. 24)
# TODO - add other salts (LiCl as priority, then KCl and CaCl2)
# TODO - add expression of Pitzer 1982 (source of CRC Handbook)
# TODO - Add tests (unittests)
# TODO - Check that Tang is indeed valid up to 80% weight fraction
# TODO - make more comprehensive examples


from ..tools import format_temperature, format_concentration, import_solute_module
from ..checks import check_validity_range



def density(solute='NaCl', T=25, unit='C', relative=False, source=None, **kwargs):
    """Return the density of an aqueous solution at a given concentration.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - relative (bool, default False): True for relative density
    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    KWARGS
    Any unit that is allowed by convert(), e.g.
    - m= : molality (mol/kg)
    - w= : mass fraction
    - x= : mole fraction

    Output
    ------
    - density in kg/m^3 or relative density (dimensionless) if relative is True

    Sources
    -------
    NaCl: 'Simion' (default), 'Tang'
    See details about the sources in the submodules.

    Examples
    --------
    - density(30) returns the density of pure water at 30°C.
    - density(w=0.1) returns the density calculated with Simion equation
    for a mass fraction of 0.1 at a temperature of 25°C.
    - density(300, 'K', m=6) returns the value at 300K for a molality of 6 mol/kg
    - density(source='Tang', x=0.1) returns the value calculated with Tang
    equation for a mole fraction of 0.1
    """

    # =============== IMPORT ADEQUATE SUBMODULE FOR CALCULATIONS =============

    modules = {'NaCl': 'density_nacl'}

    (src, formulas, concentration_types, concentration_ranges, temperature_units,
     temperature_ranges) = import_solute_module(modules, solute, source)

    # Check and format temperature ---------------------------------------------
    T = format_temperature(T, unit, temperature_units[src])
    check_validity_range(T, src, temperature_units,
                         temperature_ranges, 'temperature')

    # Check and format concentration -------------------------------------------
    value = format_concentration(kwargs, concentration_types[src], solute)
    check_validity_range(value, src, concentration_types,
                         concentration_ranges, 'concentration')

    # ============================ MAIN CALCULATIONS ===========================

    formula = formulas[src]
    rho, rho0 = formula(value, T)

    if relative:
        return rho / rho0
    else:
        return rho
