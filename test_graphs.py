from branch_and_bound import branch_and_bound_algorithm
from ip_formulation import ip_algorithm
import itertools
import random
import time
import networkx as nx


def main():

    G, terminals = test_random_graph()
    #G, terminals = test_small_graph()

    assert nx.is_connected(G), 'graph not connected'

    #print(nx.get_edge_attributes(G, 'capacity'))
    #print(nx.degree(G, weight='capacity'))
    print()

    t1 = time.time()
    final_node = branch_and_bound_algorithm(G, terminals)
    t2 = time.time()

    print('BB Final')
    print('BB Final Sets ', final_node.contained_sets)
    print('BB Final Value ', final_node.lower_bound)
    print('BB Time ', round(t2-t1, 2))
    print("\n")

    t3 = time.time()
    ip_algorithm(G, terminals)
    t4 = time.time()
    print('IP Time ', round(t4-t3, 2))


def test_random_graph():
    #G = nx.gnp_random_graph(1000, 0.01)
    #G = nx.random_lobster(1000, 0.1, 0.1)
    #G = nx.random_powerlaw_tree(1000)
    #G = nx.powerlaw_cluster_graph(1000, 10, 0.1)
    G = nx.barabasi_albert_graph(10000, 3)
    #G = nx.connected_watts_strogatz_graph(1000, 10, 0.1)
    #G = nx.newman_watts_strogatz_graph(1000, 10, 0.1)
    for edge in G.edges_iter():
        G[edge[0]][edge[1]]['capacity'] = 0.1 + random.random()
    return G, [0, 1, 2, 3]


def test_small_graph():
    # test graph 1
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, 9)])
    G.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)], capacity=2)
    G.add_edges_from([(1, 5), (2, 6), (3, 7), (4, 8)], capacity=3)
    # graph with LP 7.5, IP 8
    G2 = nx.Graph()
    G2.add_nodes_from([1, 2, 3, 12, 13, 23])
    G2.add_edges_from([(1, 12), (1, 13), (2, 12), (2, 23), (3, 13), (3, 23)], capacity=2)
    G2.add_edges_from([(12, 13), (13, 23), (12, 23)], capacity=1)
    # graph with LP 24, IP 26
    G3 = nx.Graph()
    G3.add_nodes_from([1, 2, 3, 4, 12, 13, 14, 23, 24, 34])
    G3.add_edges_from([(1, 12), (1, 13), (1, 14),
                       (2, 12), (2, 23), (2, 24),
                       (3, 13), (3, 23), (3, 34),
                       (4, 14), (4, 24), (4, 34)],
                      capacity=3)
    G3.add_edges_from([(12, 13), (12, 14), (12, 23), (12, 24),
                       (13, 14), (13, 23), (13, 34),
                       (14, 24), (14, 34),
                       (23, 24), (23, 34),
                       (24, 34)], capacity=1)
    # graph with LP 26, IP 27
    G4 = nx.Graph()
    G4.add_nodes_from([1, 2, 3, 4, 123, 124, 134, 234])
    G4.add_edges_from([(1, 123), (1, 124), (1, 134),
                       (2, 123), (2, 124), (2, 234),
                       (3, 123), (3, 134), (3, 234),
                       (4, 124), (4, 134), (4, 234)],
                      capacity=3)
    G4.add_edges_from([(123, 124), (123, 134), (123, 234),
                       (124, 134), (124, 234),
                       (134, 234)],
                      capacity=1)
    # graph with LP 105, IP 110
    G5 = nx.Graph()
    total_range = range(1, 6)
    subset_sizes = 3
    agreement = 1
    G5.add_nodes_from(total_range)
    G5.add_nodes_from(itertools.combinations(total_range, subset_sizes))
    G5.add_edges_from([(a, b)
                       for a in total_range
                       for b in itertools.combinations(total_range, subset_sizes)
                       if a in set(b)], capacity=5)
    G5.add_edges_from([(a, b)
                       for a in itertools.combinations(total_range, subset_sizes)
                       for b in itertools.combinations(total_range, subset_sizes)
                       if len(set(a) & set(b)) == agreement], capacity=1)
    return G5, total_range


if __name__ == '__main__':
    main()
