"""Parameter conversions for water and solutions."""

from ions import molar_mass, ion_magnitude

def convert(value, unit1, unit2):
    """Convert between concentrations, molalities etc. for solutions.
    
    INPUTS
    - value is the value to convert
    - unit1 is its unit ('m' : molality, 'w' : mass fraction and 'x' : mole fraction)
    - unit2 is the final unit
    
    e.g. convert(0.4, 'w', 'x') to convert a mass fraction of 0.4 in mole fraction
    """
    
    M_w = molar_mass['water'] # molar mass of water, kg/mol
    M_NaCl = molar_mass['NaCl'] # molar mass of NaCl, kg/mol
    
    if unit1 == 'w' and unit2 == 'x': # convert mass fraction in mole fraction
            x_NaCl = value / (M_NaCl * (value / M_NaCl + (1 - value) / M_w))
            return x_NaCl
    elif unit1 == 'w' and unit2 == 'm': # convert mass fraction in molality
            m_NaCl = value / ((1 - value) * M_NaCl)
            return m_NaCl
    
    
    elif unit1 == 'm' and unit2 == 'x': # convert molality in mole fraction
            x_NaCl = (value * M_w) / (value * M_w + 1)
            return x_NaCl
    elif unit1 == 'm' and unit2 == 'w': # convert molality in mass fraction
            w_NaCl = 1 / (1 + (1 / (value * M_NaCl)))
            return w_NaCl
       
    
    elif unit1 == 'x' and unit2 == 'm': # convert mole fraction in molality
        m_NaCl = value / (M_w * (1 - value))
        return m_NaCl
    elif unit1 == 'x' and unit2 == 'w': # convert mole fraction in mass fraction
        w_NaCl = value * M_NaCl / (value * M_NaCl + (1 - value) * M_w)
        return w_NaCl
    

def I_x(ion1, ion2, **kwargs):
    """Return the mole fraction ionic strength of solute.
    
    For now, just for NaCl"""
    
    for key, value in kwargs.items():
        if key == 'x':
            x_solute = value # mole fraction of NaCl
        elif key == 'w':
            x_solute = convert(value, 'w', 'x') # mole fraction in function of mass fraction
        elif key == 'm': 
            x_solute = convert(value, 'm', 'x') # mole fraction in function of molality
        else:
            raise ValueError('Concentration parameter can be m, w or x')
    
    if ion1 == 'Na':
        z_ion1 = ion_magnitude['Na']
    if ion2 == 'Cl':
        z_ion2 = ion_magnitude['Cl']
    
    x_ion1 = x_solute / (1 + x_solute)
    x_ion2 = x_solute / (1 + x_solute)
    
    I = 0.5 * (x_ion1 * z_ion1**2 + x_ion2 * z_ion2**2) #ionic strength
    return I