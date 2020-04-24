"""Surface tension of pure water as a function of temperature."""


from ..constants import Tc
from ..checks import check_validity_range
from ..tools import format_temperature


def surface_tension(T=25, unit='C', source='IAPWS'):
    """Formula of surface tension as a function of T, according to IAPWS.

    Input
    -----
    T: Temperature (default 25)
    unit: unit of temperature ('C' or 'K', default 'C')
    source: only 'IAPWS' for now.

    Output
    ------
    Surface tension in N/m

    Reference
    ---------
    IAPWS, Release on Surface Tension of Ordinary Water Substance,
    IAPWS, London, September 1994.

    Notes
    -----
    - Used by Conde2004 and Dutcher2010 for the surface tension of solutions.
    - Valid between triple point (0.01°C) and critical temperature 647.096K.
    It also provides reasonably accurate values when extrapolated into the
    supercooled region, to temperatures as low as -25°C.
    """

    src = 'IAPWS'

    temperature_units = {'IAPWS': 'K'}
    temperature_ranges = {'IAPWS': (248.15, Tc)}   # Here I have included the extrapolated range

    T = format_temperature(T, unit, temperature_units[src])

    check_validity_range(T, src, temperature_units,
                         temperature_ranges, 'temperature')

    tau = (1 - T / Tc)

    B = 235.8e-3
    b = -0.625
    mu = 1.256

    sigma = B * tau ** mu * (1 + b * tau)  # in N / m

    return sigma



