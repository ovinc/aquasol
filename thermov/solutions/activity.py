"""Activity of aqueous solutions."""

# TODO: other temperatures than 25°C
# TODO: add other salts (LiCl as priority, then KCl, CaCl2, Na2S04)
# TODO: make more comprehensive examples
# TODO: Add tests (unittests)


from ..tools import solution_calculation


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

    # Dictionary of modules to load for every solute -------------------------
    modules = {'NaCl': 'activity_nacl'}

    # Calculate activity using general solution calculation scheme -----------
    parameters = T, unit, concentration
    a_w = solution_calculation(solute, source, modules, parameters)

    return a_w
