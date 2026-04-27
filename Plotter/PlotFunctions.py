import plotly.graph_objects as go
from plotly.subplots import make_subplots

row_col = [[1, 1], [2, 1], [1, 2], [2, 2]]

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
        
    #     if showexpected:
    #         ax[j].plot(x, x, '--', label='True', color='#F4F5F7')

    #     ax[j].annotate(f'{noise_key} noise std', xy=(0.8, 0.95), xycoords='axes fraction')

    #     if x_range:
    #         ax[j].set_xlim(x_range[0], x_range[1])
    #     if y_range:
    #         ax[j].set_ylim(y_range[0], y_range[1])
    #     # ax[j].set_title(f'{noise_key} noise std')
        
    # ax[0].set_ylabel(f'{ylabel}')
    # ax[2].set_ylabel(f'{ylabel}')
    # ax[2].set_xlabel(f'{xlabel}')
    # ax[3].set_xlabel(f'{xlabel}')

    
    # handles, labels = ax[0].get_legend_handles_labels()
    # fig.legend(
    #     handles,
    #     labels,
    #     loc='center left',
    #     bbox_to_anchor=(0.00, 0.5)
    # )
    # fig.subplots_adjust(right=0.8)


    # plt.savefig(f'Out\\Plots\\{moniker}\\Quad Plot {parameter_y} vs {parameter_x} xrange=({x_range}) yrange=({y_range})).png', bbox_inches='tight')
    # plt.show()
