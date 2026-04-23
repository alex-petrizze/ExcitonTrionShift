import numpy as np
from scipy.stats import norm, cauchy
from scipy.special import voigt_profile

from .Equations import eta_linewidth, linewidth_g_l

class Lineshape:
    n_params = 0
    def profile(self, x):
        return np.exp(-x**2)
    
    def profile_norm(self, x):
        profile = self.profile(x)
        return profile / np.max(profile)
    
    def __str__(self):
        return 'blank lineshape (lol)'
    
class GaussianLineshape(Lineshape):
    n_params = 1
    p0 = [0.1]
    bounds_min = [0]
    bounds_max = [np.inf]
    label = 'Gaussian'

    def __init__(self, linewidth):
        self.linewidth=linewidth

    def profile(self, x):
        return norm.pdf(x, 0, self.linewidth)
    
    def __str__(self):
        string = f'Gaussian: {self.linewidth:0.2f}'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['linewidth'] = float(self.linewidth)
        return out_dict
    
    def __eq__(self, other):
        return isinstance(other, GaussianLineshape) and self.linewidth == other.linewidth
    
    def weight_linewidth(self):
        return 1, self.linewidth
    
class LorentzianLineshape(Lineshape):
    n_params = 1
    p0 = [0.1]
    bounds_min = [0]
    bounds_max = [np.inf]
    label = 'Lorentzian'

    def __init__(self, linewidth):
        self.linewidth=linewidth

    def profile(self, x):
        return cauchy.pdf(x, 0, self.linewidth)
    
    def __str__(self):
        string = f'Lorentzian: {self.linewidth:0.2f}'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['linewidth'] = float(self.linewidth)
        return out_dict
    
    def __eq__(self, other):
        return isinstance(other, LorentzianLineshape) and self.linewidth == other.linewidth
    
    def weight_linewidth(self):
        return 0, self.linewidth
    
class VoigtLineshape(Lineshape):
    n_params = 2
    p0 = [0.1,
          0.1]
    bounds_min = [0,
                  0]
    bounds_max = [np.inf,
                  np.inf]
    label = 'Voigt'
    
    def __init__(self, linewidth_g, linewidth_l):
        self.linewidth_l = linewidth_l
        self.linewidth_g = linewidth_g

    def profile(self, x):
        y = voigt_profile(x, self.linewidth_g, self.linewidth_l)
        return y
    
    def __str__(self):
        string = f'Voigt: {self.linewidth_g:0.2f} G, {self.linewidth_l:0.2f} L'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['linewidth_g'] = float(self.linewidth_g)
        out_dict['linewidth_l'] = float(self.linewidth_l)
        return out_dict
    
    def __eq__(self, other):
        return isinstance(other, VoigtLineshape) and self.linewidth_g == other.linewidth_g and self.linewidth_l == other.linewidth_l
    
    def weight_linewidth(self):
        weight, linewidth = eta_linewidth(self.linewidth_g, self.linewidth_l)
        return weight, linewidth
    
class PseudoVoigtLineshapePhysical(Lineshape):
    n_params = 2
    p0 = [0.1,
          0.1]
    bounds_min = [0,
                  0]
    bounds_max = [np.inf,
                  np.inf]
    label = 'Pseudo-Voigt Physical'
    
    def __init__(self, linewidth_g, linewidth_l):
        self.linewidth_l = linewidth_l
        self.linewidth_g = linewidth_g
        
        self.weight, self.linewidth = eta_linewidth(linewidth_g, linewidth_l)
        
    def profile(self, x):
        return self.weight * norm.pdf(x, 0, self.linewidth) + (1 - self.weight) * cauchy.pdf(x, 0, self.linewidth)
    
    def __str__(self):
        string = f'Pseudo-Physical: {self.linewidth_g:0.2f} G, {self.linewidth_l:0.2f} L'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['linewidth_g'] = float(self.linewidth_g)
        out_dict['linewidth_l'] = float(self.linewidth_l)
        return out_dict
    
    def __eq__(self, other):
        return isinstance(other, PseudoVoigtLineshapePhysical) and self.linewidth_g == other.linewidth_g and self.linewidth_l == other.linewidth_l
    
    def weight_linewidth(self):
        weight, linewidth = eta_linewidth(self.linewidth_g, self.linewidth_l)
        return weight, linewidth
    
class PseudoVoigtLineshapeWeight(Lineshape):
    n_params = 2
    p0 = [0.5,
          0.1]
    bounds_min = [0,
                  0]
    bounds_max = [1,
                  np.inf]
    label = 'Pseudo-Voigt Weight'
    
    def __init__(self, weight, linewidth):
        self.weight, self.linewidth = weight, linewidth
        
    def profile(self, x):
        return self.weight * norm.pdf(x, 0, self.linewidth) + (1 - self.weight) * cauchy.pdf(x, 0, self.linewidth)
    
    def __str__(self):
        string = f'Pseudo-Physical: {self.weight:0.2f} Weight, {self.linewidth:0.2f} Linewidth'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['weight'] = float(self.weight)
        out_dict['linewidth'] = float(self.linewidth)
        return out_dict
    
    def __eq__(self, other):
        return isinstance(other, PseudoVoigtLineshapeWeight) and self.weight == other.weight and self.linewidth == other.linewidth
    
    def weight_linewidth(self):
        return self.weight, self.linewidth
    
def build_lineshape(row, prefix):
    label = str(row[f"{prefix}_lineshape"]).strip().upper()

    if label == "GAUSSIAN":
        return GaussianLineshape(float(row[f"{prefix}_linewidth"]))
    elif label == "LORENTZIAN":
        return LorentzianLineshape(float(row[f"{prefix}_linewidth"]))
    elif label == "VOIGT":
        return VoigtLineshape(
            float(row[f"{prefix}_linewidth_g"]),
            float(row[f"{prefix}_linewidth_l"])
        )
    elif label == "PSEUDO-PHYSICAL":
        return PseudoVoigtLineshapePhysical(
            float(row[f"{prefix}_linewidth_g"]),
            float(row[f"{prefix}_linewidth_l"])
        )
    elif label == "PSEUDO-WEIGHT":
        return PseudoVoigtLineshapeWeight(
            float(row[f"{prefix}_weight"]),
            float(row[f"{prefix}_linewidth"])
        )
    else:
        raise ValueError(f"Unknown lineshape label: {label}")
    

def dict_to_lineshape(in_dict):
    label = in_dict['label']
    if label == 'Gaussian':
        linewidth = in_dict['linewidth']
        return GaussianLineshape(linewidth)
    if label == 'Lorentzian':
        linewidth = in_dict['linewidth']
        return LorentzianLineshape(linewidth)
    if label == 'Voigt':
        linewidth_g = in_dict['linewidth_g']
        linewidth_l = in_dict['linewidth_l']
        return VoigtLineshape(linewidth_g, linewidth_l)
    if label == 'Pseudo-Voigt Physical':
        linewidth_g = in_dict['linewidth_g']
        linewidth_l = in_dict['linewidth_l']
        return PseudoVoigtLineshapePhysical(linewidth_g, linewidth_l)
    if label == 'Pseudo-Voigt Weight':
        weight = in_dict['weight']
        linewidth = in_dict['linewidth']
        return PseudoVoigtLineshapeWeight(weight, linewidth)
    

lineshape_dictionary = {}
lineshape_dictionary["VOIGT"] = VoigtLineshape
lineshape_dictionary["GAUSSIAN"] = GaussianLineshape
lineshape_dictionary["LORENTZIAN"] = LorentzianLineshape
lineshape_dictionary["PSEUDO-PHYSICAL"] = PseudoVoigtLineshapePhysical
lineshape_dictionary["PSEUDO-WEIGHT"] = PseudoVoigtLineshapeWeight

    
# def test_plot():
#     x_test = np.linspace(-0.5, 0.5, 100)
    
#     linewidth = 0.25
#     weight = 0.5
#     linewidth_g, linewidth_l = linewidth_g_l(weight, linewidth)
    
#     y_gaussian = GaussianLineshape(linewidth).profile_norm(x_test)
#     y_lorentzian = LorentzianLineshape(linewidth).profile_norm(x_test)
#     y_voigt = VoigtLineshape(linewidth_g, linewidth_l).profile_norm(x_test)
#     y_pseudo_voigt_physical = PseudoVoigtLineshapePhysical(linewidth_g, linewidth_l).profile_norm(x_test)
#     y_pseudo_voigt_weight = PseudoVoigtLineshapeWeight(weight, linewidth).profile_norm(x_test)
    
#     import matplotlib.pyplot as plt
#     from PetrizzeTheme import petrizze_template
#     petrizze_template()
#     plt.plot(x_test, y_gaussian, label='Gaussian')
#     plt.plot(x_test, y_lorentzian, label='Lorentzian')
#     plt.plot(x_test, y_voigt, label='Voigt')
#     plt.plot(x_test, y_pseudo_voigt_physical, label='Pseudo Physical')
#     plt.plot(x_test, y_pseudo_voigt_weight, '--', label='Pseudo Weight')
#     plt.legend()
#     plt.show()
    
# test_plot()