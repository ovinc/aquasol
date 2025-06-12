"""Module for convenience functions related to solutions in pores"""


from aquasol.solutions import water_activity, aw_to_conc, convert


def pore_aw_from_drop_conc(
    drop_volume: float,
    pore_volume: float,
    solute: str = 'NaCl',
    T: float = 25.0,
    **concentration,
) -> float:
    """Calculate water activity in pores from a given drop volume and concentration

    Parameters
    ----------
    drop_volume : float
    pore_volume : float
        both drop_volume and pore_volume must be in the same units (e.g. µL)

    solute : str
        name of the solute, e.g. 'NaCl', 'glycerol', etc.

    T : float
        temperature in °C

    concentration : kwargs
        concentration input as required by aquasol, e.g.
        m=2 for molality of 2 mol / kg
        c=2300 for molarity of 2.3 mol / L
        x=0.12 for mole fraction of 12%
        etc.

    Returns
    -------
    float
        Water activity a_w in the pore solution (0 < a_w <= 1)
    """
    c_unit, = concentration.keys()
    c_value, = concentration.values()
    c_drop = convert(c_value, c_unit, 'c', T=T, solute=solute)
    c_pore = c_drop * drop_volume / pore_volume
    return water_activity(solute=solute, T=T, c=c_pore)


def drop_conc_from_pore_aw(
    a: float,
    drop_volume: float,
    pore_volume: float,
    out='m',
    solute: str = 'NaCl',
    T: float = 25.0,
) -> float:
    """Calculate concentration in droplet to achieve desired pore water activity

    Parameters
    ----------
    drop_volume : float
    pore_volume : float
        both drop_volume and pore_volume must be in the same units (e.g. µL)

    out : str
        Unit of output (e.g. 'x' for mole fraction, 'm' for molality, etc.)

    solute : str
        name of the solute, e.g. 'NaCl', 'glycerol', etc.

    T : float
        temperature in °C

    Returns
    -------
    float
        solute concentration in droplet
    """
    c_pore = aw_to_conc(a, solute=solute, T=T, out='c')
    c_drop = c_pore * pore_volume / drop_volume
    return convert(c_drop, 'c', out, solute=solute, T=T)
