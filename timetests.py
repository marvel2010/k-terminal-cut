"""Timing/profiling tests of the branch and bound algorithm."""

import random
import cProfile
import networkx as nx
from branch_and_bound_formulation import branch_and_bound_algorithm


def main():
    """
    cProfile for branch_and_bound_algorithm
    """

    graph, terminals = create_random_graph('barabasi_albert', 10000)

    assert nx.is_connected(graph), 'graph not connected'

    variable_specifications = {'branch_and_bound_algorithm': branch_and_bound_algorithm,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)", variable_specifications, {})


def create_random_graph(model_name, node_count):
    """Creates a random graph according to some model.

    Args:
        model_name: which model to use for the random graph
        node_count: number of nodes in the graph

    Returns:
        graph: the graph in networkx format
        terminals: the terminals in a list

    Raises:
        ValueError: if model_name is not a valid model name
    """

    if model_name == 'gnp':
        graph = nx.gnp_random_graph(node_count, 0.01)
    elif model_name == 'lobster':
        graph = nx.random_lobster(node_count, 0.1, 0.1)
    elif model_name == 'powerlaw_tree':
        graph = nx.random_powerlaw_tree(node_count)
    elif model_name == 'powerlaw_cluster':
        graph = nx.powerlaw_cluster_graph(node_count, 10, 0.1)
    elif model_name == 'barabasi_albert':
        graph = nx.barabasi_albert_graph(node_count, 3)
    elif model_name == 'connected_watts_strogatz':
        graph = nx.connected_watts_strogatz_graph(node_count, 10, 0.1)
    elif model_name == 'newman_watts_strogatz':
        graph = nx.newman_watts_strogatz_graph(node_count, 10, 0.1)
    else:
        raise ValueError("")

    for edge in graph.edges_iter():
        graph[edge[0]][edge[1]]['capacity'] = 0.1 + random.random()

    terminals = [0, 1, 2, 3]

    return graph, terminals


if __name__ == '__main__':
    main()
