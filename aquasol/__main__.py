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
# from .solutions import activity_coefficient
# from .solutions import surface_tension as sigma_s, density
from .solutions import density
# from .solutions import refractive_index, electrical_conductivity
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
    for source, linestyle in zip(ppty.sources, linestyles):

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
    water_activity,
    density
)


# General plotting functions -------------------------------------------------

def plot_all_sources_conc(ppty, solute, T=25, unit='C', ctype='m', ax=None, norm=1):
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
    """
    for source, linestyle in zip(ppty.sources[solute], linestyles):
        formula = ppty.get_formula(solute=solute, source=source)

        cmin, cmax = formula.concentration_range
        cunit = formula.concentration_unit

        # The 0.999... is to avoid rounding making data out of range
        if source == 'Clegg' and ppty.quantity == 'density':
            c_max = cmax * 0.75
        else:
            c_max = cmax * 0.999

        cc_raw = np.linspace(cmin, c_max, npts)

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
        ax.plot(cc, data * norm, ls=linestyle, label=name)

    ax.legend()
    ax.set_xlabel(f'concentration ({concentration_unit})')
    ax.set_ylabel(f'{ppty.quantity.capitalize()} {ppty.unit}')


for ppty in solution_properties:
    fig, ax = plt.subplots()
    fig.suptitle('Solutions')
    for solute in ppty.solutes:
        plot_all_sources_conc(ppty, solute, ctype='m', ax=ax, norm=1)


# # Electrical Conductivity  ---------------------------------------------------

# solutes = ['KCl']

# for solute in solutes:

#     plot_all_sources_conc('electrical conductivity', solute, 0, 'C', norm=1,
#                           ctype=concentration_unit, ax=ax_s_conductivity)

#     plot_all_sources_conc('electrical conductivity', solute, 25, 'C', norm=1,
#                           ctype=concentration_unit, ax=ax_s_conductivity)

#     plot_all_sources_conc('electrical conductivity', solute, 50, 'C', norm=1,
#                           ctype=concentration_unit, ax=ax_s_conductivity)

# ax_s_conductivity.set_xlabel(f'concentration ({concentration_unit})')
# ax_s_conductivity.set_ylabel('electrical conductivity (S/m)')


# ================================ FINAL =====================================


fig_w.tight_layout()

plt.show()
