import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        pass

    def build_operator_graph(parsed_sql):
        G = nx.DiGraph()

        for j in parsed_sql["joins"]:
            G.add_node(j["table"], type="join")
            G.add_edge(j["table"], j["condition"], label="on")

        if parsed_sql["where"]:
            G.add_node("σ", condition=parsed_sql["where"], type="select")

        G.add_node("π", fields=parsed_sql["select"], type="project")

        return G
