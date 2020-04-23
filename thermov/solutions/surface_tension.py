"""Surface tension of water and solutions."""

# TODO: Add solutes of interest among the various ones present in Dutcher (in particular KCl)


from ..tools import format_temperature, format_concentration, import_solute_module
from ..checks import check_validity_range


def surface_tension(solute='NaCl', T=25, unit='C', relative=False, source=None, **kwargs):
    """Surface tension of a solution as a function of concentration and temperature

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - relative (bool, default False): True for relative surface tension
    (normalized by the surface tension of pure water at the same temperature).
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
    - sigma (float): surface tension in SI units, i.e. N/m

    Examples
    --------
    - surface_tension(20) returns the surface tension of pure water at 20°C
    - surface_tension(300, 'K') returns the value at 300K
    - surface_tension(20, solute='LiCl', w=0.1) returns the surface tension of
    a LiCl aqueous solution at 20°C and weight fraction 0.1
    - surface_tension(20, solute='CaCl2', m=6) returns the surface tension of
    a CaCl2 aqueous solution at 20°C and molality 6

    Sources
    -------
    NaCl: 'Dutcher' (default)
    CaCl2: 'Dutcher' (default), 'Conde'
    LiCl: 'Conde' (default)
    See details about the sources in the submodules.
    """

    # =============== IMPORT ADEQUATE SUBMODULE FOR CALCULATIONS =============

    modules = {'NaCl': 'surface_tension_nacl',
               'LiCl': 'surface_tension_licl',
               'CaCl2': 'surface_tension_cacl2'}

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
    sigma0, sigma = formula(value, T)

    if relative:
        return sigma / sigma0
    else:
        return sigma
