"""Tests for WEAK persistence in the k-terminal-cut problem."""

from ktcut.isolation_branching import isolation_branching


def check_persistence(graph, terminals, persistence_type):
    """Tests for WEAK or STRONG persistence in graph with terminals.

    WEAK persistence means that values which are 1 in the LP relaxation remain 1 in
        an optimal IP solution.
    STRONG persistence means that values which are 0 in the LP relaxation remain 0 in
        an optimal IP solution.

    Args:
        graph: the undirected NetworkX graph for testing persistence
        terminals: the vertices in the graph which are terminals
        persistence_type: "strong" or "weak"

    Returns:
        test_result: TRUE if persistence holds, FALSE if it does not
    """

    _, unseeded_value = isolation_branching(graph,
                                            terminals)

    _, seeded_value = isolation_branching(graph,
                                          terminals,
                                          persistence=persistence_type)

    test_result = (round(unseeded_value, 8) == round(seeded_value, 8))
    return test_result
