import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ExcitonFitting import Exciton, ExcitonGroup
from ExcitonFitting.Config import X_RANGE
import numpy as np

row_col = [[1, 1], [1, 2], [2, 1], [2, 2]]

lineshape_colors = {
    'GAUSSIAN': '#ff595e',
    'LORENTZIAN': '#ffca3a', 
    'PSEUDO-PHYSICAL':'#8ac926', 
    'PSEUDO-WEIGHT':'#1982c4', 
    'VOIGT':'#6a4c93', 
}

def title(label):
    label = label.replace('_', ' ')
    label = label.replace('CHI2', 'χ2')
    label = label.replace('RED', 'Reduced')
    label = label.replace('True Fit Exciton Diff %', '% Error')
    return label

def quad_plot(df, parameter_x, parameter_y, xlabel=None, ylabel=None, x_range=None, y_range=None, showexpected=False):
    show_trendline = False
    if parameter_x == 'True_Exciton_Energy_Diff' and parameter_y == 'Fit_Exciton_Energy_Diff':
        show_trendline = True
        
    if not xlabel:
        title_x = title(parameter_x)
    if not ylabel:
        title_y = title(parameter_y)

    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0, vertical_spacing=0)
    for j, (noise_key, noise_data) in enumerate(df.groupby("NOISE_STD_VALUE")):
        row = row_col[j][0]
        col = row_col[j][1]

        for i, (lineshape_key, lineshape_data) in enumerate(noise_data.groupby("LINESHAPE_KEY")):

            x = lineshape_data[parameter_x]
            y = lineshape_data[parameter_y]

            fig.add_trace(go.Scatter(x=x, y=y, showlegend=j==0, name=lineshape_key, mode='markers', marker=dict(color=lineshape_colors[lineshape_key])), row=row, col=col)

        if show_trendline:
            fig.add_trace(go.Scatter(x=x, y=x, name='Expected', line=dict(dash='dash', color='#FFFFFF'), mode='lines', showlegend=False), row=row, col=col)

        fig.add_annotation(
            text=f'{noise_key} noise std',
            x=0.05,
            y=0.95,
            xref='x domain',
            yref='y domain',
            showarrow=False,
            row=row,
            col=col
        )
    
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.update_xaxes(showticklabels=True, row=2)
    fig.update_yaxes(showticklabels=True, col=1)
    fig.update_xaxes(showticklabels=True, row=1, side='top')
    fig.update_yaxes(showticklabels=True, col=2, side='right')

    fig.update_layout(yaxis1=dict(title=title_y))
    fig.update_layout(yaxis3=dict(title=title_y))
    fig.update_layout(xaxis3=dict(title=title_x))
    fig.update_layout(xaxis4=dict(title=title_x))

    if x_range is not None:
        fig.update_layout(xaxis1=dict(range=x_range))
        fig.update_layout(xaxis2=dict(range=x_range))
        fig.update_layout(xaxis3=dict(range=x_range))
        fig.update_layout(xaxis4=dict(range=x_range))
    if y_range is not None:
        fig.update_layout(yaxis1=dict(range=y_range))
        fig.update_layout(yaxis2=dict(range=y_range))
        fig.update_layout(yaxis3=dict(range=y_range))
        fig.update_layout(yaxis4=dict(range=y_range))

    return fig
        

def fit_plot(df, lineshape_key, true_exciton_T_energy):

    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0, vertical_spacing=0)
    for j, (noise_key, noise_data) in enumerate(df.groupby("NOISE_STD_VALUE")):
        row = row_col[j][0]
        col = row_col[j][1]

        intermediate_data = noise_data[
            noise_data['LINESHAPE_KEY'] == lineshape_key
        ]
        intermediate_intermediate_data = intermediate_data[
            np.isclose(intermediate_data['True_exciton_T_energy'], true_exciton_T_energy)
        ]

        data = intermediate_intermediate_data.iloc[0]

        true_exciton_X_dict = {'energy': data['True_exciton_X_energy'],
                               'amplitude': data['True_exciton_X_amplitude'],
                               'label': 'True X',
                               'lineshape': {'label': data['True_exciton_X_lineshape'],
                                             'linewidth': data['True_exciton_X_linewidth'],
                                             'linewidth_g': data['True_exciton_X_linewidth_g'],
                                             'linewidth_l': data['True_exciton_X_linewidth_l'],
                                             'weight': data['True_exciton_X_weight']}}
        true_exciton_X = Exciton()
        true_exciton_X.from_dict(true_exciton_X_dict)

        true_exciton_T_dict = {'energy': data['True_exciton_T_energy'],
                                'amplitude': data['True_exciton_T_amplitude'],
                                'label': 'True T',
                                'lineshape': {'label': data['True_exciton_T_lineshape'],
                                                'linewidth': data['True_exciton_T_linewidth'],
                                                'linewidth_g': data['True_exciton_T_linewidth_g'],
                                                'linewidth_l': data['True_exciton_T_linewidth_l'],
                                                'weight': data['True_exciton_T_weight']}}
        true_exciton_T = Exciton()
        true_exciton_T.from_dict(true_exciton_T_dict)

        fit_exciton_A_dict = {'energy': data['Fit_exciton_0_energy'],
                                'amplitude': data['Fit_exciton_0_amplitude'],
                                'label': 'Fit A',
                                'lineshape': {'label': data['Fit_exciton_0_lineshape'],
                                                'linewidth': data['Fit_exciton_0_linewidth'],
                                                'linewidth_g': data['Fit_exciton_0_linewidth_g'],
                                                'linewidth_l': data['Fit_exciton_0_linewidth_l'],
                                                'weight': data['Fit_exciton_0_weight']}}
        fit_exciton_A = Exciton()
        fit_exciton_A.from_dict(fit_exciton_A_dict)

        fit_exciton_B_dict = {'energy': data['Fit_exciton_1_energy'],
                                'amplitude': data['Fit_exciton_1_amplitude'],
                                'label': 'Fit B',
                                'lineshape': {'label': data['Fit_exciton_1_lineshape'],
                                                'linewidth': data['Fit_exciton_1_linewidth'],
                                                'linewidth_g': data['Fit_exciton_1_linewidth_g'],
                                                'linewidth_l': data['Fit_exciton_1_linewidth_l'],
                                                'weight': data['Fit_exciton_1_weight']}}
        fit_exciton_B = Exciton()
        fit_exciton_B.from_dict(fit_exciton_B_dict)

        true_excitons = {'X': true_exciton_X,
                         'T': true_exciton_T}
        fit_excitons = {'A': fit_exciton_A,
                         'B': fit_exciton_B}
        exciton_group_true = ExcitonGroup(true_excitons, label='True')
        exciton_group_fit = ExcitonGroup(fit_excitons, label='Fit')

        x = X_RANGE
        y_true = exciton_group_true.spectra(x)
        seed = data['SEED']
        np.random.seed(seed)
        y_true += np.random.normal(0, noise_key, y_true.shape)

        y_fit = exciton_group_fit.spectra(x)

        color = lineshape_colors[list(lineshape_colors.keys())[3]]
        fig.add_trace(go.Scatter(x=x, y=y_true, name='True Signal', line=dict(color=color), showlegend=j==0), row=row, col=col)
        color = lineshape_colors[list(lineshape_colors.keys())[0]]
        fig.add_trace(go.Scatter(x=x, y=y_fit, name='Fit Signal', line=dict(color=color), showlegend=j==0), row=row, col=col)

        for exciton in exciton_group_true.exciton_list:
                color = lineshape_colors[list(lineshape_colors.keys())[2]]
                fig.add_trace(go.Scatter(x=x, y=exciton.spectra(x), name=exciton.label, mode='lines', line=dict(color=color, dash='dash'), showlegend=j==0), row=row, col=col)

        for exciton in exciton_group_fit.exciton_list:
            color = lineshape_colors[list(lineshape_colors.keys())[1]]

            print(exciton.lineshape)

            fig.add_trace(go.Scatter(x=x, y=exciton.spectra(x), name=exciton.label, mode='lines', line=dict(color=color, dash='dash'), showlegend=j==0), row=row, col=col)


    fig.update_layout(
        xaxis3=dict(title='Energy (eV)'),
        xaxis4=dict(title='Energy (eV)'),
        yaxis=dict(title='Intensity (a.u.)'),     # NOT yaxis1
        yaxis3=dict(title='Intensity (a.u.)')
    )

    return fig

def histogram(df, parameter, label=None):
    if not label:
        label = title(parameter)

    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0, vertical_spacing=0)
    for j, (noise_key, noise_data) in enumerate(df.groupby("NOISE_STD_VALUE")):
        row = row_col[j][0]
        col = row_col[j][1]

        for i, (lineshape_key, lineshape_data) in enumerate(noise_data.groupby("LINESHAPE_KEY")):
            x = lineshape_data[parameter]

            fig.add_trace(go.Histogram(x=x, name=f'{lineshape_key} {noise_key} noise'), row=row, col=col)
    
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.update_xaxes(showticklabels=True, row=2)
    fig.update_yaxes(showticklabels=True, col=1)
    fig.update_xaxes(showticklabels=True, row=1, side='top')
    fig.update_yaxes(showticklabels=True, col=2, side='right')

    fig.update_layout(yaxis1=dict(title='Counts'))
    fig.update_layout(yaxis3=dict(title='Counts'))
    fig.update_layout(xaxis3=dict(title=label))
    fig.update_layout(xaxis4=dict(title=label))
    
    return fig