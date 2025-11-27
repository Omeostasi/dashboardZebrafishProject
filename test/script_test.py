import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

df = pd.DataFrame({
    "hpf": ["0", "2", "1"],
    "gene0" : [0, 3, 6],
    "gene1" : [0, 1, 0],
    "Type": ["0", "1", "2"]
})

print(df[df["hpf"]=="2"].index)
x = np.sort(df["hpf"].unique())