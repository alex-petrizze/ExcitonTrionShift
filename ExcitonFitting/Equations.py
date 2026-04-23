from scipy.optimize import fsolve
import numpy as np

sigma = 0
call_count = 0

def thompson_fwhm(fwhm_g, fwhm_l):
    fwhm = (fwhm_g**5  
            + 2.69269 * fwhm_g ** 4 * fwhm_l 
            + 2.42843 * fwhm_g**3 * fwhm_l**2 
            + 4.47163 * fwhm_g**2 * fwhm_l**3
            + 0.07842 * fwhm_g * fwhm_l**4
            + fwhm_l**5)**(1/5)
    return fwhm

def thompson_eta(fwhm_g, fwhm_l):
    fwhm = thompson_fwhm(fwhm_g, fwhm_l)
    return 1.36603 * (fwhm_l / fwhm) - 0.47719 * (fwhm_l / fwhm) ** 2 + 0.11116 * (fwhm_l / fwhm)**3

def eta_linewidth(fwhm_g, fwhm_l):
    eta = thompson_eta(fwhm_g, fwhm_l)
    fwhm = thompson_fwhm(fwhm_g, fwhm_l)
    return eta, fwhm

def linewidth_g_l(eta, fwhm):
    def equations(params):
        fg, fl = params
        fwhm_calc = thompson_fwhm(fg, fl)
        eta_calc = thompson_eta(fg, fl)
        return [fwhm_calc - fwhm, eta_calc - eta]
    
    fg0 = fwhm * (1 - eta)
    fl0 = fwhm * eta
    fg, fl = fsolve(equations, [fg0, fl0])
    return fg, fl

def RMSE(y_a, y_b):
    delta = y_a - y_b
    
    n_a = len(y_a)
    n_b = len(y_b)
    assert n_a == n_b
    n = n_a
    
    return np.sqrt(1 / n * np.sum(delta**2))

def RMSE_normalized(y_a, y_b):
    rmse = RMSE(y_a, y_b)
    return rmse / (np.max(y_a) - np.min(y_a))

def RMSE_percentage(y_a, y_b):
    rmse_normalized = RMSE_normalized(y_a, y_b)
    return rmse_normalized * 100

def Chi2(y_data, y_fit):
    delta = y_data - y_fit
    return np.sum((delta / sigma)**2)

def Chi2_poisson(y_data, y_fit):
    delta = y_data - y_fit
    delta_squared = delta ** 2
    points = delta_squared / y_fit
    chi2 = np.sum(points)
    return chi2

def Red_Chi2(chi2, n_data_points, n_parameters):
    dof = n_data_points - n_parameters
    chi2_reduced = chi2 / dof
    return chi2_reduced

def AIC(chi2, n_data_points, n_parameters):
    return 2 * n_parameters + n_data_points * np.log(chi2 / n_data_points)

def BIC(chi2, n_data_points, n_parameters):
    return  n_parameters * np.log(n_data_points) + n_data_points * np.log(chi2 / n_data_points)
    