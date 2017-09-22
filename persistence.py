"""Tests for WEAK persistence in the k-terminal-cut problem."""

from timetests import create_random_graph
from branch_and_bound_formulation import branch_and_bound_algorithm
from ip_formulation import ip_algorithm


def main():
    """Constructs a desired random graph and tests weak persistence on it."""
    graph, terminals = create_random_graph('barabasi_albert', 100)
    test_weak_persistence(graph, terminals)


def test_weak_persistence(graph, terminals):
    """Tests for WEAK persistence in graph with terminals

    WEAK persistence means that values which are 1 in the LP relaxation remain 1 in
    an optimal IP solution. STRONG persistence means that values which are 1 or 0 in
    the LP relaxation remain 1 or 0 (respectively) in an optimal IP solution.

    Args:
        graph: the graph for testing weak persistence
        terminals: the vertices in the graph which are terminals

    Returns:
        unseeded_value: the branch-and-bound optimal without any 1s fixed in advance
        seeded_value: the branc-and-bound optimal with LP 1s fixed in advance
    """

    _, unseeded_value = branch_and_bound_algorithm(graph,
                                                   terminals)

    lp_cut, _ = ip_algorithm(graph, terminals, relaxation=True)

    _, seeded_value = branch_and_bound_algorithm(graph,
                                                 terminals=terminals,
                                                 terminal_sets=lp_cut)

    assert unseeded_value == seeded_value, 'persistence violated'
    return unseeded_value, seeded_value


if __name__ == '__main__':
    main()
