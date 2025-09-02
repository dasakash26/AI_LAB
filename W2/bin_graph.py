import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df_bin = pd.read_csv('binary_input.csv', header=None)

G = nx.from_pandas_adjacency(df_bin)

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(6,6))
nx.draw(
    G, pos,
    with_labels=True,
    node_size=600,
    node_color='lightblue',
    edge_color='grey',
    font_size=10,
    font_weight='bold'
)
plt.title("Binary Graph", pad=15)
plt.axis('off')
plt.tight_layout()
plt.show()
