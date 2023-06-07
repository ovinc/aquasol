"""Tests for the aquasol.solutions module."""


from aquasol.solutions import activity_coefficient, water_activity
from aquasol.solutions import density, surface_tension
from aquasol.solutions import refractive_index, electrical_conductivity
from aquasol.solutions import aw_to_conc, convert

from aquasol.constants import molar_mass
from aquasol.constants import charge_numbers
from aquasol.constants import dissociation_numbers


# ============================== Test constants ==============================


def test_constants():
    solute = 'Na2SO4'
    assert round(molar_mass(solute), 3) == 0.142  # kg / mol
    assert charge_numbers[solute] == (1, 2)
    assert dissociation_numbers[solute] == (2, 1)


# =========================== Test activity coeff ============================


def test_gamma_1():
    gamma = activity_coefficient(m=6.1)  # around saturation for NaCl
    assert round(gamma, 2) == 1.0

def test_gamma_2():
    gamma = activity_coefficient(m=0)  # at infinite dilution
    assert round(gamma, 2) == 1.0

def test_gamma_3():
    gamma = activity_coefficient(m=0, solute='KCl')  # at infinite dilution
    assert round(gamma, 2) == 1.0


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
    s = surface_tension('CaCl2', 353, 'K', c=5e3)  # CaCl2, 300K, 5 mol/L
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


# ========================= Test Inverse Functions ===========================


def test_ac_1():                # in terms of weight fracton
    w = aw_to_conc(0.39)
    assert round(w, 2) == 0.49

def test_ac_2():                # in terms of molality
    m = aw_to_conc([0.39, 0.75], out='m')
    assert round(m[1], 1) == 6.2

def test_ac_3():                # in terms of mass ratio, for LiCl, at 50°C
    r = aw_to_conc(0.11, 'r', 'LiCl', T=50)
    assert round(r, 2) == 0.92
