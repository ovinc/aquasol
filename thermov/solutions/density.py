""" Density of aqueous solutions."""

# TODO - add expression of Clegg & Wexler 2011 (eq. 24)
# TODO - add other salts (LiCl as priority, then KCl and CaCl2)
# TODO - add expression of Pitzer 1982 (source of CRC Handbook)
# TODO - Add tests (unittests)
# TODO - Check that Tang is indeed valid up to 80% weight fraction
# TODO - make more comprehensive examples


from ..tools import solution_calculation


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

    # Dictionary of modules to load for every solute -------------------------
    modules = {'NaCl': 'density_nacl'}

    # Calculate density using general solution calculation scheme -----------
    parameters = T, unit, concentration
    rho0, rho = solution_calculation(solute, source, modules, parameters)

    if relative:
        return rho / rho0
    else:
        return rho
