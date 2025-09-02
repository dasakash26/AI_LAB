import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('numerical_input.csv', header=None)
G = nx.from_pandas_adjacency(df)

pos = nx.spring_layout(G)

plt.figure(figsize=(5, 5))
plt.title("Numerical Graph", pad=15)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.show()
