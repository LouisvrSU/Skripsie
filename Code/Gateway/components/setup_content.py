import dash_bootstrap_components as dbc
from dash import html, dcc


# Dash Bootstrap Layout
#----------------------------------------------------------------

layout = html.Div(
    [

        dbc.Row(
            [
                
                dbc.Col(
                    
                    html.Div(
                            [
                            dbc.Button("Event Settings", color="warning", id="event-offcanvas", n_clicks=0),
                            dbc.Offcanvas(
                                html.P(
                                    "This is the content of the Offcanvas. "
                                    "Close it by clicking on the close button, or "
                                    "the backdrop."
                                ),
                                id="offcanvas",
                                title="Event Info",
                                is_open=False,
                            ),
                        ],
                    className="d-grid gap-2",
                    ),
                ),
                
                dbc.Col(
                    
                    html.Div(
                            dbc.Button("START LORA", color="success", className="mb-3", id="start-lora", n_clicks=0),
                    className="d-grid gap-2",
                    ),
                    
                
                ),
                
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button("Download Data", id="btn_csv", color="secondary"),
                            dcc.Download(id="download-dataframe-csv"),
                        ],
                        className="d-grid gap-2",
                    ),
                ),
            ],
            
        ),
        
        
        dbc.Row(
            [
            dbc.Alert(
                "LoRa is Active!", 
                color='success',
                id='Lora-alert-start',
                is_open=False,
                duration=4000,
                fade=True

                ),   
            ],
            ),
    ]
)

