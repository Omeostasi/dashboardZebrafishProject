from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard_helpers.functions_UI import kmeans_hpf_dropdown, hpf_options
import pandas as pd
import plotly.express as px
import numpy as np
DEFAULT_STYLE = "bg-white rounded shadow-sm p-3"
def fourthRow():
    return dbc.Row(
        [
           
            dbc.Col(
                html.Div(
                    [
                        html.Label(
                            "Select HPF for K-Means:", 
                            className="fw-bold text-secondary small mb-2"
                        ),
                        kmeans_hpf_dropdown(hpf_options),
                    ],
                    
                    className=DEFAULT_STYLE 
                ),
                width=12, lg=2, 
                className="mb-4 mb-lg-0" 
            ),

            
            dbc.Col(
                [
                    
                    html.Div(
                        [
                            html.Label(
                                "Dendrogram of K-Means Clustering:", 
                                className="fw-bold text-secondary mb-3"
                            ),
                            dcc.Graph(id="dendrogram-kmeans"),
                        ],
                        
                        className=f"{DEFAULT_STYLE} mb-4" 
                    ),

                    
                    html.Div(
                        [
                            html.Label(
                                "t-SNE Plot with K-Means Clusters:", 
                                className="fw-bold text-secondary mb-3"
                            ),
                            html.Div(id="tsne-plot-kmeans-cluster"),
                        ],
                        className=DEFAULT_STYLE 
                    ),
                ],
                width=12, lg=10 
            ),
        ],
        className="g-4" 
    )