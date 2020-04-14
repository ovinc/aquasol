"""Parameter conversions for water and solutions."""

from thermov.ions import molar_mass, ion_magnitude


def convert(value, unit1, unit2, solute='NaCl'):
    """Convert between concentrations, molalities etc. for solutions.

    Parameters
    ---------------------
    - value (float): value to convert
    - unit1 (str): its unit ('m' : molality, 'w' : mass fraction and 'x' : mole fraction)
    - unit2 (str): final unit (can also be 'I' to have the ionic strength)
    - solute (str): Just 'NaCl' for now 
    
    Examples
    --------
    - convert(0.4, 'w', 'x') convert a mass fraction of 0.4 in mole fraction
    - convert(10, 'm', 'w') convert a molality of 10 in mass fraction
    - convert(0.1, 'x', 'I') gives the mole fraction ionic strength for x = 0.1
    """
    
    M_w = molar_mass['water'] # molar mass of water, kg/mol
    M = molar_mass[solute] # molar mass of solute, kg/mol
    
    if solute == 'NaCl':
        z_ion1 = ion_magnitude['Na']
        z_ion2 = ion_magnitude['Cl']
    else:
        print('Other solutes than NaCl not supported yet')
    
    
    if unit1 == 'w' and unit2 == 'x': # convert mass fraction in mole fraction
        x = value / (M * (value / M + (1 - value) / M_w))
        return x
    elif unit1 == 'w' and unit2 == 'm': # convert mass fraction in molality
        m = value / ((1 - value) * M)
        return m
    elif unit1 == 'w' and unit2 == 'I': # compute mass fraction ionic strength
        w_solute = value
        if solute == 'NaCl':
            w_ion1 = w_solute * 0.3934 # mass percentage of Na in NaCl
            w_ion2 = w_solute * 0.6066 # mass percentage of Cl in NaCl
        I = 0.5 * (w_ion1 * z_ion1**2 + w_ion2 * z_ion2**2)
        return I
    
    
    elif unit1 == 'm' and unit2 == 'x': # convert molality in mole fraction
        x = 1 / (1 + (1 / (value * M_w)))
        return x
    elif unit1 == 'm' and unit2 == 'w': # convert molality in mass fraction
        w = 1 / (1 + (1 / (value * M)))
        return w
    elif unit1 == 'm' and unit2 == 'I': # compute molality ionic strength
        m_solute = value
        m_ion1 = m_solute 
        m_ion2 = m_solute
        I = 0.5 * (m_ion1 * z_ion1**2 + m_ion2 * z_ion2**2)
        return I
    
    
    elif unit1 == 'x' and unit2 == 'm': # convert mole fraction in molality
        m = value / (M_w * (1 - value))
        return m
    elif unit1 == 'x' and unit2 == 'w': # convert mole fraction in mass fraction
        w = value * M / (value * M + (1 - value) * M_w)
        return w
    elif unit1 == 'x' and unit2 == 'I': # compute mole fraction ionic strength
        x_solute = value
        x_ion1 = x_solute / (1 + x_solute)
        x_ion2 = x_solute / (1 + x_solute)
        I = 0.5 * (x_ion1 * z_ion1**2 + x_ion2 * z_ion2**2)
        return I