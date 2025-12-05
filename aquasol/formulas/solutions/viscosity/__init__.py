"""Viscosity of solutions"""

from .NaCl import ViscosityFormulas_NaCl
from .KCl import ViscosityFormulas_KCl
from .LiCl import ViscosityFormulas_LiCl

ViscosityFormulas = (
    ViscosityFormulas_NaCl +
    ViscosityFormulas_KCl +
    ViscosityFormulas_LiCl +
    ()
)
