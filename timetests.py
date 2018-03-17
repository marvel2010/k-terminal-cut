"""Timing/profiling tests of the branch and bound algorithm."""

import random
import numpy as np
import cProfile
import networkx as nx
from branch_and_bound_algorithm import branch_and_bound_algorithm
from ip_algorithm import ip_algorithm
from read_data import read_graph
import time


def main():
    """
    cProfile for branch_and_bound_algorithm
    """

    # graph, terminals = create_random_graph('barabasi_albert', 625, terminal_count=8)
    # assert nx.is_connected(graph), 'graph not connected'
    # time_test_breakdown_branch_and_bound(graph, terminals)
    # time_test_breakdown_ip(graph, terminals)

    for dataset in ['data/polblogs.graph', 'data/celegans_metabolic.graph']:
        print("Now Reading Graph", dataset)
        print()
        graph = read_graph(dataset)
        terminals = np.random.choice(graph.nodes, size=4, replace=False)
        time_test_simple_repeated(graph, terminals, repeat=3)


def time_test_simple_repeated(graph,
                              terminals,
                              repeat=5,
                              test_bb=True,
                              test_bb_weak=False,
                              test_bb_strong=False,
                              test_ip=True):
    """
    Runs several time tests and reports average and median for each of the algorithms.
    """

    times_bb, times_bb_weak, times_bb_strong, times_ip = [], [], [], []

    for _ in range(repeat):

        time_bb, time_bb_weak, time_bb_strong, time_ip = time_test_simple(graph,
                                                                          terminals,
                                                                          test_bb,
                                                                          test_bb_weak,
                                                                          test_bb_strong,
                                                                          test_ip)

        times_bb.append(time_bb)
        times_bb_weak.append(time_bb_weak)
        times_bb_strong.append(time_bb_strong)
        times_ip.append(time_ip)

    if test_bb:
        print("Raw Times for B&B:", times_bb)
        print("Average Time for B&B:", np.average(times_bb))
        print("Median Time for B&B:", np.median(times_bb))
        print()

    if test_bb_weak:
        print("Raw Times for B&B Weak:", times_bb_weak)
        print("Average Time for B&B Weak:", np.average(times_bb_weak))
        print("Median Time for B&B Weak:", np.median(times_bb_weak))
        print()

    if test_bb_strong:
        print("Raw Times for B&B Strong:", times_bb_strong)
        print("Avg Time for B&B Strong:", np.average(times_bb_strong))
        print("Med Time for B&B Strong:", np.median(times_bb_strong))
        print()

    if test_ip:
        print("Raw Times for Integer Program:", times_ip)
        print("Average Time for Integer Program:", np.average(times_ip))
        print("Median Time for Integer Program:", np.median(times_ip))
        print()

    print()

    return (np.average(times_bb),
            np.average(times_bb_weak),
            np.average(times_bb_strong),
            np.average(times_ip)
    )


def time_test_simple(graph,
                     terminals,
                     test_bb,
                     test_bb_weak,
                     test_bb_strong,
                     test_ip):
    """
    Runs a single time test of each of the algorithms (B&B, B&B-weak, B&B-strong, IP).
    """
    t1 = time.time()

    if test_bb:
        branch_and_bound_algorithm(graph.copy(), terminals)

    t2 = time.time()

    if test_bb_weak:
        branch_and_bound_algorithm(graph.copy(), terminals, persistence='weak')

    t3 = time.time()

    if test_bb_strong:
        branch_and_bound_algorithm(graph.copy(), terminals, persistence='strong')

    t4 = time.time()

    if test_ip:
        ip_algorithm(graph.copy(), terminals)

    t5 = time.time()

    return t2-t1, t3-t2, t4-t3, t5-t4


def time_test_breakdown_branch_and_bound(graph,
                                         terminals):
    """
    Runs cProfile to determine the time spent within each function.
    """
    variable_specifications = {'branch_and_bound_algorithm': branch_and_bound_algorithm,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)", variable_specifications, {})


def time_test_breakdown_ip(graph,
                           terminals):
    """
    Runs cProfile to determine the time spent within each function.
    """
    variable_specifications = {'ip_algorithm': ip_algorithm,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("ip_algorithm(graph, terminals)", variable_specifications, {})


def create_random_graph(model_name,
                        node_count,
                        terminal_count=4):
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
