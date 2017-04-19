from branch_and_bound import branch_and_bound_algorithm
from ip_formulation import ip_algorithm
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
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, 9)])
    G.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)], capacity=2)
    G.add_edges_from([(1, 5), (2, 6), (3, 7), (4, 8)], capacity=3)
    return G, [1, 2, 3, 4]

if __name__ == '__main__':
    main()
