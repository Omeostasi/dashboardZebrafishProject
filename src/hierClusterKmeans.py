import pandas as pd
from sklearn.cluster import AgglomerativeClustering


# Load data
df = pd.read_csv('data/df_kmeans.csv')
X = df.iloc[:, :-2]  # Exclude the last two columns (Type and hpf)
X = X.groupby(df['KMeans_Cluster']).mean()


model = AgglomerativeClustering(n_clusters=3, linkage='ward', compute_distances=True)


labels = model.fit_predict(X)





