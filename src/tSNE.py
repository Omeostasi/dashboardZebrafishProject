import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

### CREATING TSNE DATASET

df_original = pd.read_csv("data/zfish_formatted.csv")
hpfs_list = df_original['hpf'].unique().tolist()

# Get t-SNE for the first hpf to initialize the dataframe
df_hpf = df_original[df_original['hpf'] == hpfs_list[0]].iloc[:, :-2]
# Initialize t-SNE with 2 components and best perplexity and learning rate found
tsne = TSNE(n_components=2, random_state=42, learning_rate=600, perplexity=50)
df_tsne = pd.DataFrame(tsne.fit_transform(df_hpf))

# Loop through the rest of the hpfs and concatenate the results
for hpf in hpfs_list[1:]:
    df_hpf = df_original[df_original['hpf'] == hpf].iloc[:, :-2]
    tsne = TSNE(n_components=2, random_state=42, learning_rate=600, perplexity=50)
    df_tsne_temp = pd.DataFrame(tsne.fit_transform(df_hpf))
    df_tsne = pd.concat([df_tsne, df_tsne_temp], axis=0,  ignore_index=True)

df_tsne.columns = ["TSNE1", "TSNE2"]

df_tsne = pd.concat([df_tsne, df_original], axis=1)

df_tsne.to_csv("data/df_tsne.csv", index=False)

### END CREATING TSNE DATASET ###