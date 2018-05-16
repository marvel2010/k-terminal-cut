"""Timing/profiling tests of the branch and bound algorithm."""

import random
import numpy as np
import cProfile
import networkx as nx
from branch_and_bound_algorithm import branch_and_bound_algorithm
from ip_algorithm import ip_algorithm
from read_data import read_graph
import time
from spectral_clustering import suggested_terminals


def main():

    model = 'powerlaw_cluster'
    for size in range(1000, 10000, 1000):
        time_test_synthetic_repeated(model, size, 4, repeat=5)

    # for dataset in [
    #     'data/celegans_metabolic.graph',
    #     'data/netscience.graph',
    #     'data/email.graph',
    #     'data/power.graph',
    #     'data/hep-th.graph',
    #     'data/polblogs.graph',
    #     'data/PGPGiantcompo.graph',
    #     'data/as-22july06.graph',
    #     'data/cond-mat-2003.graph',
    #     'data/astro-ph.graph'
    # ]:
    #     print("Now Reading Graph", dataset)
    #     graph = read_graph(dataset)
    #     print('Is connected?', dataset, nx.is_connected(graph))
    #     print('Vertices', len(graph.nodes))
    #     print('Component Count', len([c for c in nx.connected_components(graph)]))
    #     print('Max Component Size', max(len(component) for component in nx.connected_components(graph)), '\n')
    #     terminals, total_degree = suggested_terminals(graph, 8)
    #     print("Terminals Suggested. \n")
    #
    #     # Some Basic Information about the Cuts
    #     partition, cut_size = branch_and_bound_algorithm(graph, terminals, reporting=True)
    #
    #     # print()
    #     # time_test_breakdown_branch_and_bound(graph, terminals)
    #     # time_test_breakdown_ip(graph, terminals)


def time_test_synthetic_repeated(model_name,
                                 node_count,
                                 terminal_count,
                                 repeat=3,
                                 test_bb=True,
                                 test_bb_weak=False,
                                 test_bb_strong=False,
                                 test_ip=True):
    """
    Runs several time tests and reports average and median for each of the algorithms.
    """

    times_bb, times_bb_weak, times_bb_strong, times_ip = [], [], [], []

    for _ in range(repeat):

        graph, _ = create_random_graph(model_name=model_name,
                                       node_count=node_count,
                                       terminal_count=terminal_count)
        terminals, _ = suggested_terminals(graph=graph,
                                           terminal_count=terminal_count)
        print(len(graph.nodes), len(graph.edges))

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

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)",
                    variable_specifications, {}, sort='cumtime')


def time_test_breakdown_ip(graph,
                           terminals):
    """
    Runs cProfile to determine the time spent within each function.
    """
    variable_specifications = {'ip_algorithm': ip_algorithm,
                               'graph': graph,
                               'terminals': terminals}

    cProfile.runctx("ip_algorithm(graph, terminals)",
                    variable_specifications, {}, sort='cumtime')


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
        # n = the number of nodes
        # m = the number of random edges to add for each new node
        # p = probability of adding a triangle after adding a random edge
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
