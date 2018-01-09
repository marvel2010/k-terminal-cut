"""Tests for WEAK persistence in the k-terminal-cut problem."""

from timetests import create_random_graph
from branch_and_bound_algorithm import branch_and_bound_algorithm
from lp_algorithm import lp_algorithm


def test_persistence(graph, terminals, persistence_type):
    """Tests for WEAK or STRONG persistence in graph with terminals

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

    _, seeded_value = branch_and_bound_algorithm(graph,
                                                 terminals=terminals,
                                                 persistence=persistence_type)

    return round(unseeded_value, 8) == round(seeded_value, 8)