
import numpy as np
from .Exciton import Exciton
from .ExcitonGroup import ExcitonGroup
from .Lineshape import VoigtLineshape

PLOT_DIRECTORY = 'Out\\Plots\\'

SEED = 12345

X_RANGE = np.linspace(1, 3, 1000)

SIGNAL_TO_NOISE_LEVELS = {}
SIGNAL_TO_NOISE_LEVELS["HIGH"] = 0.001
SIGNAL_TO_NOISE_LEVELS["STANDARD"] = 0.025
SIGNAL_TO_NOISE_LEVELS["LOW"] = 0.125
SIGNAL_TO_NOISE_LEVELS["AWFUL"] = 0.3
SIGNAL_TO_NOISE_LEVELS["LABEL"] = "STANDARD"

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
TRUE_EXCITON_GROUP = ExcitonGroup(true_excitons, label='True Excitons')

# Guess Excitons

# Variable Ranges
ENERGY_RANGE_B = np.arange(1.7, 1.9, 0.001)


# "GAUSSIAN"
# "LORENTZIAN"
# "VOIGT"
# "PSEUDO-PHYSICAL"
# "PSEUDO-WEIGHT"

FIT_EXCITON_SHAPES = ["GAUSSIAN",
                      "LORENTZIAN",
                      "VOIGT",
                      "PSEUDO-PHYSICAL",
                      "PSEUDO-WEIGHT"]

# linewidth_g_range_a = np.arange(TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_G"]["MIN"], 
#                                 TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_G"]["MAX"], 
#                                 TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_G"]["DELTA"])
# linewidth_l_range_a = np.arange(TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_L"]["MIN"], 
#                                 TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_L"]["MAX"], 
#                                 TRUE_EXCITONS["A"]["LINESHAPE"]["LINESHAPE_L"]["DELTA"])
# energy_range_b = np.arange(TRUE_EXCITONS["B"]["ENERGY"]["MIN"], 
#                                 TRUE_EXCITONS["B"]["ENERGY"]["MAX"], 
#                                 TRUE_EXCITONS["B"]["ENERGY"]["DELTA"])
# amplitude_range_b = np.arange(TRUE_EXCITONS["B"]["AMPLITUDE"]["MIN"], 
#                                 TRUE_EXCITONS["B"]["AMPLITUDE"]["MAX"], 
#                                 TRUE_EXCITONS["B"]["AMPLITUDE"]["DELTA"])
# linewidth_g_range_b = np.arange(TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_G"]["MIN"], 
#                                 TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_G"]["MAX"], 
#                                 TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_G"]["DELTA"])
# linewidth_l_range_b = np.arange(TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_L"]["MIN"], 
#                                 TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_L"]["MAX"], 
#                                 TRUE_EXCITONS["B"]["LINESHAPE"]["LINESHAPE_L"]["DELTA"])

# variable_params = {
#     "True_exciton_A_linewidth_g": linewidth_g_range_a,
#     "True_exciton_A_linewidth_l": linewidth_l_range_a,
#     "True_exciton_B_energy": energy_range_b,
#     "True_exciton_B_amplitude": amplitude_range_b,
#     "True_exciton_B_linewidth_g": linewidth_g_range_b,
#     "True_exciton_B_linewidth_l": linewidth_l_range_b,
# }

# units = {
#     "True_exciton_A_linewidth_g": 'eV',
#     "True_exciton_A_linewidth_l": 'eV',
#     "True_exciton_B_energy": 'eV',
#     "True_exciton_B_amplitude": '(a.u.)',
#     "True_exciton_B_linewidth_g": 'eV',
#     "True_exciton_B_linewidth_l": 'eV',
# }