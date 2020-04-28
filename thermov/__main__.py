"""Plot properties of water and solutions."""

# TODO: plot solution properties as a function of temperature


import matplotlib.pyplot as plt
import numpy as np

from .format import format_temperature, format_concentration

from .water import vapor_pressure, surface_tension as sigma_w
from .water.general import get_infos as infos_water

from .solutions import water_activity, surface_tension as sigma_s, density
from .solutions.general import get_infos as infos_solutions
from .solutions import convert


npts = 100

temperature_unit = 'C'
concentration_unit = 'w'


# ================================ WATER =====================================


fig_w, (ax_w_psat, ax_w_sigma) = plt.subplots(1, 2)

fig_w.suptitle('Water')

functions = {'vapor pressure': vapor_pressure,
             'surface tension': sigma_w}


# General plotting functions -------------------------------------------------

def plot_all_sources(propty, ax, norm=1):
    """Plot all available sources for a given property

    Inputs
    ------
    propty (str): name of property (e.g. 'surface tension', 'vapor pressure')
    ax: Matplotlib axes in which to plot the data
    norm (float): normalization factor for plotting the property (default 1)
    """

    infos = infos_water(propty)
    func = functions[propty]

    for source in infos['sources']:

        tmin, tmax = infos['temp ranges'][source]
        unit = infos['temp units'][source]

        tt_raw = np.linspace(tmin, tmax, npts)
        tt = format_temperature(tt_raw, unit, temperature_unit)

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


fig_s_act, ax_s_act = plt.subplots()
fig_s_act.suptitle('Solutions, activity')

fig_s_surf, ax_s_surf = plt.subplots()
fig_s_surf.suptitle('Solutions, surface tension')

fig_s_dens, ax_s_dens = plt.subplots()
fig_s_dens.suptitle('Solutions, density')

functions = {'water activity': water_activity,
             'surface tension': sigma_s,
             'density': density}


# General plotting functions -------------------------------------------------

def plot_all_sources_conc(propty, solute, T, unit, ctype='m', relative=False, ax=None, norm=1):
    """Plot all available sources for a given property/solute as a function of concentration

    Inputs
    ------
    propty (str): name of property (e.g. 'surface tension', 'vapor pressure')
    solute (str): name of solute (e.g. 'NaCl')
    T, unit : temperature and temperature unit
    ctype: unit of concentration to plot the data (e.g. 'x', 'm', 'c' etc.)
    relative (bool): if True, use the relative option when applicable
    ax: Matplotlib axes in which to plot the data
    norm (float): normalization factor for plotting the property (default 1)
    """

    infos = infos_solutions(propty, solute)
    func = functions[propty]

    for source in infos['sources']:

        cmin, cmax = infos['conc ranges'][source]
        cunit = infos['conc units'][source]

        cc_raw = np.linspace(cmin, cmax, npts)

        concentration = {cunit: cc_raw}
        cc = format_concentration(concentration, ctype, solute, convert)
        concentration = {ctype: cc}

        if propty in ['surface tension', 'density']:
            pty = func(solute, T, unit, relative, source, **concentration)
        else:
            pty = func(solute, T, unit, source, **concentration)

        name = solute + ', ' + source
        ax.plot(cc, pty * norm, label=name)

    ax.legend()


# Activity -------------------------------------------------------------------

solutes = ['NaCl', 'LiCl', 'CaCl2']

for solute in solutes:
    plot_all_sources_conc('water activity', solute, 25, 'C',
                          ctype=concentration_unit, ax=ax_s_act)

ax_s_act.set_xlabel(f'concentration ({concentration_unit})')
ax_s_act.set_ylabel(f'a_w')


# Surface tension ------------------------------------------------------------

solutes = ['NaCl', 'LiCl', 'CaCl2']

for solute in solutes:
    plot_all_sources_conc('surface tension', solute, 25, 'C', norm=1e3,
                          ctype=concentration_unit, ax=ax_s_surf, relative=False)

ax_s_surf.set_xlabel(f'concentration ({concentration_unit})')
ax_s_surf.set_ylabel(f'surface tension (mN/m)')


# Density --------------------------------------------------------------------

solutes = ['NaCl']

for solute in solutes:
    plot_all_sources_conc('density', solute, 25, 'C', norm=1e-3,
                          ctype=concentration_unit, ax=ax_s_dens, relative=False)

ax_s_dens.set_xlabel(f'concentration ({concentration_unit})')
ax_s_dens.set_ylabel(f'density (kg/m^3)')


# ================================ FINAL =====================================


fig_w.tight_layout()

plt.show()


