"""Gathers the formulas for the refractive index of NaCl solutions.

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

import numpy as np

# General Info about the formulas

default_source = 'Tan'

concentration_types = {'Tan': 'w',
                       }

concentration_ranges = {'Tan': (0, 0.25),
                        }

temperature_units = {'Tan': 'C',
                     }

temperature_ranges = {'Tan': (20, 45),
                      }


# ============================== FORMULAS ====================================


def n_tan(w, T):

    c = w * 100  # avoid using *= to not mutate objects in place

    n0 = 1.3373
    a1, a2 = 1.7682e-3, 0 # modified -5.8e-6 to 0 to fit the data adequately
    b1, b2 = -1.3531e-4, -5.1e-8

    return n0 + a1 * c + a2 * c**2 + b1 * T + b2 * T**2


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Tan': n_tan,
            }

sources = [source for source in formulas]

# ====================== DIRECT RUN (test of formulas) =======================

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np

    from aquasol.solutions import refractive_index

    # This shows that the quadratic term in the Tan paper for concentration is
    # not correct and should be ignored 

    ws = 0.01, 0.05, 0.10, 0.15, 0.20, 0.25  # experimental weight fraction
    ww = np.linspace(0, 0.25, 100)           # weight fraction for fit

    nexps = {25: [1.3359, 1.3428, 1.3514, 1.3604, 1.3692, 1.3788], # 25°C
             45: [1.3333, 1.3398, 1.3485, 1.3572, 1.3661, 1.3757]} # 45°C

    fig, ax = plt.subplots()

    for T, ns in nexps.items():
        
        nn = refractive_index(w=ww, T=T)

        ax.plot(ws, ns, '.')
        ax.plot(ww, nn, '-')

    plt.show()