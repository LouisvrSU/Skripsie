import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
import pandas as pd

from data import data_func

from sqlalchemy import create_engine

df = data_func.db_init()



layout = html.Div(
    [
        dbc.Row(
            [
                
            ],
            ),
        dbc.Row(
            [
                    
                # html.Div(id="table-container",style={"maxHeight": "500px", "overflow": "hidden auto", "position": "relative"}), 
                
                dcc.Interval(
                id='interval-component',
                interval=1*5000, # in milliseconds
                n_intervals=0
                ),
                dcc.Slider(0, 1, 1,
                value=0,
                id='my-slider'
                ), 
                    
                dash_table.DataTable(
                        id='datatable-interactivity',
                        columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                        ],
                        data=df.to_dict('records'),
                        editable=False,
                        row_deletable=False,
                        page_action='native',
                        page_size=10,
                        # column_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        # page_current=fun.page_number,
                        # page_action='native',
                        # style_table={'height': '300px', 'overflowY': 'auto'},
                        style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white' ,'fontWeight': 'bold'},
                        style_data={'backgroundColor': 'rgb(80, 80, 80)','color': 'white'},
                        style_cell={'textAlign': 'left'},
                        style_cell_conditional=[{'if': {'column_id': 'Region'},'textAlign': 'left'},],
                        )        
                        
                # html.Div(id='my-table-output',className="d-grid gap-2",),
                
                # dash_table.DataTable(
                #         id='datatable-interactivity',
                #         columns=[
                #             {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                #         ],
                #         data=df.to_dict('records'),
                #         editable=False,
                #         row_deletable=False,
                #         page_action='native',
                #         page_size=10,
                #         # column_deletable=False,
                #         selected_columns=[],
                #         selected_rows=[],
                #         # page_current=page_number,
                #         # page_action='native',
                #         # style_table={'height': '300px', 'overflowY': 'auto'},
                #         style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white' ,'fontWeight': 'bold'},
                #         style_data={'backgroundColor': 'rgb(80, 80, 80)','color': 'white'},
                #         style_cell={'textAlign': 'left'},
                #         style_cell_conditional=[{'if': {'column_id': 'Region'},'textAlign': 'left'},],
                #         )
                
            ],
        ),
    ],

)

# scanner_table_data = dash_table.DataTable(
#                         id='datatable-interactivity',
#                         columns=[
#                             {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
#                         ],
#                         # data=df.to_dict('records'),
#                         editable=False,
#                         row_deletable=False,
#                         page_action='native',
#                         page_size=10,
#                         # column_deletable=False,
#                         selected_columns=[],
#                         selected_rows=[],
#                         # page_current=page_number,
#                         # page_action='native',
#                         # style_table={'height': '300px', 'overflowY': 'auto'},
#                         style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white' ,'fontWeight': 'bold'},
#                         style_data={'backgroundColor': 'rgb(80, 80, 80)','color': 'white'},
#                         style_cell={'textAlign': 'left'},
#                         style_cell_conditional=[{'if': {'column_id': 'Region'},'textAlign': 'left'},],
#                         )
