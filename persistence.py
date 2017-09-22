"""Tests for WEAK persistence in the k-terminal-cut problem."""

from timetests import create_random_graph
from branch_and_bound_formulation import branch_and_bound_algorithm
from ip_formulation import ip_algorithm


def main():
    graph, terminals = create_random_graph('barabasi_albert', 100)
    test_weak_persistence(graph, terminals)


def test_weak_persistence(graph, terminals):

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
