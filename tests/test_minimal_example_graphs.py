""" Test Graph. """


def test_graph_tutte():
    from networkx.generators.small import tutte_graph
    from ktcut.branch_and_bound_algorithm import branch_and_bound_algorithm
    graph = tutte_graph()
    terminals = [1, 17, 34]
    partition, cut_value = branch_and_bound_algorithm(graph, terminals)
