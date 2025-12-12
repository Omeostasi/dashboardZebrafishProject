# Dashboard
## import necessary libraries
from dash import Dash, html, dcc, callback, Output, Input, State
from dashboard_helpers import *
from src.dbscan import generate_dbscan_dataframe
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# loading css style
DEFAULT_STYLE = "bg-white rounded shadow-sm p-3"

# loading heavy data data
df_tsne = pd.read_csv("data/df_tsne.csv")
df_selected_genes = pd.read_csv("data/selected_genes.csv")
df_kmeans = pd.read_csv("data/df_kmeans.csv")

# LAYOUT OF THE DASHBOARD
app.layout = dbc.Container([
    # FIRST ROW: TITLE
    firstRow(),
    # SECOND ROW: DROPDOWN FOR HPF TSNE, DROPDOWN GENE SELECTION
    secondRow(),
    # THIRD ROW: TSNE BY HPF AND HEATMAP 
    thirdRow(),
    # FOURTH ROW: DROPDOWN HPF FOR K-MEANS, PLOT DENDOGRAM, PLOT TSNE-CLUSTER
    fourthRow(),
    dcc.Store(id='clickData_dendrogram_store'),
    dcc.Store(id='start_dendrogram', data='start'),
    # FIFTH ROW: DROPDOWN HPF FOR DBSCAN AND INPUT/SLIDER FOR PARAMETERS, PCA PLOT FOR DBSCAN
    fifthRow(),
    dcc.Store(id='df_dbscan_store'),
])



# CALLBACKS

## SEECOND-THIRD ROWS
### UPDATE TSNE BASED ON HPF SELECTION
@callback(
    Output('tsne-graph-by-hpf', 'figure'),
    Input('hpf-dropdown-tsne', 'value')
)
def update_tsne_graph(selected_hpf):
    return plot_tsne_hpf(selected_hpf, df_tsne)

### UPDATE GENE EXPRESSION HEATMAP BASED ON GENE SELECTION and TSNE SELECTION
@callback(
    Output('heatmap-container', 'children'),
    Input('gene-selection-method-dropdown', 'value'),
    Input('tsne-graph-by-hpf', 'selectedData')

)
def update_gene_expression_heatmap(selected_genes, selected_tsne):
    if selected_tsne and selected_tsne["points"]:
        return plot_gene_expression_heatmap(selected_genes, selected_tsne, df_tsne, df_selected_genes)
    else:
        return html.Div(
            [
                # Small icon or header to grab attention (optional)
                html.H6("No Data Selected", className="fw-bold text-secondary mb-1"),
      
                html.P(
                    "Select [selection box] specific points in the t-SNE plot to generate this heatmap.", 
                    className="text-muted small mb-0"
                )
            ],
         
            className="d-flex flex-column justify-content-center align-items-center bg-light border rounded p-4 h-100"
        )


## FOURTH ROW
### RENDER DENDROGRAM
@callback(
    Output('dendrogram-kmeans', 'figure'),
    Input('start_dendrogram', 'data')
)
def render_dendrogram(data):
    return plot_dendogram(df_kmeans)

### STORE CLICKDATA FROM DENDROGRAM
@callback(
    Output('clickData_dendrogram_store', 'data'),
    Input('dendrogram-kmeans', 'clickData'),
    State('clickData_dendrogram_store', 'data')
)
def store_clickdata_dendrogram(clickData, stored_clickData):
    if clickData and clickData["points"]:
        if int(clickData["points"][0]["customdata"]) in stored_clickData:
            stored_clickData.remove(int(clickData["points"][0]["customdata"]))
            return stored_clickData
        else:
            stored_clickData.append(int(clickData["points"][0]["customdata"]))
            return stored_clickData
    if stored_clickData is None:
            stored_clickData = []
            return stored_clickData
### TSNE-CLUSTER BASED ON HPF SELECTION and DENDOGRAM CLICKDATA
@callback(
    Output('tsne-plot-kmeans-cluster', 'children'),
    Input('clickData_dendrogram_store', 'data'),
    Input('kmeans-hpf-dropdown', 'value')
)
def update_dendrogram_and_tsne(clickData, selected_hpf):
    if clickData is None or len(clickData) == 0:
        # if nothing selected
        return html.Div(
            [
                html.H6("No Cluster Selected", className="fw-bold text-secondary mb-1"),
                html.P(
                    "Click on a  leaf in the dendrogram to visualize the t-SNE projection and the specific cluster points.", 
                    className="text-muted small mb-0"
                )
            ],
          
            className="d-flex flex-column justify-content-center align-items-center bg-light border rounded p-4 h-100"
        )
    else:
        return plot_tsne_kMeans(clickData, selected_hpf, df_tsne)  

## FIFTH ROW
### GENERATE AND STORE NEW DBSCAN DATA BASED ON EPS INPUT
@callback(
    Output('df_dbscan_store', 'data'),
    Input('dbscan-parameter-slider', 'value')
)
def generate_dbscan_data(eps_value):
    df_dbscan = generate_dbscan_dataframe(eps_value, df_kmeans)
    return df_dbscan.to_json()

### UPDATE PCA BASED ON DBSCAN PARAMETERS AND HPF SELECTION
@callback(
    Output('dbscan-pca-plot-container', 'children'),
    Input('dbscan-hpf-dropdown', 'value'),
    Input('df_dbscan_store', 'data')
)
def update_dbscan_plot(selected_hpf, df_dbscan_json):
    df_dbscan = pd.read_json(df_dbscan_json)
    return dbscan_hpf_plots_generatator(selected_hpf, df_dbscan)



if __name__ == '__main__':
    app.run(debug=True)
