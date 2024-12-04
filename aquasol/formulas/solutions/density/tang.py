"""Functions for the calculation of the density of solutions based on Tang 1997

Note:
    Tang 1997 cites other papers (e.g. Tang 1996) of his but compiles data
    in Table I. Some validity ranges (e.g. Na2SO4) are not correct in table I
    and I have taken them from the original sources.

Source
------
- Tang 1997 :
    Tang, I. N.
    Thermodynamic and optical properties of mixed-salt aerosols of atmospheric
    importance. Journal of Geophysical Research 102, 1883-1893 (1997).

Cites :

[NaCl]
Tang, I. N.
Chemical and size effects of hygroscopic aerosols on light scattering
coefficients.
Journal of Geophysical Research: Atmospheres 101, 19245-19250 (1996).

[Na2SO4]
Tang, I. N. & Munkelwitz, H. R.
Simultaneous Determination of Refractive Index and Density of an Evaporating
Aqueous Solution Droplet.
Aerosol Science and Technology 15, 201-207 (1991).

[Also Na2SO4]
Tang, I. N. & Munkelwitz, H. R.
Water activities, densities, and refractive indices of aqueous sulfates and
sodium nitrate droplets of atmospheric importance.
Journal of Geophysical Research 99, 18801 (1994).

[KCl]
Couldn't find the info in these other papers except Tang 1997
"""

from ...general import SolutionFormula


class Density_Tang_Base(SolutionFormula):

    source = 'Tang'
    solute = None  # define in subclasses

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'w'
    concentration_range = None  # define in subclasses

    with_water_reference = True

    def calculate(self, w, T):
        """From Tang 1996, only at 25°C"""
        w = w * 100
        rho0 = 997.1  # density of pure water (at 25°C)
        rho = rho0
        for i, coeff in enumerate(self.coeffs):
            rho += coeff * 1000 * w ** (i + 1)
        return rho0, rho


class Density_KCl_Tang_Base(Density_Tang_Base):
    solute = 'KCl'
    concentration_range = (0, 0.44)
    coeffs = (6.13e-3, 4.53e-5, -1.242e-6, 1.582e-8)


class Density_Na2SO4_Tang_Base(Density_Tang_Base):
    solute = 'Na2SO4'
    concentration_range = (0, 0.68)
    coeffs = (8.871e-3, 3.195e-5, 2.28e-7)


class Density_NaCl_Tang_Base(Density_Tang_Base):
    solute = 'NaCl'
    concentration_range = (0, 0.45)
    coeffs = (7.41e-3, -3.741e-5, 2.252e-6, -2.06e-8)
