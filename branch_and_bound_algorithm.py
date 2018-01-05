"""Solves the Branch and Bound Formulations of the Multiterminal Cut Problem."""

from branch_and_bound_tree import BranchAndBoundTree


def branch_and_bound_algorithm(graph,
                               terminals,
                               terminal_sets=None,
                               terminals_by_vertex=None):
    """Wrapper for solving the branch_and_bound algorithm for a given graph and terminals.

    The multi-terminal cut partitions the graph into sets such that each partition
        contains exactly one terminal node and the weight of edges between sets is minimized.

    Args:
        graph: the networkx graph in which to find the multi-terminal cut
        terminals: the terminals of the networkx graph
        terminal_sets: fixed assignments of some nodes to terminals
        terminals_by_vertex: vertices that can only be assigned to some terminals

    Returns:
        source_sets: the partition of the nodes of the graph which defines the minimum cut
        cut_value: the weight of the optimal multi-terminal cut
    """
    branch_and_bound_tree = BranchAndBoundTree(graph,
                                               terminals=terminals,
                                               terminal_sets=terminal_sets,
                                               terminals_by_vertex=terminals_by_vertex)
    return branch_and_bound_tree.solve()
