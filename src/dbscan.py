###
# FUNCTION TO PLOT DBSCAN CLUSTERS BASED ON EPS VALUE
###
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

def generate_dbscan_dataframe(eps_value):
    df_dbscan = pd.read_csv('data/pca.csv').iloc[:,:2] # Using first two PCA components for plotting
    labels = DBSCAN(eps=eps_value, min_samples=5).fit_predict(df_dbscan)
    df_dbscan['DBSCAN'] = labels
    df_meta = pd.read_csv('data/zfish_formatted.csv', usecols=['Type', 'hpf'])
    df_dbscan = pd.concat([df_dbscan, df_meta], axis=1)
    return df_dbscan.to_json(orient='split', date_format='iso')