"""Test README example."""


def test_graph_tutte():
    from networkx.generators.small import tutte_graph
    from ktcut.isolation_branching import isolation_branching
    graph = tutte_graph()
    terminals = [1, 17, 34]
    partition, cut_value = isolation_branching(graph, terminals)
