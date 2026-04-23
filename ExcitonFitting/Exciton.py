from .Lineshape import dict_to_lineshape
from .Lineshape import PseudoVoigtLineshapeWeight
import numpy as np

class Exciton:
    def __init__(self, energy=0, amplitude=0, lineshape=0, label='Unlabled Exciton'):
        self.energy = energy
        self.amplitude = amplitude
        self.lineshape = lineshape
        self.label = label

    def copy(self):
        new_exciton = Exciton()
        new_exciton.label = self.label
        new_exciton.amplitude = self.amplitude
        new_exciton.lineshape = self.lineshape
        new_exciton.energy = self.energy
        return new_exciton
        
    def spectra(self, x):
        return self.amplitude * self.lineshape.profile_norm(x - self.energy)
    
    @property
    def p0(self):
        out_p0 = []
        out_p0.append(self.energy)
        out_p0.append(self.amplitude)
        out_p0.extend(self.lineshape.p0)
        return out_p0
    
    @property
    def bounds(self):
        bounds_min = []
        bounds_min.append(0)
        bounds_min.append(0)
        bounds_min.extend(self.lineshape.bounds_min)
        bounds_max = []
        bounds_max.append(np.inf)
        bounds_max.append(np.inf)
        bounds_max.extend(self.lineshape.bounds_max)
        return bounds_min, bounds_max
    
    def __str__(self):
        string = f'{self.label}:'
        string += f'\n\tEnergy: {self.energy}'
        string += f'\n\tAmplitude: {self.amplitude}'
        string += f'\n\tLineshape: {self.lineshape}'
        return string
    
    def to_dict(self):
        out_dict = {}
        out_dict['label'] = self.label
        out_dict['amplitude'] = float(self.amplitude)
        out_dict['energy'] = float(self.energy)
        out_dict['lineshape'] = self.lineshape.to_dict()
        return out_dict

    def from_dict(self, in_dict):
        self.energy = in_dict['energy']
        self.amplitude = in_dict['amplitude']
        self.label = in_dict['label']
        self.lineshape = dict_to_lineshape(in_dict['lineshape'])

    def __eq__(self, other):
        return self.energy == other.energy and self.amplitude == other.amplitude and self.lineshape == other.lineshape
    
    def __sub__(self, other):
        diff_exciton = Exciton()
        diff_exciton.energy = self.energy - other.energy
        diff_exciton.amplitude = self.amplitude - other.amplitude
        
        self_weight, self_linewidth = self.lineshape.weight_linewidth()
        other_weight, other_linewidth = other.lineshape.weight_linewidth()

        diff_exciton.lineshape = PseudoVoigtLineshapeWeight(weight=self_weight - other_weight,
                                                   linewidth=self_linewidth - other_linewidth)





    
    