"""Tests for the aquasol.solutions module."""

import numpy as np

from aquasol.solutions import activity_coefficient
from aquasol.solutions import water_activity
from aquasol.solutions import density
from aquasol.solutions import surface_tension
from aquasol.solutions import refractive_index
from aquasol.solutions import electrical_conductivity
from aquasol.solutions import solubility, aw_saturated

from aquasol.solutions import osmotic_coefficient, osmotic_pressure
from aquasol.solutions import aw_to_conc
from aquasol.solutions import convert

from aquasol.constants import molar_mass
from aquasol.constants import charge_numbers
from aquasol.constants import dissociation_numbers


# ============================== Test constants ==============================


def test_constants():
    solute = 'Na2SO4'
    assert round(molar_mass(solute), 3) == 0.142  # kg / mol
    assert charge_numbers[solute] == (1, 2)
    assert dissociation_numbers[solute] == (2, 1)


# # =========================== Test activity coeff ============================


def test_gamma_1():
    gamma = activity_coefficient(m=[6.1, 10])  # around saturation for NaCl
    assert round(gamma[0], 2) == 1.0

def test_gamma_2():
    gamma = activity_coefficient(m=0)  # at infinite dilution
    assert round(gamma, 2) == 1.0

def test_gamma_3():
    gamma = activity_coefficient(m=0, solute='KCl')  # at infinite dilution
    assert round(gamma, 2) == 1.0

def test_gamma_KCl():
    kwargs = {'c': 2000, 'solute': 'KCl'}
    g1 = activity_coefficient(source='Tang', **kwargs)
    g2 = activity_coefficient(source='Steiger 2008', **kwargs)
    assert (round(g1, 2) == round(g2, 2) == 0.57)

def test_gamma_KCl_supersaturated():
    g1 = activity_coefficient('KCl', T=5, m=6)
    g2 = activity_coefficient('KCl', T=45, m=6)
    assert round(np.log(g1), 2) == -0.56
    assert round(np.log(g2), 2) == -0.46

def test_gamma_Na2SO4():
    kwargs = {'m': 10, 'solute': 'Na2SO4'}
    g1 = activity_coefficient(source='Steiger 2005', **kwargs)
    g2 = activity_coefficient(source='Steiger 2008', **kwargs)
    assert round(g1, 2) == round(g2, 2) == 0.16

def test_gamma_NaCl():
    kwargs = {'x': 0.15, 'solute': 'NaCl'}
    g1 = activity_coefficient(source='Steiger 2005', **kwargs)
    g2 = activity_coefficient(source='Steiger 2008', **kwargs)
    g3 = activity_coefficient(source='Tang', **kwargs)
    assert (round(g1, 1) == round(g2, 1) == round(g3, 1) == 1.5)


# =========================== Test water activity ============================


def test_aw_1():
    aw = water_activity(x=0.1)  # a_w for a mole fraction of 0.1 of NaCl
    assert round(aw, 2) == 0.75

def test_aw_2():
    aw = water_activity(w=0.2)  # a_w for a mass fraction of 0.2 of NaCl
    assert round(aw, 2) == 0.84

def test_aw_3():
    aw = water_activity(c=5000)  # a_w for a molality of 5 mol/L of NaCl
    assert round(aw, 2) == 0.78

def test_aw_4():
    aw = water_activity(m=6)      # a_w for a molality of 6 mol/kg of NaCl
    assert round(aw, 2) == 0.76

def test_aw_5():
    aw = water_activity('LiCl', m=6)  # same for LiCl
    assert round(aw, 2) == 0.68

def test_aw_6():
    aw = water_activity('LiCl', m=6, T=70)  # same for LiCl at 70°C
    assert round(aw, 2) == 0.70

def test_aw_7():
    aw = water_activity('LiCl', 293, 'K', m=6)  # same for LiCl at 293K.
    assert round(aw, 2) == 0.68

def test_aw_8():
    aw = water_activity(solute='CaCl2', T=50, m=[2, 4, 6])  # iterable conc.
    assert round(aw[2], 2) == 0.45

def test_aw_9():
    aw = water_activity(solute='KCl', m=3)  # KCl
    assert round(aw, 2) == 0.90

def test_aw_10():
    """Check different formulas are consistent"""
    aw1 = water_activity(solute='Na2SO4', m=4, source='Clegg')
    aw2 = water_activity(solute='Na2SO4', m=4, source='Steiger 2005')
    aw3 = water_activity(solute='Na2SO4', m=4, source='Steiger 2008')
    assert round(aw1, 2) == 0.85
    assert round(aw2, 2) == 0.85
    assert round(aw3, 2) == 0.85

def test_aw_11():
    """Check CaCl2"""
    aw = water_activity('CaCl2', w=0.1)  # CaCl2
    assert round(aw, 2) == 0.94


# Test extensions of water activity ------------------------------------------


def test_osmotic_pressure():
    pi = osmotic_pressure(m=4)
    assert round(pi / 1e6, 1) == 22.1


def test_osmotic_coefficient():
    phi = osmotic_coefficient(w=0.27)
    assert round(phi, 1) == 1.3


# =============================== Test density ===============================


def test_rho_1():
    rho = density(w=0.1)  # NaCl solution, at mass fraction of 0.1 at 25°C.
    assert round(rho) == 1069

def test_rho_2():
    rho = density('LiCl', 300, 'K', m=6)  # LiCl solution at 300K, 6 mol/kg
    assert round(rho) == 1116

def test_rho_3():
    rho = density(source='Tang', x=0.23)  # supersaturatad NaCl, Tang equation
    assert round(rho) == 1419

def test_rho_4():
    rho = density(c=5000, relative=True)  # relative density of NaCl,  5 mol/L.
    assert round(rho, 2) == 1.19

def test_rho_5():
    rho = density(w=[0.05, 0.12, 0.25])  # iterable concentration
    assert round(rho[2]) == 1186

def test_rho_Na2SO4():
    rho = density('Na2SO4', w=0.5)
    assert round(rho) == 1549

def test_rho_MgCl2():
    rho = density('MgCl2', w=0.1)
    assert round(rho) == 1082

def test_rho_KI():
    rho = density('KI', w=0.1)
    assert round(rho) == 1074

def test_rho_KCl():
    rho = density('KCl', w=0.1)
    assert round(rho) == 1061

def test_rho_CaCl2():
    rho = density('CaCl2', w=0.1)
    assert round(rho) == 1082


# =========================== Test surface tension ===========================


def test_sigma_1():
    s = surface_tension(x=0.09)  # NaCl at 25°C and a mole fraction of 9%
    assert round(s, 3) == 0.080

def test_sigma_2():
    s = surface_tension('LiCl', w=0.1)  # LiCl, 25°C and weight fract. of 10%
    assert round(s, 3) == 0.076

def test_sigma_3():
    s = surface_tension('CaCl2', 20, m=6.6666)  # CaCl2, 20°C, devil molality
    assert round(s, 3) == 0.096

def test_sigma_4():
    s = surface_tension('CaCl2', 353.15, 'K', c=5e3)  # CaCl2, 80°C, 5 mol/L
    assert round(s, 3) == 0.087

def test_sigma_5():
    s = surface_tension(x=[0.02, 0.04, 0.06, 0.08, 0.1], T=21)  # iterable conc.
    assert round(s[4], 3) == 0.082


# ========================== Test refractive index ===========================


def test_n_1():
    n = refractive_index(x=0.08)  # mole fraction of 0.08 of NaCl
    assert round(n, 2) == 1.37

def test_n_2():
    n = refractive_index(w=0.2)  # mass fraction of 0.2 of NaCl
    assert round(n, 2) == 1.37

def test_n_3():
    n = refractive_index(c=4321)  # molality of 4.321 mol/L of NaCl
    assert round(n, 2) == 1.37

def test_n_4():
    n = refractive_index(m=3)   # molality of 6 mol/kg of NaCl
    assert round(n, 2) == 1.36

def test_n_5():
    n = refractive_index('KCl', m=1.6)  # KCl, 1.6 mol/kg, 25°C
    assert round(n, 2) == 1.35

def test_n_6():
    n = refractive_index('KCl', m=1.9, T=40)  # KCl at 40°C, 1.9 mol/kg
    assert round(n, 2) == 1.35

def test_n_7():
    n = refractive_index('KCl', 312, 'K', m=1.9)  # KCl at 312K, 1.9 mol/kg
    assert round(n, 2) == 1.35

def test_n_8():
    n = refractive_index('KCl', T=22, w=[0.05, 0.1, 0.15])  # iterable conc.
    assert round(n[2], 2) == 1.36


# ====================== Test electrical conductivity ========================


def test_conduc_concs():
    s1, s2, s3 = electrical_conductivity('KCl', m=[0.01, 0.1, 1])  # At 25°C
    assert round(s1, 4) == 0.1408
    assert round(s2, 3) == 1.282
    assert round(s3, 2) == 10.86


def test_conduc_temps():
    s_0, s_25, s_50 = electrical_conductivity('KCl', m=1, T=[0, 25, 50])
    assert round(s_0, 2) == 6.35
    assert round(s_25, 2) == 10.86
    assert round(s_50, 2) == 15.75



# ============================= Test solubility ==============================


def test_solubility_1():
    m_sat = solubility()          # solubility (molality) of NaCl at 25°C
    assert round(m_sat, 2) == 6.15

def test_solubility_2():
    m_sat = solubility(T=40)      # solubility (molality) of NaCl at 40°C
    assert round(m_sat, 2) == 6.22

def test_solubility_3():
    x_sat = solubility(out='x')   # solubility (mole fraction) of NaCl at 25°C
    assert round(x_sat, 2) == 0.1

def test_solubility_4():
    c_sat = solubility(out='c')   # solubility (molarity) of NaCl at 25°C
    assert round(c_sat / 1000, 1) == 5.4

def test_solubility_6():
    m_sat = solubility(T=[10, 15, 20, 25, 30])     # iterables accepted too
    assert round(m_sat[-2], 2) == 6.15

def test_solubility_7():
    """Must correspond to CRC Handbook values"""
    m_sat_10 = solubility(T=5, source='CRC Handbook')
    m_sat_40 = solubility(T=40, source='CRC Handbook')
    assert round(m_sat_10, 2) == 6.11
    assert round(m_sat_40, 2) == 6.22

def test_solubility_7():
    """Must correspond to CRC Handbook values"""
    m_sat_10 = solubility('LiCl', T=10)
    m_sat_25 = solubility('LiCl', T=25)
    assert round(m_sat_10, 3) == 19.296
    assert round(m_sat_25, 3) == 19.935

def test_solubility_KCl():
    s1 = solubility('KCl', out='w', T=290, unit='K')
    s2 = solubility('KCl', out='m', T=45)
    assert round(s1, 2) == 0.25
    assert round(s2, 1) == 5.6

def test_solubility_Na2SO4():
    T = 32.38  # This is the point of equilibrium thenardite/mirabilite
    s1 = solubility('Na2SO4', out='m', T=T)
    s2 = solubility('Na2SO4,10H2O', out='m', T=T)
    assert round(s1, 2) == round(s2, 2) == 3.51

def test_solubility_Halite():
    T = 0.1  # This is the point of equilibrium halite/hydrohalite
    s1 = solubility('NaCl', out='m', T=T)
    s2 = solubility('NaCl,2H2O', out='m', T=T)
    assert round(s1, 2) == round(s2, 2) == 6.10


# ------------------------- Extensions of solubility -------------------------

def test_aw_saturated_NaCl():
    aw_sat_25 = aw_saturated()     # NaCl at 25°C
    aw_sat_07 = aw_saturated(T=7)  # NaCl at 7°C
    assert round(100 * aw_sat_25, 1) == 75.3
    assert round(100 * aw_sat_07, 1) == 75.7

def test_aw_saturated_KCl():
    aw_sat_25 = aw_saturated('KCl')        # KCl at 25°C
    aw_sat_10 = aw_saturated('KCl', T=10)  # KCl at 10°C
    assert round(100 * aw_sat_25) == 84
    assert round(100 * aw_sat_10) == 87

def test_aw_saturated_4():
    aw_sat_25 = aw_saturated('LiCl')        # LiCl at 25°C
    aw_sat_10 = aw_saturated('LiCl', T=10)  # LiCl at 10°C
    assert round(100 * aw_sat_25) == 11
    assert round(100 * aw_sat_10) == 10

# =============================== Test convert ===============================

def test_convert_1():
    x = convert(0.4, 'w', 'x') # mass fraction 0.4 into mole fraction for NaCl
    assert round(x, 2) == 0.17

def test_convert_2():
    w = convert(10, 'm', 'w')  # molality 10 mol/kg into mass fraction of NaCl
    assert round(w, 2) == 0.37

def test_convert_3():
    w = convert(17, 'm', 'w', 'LiCl')  # 10 mol/kg of LiCl into mass fraction
    assert round(w, 2) == 0.42

def test_convert_4():
    x = convert(5120, 'c', 'x')  # 5.12 mol/m^3 to mole fraction, NaCl, 25°C
    assert round(x, 3) == 0.094

def test_convert_5():
    x = convert(3300, 'c', 'x', T=30)  # 3.3 mol/m^3 to x at 30°C
    assert round(x, 3) == 0.060

def test_convert_6():
    x = convert(3300, 'c', 'x', T=300, unit='K')  # same but at 300 K
    assert round(x, 3) == 0.060

def test_convert_7():
    x = convert(3300, 'c', 'x', solute='LiCl')  # LiCl at 25°C
    assert round(x, 3) == 0.060

def test_convert_8():
    x = convert([3300, 4400], 'c', 'x', solute='NaCl', T=40)  # iterable ok
    assert round(x[1], 3) == 0.081

def test_convert_9():
    m = convert(5305, 'c', 'm', density_source='Tang')  # different source
    assert round(m, 2) == 6


# # ========================= Test Inverse Functions ===========================


def test_ac_1():                # in terms of weight fracton
    w = aw_to_conc(0.45)
    assert round(w, 2) == 0.46

def test_ac_2():                # in terms of molality
    m = aw_to_conc([0.5, 0.75], out='m')
    assert round(m[1], 1) == 6.2

def test_ac_3():                # in terms of mass ratio, for LiCl, at 50°C
    r = aw_to_conc(0.11, 'r', 'LiCl', T=50)
    assert round(r, 2) == 0.92
