""" Functions to calculate the density of glycerol-water solutions using Volk formulas.
Volk, A. & Kähler, C. J. Density model for aqueous glycerol solutions. Exp Fluids 59, 75 (2018).
"""

import numpy as np

def glycerol_density(T):
    """
    Calculate the density (kg/m^3) of pure glycerol based on temperature (K).
    """
    return 1273 - 0.612*T # kg/m^3

def water_density(T):
    """
    Calculate the density (kg/m^3) of pure water based on temperature (K).
    """
    return 1000 * (1 - np.abs((T - 3.98) / 615) ** 1.71) # kg/m^3

def density_water_glycerol(w, T):
    """
    Calculate the density (kg/m^3) of a glycerol-water solution based on mass fraction of glycerol and T.
    """
    A = 1.78e-6 * T**2 - 1.82e-4 * T + 1.41e-2
    kappa = 1 + A * np.sin(w**1.31 * np.pi)**0.81

    return kappa * (water_density(T) + w * (glycerol_density(T) - water_density(T)) / (w + (glycerol_density(T) / water_density(T)) * (1 - w))) # kg/m^3
