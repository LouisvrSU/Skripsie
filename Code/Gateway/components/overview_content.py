import dash_bootstrap_components as dbc
from dash import html, dcc


# Dash Bootstrap Layout
#----------------------------------------------------------------

layout = html.Div(
    [
        
                    dcc.Interval(
                    id='interval-component',
                    interval=1500,  # in milliseconds
                    n_intervals=0,
                ),
        
    ],
)
