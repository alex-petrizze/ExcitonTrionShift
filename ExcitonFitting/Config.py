
import numpy as np
from .Exciton import Exciton
from .ExcitonGroup import ExcitonGroup
from .Lineshape import VoigtLineshape
from .Equations import linewidth_g_l, eta_linewidth

X_RANGE = np.linspace(1.4, 2.4, 1000)

NOISE_STDS = {}
NOISE_STDS["HIGH"] = 0.001
NOISE_STDS["STANDARD"] = 0.025
NOISE_STDS["LOW"] = 0.125
NOISE_STDS["AWFUL"] = 0.3

exciton_X_effective_linewidth = 0.074 # eV
exciton_T_effective_linewidth = 0.064 # eV

lineshape_ratio = 1 # Gaussian

moniker = 'Gaussian'

linewidth_g_X, linewidth_l_X = linewidth_g_l(lineshape_ratio, exciton_X_effective_linewidth)
linewidth_g_T, linewidth_l_T = linewidth_g_l(lineshape_ratio, exciton_T_effective_linewidth)

print(linewidth_g_X, linewidth_l_X)

# True Excitons
true_exciton_a = Exciton()
true_exciton_a.energy = 1.9
true_exciton_a.amplitude = 1
true_exciton_a.label = "X"
true_exciton_a.lineshape = VoigtLineshape(linewidth_g=linewidth_g_X,
                                          linewidth_l=linewidth_l_X)

true_exciton_b = Exciton()
true_exciton_b.energy = 1.75
true_exciton_b.amplitude = 0.5
true_exciton_b.label = "T"
true_exciton_b.lineshape = VoigtLineshape(linewidth_g=linewidth_g_T,
                                          linewidth_l=linewidth_l_T)

true_excitons = {"X": true_exciton_a, 
                 "T": true_exciton_b}
TRUE_EXCITON_GROUP = ExcitonGroup(true_excitons, label='True')

# Variable Ranges
ENERGY_RANGE_B = np.arange(1.7, 1.9, 0.001)

# Bounds
bounds_min_energy = 0
bounds_max_energy = np.inf
bounds_min_amplitude = 0
bounds_max_amplitude = np.inf
bounds_min_linewidth = 0
bounds_max_linewidth = 0.1
bounds_min_eta = 0
bounds_max_eta = 1


# "GAUSSIAN"
# "LORENTZIAN"
# "VOIGT"
# "PSEUDO-PHYSICAL"
# "PSEUDO-WEIGHT"

FIT_EXCITON_SHAPE_KEYS = ["GAUSSIAN",
                      "LORENTZIAN",
                      "VOIGT",
                      "PSEUDO-PHYSICAL",
                      "PSEUDO-WEIGHT"]


