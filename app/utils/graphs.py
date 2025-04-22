import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        pass

    def build_operator_graph(self, parsed_sql):
        G = nx.DiGraph()

        for j in parsed_sql["joins"]:
            G.add_node(j["table"], type="join")
            G.add_edge(j["table"], j["condition"], label="on")

        if parsed_sql["where"]:
            G.add_node("σ", condition=parsed_sql["where"], type="select")

        G.add_node("π", fields=parsed_sql["select"], type="project")
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)

        # Nós
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=1500)

        # Arestas
        nx.draw_networkx_edges(G, pos, ax=ax, arrowstyle='->', arrowsize=20)

        # Rótulos dos nós
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12)

        # Rótulos das arestas
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_color='red')

        ax.axis('off')
        return fig

