# imports
import pandas as pd
import numpy as np


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
print("done")