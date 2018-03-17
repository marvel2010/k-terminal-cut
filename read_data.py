import networkx as nx


def read_graph(filename):
    """
    Read a graph from a file in the format specified for the DIMACS challenge.
    """
    graph = nx.Graph()
    f = open(filename)
    count = 0
    for line in f:
        if count:
            for neighbor in line.split():
                graph.add_edge(count, int(neighbor), capacity=1)
        else:
            node_count, edge_count, _ = line.split()
            graph.add_nodes_from(range(1, int(node_count) + 1))
        count += 1
    return graph
