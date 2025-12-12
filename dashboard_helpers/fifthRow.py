from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard_helpers.functions_UI import hpf_options, dbscan_hpf_dropdown, dbscan_parameter_slider
import pandas as pd
import plotly.express as px
import numpy as np
DEFAULT_STYLE = "bg-white rounded shadow-sm p-3"

def fifthRow():
    return dbc.Row(
        [
            dbc.Col(

                [ dbc.Row([

                    dbc.Col([
                            html.Label("Select HPF for DBSCAN Clustering:"),
                            dbscan_hpf_dropdown(hpf_options),
                    ]),
                ]),

                dbc.Row([

                    dbc.Col([
                              
                    html.Label("Set DBSCAN Epsilon Parameter:"),
                    dbscan_parameter_slider(),
                
                    ]),
                
                ]),
        ], width=3,),
            dbc.Col(
                [
                    html.Label("PCA Plot with DBSCAN Clusters:"),
                    html.Div(id='dbscan-pca-plot-container'),
                ],
                width=9,
            ),
        ],
        className=DEFAULT_STYLE
    )