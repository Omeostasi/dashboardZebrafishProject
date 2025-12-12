from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard_helpers.functions_UI import hpf_dropdown_tsne, gene_selection_method_dropdown, hpf_options
import pandas as pd
import plotly.express as px
import numpy as np
DEFAULT_STYLE = "bg-white rounded shadow-sm p-4" 

def secondRow():
    return dbc.Row(
        [
            dbc.Col(
                [
   
                    html.Label(
                        "Select HPF for t-SNE:", 
                        className="fw-bold text-secondary small mb-2"
                    ),
                    hpf_dropdown_tsne(
                        hpf_options
                    ),
                ],
                width=6,
            ),

            dbc.Col(
                [
                    
                    html.Label(
                        "Select Gene Selection Method:", 
                        className="fw-bold text-secondary small mb-2"
                    ),
                    gene_selection_method_dropdown(),
                ],
                width=6,
            ),
        ],

        className=f"{DEFAULT_STYLE} g-4 align-items-center" 
    )