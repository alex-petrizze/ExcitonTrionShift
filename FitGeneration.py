import numpy as np
import matplotlib.pyplot as plt
from PetrizzeTheme import petrizze_template
from ExcitonFitting import Config
from ExcitonFitting import Lineshape
from ExcitonFitting import Exciton
from ExcitonFitting import ExcitonGroup
from scipy.optimize import curve_fit
from ExcitonFitting.Equations import RMSE, RMSE_normalized, RMSE_percentage, Chi2_gaussian, Red_Chi2, AIC, BIC
import pandas as pd
from datetime import datetime

petrizze_template()

def create_true_excitons(i=0):
    true_excitons = Config.TRUE_EXCITON_GROUP.copy()
    true_excitons.label = "True"
    true_excitons["T"].energy = Config.ENERGY_RANGE_B[i]

    return true_excitons

def fit_function(lineshape, n_fit_excitons=2):
    n_lineshape_params = lineshape.n_params

    def f(x, *params):
        y = np.zeros(x.shape)

        idx = 0
        for i in range(n_fit_excitons):
            exciton = Exciton()
            exciton.energy = params[idx]
            idx += 1
            exciton.amplitude = params[idx]
            idx += 1

            lineshape_params = params[idx : idx + n_lineshape_params]
            idx += lineshape.n_params
            
            new_lineshape = lineshape(*lineshape_params)

            exciton.lineshape = new_lineshape

            y += exciton.spectra(x)

        return y

    return f

def get_p0(fit_exciton_lineshape):
    p0 = []
    for exciton in Config.TRUE_EXCITON_GROUP.exciton_list:
        energy = exciton.energy + np.random.normal(0, 0.2)
        energy = np.clip(energy, 0, np.inf)
        amplitude = exciton.amplitude + np.random.normal(0, 0.1)
        amplitude = np.clip(amplitude, 0, np.inf)

        p0.append(energy)
        p0.append(amplitude)
        p0.extend(fit_exciton_lineshape.p0)
    return p0

def get_bounds(fit_exciton_lineshape):
    bounds_min = []
    bounds_max = []
    for exciton in Config.TRUE_EXCITON_GROUP.exciton_list:
        bounds_min.append(Config.bounds_min_energy)
        bounds_min.append(Config.bounds_min_amplitude)
        bounds_min.extend(fit_exciton_lineshape.bounds_min)

        bounds_max.append(Config.bounds_max_energy)
        bounds_max.append(Config.bounds_max_amplitude)
        bounds_max.extend(fit_exciton_lineshape.bounds_max)
    return [bounds_min, bounds_max]


x_true = Config.X_RANGE

rows = []
for noise_stds_key, noise_stds_value in Config.NOISE_STDS.items():
    for fit_exciton_lineshape_key, fit_exciton_lineshape_value in Lineshape.lineshape_dictionary.items():
        print(noise_stds_key, fit_exciton_lineshape_key)
        for i in range(len(Config.ENERGY_RANGE_B)):
            true_exciton_group = create_true_excitons(i)

            y_true = true_exciton_group.spectra(x_true)
            seed = np.random.randint(0, 2**16 - 1)
            np.random.seed(seed)
            y_true += np.random.normal(0, noise_stds_value, y_true.shape)

            p0 = get_p0(fit_exciton_lineshape_value)
            bounds = get_bounds(fit_exciton_lineshape_value)

            f = fit_function(fit_exciton_lineshape_value)
            try:
                now = datetime.now()
                popt, pcov = curve_fit(f, x_true, y_true, p0=p0, bounds=bounds)
                converged = True
                time = (datetime.now() - now).total_seconds()
            except:
                popt, pcov = None, None
                converged = False

            if converged:
                row = {}

                guess_exciton_group = ExcitonGroup(label='Guess')
                guess_exciton_group.from_popt(p0, fit_exciton_lineshape_value)

                fit_exciton_group = ExcitonGroup(label='Fit')
                fit_exciton_group.from_popt(popt, fit_exciton_lineshape_value)
                y_fit = fit_exciton_group.spectra(x_true)

                row["CONVERGED"] = converged
                row["SEED"] = seed
                row["TIME"] = time
                
                true_exciton_group.to_row(row)
                guess_exciton_group.to_row(row)
                fit_exciton_group.to_row(row)
                
                chi2 = Chi2_gaussian(y_true, y_fit, noise_stds_value)
                row["CHI2"] = chi2
                row["RED_CHI2"] = Red_Chi2(chi2, len(x_true), len(popt))
                row["AIC"] = AIC(chi2, len(x_true), len(popt))
                row["BIC"] = BIC(chi2, len(x_true), len(popt))

                row["RMSE"] = RMSE(y_true, y_fit)
                row["RMSE_NORMALIZED"] = RMSE_normalized(y_true, y_fit)
                row["RMSE_%"] = RMSE_percentage(y_true, y_fit)

                row["NOISE_STD_KEY"] = noise_stds_key
                row["NOISE_STD_VALUE"] = noise_stds_value
                row["LINESHAPE_KEY"] = fit_exciton_lineshape_key

                rows.append(row)

            


df = pd.DataFrame(rows)
df.to_parquet(f"Out\\Data.parquet")


