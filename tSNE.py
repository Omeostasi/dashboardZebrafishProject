import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

# Initialize t-SNE with 2 components
tsne = TSNE(n_components=2, random_state=42, perplexity=50) # 50 is a good starting point for larger datasets

