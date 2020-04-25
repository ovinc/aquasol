"""Plot properties and water and solutions."""

import matplotlib.pyplot as plt
import numpy as np

from .format import format_temperature

from .water import vapor_pressure, surface_tension
from .water.general import get_infos

from .solutions import water_activity


npts = 1000

temperature_unit = 'C'


# ================================ WATER =====================================


fig_w, (ax_w_psat, ax_w_sigma) = plt.subplots(1, 2)

fig_w.suptitle('Water')

functions = {'vapor pressure': vapor_pressure,
             'surface tension': surface_tension}


# General plotting functions -------------------------------------------------

def plot_all_sources(propty, ax, norm=1):
    """Plot all available sources for a given property

    Inputs
    ------
    propty (str): name of property (e.g. 'surface tension', 'vapor pressure')
    ax: Matplotlib axes in which to plot the data
    norm (float): normalization factor for plotting the property (default 1)
    """

    infos = get_infos(propty)

    for source in infos['sources']:

        tmin, tmax = infos['temp ranges'][source]
        unit = infos['temp units'][source]

        tt_raw = np.linspace(tmin, tmax, npts)
        tt = format_temperature(tt_raw, unit, temperature_unit)

        func = functions[propty]
        pty = func(tt, temperature_unit, source)

        ax.plot(tt, pty * norm, label=source)

    ax.legend()


# Vapor pressure -------------------------------------------------------------

plot_all_sources('vapor pressure', ax_w_psat, 1e-3)

ax_w_psat.set_xlabel(f'T ({temperature_unit})')
ax_w_psat.set_ylabel(f'Psat (kPa)')


# Surface tension ------------------------------------------------------------

plot_all_sources('surface tension', ax_w_sigma, 1e3)

ax_w_sigma.set_xlabel(f'T ({temperature_unit})')
ax_w_sigma.set_ylabel(f'Surf. Tension (mN / m)')


# ============================== SOLUTIONS ===================================


fig_s, ax_s_act = plt.subplots()

fig_s.suptitle('Solutions')

functions = {'vapor pressure': vapor_pressure,
             'surface tension': surface_tension}


# # General plotting functions -------------------------------------------------

# def plot_all_sources(propty, ax, norm=1):
#     """Plot all available sources for a given property

#     Inputs
#     ------
#     propty (str): name of property (e.g. 'surface tension', 'vapor pressure')
#     ax: Matplotlib axes in which to plot the data
#     norm (float): normalization factor for plotting the property (default 1)
#     """

#     infos = get_infos(propty)

#     for source in infos['sources']:

#         tmin, tmax = infos['temp ranges'][source]
#         unit = infos['temp units'][source]

#         tt_raw = np.linspace(tmin, tmax, npts)
#         tt = format_temperature(tt_raw, unit, temperature_unit)

#         func = functions[propty]
#         pty = func(tt, temperature_unit, source)

#         ax.plot(tt, pty * norm, label=source)

#     ax.legend()


# # Vapor pressure -------------------------------------------------------------

# plot_all_sources('vapor pressure', ax_w_psat, 1e-3)

# ax_w_psat.set_xlabel(f'T ({temperature_unit})')
# ax_w_psat.set_ylabel(f'Psat (kPa)')


# # Surface tension ------------------------------------------------------------

# plot_all_sources('surface tension', ax_w_sigma, 1e3)

# ax_w_sigma.set_xlabel(f'T ({temperature_unit})')
# ax_w_sigma.set_ylabel(f'Surf. Tension (mN / m)')



# ================================ FINAL =====================================


fig_w.tight_layout()

plt.show()


