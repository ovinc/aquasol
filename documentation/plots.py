"""Here are some examples to plot water activity and solution density in NaCl
solutions,compare with experimental values and look at the dependence of
density with temperature.
"""


import numpy as np
import matplotlib.pyplot as plt

from thermov.activity import a_w
from thermov.density import density
from thermov.vapor_pressure import psat

activity_plot = True
activity_temperature = True #activity plot need to be True

density_plot = True
density_temperatures = [5, 20, 50] # used for the temperature-dependent plots

vapor_pressure_plot = True
temperature_range = [0, 50, 'C'] # temperature range for psat plot
                                 # last term is the unit, 'C' for Celsius, 'K' for Kelvin

# ============================== Activity plot ===============================

if activity_plot == True :

    # Experimental values : Chirife and Resnik -------------------------------

    #Chirife and Resnik, 25°C, source 1
    m0 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    a0 = [0.9967, 0.9934, 0.9901, 0.9868, 0.9836, 0.9803, 0.9769, 0.9736, 0.9702, 0.9669, 0.9601, 0.9532, 0.9497, 0.9461, 0.9389, 0.9316, 0.9127, 0.8932, 0.8727, 0.8515, 0.8295, 0.8068, 0.7836, 0.7598]

    #Chirife and Resnik, 15°C, source 3
    m5 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    a5 = [0.9966, 0.9934, 0.9901, 0.9869, 0.9836, 0.9803, 0.9771, 0.9738, 0.9705, 0.9671, 0.9501, 0.9322, 0.9137, 0.8945, 0.8743, 0.8532, 0.8314, 0.8088, 0.7857, 0.7621]

    #Chirife and Resnik, 37°C, source 3
    m6 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    a6 = [0.9966, 0.9934, 0.9901, 0.9868, 0.9835, 0.9802, 0.9768, 0.9735, 0.9701, 0.9667, 0.9492, 0.9310, 0.9121, 0.8925, 0.8720, 0.8508, 0.8290, 0.8066, 0.7834, 0.7596]

    #Chirife and Resnik, 50°C, source 2
    m7 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    a7 = [0.9967, 0.9934, 0.9901, 0.9868, 0.9835, 0.9802, 0.9768, 0.9735, 0.9701, 0.9666, 0.9597, 0.9527, 0.9491, 0.9455, 0.9382, 0.9308, 0.9118, 0.8921, 0.8716, 0.8505, 0.8288, 0.8066, 0.7840, 0.7611]

    #Chirife and Resnik, 60°C, source 1
    m8 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    a8 = [0.9967, 0.9934, 0.9901, 0.9868, 0.9835, 0.9802, 0.9768, 0.9734, 0.9666, 0.9490, 0.9305, 0.9113, 0.8917, 0.8714, 0.8497]

    # Experimental values : Clegg ------------ -------------------------------

    #Clegg 1997 source c (1st page of table 1)
    m1 = [3.20, 3.64, 3.84, 3.88, 4.01, 4.47, 4.60, 4.83, 5.15, 5.35, 5.50, 5.76, 5.94, 6.08, 6.36, 6.54, 6.70, 6.88, 7.07, 7.18, 7.40, 7.58, 7.74, 8.16, 8.44, 8.73, 8.88, 9.24, 9.51, 9.97, 10.51, 11.11, 11.48, 11.97, 12.47, 12.88]
    a1 = [0.8858, 0.8666, 0.8579, 0.8565, 0.8528, 0.8298, 0.8261, 0.8112, 0.7973, 0.7920, 0.7831, 0.7742, 0.7600, 0.7583, 0.7433, 0.7358, 0.7255, 0.7145, 0.7064, 0.7057, 0.6928, 0.6834, 0.6786, 0.6570, 0.6468, 0.6323, 0.6226, 0.6118, 0.6030, 0.5855, 0.5675, 0.5437, 0.5331, 0.5113, 0.5014, 0.4822]

    #Clegg 1997 1997 source a (2nd page of table 1, with n = 2)
    m2 = [11.12, 11.95, 12.68, 13.09, 13.45, 13.85, 14.15, 14.40, 14.62, 14.96, 15.31, 15.53, 15.80, 16.04, 16.20, 16.45, 16.68]
    a2 = [0.5347, 0.5133, 0.4947, 0.4821, 0.4697, 0.4612, 0.4534, 0.4489, 0.4403, 0.4328, 0.4258, 0.4195, 0.4121, 0.4067, 0.4028, 0.3967, 0.3911]

    #Clegg 1997 source a (1st and 2nd page of table 1, with n = 1)
    m3 = [10.75, 11.81, 12.36, 12.84, 13.16, 13.91, 14.39, 14.96, 15.44, 15.91, 16.60]
    a3 = [0.5380, 0.5140, 0.5012, 0.4843, 0.4797, 0.4571, 0.4473, 0.4313, 0.4182, 0.4076, 0.3959]

    #Clegg 1997 source a (1st and 2nd page of table 1, with n = 2*)
    m4 = [5.05, 5.60, 6.44, 7.41, 8.33, 9.21, 9.76, 10.27]
    a4 = [0.8104, 0.7833, 0.7401, 0.6856, 0.6430, 0.6056, 0.5778, 0.5561]


    # Plot : activity at 25°C ------------------------------------------------

    fig, ax = plt.subplots()
    molality = np.linspace(0, 16.68, 200)
    ax.plot(molality, a_w(m=molality), c='0', label='Clegg formula at 25°C')

    ax.scatter(m0, a0, c='none', ec='0.66', marker='o', label='Chirife & Resnik, source 1')
    ax.scatter(m1, a1, c='none', ec='0.5', marker='s', label='Clegg, source c')
    ax.scatter(m4, a4, c='none', ec='0.3', marker='H', label='Clegg, source a, n = 2*')
    ax.scatter(m2, a2, c='none', ec='0.2', marker='D', label='Clegg, source a, n = 2')
    ax.scatter(m3, a3, c='none', ec='0', marker='d', label='Clegg, source a, n = 1')


    ax.set_xlabel("Molality")
    ax.set_ylabel("Water activity")
    ax.legend()
    plt.show()

    # Plot : activity at various temperature ---------------------------------

    if activity_temperature == True:
        fig, ax = plt.subplots()

        ax.scatter(m5, a5, c='none', ec='0.66', marker='o', label='Chirife & Resnik, 15°C')
        ax.scatter(m0, a0, c='none', ec='0.5', marker='s', label='Chirife & Resnik, 25°C')
        ax.scatter(m6, a6, c='none', ec='0.35', marker='D', label='Chirife & Resnik, 37°C')
        ax.scatter(m7, a7, c='none', ec='0.2', marker='d', label='Chirife & Resnik, 50°C')
        ax.scatter(m8, a8, c='none', ec='0', marker='H', label='Chirife & Resnik, 60°C')

        ax.set_xlabel("Molality")
        ax.set_ylabel("Water activity")
        ax.legend()
        plt.show()


# =============================== Density plot ===============================

if density_plot == True:

    fig, ax = plt.subplots()

    mass_fraction1 = np.linspace(0, 0.26, 200)
    mass_fraction2 = np.linspace(0, 0.80, 200)
    ax.plot(mass_fraction2, density(source='Tang', w=mass_fraction2),c='0', label='Tang formula (25°C)')

    for T in density_temperatures:
        data = density(T, w=mass_fraction1)
        label = f'Simion et al. at {T}°C'
        ax.plot(mass_fraction1, data, label=label)

    ax.set_xlabel("Mass fraction")
    ax.set_ylabel("Solution density")
    ax.legend()
    plt.show()
# ========================= Water vapor pressure plot =========================

if vapor_pressure_plot == True:
    fig, ax = plt.subplots()
    T1 = np.linspace(temperature_range[0], temperature_range[1], 100)

    ax.plot(T1, psat(T1, temperature_range[2], source='Wexler17'), label='Wexler17')
    ax.plot(T1, psat(T1, temperature_range[2], source='Wexler18'), label='Wexler18')
    ax.plot(T1, psat(T1, temperature_range[2], source='Bridgeman'), label='Bridgeman')
    ax.plot(T1, psat(T1, temperature_range[2], source='Wagner'), label='Wagner')

    ax.set_xlabel(f"T ({temperature_range[2]})")
    ax.set_ylabel("Water vapor pressure")
    ax.legend()
    plt.show()