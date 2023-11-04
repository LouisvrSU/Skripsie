from dash import Dash, dash_table, html,dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import math


################################################################
from components import (setup_content,map_content,table_content,overview_content)
from Lora import main as lora_func
from data import data_func
################################################################

# global variables
# global lora_active

lora_active = False
# page_number = 0

################################################################
# Data base Initialization
################################################################
# data_func.db_init()


# Initialize a Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
# Define the app layout
app.layout = dbc.Container(
    [
        
    dcc.Store(id='store'),
    
    dbc.Row(
        [
            
            html.Div(
                [
                dbc.Row(
                    [
        
                    dbc.Col(
                        html.Div(
                            [
                                html.H1('LoRa Tracking Dashboard'),
                            ],
                        ),
                    ),
            
                    dbc.Col(
                        html.Div(
                            [
                            dbc.Progress(value=100, id="battery-progress", animated=True, striped=True, style={"height": "30px"}),
                            ],
                        ),
                    ),
                ],
                align="center",
                ),
            ],
            ),

        ],
        ),
    
    dbc.Row(html.Hr(),),
    
    dbc.Row(
        [
            
    ################################################################
    # LIVE OVERVIEW
    ################################################################
                html.Div(
        [
            dbc.Button(
                "Live-Table",
                id="live-overview-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(overview_content.layout)),
                id="live-collapse",
                is_open=False,
            ),
        ],
        className="d-grid gap-2",
    ),
            
        ],
    ),
        

    dbc.Row(
        [
    ################################################################
    # Setup  
    ################################################################
        html.Div(
        [
            dbc.Button(
                "Setup",
                id="setup-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(setup_content.layout)),
                id="setup-collapse",
                is_open=False,
            ),
        ],
        className="d-grid gap-2",
    ),
    ################################################################
    # MAP
    ################################################################
            html.Div(
        [
            dbc.Button(
                "MAP",
                id="map-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(map_content.layout)),
                id="map-collapse",
                is_open=False,
            ),
        ],
        className="d-grid gap-2",
    ),
    
    ################################################################
    # TABLE
    ################################################################
                html.Div(
        [
            dbc.Button(
                "Table",
                id="table-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(table_content.layout)),
                id="table-collapse",
                is_open=False,
            ),
        ],
        className="d-grid gap-2",
    ),
    
    
    ################################################################
    ],
    ),
    ],
)

################################################################
# Callback functions (app)
################################################################
#----------------------------------------------------------------
# LIVE-OVERVIEW
#----------------------------------------------------------------
@app.callback(
    Output("overview-collapse", "is_open"),
    [Input("overview-collapse-button", "n_clicks")],
    [State("overview-collapse", "is_open")],
)
def toggle_collapse_overview(n, is_open):
    if n:
        return not is_open
    return is_open
#----------------------------------------------------------------
# Setup
#----------------------------------------------------------------
@app.callback(
    Output("setup-collapse", "is_open"),
    [Input("setup-collapse-button", "n_clicks")],
    [State("setup-collapse", "is_open")],
)
def toggle_collapse_setup(n, is_open):
    if n:
        return not is_open
    return is_open

#----------------------------------------------------------------
# MAP
#----------------------------------------------------------------
@app.callback(
    Output("map-collapse", "is_open"),
    [Input("map-collapse-button", "n_clicks")],
    [State("map-collapse", "is_open")],
)
def toggle_collapse_map(n, is_open):
    if n:
        return not is_open
    return is_open

#----------------------------------------------------------------
# Table
#----------------------------------------------------------------
@app.callback(
    Output("table-collapse", "is_open"),
    [Input("table-collapse-button", "n_clicks")],
    [State("table-collapse", "is_open")],
)
def toggle_collapse_table(n, is_open):
    if n:
        return not is_open
    return is_open


################################################################
# Callback functions (Setup)
################################################################

@app.callback(Output('start-lora', 'disabled'), Input('start-lora', 'n_clicks'), prevent_initial_call=True)
def start_button_click(n):
    global lora_active
    
    # print("Lora Start Button Click")
    
    if lora_active:
        return True
    else:
        if n is None:
            return False
        elif n == 1:
            lora_active = True
            lora_func.Lora_Manager()
            return True

@app.callback(
    Output("Lora-alert-start", "is_open"),
    [Input("start-lora", "n_clicks")],
    [State("Lora-alert-start", "is_open")],
)
def toggle_alert_start(n, is_open):
    
        if n==1:
            return not is_open
        if n==0:
            return is_open
        

@app.callback(
    Output("offcanvas", "is_open"),
    Input("event-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    df = data_func.db_update()
    return dcc.send_data_frame(df.to_csv, "race_data.csv")


################################################################
# Callback functions (MAP)
################################################################
@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = px.data.election() # replace with your own data source
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


################################################################
# Callback functions (Table)
################################################################

# @app.callback(Output('datatable-interactivity', 'data'), Input('interval-component', 'n_intervals'))
# def make_table(n_intervals):
    
#     df = data_func.db_update()
#     size_df = round(len(df.index))
#     print(len(df.index))
#     data = df.to_dict('records')
#     return #data


@app.callback(
    Output('datatable-interactivity', 'data'),
    Input('interval-component', 'n_intervals'),
    Input('datatable-interactivity','page_current'))
def update_table(n_intervals, page_current):
    global page_number
    # print("Table Output Callback")
    df = data_func.db_update()
    page_number = page_current
    # print("Current Page Numvber",page_number)
    
    # my_data = df.iloc[page_current*10:(page_current+ 1)*10].to_dict('records')
    my_data = df.to_dict('records')
    return my_data

@app.callback(
    Output('datatable-interactivity', 'page_current'),
    Input('interval-component', 'n_intervals'),
    Input('my-slider', 'value'),
    prevent_initial_call=True)
def update_output_page(n_intervals, value):
    df = data_func.db_update()
    # print("Number of Pages",round(len(df)/10))
    last_page = math.ceil(len(df)/10)-1
    if value == 0:
        return page_number
    else: 
        return last_page


def live_update():
    global page_number
    # print(page_number)
    return page_number

################################################################
# Start the Dash app in local development mode
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
    
################################################################