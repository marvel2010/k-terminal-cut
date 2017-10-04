"""Tests for WEAK persistence in the k-terminal-cut problem."""

from timetests import create_random_graph
from branch_and_bound_formulation import branch_and_bound_algorithm
from ip_formulation import ip_algorithm


def main():
    """Constructs a desired random graph and tests weak persistence on it."""
    graph, terminals = create_random_graph('barabasi_albert', 100)
    test_weak_persistence(graph, terminals)
    test_strong_persistence(graph, terminals)


def test_weak_persistence(graph, terminals):
    """Tests for WEAK persistence in graph with terminals

    WEAK persistence means that values which are 1 in the LP relaxation remain 1 in
    an optimal IP solution.

    Args:
        graph: the graph for testing weak persistence
        terminals: the vertices in the graph which are terminals

    Returns:
        unseeded_value: the branch-and-bound optimal without any 1s fixed in advance
        seeded_value: the branch-and-bound optimal with LP 1s fixed in advance
    """

    _, unseeded_value = branch_and_bound_algorithm(graph,
                                                   terminals)

    lp_cut, _ = ip_algorithm(graph,
                             terminals,
                             relaxation=True)

    _, seeded_value = branch_and_bound_algorithm(graph,
                                                 terminals=terminals,
                                                 terminal_sets=lp_cut)

    assert round(unseeded_value, 8) == round(seeded_value, 8), ('persistence violated %s %s'
                                                                % (unseeded_value, seeded_value))
    return unseeded_value, seeded_value


def test_strong_persistence(graph, terminals):
    """Tests for STRONG persistence in graphs with terminals

    STRONG persistence means that the values which are 0 in the LP relaxation remain 1
    in the optimal IP solution (WEAK persistence is a consequence).

    Args:
        graph: the graph for testing strong persistence
        terminals: the vertices in the graph which are terminals

    Returns:
        unseeded_value: the branch-and-bound optimal without any 0s fixed in advance
        seeded_value: the branch-and-bound optimal with LP 0s fixed in advance
    """

    _, unseeded_value = branch_and_bound_algorithm(graph,
                                                   terminals)

    terminals_by_vertex, _ = ip_algorithm(graph,
                                          terminals,
                                          relaxation=True,
                                          persistence_sets=True)

    (final_terminal_assignments,
     seeded_value) = branch_and_bound_algorithm(graph,
                                                terminals=terminals,
                                                terminals_by_vertex=terminals_by_vertex)

    assert round(unseeded_value, 8) == round(seeded_value, 8), ('persistence violated %s %s'
                                                                % (unseeded_value, seeded_value))

    for node in graph.nodes():
        assert sum(node in final_terminal_assignments[t]
                   for t in terminals_by_vertex[node]) == 1, 'persistence violated'

    return unseeded_value, seeded_value


if __name__ == '__main__':
    main()
