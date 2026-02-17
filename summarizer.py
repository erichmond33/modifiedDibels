import json
import networkx as nx
from collections import Counter

data = json.load(open('code_index_graph.json'))
G = nx.node_link_graph(data)

print(f"Total nodes: {G.number_of_nodes()}")
print(f"Total edges: {G.number_of_edges()}")

# Count by type
types = [G.nodes[n].get('type', 'unknown') for n in G.nodes]
print(Counter(types))

# Example: how many functions were found?
functions = [n for n, d in G.nodes(data=True) if d.get('type') == 'function']
print(f"Functions indexed: {len(functions)}")

# Look for Django-specific patterns
model_classes = [n for n in G.nodes if 'models.py' in n and G.nodes[n].get('type') == 'class']
print(f"Model classes found: {len(model_classes)}")