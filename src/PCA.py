from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize PCA with 10 components
pca= PCA(n_components=10)

df = pd.read_csv('data/zfish_formatted.csv')

# transform the data using PCA

df_pca = pca.fit_transform(df.iloc[:,:-2])

df_pca = pd.DataFrame(df_pca, columns=[f'PC{i+1}' for i in range(df_pca.shape[1])])

# store results in a csv file
df_pca.to_csv('data/pca.csv', index=False)

