"""Surface tension of water and solutions."""

# TODO: Add solutes of interest among the various ones present in Dutcher (in particular KCl)


from ..tools import solution_calculation


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

    # Dictionary of modules to load for every solute -------------------------
    modules = {'NaCl': 'surface_tension_nacl',
               'LiCl': 'surface_tension_licl',
               'CaCl2': 'surface_tension_cacl2'}

    # Calculate surface tension using general solution calculation scheme ----
    parameters = T, unit, concentration
    sigma0, sigma = solution_calculation(solute, source, modules, parameters)

    if relative:
        return sigma / sigma0
    else:
        return sigma
