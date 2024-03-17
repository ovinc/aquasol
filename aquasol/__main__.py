"""Plot properties of water and solutions."""

# General imports (non-standard)
import matplotlib.pyplot as plt
import numpy as np

# Local imports
from .format import format_temperature, format_concentration

from .water import vapor_pressure, surface_tension as sigma_w
from .water import density_atm, density_sat
from .water import diffusivity_in_air, viscosity_atm

from .solutions import water_activity
from .solutions import activity_coefficient
from .solutions import surface_tension as sigma_s
from .solutions import density
from .solutions import refractive_index, electrical_conductivity
from .solutions import solubility
from .solutions import convert


npts = 200

temperature_unit = 'C'
concentration_unit = 'm'

LINESTYLES = [
    '-',
    '--',
    '-.',
    ':',
    (5, (10, 3)),             # long dash with offset
    (0, (3, 1, 1, 1, 1, 1)),  # densely dashdotdotted
    (0, (3, 5, 1, 5, 1, 5)),  # dashdotdotted
]


# ================================ WATER =====================================


faxs = plt.subplots(2, 3)
fig_w, ((ax_w_psat, ax_w_sigma, ax_w_rho), (ax_w_diff, ax_w_visc, _)) = faxs

fig_w.suptitle('Water')

water_properties = (
    vapor_pressure,
    sigma_w,
    density_sat,
    density_atm,
    diffusivity_in_air,
    viscosity_atm,
)

# General plotting functions -------------------------------------------------

def plot_all_sources(ppty, ax, norm=1):
    """Plot all available sources for a given property

    Inputs
    ------
    ppty: property object/function (e.g. surface_tension, vapor_pressure etc.)
    ax: Matplotlib axes in which to plot the data
    norm (float): normalization factor for plotting the property (default 1)
    """
    for source, linestyle in zip(ppty.sources, LINESTYLES):

        formula = ppty.get_formula(source)

        tmin, tmax = formula.temperature_range
        unit = formula.temperature_unit

        tt_raw = np.linspace(tmin, tmax, npts)
        tt = format_temperature(tt_raw, unit, temperature_unit)

        data = ppty(T=tt, unit=temperature_unit, source=source)
        ax.plot(tt, data * norm, ls=linestyle, label=source)

    ax.legend()
    ax.set_xlabel(f'T ({temperature_unit})')
    ax.set_ylabel(f'{ppty.quantity.capitalize()} {ppty.unit}')


# Plots
plot_all_sources(vapor_pressure, ax_w_psat, norm=1e-3)
ax_w_psat.set_ylabel('Vapor pressure [kPa]')

plot_all_sources(sigma_w, ax_w_sigma, norm=1e3)
ax_w_sigma.set_ylabel('Surface tension [mN/m]')

plot_all_sources(density_sat, ax_w_rho)
plot_all_sources(density_atm, ax_w_rho)
ax_w_rho.set_ylabel('Density [kg / m^3]')

plot_all_sources(diffusivity_in_air, ax_w_diff)
plot_all_sources(viscosity_atm, ax_w_visc)


# # ============================== SOLUTIONS ===================================


solution_properties = (
    activity_coefficient,
    water_activity,
    density,
    sigma_s,
    refractive_index,
    electrical_conductivity,
)

COLORS = {
    'NaCl': 'cornflowerblue',
    'KCl': 'darkblue',
    'LiCl': 'lightblue',
    'KI': 'darkgreen',
    'MgCl2': 'gold',
    'CaCl2': 'orange',
    'Na2SO4': 'brown',
}


# General plotting functions -------------------------------------------------

def plot_all_sources_conc(
    ppty,
    solute,
    T=25,
    unit='C',
    ctype='m',
    ax=None,
    norm=1,
    linestyle=None,
    color=None,
):
    """Plot all available sources for a given property/solute as a function of concentration

    Inputs
    ------
    ppty: property object/function (e.g. surface_tension, density etc.)
    solute (str): name of solute (e.g. 'NaCl')
    T, unit : temperature and temperature unit
    ctype: unit of concentration to plot the data (e.g. 'x', 'm', 'c' etc.)
    relative (bool): if True, use the relative option when applicable
    ax: Matplotlib axes in which to plot the data
    norm (float): normalization factor for plotting the property (default 1)
    linestyle, color: if not None, override default COLORS/LINESTYLES
    """
    for source, ls in zip(ppty.sources[solute], LINESTYLES):
        formula = ppty.get_formula(solute=solute, source=source)

        cmin, cmax = formula.concentration_range
        cunit = formula.concentration_unit

        # The 0.999... is to avoid rounding making data out of range
        if source == 'Clegg' and ppty.quantity == 'density':
            c_max = cmax * 0.75
        else:
            c_max = cmax * 0.999

        c_min = cmin if cmin == 0 else 1.001 * cmin

        cc_raw = np.linspace(c_min, c_max, npts)

        cc = format_concentration(
            concentration={cunit: cc_raw},
            unit_out=ctype,
            solute=solute,
            converter=convert,
        )

        kwargs = {
            'solute': solute,
            'T': T,
            'unit': unit,
            'source': source,
            ctype: cc,
        }

        data = ppty(**kwargs)

        name = f"{solute}, {source} (T={T})"

        plot_kwargs = {'label': name}
        plot_kwargs['color'] = COLORS[solute] if color is None else color
        plot_kwargs['ls'] = ls if linestyle is None else linestyle

        ax.plot(cc, data * norm, **plot_kwargs)

    ax.legend()
    ax.set_xlabel(f'concentration ({concentration_unit})')
    ax.set_ylabel(f'{ppty.quantity.capitalize()} {ppty.unit}')


for ppty in solution_properties:
    fig, ax = plt.subplots()
    fig.suptitle('Solutions')
    for solute in ppty.solutes:
        kwargs = {'ctype': 'm', 'ax': ax, 'norm': 1}
        plot_all_sources_conc(ppty, solute, **kwargs)
        if ppty.quantity == 'electrical conductivity':
            plot_all_sources_conc(ppty, solute, T=0, linestyle=':', **kwargs)
            plot_all_sources_conc(ppty, solute, T=50, linestyle='--', **kwargs)
    fig.tight_layout()


# ---------------------------- Solubility diagrams ---------------------------

fig, ax = plt.subplots()


# KCl and LiCl --------------

T_KCl = np.linspace(0, 50)
T_LiCl = np.linspace(10, 25)

sol_KCl = solubility('KCl', T=T_KCl)
sol_LiCl = solubility('LiCl', T=T_LiCl)

ax.plot(T_KCl, sol_KCl, '-', c=COLORS['KCl'], label='KCl')
ax.plot(T_LiCl, sol_LiCl, '-', c=COLORS['LiCl'], label='LiCl')


# NaCl --------------

T_hydrohalite = np.linspace(-10, 0.1)
T_halite = np.linspace(0.1, 50)

sol_hydrohalite = solubility('NaCl,2H2O', T=T_hydrohalite)
sol_halite = solubility('NaCl', T=T_halite)

c = COLORS['NaCl']

ax.plot(T_hydrohalite, sol_hydrohalite, '--', c=c, label='NaCl,2H2O (hydrohalite)')
ax.plot(T_halite, sol_halite, '-', c=c, label='NaCl (halite)')


# Na2SO4 ----------

T_mirabilite = np.linspace(0, 32.38)
T_thenardite = np.linspace(0, 50)

sol_mirabilite = solubility('Na2SO4,10H2O', T=T_mirabilite)
sol_thenardite = solubility('Na2SO4', T=T_thenardite)

c = COLORS['Na2SO4']

ax.plot(T_mirabilite, sol_mirabilite, '--', c=c, label='Na2SO4,10H2O (mirabilite)')
ax.plot(T_thenardite, sol_thenardite, '-', c=c, label='Na2SO4 (thenardite)')


# -----------------

ax.set_xlabel('T (°C)')
ax.set_ylabel('$m_\mathrm{sat}$ [mol/kg]')
ax.set_xlim(-10, 50)
ax.grid()
ax.legend()


# ================================ FINAL =====================================


fig_w.tight_layout()
plt.show()
