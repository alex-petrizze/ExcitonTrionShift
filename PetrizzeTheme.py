import matplotlib.pyplot as plt
from cycler import cycler

background_color = '#101316'
color_grey = '#F2F5FA'

# colors = [
#     '#636EFA', # Blue
#     '#EF553B', # Red
#     '#00CC96', # Green
#     '#FF820E', # Orange
#     '#980FFE', # Violet
#     '#19D3F3', # Cyan
#     '#FF6692', # Peach
#     '#B6E880', # Other Green
#     '#FF97FF', # Pink
#     '#FECB52'  # Yellow
# ]

colors = [
    '#ff595e', # Red
    '#ffca3a', # Yellow
    '#8ac926', # Green
    '#1982c4', # Blue
    '#6a4c93', # Purple,
    '#59FFFA', # Cyan
]

# colors = [
#     '#1982c4', # Red
#     '#ff595e', # Yellow
#     '#8ac926', # Green
#     '#1982c4', # Blue
#     '#6a4c93', # Purple,
#     '#59FFFA', # Cyan
# ]

# colors = [
#     '#C72138', # Red
#     '#E06236', # Yellow
#     '#D7A64B', # Green
#     '#304C7A', # Purple,
#     '#7547B2', # Cyan
# ]

def petrizze_template():
    plt.style.use('dark_background')

    plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

    plt.rcParams.update({
        'figure.facecolor': background_color,
        'axes.facecolor': background_color,
        'axes.edgecolor': color_grey,
        'axes.labelcolor': color_grey,
        'xtick.color': color_grey,
        'ytick.color': color_grey,
        'text.color': color_grey,
        'legend.facecolor': background_color,
        'legend.edgecolor': color_grey,
    })

def petrizze_template_go():
    import plotly.graph_objects as go
    import plotly.io as pio

    pio.templates['petrizze'] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=background_color,
            plot_bgcolor=background_color,

            font=dict(color=color_grey),  # 👈 THIS

            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                mirror=True,
                linecolor=color_grey,   # 🔥 FIX
                linewidth=1
            ),

            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=True,
                mirror=True,
                linecolor=color_grey,   # 🔥 FIX
                linewidth=1,
                automargin=True
            ),


            colorway=colors,
        )
    )

    pio.templates.default = 'petrizze'


def borys_template():
    import plotly.io as pio

    pio.templates["borys"] = pio.templates["plotly_white"]

    pio.templates["borys"].layout.update(
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=1,
            mirror=True,
            ticks='outside',
            tickcolor='black'
        ),

        yaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=1,
            mirror=True,
            ticks='outside',
            tickcolor='black'
        )
    )

    pio.templates.default = 'borys'