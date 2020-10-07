from aquasol.water import vapor_pressure, surface_tension
from aquasol.water import density_sat, density_atm
from aquasol.water import dewpoint, kelvin_humidity, kelvin_radius
import numpy as np

# =========================== Test Vapor Pressure ============================

def test_psat_1():
    p = vapor_pressure(1)
    assert round(p) == 657

def test_psat_2():
    p1 = vapor_pressure(T=1)
    p2 = vapor_pressure(274.15, 'K')
    assert p1 == p2

def test_psat_3():
    p = vapor_pressure()
    assert round(p) == 3170

def test_psat_4():
    p = vapor_pressure(T=293, unit='K')
    assert type(p) is float

def test_psat_5():
    p = vapor_pressure(T=[5, 15, 25])
    assert type(p) is np.ndarray

def test_psat_6():
    p = vapor_pressure(T=[5, 15, 25])
    assert p.shape == (3,)

def test_psat_7():
    p = vapor_pressure(T=[5, 15, 25])
    assert round(p[1]) == 1706

# =========================== Test Surface Tension ===========================

def test_sigma_1():
    s = surface_tension(1)
    assert round(s, 4) == 0.0755

def test_sigma_2():
    s1 = surface_tension(T=1)
    s2 = surface_tension(274.15, 'K')
    assert s1 == s2

def test_sigma_3():
    s = surface_tension()
    assert round(s, 3) == 0.072

def test_sigma_4():
    s = surface_tension(T=293, unit='K')
    assert type(s) is float

def test_sigma_5():
    s = surface_tension(T=[0, 60, 100])
    assert type(s) is np.ndarray

def test_sigma_6():
    s = surface_tension(T=[0, 60, 100])
    assert s.shape == (3,)

def test_sigma_7():
    s = surface_tension(T=[0, 60, 100])
    assert round(s[1], 3) == 0.066

# ========================= Test Atmospheric Density =========================

def test_rhoatm_1():
    rho = density_atm(4)
    assert round(rho) == 1000

def test_rhoatm_2():
    s1 = density_atm(T=1)
    s2 = density_atm(274.15, 'K')
    assert s1 == s2

def test_rhoatm_3():
    rho = density_atm()
    assert round(rho) == 997

def test_rhoatm_4():
    rho = density_atm(T=293, unit='K')
    assert type(rho) is float

def test_rhoatm_5():
    rho = density_atm(T=[0, 60, 100])
    assert type(rho) is np.ndarray

def test_rhoatm_6():
    rho = density_atm(T=[0, 60, 100])
    assert rho.shape == (3,)

def test_rhoatm_7():
    rho = density_atm(T=[0, 60, 100])
    assert round(rho[1]) == 983

# ========================== Test Saturated Density ==========================

def test_rhosat_1():
    rho = density_atm(4)
    assert round(rho) == 1000

def test_rhosat_2():
    s1 = density_atm(T=1)
    s2 = density_atm(274.15, 'K')
    assert s1 == s2

def test_rhosat_3():
    rho = density_atm()
    assert round(rho) == 997

def test_rhosat_4():
    rho = density_atm(T=293, unit='K')
    assert type(rho) is float

def test_rhosat_5():
    rho = density_atm(T=[0, 60, 100])
    assert type(rho) is np.ndarray

def test_rhosat_6():
    rho = density_atm(T=[0, 60, 100])
    assert rho.shape == (3,)

def test_rhosat_7():
    rho = density_atm(T=[0, 60, 100])
    assert round(rho[1]) == 983

# ============================== Test Dewpoint ===============================

def test_dewpoint_p_1():
    dp = dewpoint(p=1000)  # Dew point of a vapor at 1kPa
    assert round(dp, 1) == 7

def test_dewpoint_p_2():
    dp = dewpoint(p=1000, unit='K')  # Same, but temperature is returned in K
    assert round(dp, 1) == 280.1

def test_dewpoint_p_3():
    dp = dewpoint('K', p=1000)  # same thing
    assert round(dp, 1) == 280.1

def test_dewpoint_p_4():
    """Check that return float when input is single value."""
    dp = dewpoint(p=1000)
    assert type(dp) is float

def test_dewpoint_p_5():
    """Check that array returned when input is a list."""
    dp = dewpoint(p=[1000, 2000, 3000])
    assert type(dp) is np.ndarray

def test_dewpoint_p_6():
    """Check that length of array returned corresponds to input"""
    dp = dewpoint(p=[1000, 2000, 3000])
    assert dp.shape == (3,)

def test_dewpoint_p_7():
    """Check that values in array are ok."""
    dp = dewpoint(p=[1000, 2000, 3000])
    assert round(dp[2], 1) == 24.1

def test_dewpoint_rhaw_1():
    dp = dewpoint(rh=50)  # Dew point at 50%RH and 25°C (default)
    assert round(dp, 1) == 13.9

def test_dewpoint_rhaw_2():
    dp1 = dewpoint(rh=50)  # Dew point at 50%RH and 25°C (default)
    dp2 = dewpoint(aw=0.5)  # same thing
    assert dp1 == dp2

def test_dewpoint_rhaw_3():
    dp = dewpoint(aw=0.5, T=20)  # same thing, but at 20°C
    assert round(dp, 1) == 9.3

def test_dewpoint_rhaw_4():
    dp = dewpoint('K', 300, aw=0.5)  # same thing, but at 300K (dewpoint also in K)
    assert round(dp, 1) == 288.7

def test_dewpoint_rhaw_5():
    dp = dewpoint(rh=50)  # Single input should result in float output
    assert type(dp) is float

def test_dewpoint_rhaw_6():
    dp = dewpoint(aw=[0.3, 0.5, 0.7, 0.9])  # It is possible to input lists, tuples, arrays
    assert type(dp) is np.ndarray

def test_dewpoint_rhaw_7():
    dp = dewpoint(aw=[0.3, 0.5, 0.7, 0.9])
    assert dp.shape == (4,)

def test_dewpoint_rhaw_8():
    dp = dewpoint(aw=[0.3, 0.5, 0.7, 0.9])
    assert round(dp[3], 1) == 23.2

# ========================== Test Kelvin relations ===========================

# Radius ---------------------------------------------------------------------
def test_kelvin_radius_1():
    r = kelvin_radius(aw=0.8) * 1e9  # Kelvin radius at 80%RH and T=25°C
    assert round(r, 1) == 4.7

def test_kelvin_radius_2():
    r = kelvin_radius(rh=80) * 1e9           # same
    assert round(r, 1) == 4.7

def test_kelvin_radius_3():
    r = kelvin_radius(rh=80, ncurv=1) * 1e9   # assume cylindrical meniscus instead of spherical
    assert round(r, 2) == 2.35

def test_kelvin_radius_4():
    r = kelvin_radius(p=1000, T=20) * 1e9      # at 1000Pa, 20°C
    assert round(r, 2) == 1.27

def test_kelvin_radius_5():
    r = kelvin_radius(p=1000, T=293.15, unit='K') * 1e9      # same
    assert round(r, 2) == 1.27

def test_kelvin_radius_6():
    r = kelvin_radius(aw=[0.5, 0.7, 0.9]) * 1e9    # possible to use iterables
    assert round(r[1], 2) == 2.94

# Humidity ---------------------------------------------------------------------

def test_kelvin_humidity_1():
    a = kelvin_humidity(4.7e-9)  # activity corresponding to Kelvin radius of 4.7 nm at 25°C
    assert round(a, 2) == 0.80

def test_kelvin_humidity_2():
    rh = kelvin_humidity(4.7e-9, out='rh')  # same, but expressed in %RH instead of activity
    assert round(rh) == 80

def test_kelvin_humidity_3():
    p = kelvin_humidity(4.7e-9, out='p')  # same, but in terms of pressure (Pa)
    assert round(p) == 2536

def test_kelvin_humidity_4():
    p = kelvin_humidity(4.7e-9, out='p', T=293.15, unit='K')  # at a different temperature
    assert round(p) == 1860

def test_kelvin_humidity_5():
    a = kelvin_humidity(4.7e-9, ncurv=1)  # cylindrical interface
    assert round(a, 2) == 0.89

def test_kelvin_humidity_6():
    aa = kelvin_humidity([3e-9, 5e-9])  # with iterables
    assert round(aa[1], 2) == 0.81
