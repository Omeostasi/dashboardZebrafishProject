import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from plotly.figure_factory  import create_dendrogram
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from src.dbscan import *
import textwrap
from dash import no_update, dcc

#
# FUNCTION TO PLOT HIERARCHICAL CLUSTERING DENDROGRAM
#
def plot_dendogram(df_kmeans):
    data = df_kmeans
    n_clusters = 3
    data = data.iloc[:, :-2]  # Exclude the last two columns (Type and hpf)
    X = data.groupby(data.columns[-1]).mean()
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward', compute_distances=True)
    model = model.fit(X)
    Z, kwargs = get_linkage_matrix(model, n_clusters=n_clusters)
    # Actually create the dendrogram figure from plotly
    fig = create_dendrogram(
    X,
    linkagefun=lambda x: Z,
    color_threshold=kwargs['color_threshold'] 
    )
     # Add a horizontal line to visualize the cut threshold
    fig.add_shape(
        type='line',
        x0=0, x1=len(X)*10,    # Extend line across the plot
        y0=kwargs['color_threshold'],
        y1=kwargs['color_threshold'],
        line=dict(color='black', width=2, dash='dash')
    )
    fig.update_layout(
    title=f"Dendrogram with Cut Threshold at {kwargs['color_threshold']}",
    width=800,
    height=500
    )


 
    dendro_leaves_x = fig['layout']['xaxis']['tickvals']
    dendro_leaves_labels = fig['layout']['xaxis']['ticktext']


   
    invisible_trace = go.Scatter(
        x=dendro_leaves_x,
        y=[0] * len(dendro_leaves_x),        # All at y=0
        mode='markers',
        marker=dict(size=10, opacity=0),     # Invisible (opacity 0)
        customdata=dendro_leaves_labels,     # Store the index/label here
        hoverinfo='text',                    # Show text on hover
        hovertext=[f"Cluster: {label}" for label in dendro_leaves_labels], 
        showlegend=False
    )

    # 3. Add to figure
    fig.add_trace(invisible_trace)

    return fig




#
#  HELPER FUNCTION: Convert Sklearn model to Linkage Matrix
#
def get_linkage_matrix(model, n_clusters=None, **kwargs):
    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Using uniform distances as per your original snippet
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # --- LOGIC TO SHOW 3 CLUSTERS ---
    # If n_clusters is requested, we calculate the cut threshold
    if n_clusters is not None:
        # We look at the merge that reduced n_clusters to (n_clusters - 1)
        # This merge happens at the 2nd to last index for 3 clusters, etc.
        # We set the threshold slightly below that distance.
        if linkage_matrix.shape[0] >= n_clusters:
            # The merge index we want to be "above" the cut
            last_merge_index = -(n_clusters - 1) 
            cut_height = linkage_matrix[last_merge_index, 2]
            
            # Set threshold slightly lower than the merge height
            kwargs['color_threshold'] = cut_height - 0.5

    return linkage_matrix, kwargs


####### END DENDOGRM PLOTTING FUNCTIONALITY #########

### START tSNE VISUALIZATION
import plotly.express as px


#
# FUNCTION TO PLOT T-SNE VISUALIZATION BASED ON CLUSTER  and hpf
#

def plot_tsne_kMeans(clickData,  hpf_list, df_tsne):
    # Extract cluster numbers from clickData
    
    if len(clickData) > 0:
        cluster_numbers = clickData
    else:
        return no_update
                                         
     # Filtering cluster numbers from clickData and hpf_list
    data = df_tsne[df_tsne["K-Means"].isin(cluster_numbers) & (df_tsne['hpf'].isin(hpf_list))]
    fig = px.scatter(
        data,
        x='TSNE1',
        y='TSNE2',
        # subplot per hpf value
        facet_col='hpf',
        facet_col_wrap=2,
        color='Type',
        symbol= 'K-Means',
        title=f"t-SNE Visualization for hpf: {', '.join(map(str, hpf_list))} and K-Means Clusters: {', '.join(map(str, cluster_numbers))}",
        labels={'TSNE1': 't-SNE Dimension 1', 'TSNE2': 't-SNE Dimension 2'},
        hover_data=['Type', 'hpf', "K-Means"]
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(legend_title_text='Type')
    # to fix the size of the plot and prevent it from growing vertically
    fig.update_layout(
        legend_title_text='Type',
        height=700,  # Explicit height stops vertical growth
        width=1000   
    )
    return dcc.Graph(figure=fig)

#
# FUNCTION TO PLOT T-SNE VISUALIZATION BASED on hpf only
#
def plot_tsne_hpf(hpf_list, df_tsne):

    df_tsne = df_tsne
    data = df_tsne[df_tsne['hpf'].isin(hpf_list)]


    fig = px.scatter(
        data,
        x='TSNE1',
        y='TSNE2',
        color='Type',
        # subplot per hpf value
        facet_col='hpf',    
        facet_col_wrap=2,    # wrapt to next row after 2
        title=f"t-SNE Visualization for hpf: {', '.join(map(str, hpf_list))}",
        labels={'TSNE1': 't-SNE Dimension 1', 'TSNE2': 't-SNE Dimension 2'},
        hover_data=['Type', 'hpf', 'K-Means']
    )

    # Style updates
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(legend_title_text='Type', height=700, width=1000)

    return fig

#### END tSNE VISUALIZATION FUNCTIONALITY #########

### START GENES EXPRESSION VISUALIZATION

#
# FUNCTION TO PLOT HEATMAP OF GENE EXPRESSION
#
def plot_gene_expression_heatmap(gene_method, selectedData, df_tsne, df_selected_genes):
    # getting index from selected data

    if selectedData and selectedData['points']:
        
        # --- Data IS selected ---
        selected_index = [point['pointIndex'] for point in selectedData['points']]
    else:
        # --- No Data is selected  ---
            return no_update
    # Filter the dataframe for the selected genes
  
    data = df_tsne.iloc[selected_index]
    gene_list = df_selected_genes[gene_method].tolist()
    # Create heatmap
    fig = px.imshow(
        data[gene_list],
        labels=dict(x="Genes", y="Cells (Index)", color="Expression Level"),
        color_continuous_scale='Viridis',
        title='Selected Genes and Selected Cells Expression Heatmap',
        aspect='auto'  
    )
    
    return dcc.Graph(figure=fig)

#### END GENE EXPRESSION VISUALIZATION FUNCTIONALITY #########

### START DBSCAN PLOTTING FUNCTIONALITY
#
# FUNCTION TO PLOT DBSCAN CLUSTERS BASED ON EPS VALUE and HPF
#
def plot_dbscan_clusters(hpf_list, df_dbscan):
    
    data = df_dbscan[df_dbscan['hpf'].isin(hpf_list)]
    fig = px.scatter(
        data,
        x='PC1',
        y='PC2',
        color='Type',
        facet_col='hpf',
        facet_col_wrap=2,
        symbol='DBSCAN',
        title=f't-SNE Visualization of DBSCAN Clusters',
        labels={'TSNE1': 't-SNE Dimension 1', 'TSNE2': 't-SNE Dimension 2'},
        hover_data=['Type', 'hpf', 'DBSCAN']
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(legend_title_text='DBSCAN Cluster', height=700, width=1000)
    return fig


#
# FUNCTION TO PLOT FOR EACH HPF A DIFFERENT GRAPH
#
def dbscan_hpf_plots_generatator(hpf_list, df_dbscan):
    plots = []
    for hpf in hpf_list:
        data = df_dbscan[df_dbscan['hpf'] == hpf]
        # Make DBSCAN discrete
        data['DBSCAN'] = data['DBSCAN'].astype(str)

        fig = px.scatter(
            data,
            x='PC1',
            y='PC2',
            color='DBSCAN',
            symbol='Type',
            title=f"DBSCAN Clusters for hpf: {hpf}",
            labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'},
            hover_data=['Type', 'hpf', 'DBSCAN']
        )

        # Improve markers
        fig.update_traces(
            marker=dict(
                size=5,
                opacity=0.6,
                line=dict(width=0.3, color='black')
            )
        )

        # Better layout
        fig.update_layout(
            legend_title_text='DBSCAN Cluster',
            height=700,
            width=900,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05
            )
        )
        plots.append(dcc.Graph(figure=fig))
    return plots