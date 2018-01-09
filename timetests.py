"""Timing/profiling tests of the branch and bound algorithm."""

import random
import cProfile
import networkx as nx
from branch_and_bound_algorithm import branch_and_bound_algorithm
from ip_algorithm import ip_algorithm
import time


def main():
    """cProfile for branch_and_bound_algorithm"""

    graph, terminals = create_random_graph('barabasi_albert', 10000, terminal_count=4)

    assert nx.is_connected(graph), 'graph not connected'

    time_test_breakdown(graph, terminals)
    time_test_simple(graph, terminals)

    # # WORKING
    # partition, value = branch_and_bound_algorithm(graph.copy(), terminals)
    # print(partition)
    # print(value)
    # print({t: len(partition[t]) for t in terminals})
    # print()
    #
    # # WORKING
    # partition_ip, value_ip = ip_algorithm(graph.copy(), terminals)
    # print(partition_ip)
    # print(value_ip)
    # print({t: len(partition_ip[t]) for t in terminals})
    # print()

def time_test_simple(graph, terminals):
    t1 = time.time()

    branch_and_bound_algorithm(graph.copy(), terminals)

    t2 = time.time()
    print("Time for Branch and Bound (no persistence): %s" % (t2-t1))

    branch_and_bound_algorithm(graph.copy(), terminals, persistence='weak')

    t3 = time.time()
    print("Time for Branch and Bound (weak persistence): %s" % (t3 - t2))

    branch_and_bound_algorithm(graph.copy(), terminals, persistence='strong')

    t4 = time.time()
    print("Time for Branch and Bound (strong persistence): %s" % (t4 - t3))

    ip_algorithm(graph.copy(), terminals)

    t5 = time.time()
    print("Time for Integer Program: %s" % (t5 - t4))


def time_test_breakdown(graph, terminals):
    """
    Runs cProfile to determine the time spent within each function.
    """
    variable_specifications = {'branch_and_bound_algorithm': branch_and_bound_algorithm,
                               'ip_algorithm': ip_algorithm,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)", variable_specifications, {})
    cProfile.runctx("ip_algorithm(graph, terminals)", variable_specifications, {})

def create_random_graph(model_name, node_count, terminal_count=4):
    """Creates a random graph according to some model.

    Args:
        model_name: which model to use for the random graph
        node_count: number of nodes in the graph
        terminal_count: number of terminals in the graph

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

    for edge in graph.edges():
        graph[edge[0]][edge[1]]['capacity'] = 0.1 + random.random()

    terminals = range(terminal_count)

    return graph, terminals


if __name__ == '__main__':
    main()
