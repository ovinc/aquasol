"""Gathers the formulas for the refractive index of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter:
- n (index of refraction, dimensionless)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Tan (default) : "Dependence of Refractive Index on Concentration and
Temperature in Electrolyte Solution, Polar Solution, Nonpolar Solution, and
Protein Solution", Tan & Huang, J. Chem. Eng. Data  (2015).
Valid from w = 0 to w = 0.25 and for temperatures between 20 and 45°C
"""

from .tan import RefractiveIndex_CaCl2_Tan_Base


class RefractiveIndex_CaCl2_Tan(RefractiveIndex_CaCl2_Tan_Base):
    """Already defined in tan module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

RefractiveIndexFormulas_CaCl2 = (
    RefractiveIndex_CaCl2_Tan,
)

# ====================== DIRECT RUN (test of formulas) =======================

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np

    from aquasol.solutions import refractive_index

    ws = 0.01, 0.05, 0.10, 0.15, 0.20, 0.25  # experimental weight fraction
    ww = np.linspace(0, 0.25, 100)           # weight fraction for fit

    nexps = {25: [1.3353, 1.3437, 1.3561, 1.3686, 1.3814, 1.3943], # 25°C
             45: [1.3331, 1.3414, 1.3539, 1.3662, 1.3789, 1.3920]} # 45°C

    fig, ax = plt.subplots()

    for T, ns in nexps.items():

        nn = refractive_index(w=ww, T=T, solute='CaCl2')

        ax.plot(ws, ns, '.')
        ax.plot(ww, nn, '-')

    plt.show()