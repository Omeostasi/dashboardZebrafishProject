from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard_helpers.functions_UI import hpf_dropdown_tsne, gene_selection_method_dropdown, hpf_options
import pandas as pd
import plotly.express as px
import numpy as np

DEFAULT_STYLE = "bg-white rounded shadow-sm p-4"
def thirdRow():
    return dbc.Row(
        [
            # --- Graph 1: t-SNE ---
            dbc.Col(
                html.Div(
                    [
                        html.Label(
                            "t-SNE Visualization by Selected HPF:", 
                            className="fw-bold text-secondary mb-3"
                        ),
                        dcc.Graph(id="tsne-graph-by-hpf"),
                    ],
                    className=DEFAULT_STYLE 
                ),
                width=12,
                className="mb-4" # Adds space between this graph and the one below
            ),

            # --- Graph 2: Heatmap ---
            dbc.Col(
                html.Div(
                    [
                        html.Label(
                            "Heatmap of Gene Expression Levels:", 
                            className="fw-bold text-secondary mb-3"
                        ),
                        html.Div(id="heatmap-container")
                    ],
                    className=DEFAULT_STYLE 
                ),
                width=12, 
            ),
        ]
    )