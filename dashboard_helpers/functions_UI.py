###
# Functions to store UI components for the dashboard
###

# Importing necessary libraries
from dash import dcc, html
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
    "Anova",
    "Intersection"]
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
def dbscan_parameter_slider():
    return dcc.Slider(id="dbscan-parameter-slider",
                      min=0.2,
                      max=2.0,
                      step=0.1,
                      value=0.9,
                      marks={i/10: f"{i/10:.1f}" for i in range(2, 21, 5)} | {2.0: '2.0'},
                      tooltip={"placement": "bottom", "always_visible": True},
                      persistence_type='session'
                     )


#
# UI: INPUT FOR eps IN DBSCAN
#

def dbscan_eps_input():
    return dcc.Input(
        id="dbscan-eps-input",
        type="number",
        placeholder='Enter a value from 0.1 to 5.0',
        min=0.1,
        max=5.0,
        value=0.5,
        style={'width': '100px'}
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