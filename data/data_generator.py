# imports
import pandas as pd
import numpy as np
from src.dbscan import generate_dbscan_dataframe


# Load data
df_original = pd.read_csv('data/zfish.csv')

# Convert 'Type' to string for categorical treatment
types = [
    "Pluripotent",
    "Epidermal",
    "Endoderm",
    "Forebrain",
    "Hindbrain",
    "Neural Crest",
    "Midbrain",
    "Germline",
    "Mesoderm",
    "Other/NaN"
]

df = df_original.copy()

for i, type in enumerate(types):
    df.loc[df['Type'] == i, 'Type'] = type

# Convert RGB columns to categorical
hpfs = [
    "4hpf",
    "6hpf",
    "8hpf",
    "10hpf",
    "14hpf",
    "18hpf",
    "24hpf"
]

df["hpf"] = df['R'].astype(str) + '-' + df['G'].astype(str) + '-' + df['B'].astype(str)

hpf_rgb = df['hpf'].unique().tolist()

for i, hpf in enumerate(hpfs):
    rgb_value = hpf_rgb[i]
    df.loc[df['hpf'] == rgb_value, 'hpf'] = hpf

df = df.drop(columns=['R', 'G', 'B'])


# standardize the data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save processed data
df.to_csv('data/zfish_formatted.csv', index=False)
print("zebrafish dataset correctly formatted: done")


### PART ABOUT PCA
import subprocess
import sys
try:
    subprocess.run([sys.executable, "src/PCA.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running PCA.py: {e.returncode}")

print("PCA transformation: done")



### Creating datastet for K-Means
try:
    subprocess.run([sys.executable, "src/kMEANS.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running kMEANS.py: {e.returncode}")

df_kmeans = pd.read_csv('data/df_kmeans.csv')
df_kmeans = pd.concat([df_kmeans, df.loc[:,["Type", "hpf"]]], axis=1)
df_kmeans.to_csv('data/df_kmeans.csv', index=False)
print("K-Means clustering: done")


### Creating dataset for T-SNE final visualization
print("Creating T-SNE final dataset... is going to take some time")
try:
    subprocess.run([sys.executable, "src/tSNE.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running tSNE.py: {e.returncode}")

df_tsne = pd.read_csv('data/df_tsne.csv')
df_tsne["K-Means"] = df_kmeans["K-Means"]
df_tsne.to_csv('data/df_tsne.csv', index=False)
print("T-SNE final dataset creation: done")

### Creating datastet for selected genes
try:
    subprocess.run([sys.executable, "src/selectedGenes.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running selectedGenes.py: {e.returncode}")

### Created first dataset for DBSCAN
print("Creating initial DBSCAN dataset...")
df_dbscan = generate_dbscan_dataframe(eps_value=0.5, df_kmeans=df_kmeans)
df_dbscan.to_csv('data/df_dbscan.csv', index=False)
print("Initial DBSCAN dataset creation: done")