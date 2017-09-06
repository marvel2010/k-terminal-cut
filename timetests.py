"""Timing/profiling tests of the branch and bound algorithm."""

import random
import cProfile
import networkx as nx
from branch_and_bound_tree import branch_and_bound_algorithm
from ip_formulation import ip_algorithm


def main():

    graph, terminals = create_random_graph()

    assert nx.is_connected(graph), 'graph not connected'

    # print(nx.get_edge_attributes(G, 'capacity'))
    # print(nx.degree(G, weight='capacity'))

    # print(ip_algorithm(graph, terminals))

    # final_node = branch_and_bound_algorithm(G, terminals)

    # print('BB Final')
    # print('BB Final Sets ', final_node.contained_sets)
    # print('BB Final Value ', final_node.lower_bound)
    # print('BB Time ', round(t2-t1, 2))
    # print("\n")

    cProfile.runctx("branch_and_bound_algorithm(graph, terminals)", {'branch_and_bound_algorithm': branch_and_bound_algorithm,
                                                                     'graph': graph,
                                                                     'terminals': terminals}, {})


def create_random_graph():
    """Creates a random graph according to some model."""

    # G = nx.gnp_random_graph(1000, 0.01)
    # G = nx.random_lobster(1000, 0.1, 0.1)
    # G = nx.random_powerlaw_tree(1000)
    # G = nx.powerlaw_cluster_graph(1000, 10, 0.1)
    graph = nx.barabasi_albert_graph(10000, 3)
    # G = nx.connected_watts_strogatz_graph(1000, 10, 0.1)
    # G = nx.newman_watts_strogatz_graph(1000, 10, 0.1)

    for edge in graph.edges_iter():
        graph[edge[0]][edge[1]]['capacity'] = 0.1 + random.random()
        #G[edge[0]][edge[1]]['capacity'] = 1 + int(9*random.random())

    return graph, [0, 1, 2, 3]


if __name__ == '__main__':
    main()
