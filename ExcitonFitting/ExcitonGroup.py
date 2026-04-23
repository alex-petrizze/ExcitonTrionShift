import numpy as np
from .Exciton import Exciton

class ExcitonGroup:
    def __init__(self, excitons={}, label='Unabeled Exciton Group'):
        self.excitons = excitons
        self.exciton_list = excitons.values()
        self.label = label

    def __getitem__(self, key):
        return self.excitons[key]
    
    @property
    def count(self):
        return len(self.exciton_list)
    
    @property
    def p0(self):
        out_p0 = []
        for exciton in self.exciton_list:
            out_p0.extend(exciton.p0)
        return out_p0
    
    @property
    def bounds(self):
        out_bounds_min = []
        out_bounds_max= []
        for exciton in self.exciton_list:
            bounds_min, bounds_max = exciton.bounds
            out_bounds_min.extend(bounds_min)
            out_bounds_max.extend(bounds_max)
        bounds = [out_bounds_min, out_bounds_max]
        return bounds
    
    def from_popt(self, popt, lineshape):
        n_params_per_exciton = 2 + lineshape.n_params
        n_excitons = len(popt) // n_params_per_exciton

        idx = 0
        self.exciton_list = []
        for n_exciton in range(n_excitons):
            new_exciton = Exciton(label=f'{n_exciton}')
            new_exciton.energy = popt[idx]
            idx += 1
            new_exciton.amplitude = popt[idx]
            idx += 1

            lineshape_params = popt[idx : idx + lineshape.n_params]
            idx += lineshape.n_params
            new_lineshape = type(lineshape)(*lineshape_params)  

            new_exciton.lineshape = new_lineshape

            self.exciton_list.append(new_exciton)

    def spectra(self, x):
        y = np.zeros(x.shape)
        for exciton in self.exciton_list:
            y += exciton.spectra(x)
        return y
    
    def __str__(self):
        string = f'{self.label}:'
        for exciton in self.exciton_list:
            string += f'\n\t{exciton}'
        return string
    
    def to_dict(self):
        out_dict = {}
        for exciton in self.exciton_list:
            out_dict[exciton.label] = exciton.to_dict()

        return out_dict
    
    def from_dict(self, in_dict):
        self.exciton_list = []
        for exciton_key in in_dict:
            exciton_dict = in_dict[exciton_key]
            new_exciton = Exciton()
            new_exciton.from_dict(exciton_dict)
            self.exciton_list.append(new_exciton)

    def __eq__(self, other):
        return isinstance(other, ExcitonGroup) and \
            len(self.exciton_list) == len(other.exciton_list) and \
            all(a == b for a, b in zip(self.exciton_list, other.exciton_list))
    
    def copy(self):
        new_exciton_dict = {}
        for exciton in self.exciton_list:
            new_exciton_dict[exciton.label] = exciton.copy()
        return ExcitonGroup(new_exciton_dict)
    

    def to_row(self, row):
        for exciton in self.exciton_list:
            base = f'{self.label}_exciton_{exciton.label}'
            row[f'{base}_energy'] = np.float32(exciton.energy)
            row[f'{base}_amplitude'] = np.float32(exciton.amplitude)
            row[f'{base}_lineshape'] = exciton.lineshape.label
            row[f'{base}_linewidth'] = np.float32(getattr(exciton.lineshape, 'linewidth', np.nan))
            row[f'{base}_linewidth_g'] = np.float32(getattr(exciton.lineshape, 'linewidth_g', np.nan))
            row[f'{base}_linewidth_l'] = np.float32(getattr(exciton.lineshape, 'linewidth_l', np.nan))
            row[f'{base}_weight'] = np.float32(getattr(exciton.lineshape, 'weight', np.nan))