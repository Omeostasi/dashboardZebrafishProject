from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Load PCA-transformed data
df_pca = pd.read_csv('data/pca.csv')




# Run K-Means on the PCA result (best k = 10)
kmeans = KMeans(n_clusters=10, random_state=42)
labels = kmeans.fit_predict(df_pca)

# Add cluster labels to the DataFrame

df_kmeans = df_pca.copy()
df_kmeans['K-Means'] = labels
# Save the results
df_kmeans.to_csv('data/df_kmeans.csv', index=False)