"""Functions for calculating the activity of water in glycerol-water solutions based on Zhang 2022.

Source
------
- Zhang, L., Grace, P. M. & Sun, D.-W. 
An accurate water activity model for glycerol solutions and its implementation on moisture sorption isotherm determination.
Drying Technology 40, 2404-2413 (2022).
"""


import numpy as np

def water_activity_glycerol(x, T):
    """
    Calculate the activity of water in a glycerol-water solution based on mole fraction and temperature (K).

    Wilson model from:
    Zhang, L., Grace, P. M. & Sun, D.-W.
    An accurate water activity model for glycerol solutions and its implementation on moisture sorption isotherm determination.
    Drying Technology 40, 2404-2413 (2022).
    """
    a12 = 0.89924067
    a21 = -1.9173013
    b12 = 127.07511
    b21 = 91.465969
    v1 = 0.0188311
    v2 = 0.08685

    y = 1 - x

    term1 = - np.log(1 + (v2 / v1) * (x / y) * np.exp(-(a12 + b12 / T)))
    term2 = (x / y) / ((v1 / v2) * np.exp(a12 + b12 / T) + x / y)
    term3 = - ((x / y) * (v2 / v1) * np.exp(-(a12 + b12 / T))) / (x / y + (v1 / v2) * np.exp(-(a21 + b21/T)))

    lnaw = term1 + term2 + term3
    return np.exp(lnaw)
