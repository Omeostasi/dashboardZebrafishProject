import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from plotly.figure_factory  import create_dendrogram
import numpy as np
from src.dbscan import *

#
# FUNCTION TO PLOT HIERARCHICAL CLUSTERING DENDROGRAM
#
def plot_dendogram():
    data = pd.read_csv('data/df_kmeans.csv')
    n_clusters = 3
    data = data.iloc[:, :-2]  # Exclude the last two columns (Type and hpf)
    X = data.groupby(data.columns[-1]).mean()
    Z, kwargs = get_linkage_matrix(model, n_clusters=n_clusters)
    # Actually create the dendrogram figure from plotly
    fig = create_dendrogram(
    X,
    linkagefun=lambda x: Z,
    color_threshold=kwargs['color_threshold']  # <--- The key parameter
    )
     # Add a horizontal line to visualize the cut threshold
    fig.add_shape(
        type='line',
        x0=0, x1=len(X)*10,    # Span the whole width (Plotly defaults to 10 units per leaf)
        y0=kwargs['color_threshold'],
        y1=kwargs['color_threshold'],
        line=dict(color='black', width=2, dash='dash')
    )
    fig.update_layout(
    title=f"Dendrogram with Cut Threshold at {kwargs['color_threshold']}",
    width=800,
    height=500
    )
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
def plot_tsne_kMeans(cluster_numbers : list, df_tsne, hpf_list):
    data = df_tsne[df_tsne["K-Means"].isin(cluster_numbers) & (df_tsne['hpf'].isin(hpf_list))]
    data = data.sort_values('hpf')
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
    return fig

#
# FUNCTION TO PLOT T-SNE VISUALIZATION BASED on hpf only
#
def plot_tsne_hpf(hpf_list, df_tsne):
    
    data = df_tsne[df_tsne['hpf'].isin(hpf_list)]
    
    # Sort data to ensure subplots appear in order
    data = data.sort_values('hpf')

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
    fig.update_layout(legend_title_text='Type')

    return fig

#### END tSNE VISUALIZATION FUNCTIONALITY #########

### START GENES EXPRESSION VISUALIZATION

#
# FUNCTION TO PLOT HEATMAP OF GENE EXPRESSION
#
def plot_gene_expression_heatmap(gene_method, selected_index, df_tsne, df_selected_genes):
    # Filter the dataframe for the selected genes
    data = df_tsne[df_tsne.index.isin(selected_index)]
    gene_list = df_selected_genes[gene_method].tolist()
    # Create heatmap
    fig = px.imshow(
        data[gene_list],
        labels=dict(x="Genes", y="Cells (Index)", color="Expression Level"),
        color_continuous_scale='Viridis',
        title='Selected Genes and Selected Cells Expression Heatmap',
        aspect='auto'  
    )
    
    fig.update_layout(
        xaxis_nticks=20,
        height=600,
        width=1000
    )
    
    return fig

#### END GENE EXPRESSION VISUALIZATION FUNCTIONALITY #########

### START DBSCAN PLOTTING FUNCTIONALITY
#
# FUNCTION TO PLOT DBSCAN CLUSTERS BASED ON EPS VALUE and HPF
#
def plot_dbscan_clusters(hpf_list, df_dbscan):
    df_dbscan = pd.read_json(df_dbscan, orient='split')
    data = df_dbscan[df_dbscan['hpf'].isin(hpf_list)]
    data = data.sort_values('hpf')
    fig = px.scatter(
        data,
        x='PCA1',
        y='PCA2',
        color='DBSCAN',
        facet_col='hpf',
        facet_col_wrap=2,
        title=f't-SNE Visualization of Zebrafish Data for DBSCAN Clusters at eps={eps_value} and hpf={", ".join(map(str, hpf_list))}',
        labels={'TSNE1': 't-SNE Dimension 1', 'TSNE2': 't-SNE Dimension 2'},
        hover_data=['Type', 'hpf', 'DBSCAN']
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(legend_title_text='DBSCAN Cluster')
    return fig