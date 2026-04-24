
import numpy as np
from .Exciton import Exciton
from .ExcitonGroup import ExcitonGroup
from .Lineshape import VoigtLineshape

X_RANGE = np.linspace(1, 3, 1000)

NOISE_STDS = {}
NOISE_STDS["HIGH"] = 0.001
NOISE_STDS["STANDARD"] = 0.025
NOISE_STDS["LOW"] = 0.125
NOISE_STDS["AWFUL"] = 0.3

# True Excitons
true_exciton_a = Exciton()
true_exciton_a.energy = 1.9
true_exciton_a.amplitude = 1
true_exciton_a.label = "X"
true_exciton_a.lineshape = VoigtLineshape(linewidth_g=0.1,
                                          linewidth_l=0.1)

true_exciton_b = Exciton()
true_exciton_b.energy = 1.75
true_exciton_b.amplitude = 0.2
true_exciton_b.label = "T"
true_exciton_b.lineshape = VoigtLineshape(linewidth_g=0.1,
                                          linewidth_l=0.1)

true_excitons = {"X": true_exciton_a, 
                 "T": true_exciton_b}
TRUE_EXCITON_GROUP = ExcitonGroup(true_excitons, label='True')

# Variable Ranges
ENERGY_RANGE_B = np.arange(1.7, 1.9, 0.01)

# Bounds
bounds_min_energy = 0
bounds_max_energy = np.inf
bounds_min_amplitude = 0
bounds_max_amplitude = np.inf
bounds_min_linewidth = 0
bounds_max_linewidth = np.inf
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


