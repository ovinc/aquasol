"""Plot properties of water and solutions."""

# TODO: plot solution properties as a function of temperature


# General imports (non-standard)
import matplotlib.pyplot as plt
import numpy as np

# Local imports
from .format import format_temperature, format_concentration

from .water import vapor_pressure, surface_tension as sigma_w
from .water import density_atm, density_sat
from .water import diffusivity_in_air, viscosity_atm

from .water.general import get_infos as infos_water

from .solutions import activity_coefficient, water_activity
from .solutions import surface_tension as sigma_s, density
from .solutions import refractive_index, electrical_conductivity
from .solutions.general import get_infos as infos_solutions
from .solutions import convert


npts = 200

temperature_unit = 'C'
concentration_unit = 'w'

linestyles = [
    '-',
    '--',
    '-.',
    ':',
    (5, (10, 3)),             # long dash with offset
    (0, (3, 1, 1, 1, 1, 1)),  # densely dashdotdotted
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdotted
]


# ================================ WATER =====================================


fig_w, ((ax_w_psat, ax_w_sigma, ax_w_rho), (ax_w_diff, ax_w_visc, _)) = plt.subplots(2, 3)

fig_w.suptitle('Water')

functions = {'vapor pressure': vapor_pressure,  # names have to match general.py
             'surface tension': sigma_w,
             'density saturated': density_sat,
             'density ambient': density_atm,
             'diffusivity in air': diffusivity_in_air,
             'viscosity ambient': viscosity_atm,
             }


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

    for source, linestyle in zip(infos['sources'], linestyles):

        tmin, tmax = infos['temp ranges'][source]
        unit = infos['temp units'][source]

        tt_raw = np.linspace(tmin, tmax, npts)
        tt = format_temperature(tt_raw, unit, temperature_unit)

        pty = func(tt, temperature_unit, source)

        ax.plot(tt, pty * norm, ls=linestyle, label=source)

    ax.legend()


# Vapor pressure -------------------------------------------------------------

plot_all_sources('vapor pressure', ax_w_psat, 1e-3)

ax_w_psat.set_xlabel(f'T ({temperature_unit})')
ax_w_psat.set_ylabel(f'Psat (kPa)')


# Surface tension ------------------------------------------------------------

plot_all_sources('surface tension', ax_w_sigma, 1e3)

ax_w_sigma.set_xlabel(f'T ({temperature_unit})')
ax_w_sigma.set_ylabel(f'Surf. Tension (mN / m)')

# Density (saturated) --------------------------------------------------------

plot_all_sources('density saturated', ax_w_rho)

ax_w_rho.set_xlabel(f'T ({temperature_unit})')
ax_w_rho.set_ylabel(f'Density (kg / m^3)')

# Density (ambient) ----------------------------------------------------------

plot_all_sources('density ambient', ax_w_rho)

ax_w_rho.set_xlabel(f'T ({temperature_unit})')
ax_w_rho.set_ylabel(f'Density (kg / m^3)')

# Diffusivity in air ---------------------------------------------------------

plot_all_sources('diffusivity in air', ax_w_diff)

ax_w_diff.set_xlabel(f'T ({temperature_unit})')
ax_w_diff.set_ylabel(f'Diffusivity (m^2 / s)')

# Viscosity ------------------------------------------------------------------

plot_all_sources('viscosity ambient', ax_w_visc)

ax_w_visc.set_xlabel(f'T ({temperature_unit})')
ax_w_visc.set_ylabel(f'Viscosity (Pa.s)')


# ============================== SOLUTIONS ===================================


fig_s_act, ax_s_act = plt.subplots()
fig_s_act.suptitle('Solutions, water activity')

fig_s_gamma, ax_s_gamma = plt.subplots()
fig_s_gamma.suptitle('Solutions, activity coefficient')

fig_s_surf, ax_s_surf = plt.subplots()
fig_s_surf.suptitle('Solutions, surface tension')

fig_s_dens, ax_s_dens = plt.subplots()
fig_s_dens.suptitle('Solutions, density')

fig_s_index, ax_s_index = plt.subplots()
fig_s_index.suptitle('Solutions, refractive index')

fig_s_conductivity, ax_s_conductivity = plt.subplots()
fig_s_conductivity.suptitle('Solutions, electrical conductivity')

functions = {
    'activity coefficient': activity_coefficient,
    'water activity': water_activity,
    'surface tension': sigma_s,
    'density': density,
    'refractive index': refractive_index,
    'electrical conductivity': electrical_conductivity,
}


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

    for source, linestyle in zip(infos['sources'], linestyles):

        cmin, cmax = infos['conc ranges'][source]
        cunit = infos['conc units'][source]

        # The 0.999... is to avoid rounding making data out of range
        cc_raw = np.linspace(cmin, cmax * 0.99999, npts)

        concentration = {cunit: cc_raw}
        cc = format_concentration(concentration, ctype, solute, convert)
        concentration = {ctype: cc}

        if propty in ['surface tension', 'density']:
            pty = func(solute, T, unit, relative, source, **concentration)
        else:
            pty = func(solute, T, unit, source, **concentration)

        name = f"{solute} , {source} (T={T})"
        ax.plot(cc, pty * norm, ls=linestyle, label=name)

    ax.legend()


# Activity coefficient -------------------------------------------------------

solutes = ['NaCl', 'KCl', 'Na2SO4']

for solute in solutes:
    plot_all_sources_conc('activity coefficient', solute, 25, 'C',
                          ctype=concentration_unit, ax=ax_s_gamma)

ax_s_gamma.set_xlabel(f'concentration ({concentration_unit})')
ax_s_gamma.set_ylabel(r'$\gamma$')


# Activity -------------------------------------------------------------------

solutes = ['NaCl', 'LiCl', 'CaCl2', 'Na2SO4', 'KCl']

for solute in solutes:
    plot_all_sources_conc('water activity', solute, 25, 'C',
                          ctype=concentration_unit, ax=ax_s_act)

ax_s_act.set_xlabel(f'concentration ({concentration_unit})')
ax_s_act.set_ylabel(r'$a_w$')



# Surface tension ------------------------------------------------------------

solutes = ['NaCl', 'LiCl', 'CaCl2', 'KCl', 'Na2SO4', 'MgCl2']

for solute in solutes:
    plot_all_sources_conc('surface tension', solute, 25, 'C', norm=1e3,
                          ctype=concentration_unit, ax=ax_s_surf, relative=False)

ax_s_surf.set_xlabel(f'concentration ({concentration_unit})')
ax_s_surf.set_ylabel('surface tension (mN/m)')


# Density --------------------------------------------------------------------

solutes = ['NaCl', 'Na2SO4', 'CaCl2', 'KCl', 'KI', 'LiCl', 'MgCl2']

for solute in solutes:
    plot_all_sources_conc('density', solute, 25, 'C', norm=1e-3,
                          ctype=concentration_unit, ax=ax_s_dens, relative=False)

ax_s_dens.set_xlabel(f'concentration ({concentration_unit})')
ax_s_dens.set_ylabel('density (kg/m^3)')


# Refractive Index  ----------------------------------------------------------

solutes = ['NaCl', 'CaCl2', 'KCl']

for solute in solutes:
    plot_all_sources_conc('refractive index', solute, 25, 'C', norm=1,
                          ctype=concentration_unit, ax=ax_s_index)

ax_s_index.set_xlabel(f'concentration ({concentration_unit})')
ax_s_index.set_ylabel('refractive index')


# Electrical Conductivity  ---------------------------------------------------

solutes = ['KCl']

for solute in solutes:

    plot_all_sources_conc('electrical conductivity', solute, 0, 'C', norm=1,
                          ctype=concentration_unit, ax=ax_s_conductivity)

    plot_all_sources_conc('electrical conductivity', solute, 25, 'C', norm=1,
                          ctype=concentration_unit, ax=ax_s_conductivity)

    plot_all_sources_conc('electrical conductivity', solute, 50, 'C', norm=1,
                          ctype=concentration_unit, ax=ax_s_conductivity)

ax_s_conductivity.set_xlabel(f'concentration ({concentration_unit})')
ax_s_conductivity.set_ylabel('electrical conductivity (S/m)')


# ================================ FINAL =====================================


fig_w.tight_layout()

plt.show()
