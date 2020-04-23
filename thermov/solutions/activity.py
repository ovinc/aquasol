"""Activity of aqueous solutions."""

# TODO: other temperatures than 25°C
# TODO: add other salts (LiCl as priority, then KCl, CaCl2, Na2S04)
# TODO: make more comprehensive examples
# TODO: Add tests (unittests)


from ..tools import format_temperature, format_concentration, import_solute_module
from ..checks import check_validity_range


def activity(solute='NaCl', T=25, unit='C', source=None, **kwargs):
    """Return water activity of an aqueous solution at a given concentration.

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
    - C= : molarity (mol/m^3)

    Output
    ------
    - Water activity (range 0-1)

    Sources
    -------
    NaCl: 'Clegg' (default)
    See details about the sources in the submodules.

    Examples
    --------
    - a_w(x=0.1) returns water activity for a 0.1 mole fraction solution
    - a_w(m=6) returns water activity for a 6 molality solution
    - a_w(w=0.2) returns water activity for a 0.2 mass fraction solution
    """

    # =============== IMPORT ADEQUATE SUBMODULE FOR CALCULATIONS =============

    modules = {'NaCl': 'activity_nacl'}

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
    a_w = formula(value, T)

    return a_w
