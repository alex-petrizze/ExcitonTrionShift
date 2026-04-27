import pandas as pd
import numpy as np

moniker = '5050'

def load_data(name):
    df = pd.read_parquet(f"Out\\Data-True {name}.parquet")

    df["True_Exciton_Energy_Diff"] = df["True_exciton_T_energy"] - df["True_exciton_X_energy"]
    a = df["Fit_exciton_1_energy"]
    b = df["Fit_exciton_0_energy"]
    df["Fit_Exciton_Energy_Diff"] = np.minimum(a, b) - np.maximum(a, b)
    df["True_Fit_Exciton_Diff"] = df["Fit_Exciton_Energy_Diff"] - df["True_Exciton_Energy_Diff"]
    true = df["True_Exciton_Energy_Diff"]
    fit = df["Fit_Exciton_Energy_Diff"]
    df["True_Fit_Exciton_Diff_%"] = (true - fit) / true * 100

    return df