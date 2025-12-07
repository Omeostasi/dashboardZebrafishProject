###
# Functions to store UI components for the dashboard
###

# Importing necessary libraries
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash import callback, Input, Output

### MAIN T-SNE PARAMETER SELECTION PART #########
#
# UI: DROP DOWN FOR HPF SELECTION
#
hpf_options = [
    "4hpf",
    "6hpf",
    "8hpf",
    "10hpf",
    "14hpf",
    "18hpf",
    "24hpf"
]
def hpf_dropdown_tsne(hpf_options):
    return dcc.Dropdown(
        id="hpf-dropdown-tsne",
        options=[{'label': hpf, 'value': hpf} for hpf in hpf_options],
        value=[hpf_options[0]],
        multi=True,
        clearable=False,
        style={'width': '200px'}
    )

#
# UI: DROPDOWN FOR GENE SELECTION
#
selection_genes_methods = [
    "Random Forest",
    "ANOVA",
    "Interesection"]
def gene_selection_method_dropdown():    
    return dcc.Dropdown(
        id="gene-selection-method-dropdown",
        options=[{'label': method, 'value': method} for method in selection_genes_methods],
        value=selection_genes_methods[0],
        clearable=False,
        style={'width': '250px'},
        multi=False
    )   



#### PART ABOUT CLUSTER METHOD SELECTION AND PARAMETER SLIDER #########

#
# UI: SLIDER FOR DBSCAN 
#
def cluster_parameter_slider():
    return dcc.Slider(id="dbscan-parameter-slider",
                      min=0.1,
                      max=1.0,
                      step=0.1,
                      value=0.5,
                      marks={i/10: str(i/10) for i in range(1, 11, 5)},
                      tooltip={"placement": "bottom", "always_visible": True}
                     )


#
#   UI: DROPDOWN FOR hpf IN DBSCAN PLOTTING
# 

def dbscan_hpf_dropdown(hpf_options):
    return dcc.Dropdown(
        id="dbscan-hpf-dropdown",
        options=[{'label': hpf, 'value': hpf} for hpf in hpf_options],
        value=[hpf_options[0]],
        multi=True,
        clearable=False,
        style={'width': '200px'}
    )
  

#
# UI: DROPDOWN FOR hpf IN K-MEANS PLOTTING
#

def kmeans_hpf_dropdown(hpf_options):
    return dcc.Dropdown(
        id="kmeans-hpf-dropdown",
        options=[{'label': hpf, 'value': hpf} for hpf in hpf_options],
        value=[hpf_options[0]],
        multi=True,
        clearable=False,
        style={'width': '200px'}
    )