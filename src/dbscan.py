###
# FUNCTION TO PLOT DBSCAN CLUSTERS BASED ON EPS VALUE
###
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

def generate_dbscan_dataframe(eps_value, df_kmeans):
    df_dbscan = df_kmeans.iloc[:,:2] # Using first two PCA components for plotting
    labels = DBSCAN(eps=eps_value, min_samples=5).fit_predict(df_dbscan)
    df_dbscan['DBSCAN'] = labels
    df_dbscan = pd.concat([df_dbscan, df_kmeans.iloc[:,-2:]], axis=1) # Adding back 'Type' and 'hpf' columns
    return df_dbscan