"""Surface tension of water and solutions."""

def main():
    pass


def surface_tension(T=25, unit='C', solute=None, **kwargs):
    """Surface tension of water as a function of temperature.

    Parameters
    ---------------------
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - substance (str): 'water' (no other option at the moment)
    - solute: None at the moment.

    KWARGS
    - m= : molality (mol/kg)
    - c= : molarity (mol/m^3)
    - w= : mass fraction
    - x= : mole fraction
    (not all available at the moment)

    Output
    ------
    - sigma (float): surface tension in SI units, i.e. N/m)

    Examples
    --------
    - surface_tension(20) returns the surface tension of pure water at 20°C
    - surface_tension(300, 'K') returns the value at 300K
    - surface_tension(20, solute='LiCl', w=0.1) returns the surface tension of
    a LiCl aqueous solution at 20°C and weight fraction 0.1.

    Sources
    -------
    
    - Pure water: IAPWS "Revised Release on Surface Tension of Ordinary Water 
    Substance" (2014). Valid between the triple point (0.01 °C) and  critical 
    temperature, Tc = 647.096K. Provides reasonably accurate values when 
    extrapolated into the  supercooled region, to temperatures as low as -25°C.

    - LiCl and CaCl2 solutions: Conde IJTS 2004. The range of validity seems
    to be 0-100°C in temperature, and 0-0.45 (approx) in weight fraction.
    """

    if unit == 'C':
        T += 273.15
    elif unit == 'K':
        pass
    else:
        raise ValueError(f'{unit} not a valid unit')

    Tc = 647.096  # critical temperature in K
    t = T /  Tc

    B = 235.8e-3
    b = -0.625
    mu = 1.256
    tau = (1 - t)

    sigma_w = B * tau ** mu * (1 + b*tau)

    if solute is None:
        return sigma_w
    else:
        if 'w' not in kwargs:
            raise ValueError('Units other than weight fraction not supported yet')
        else:
            w = kwargs['w']
                

    if solute in ['LiCl', 'CaCl2']:

        if solute == 'LiCl':
            s = [2.757115, -12.011299, 14.751818, 2.443204, -3.147739]
        else:  # CaCl2
            s = [2.33067, -10.78779, 13.56611, 1.95017, -1.77990]

        ratio = 1 + s[0]*w + s[1]*w*t + s[2]*w*t**2 + s[3]*w**2 + s[4]*w**3

        return sigma_w * ratio



if __name__ == '__main__':
    main()