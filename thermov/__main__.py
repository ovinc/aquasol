"""Plot properties and water and solutions."""

import matplotlib.pyplot as plt
import numpy as np

from .format import format_temperature


npts = 1000

temperature_unit = 'C'


# ================================ WATER =====================================

from .water import psat, surface_tension


fig_w, (ax_w_psat, ax_w_sigma) = plt.subplots(1, 2)

fig_w.suptitle('Water')


# Vapor pressure -------------------------------------------------------------


from .water.formulas.psat import sources, temperature_units, temperature_ranges

for source in sources:

    tmin, tmax = temperature_ranges[source]
    unit = temperature_units[source]

    tt_raw = np.linspace(tmin, tmax, npts)
    tt = format_temperature(tt_raw, unit, temperature_unit)

    pp = psat(tt, temperature_unit, source)

    ax_w_psat.plot(tt, pp / 1e3)

ax_w_psat.set_xlabel(f'T ({temperature_unit})')
ax_w_psat.set_ylabel(f'Psat (kPa)')


from .water.formulas.surface_tension import sources, temperature_units, temperature_ranges

for source in sources:

    tmin, tmax = temperature_ranges[source]
    unit = temperature_units[source]

    tt_raw = np.linspace(tmin, tmax, npts)
    tt = format_temperature(tt_raw, unit, temperature_unit)

    ss = surface_tension(tt, temperature_unit, source)

    ax_w_sigma.plot(tt, ss * 1e3)

ax_w_sigma.set_xlabel(f'T ({temperature_unit})')
ax_w_sigma.set_ylabel(f'Surf. Tension (mN / m)')


# ================================ FINAL =====================================


fig_w.tight_layout()

plt.show()


