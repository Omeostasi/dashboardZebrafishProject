###
# This file loads the selected genes for visualizations of gene expression
###
import pandas as pd
import numpy as np


# top 5 genes based on Anova
anova_genes = ["gene699", "gene698","gene47", "gene547", "gene302"]

# top 5 genes based on random forest importance
rf_genes = [ "gene302", "gene911", "gene912", "gene574", "gene805"]

# top 5 genes based on interesection of Anova and random forest importance
intersection_genes = ["gene47", "gene692", "gene698","gene302", "gene547"]

# Generate csv to store results
selected_genes_dict = {
    "Anova": anova_genes,
    "Random Forest": rf_genes,
    "Intersection": intersection_genes
}
df_selected_genes = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in selected_genes_dict.items() ]))
df_selected_genes.to_csv('data/selected_genes.csv', index=False)