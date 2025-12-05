"""Viscosity of solutions"""


from .NaCl import ViscosityFormulas_NaCl

ViscosityFormulas = (
    ViscosityFormulas_NaCl +
    ()
)
