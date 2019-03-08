import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AffinityPropagation
from sklearn import metrics


def suggested_terminals_spectral(graph, terminal_count):
    """Suggests a set of terminal vertices for the given graph.

    The terminals are suggested according to a two-step procedure.
        First, we perform a spectral clustering on the graph with
        terminal_count clusters. Then, within each cluster, we suggest
        the vertex which has the highest degree.

    Args:
        graph: the graph in which to suggest the terminals.
        terminal_count: the number of terminals to suggest.

    Returns:
        terminals: the suggested terminal vertices in the graph.
        total_degree: total degree of the terminal vertices in the graph.
    """
    adj_matrix = nx.to_numpy_matrix(graph)

    sc = SpectralClustering(n_clusters=terminal_count, affinity="precomputed")
    sc.fit(adj_matrix)

    deg = graph.degree()

    terminals = []
    total_degree = 0

    for c in range(terminal_count):
        restricted_nodes = [
            (degree, node)
            for node, degree in deg
            if sc.labels_[list(graph).index(node)] == c
        ]
        maximizer = max(restricted_nodes)
        total_degree += maximizer[0]
        terminals.append(maximizer[1])

    return terminals, total_degree
