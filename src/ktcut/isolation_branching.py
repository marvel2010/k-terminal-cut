""" Solves the Multiterminal Cut Problem using Branch and Bound. """
from ktcut.lp_algorithm import lp_algorithm
from ktcut.branch_and_bound_tree import BranchAndBoundTree


def isolation_branching(graph, terminals, persistence=None, reporting=False):
    """
    Wrapper for solving the branch_and_bound algorithm
        for a given graph and terminals.

    The multi-terminal cut partitions the graph into sets
        such that each partition contains exactly one terminal node
        and the weight of edges between sets is minimized.

    Assumes that the graph has 'capacity' along each edge. Otherwise,
        assumes the capacity should be 1.0.

    Args:
        graph: the networkx graph in which to find the multi-terminal cut
        terminals: the terminals of the networkx graph
        persistence: if persistence is assumed [strong, weak, None]

    Returns:
        source_sets: the partition of the nodes of the graph which defines the minimum cut
        cut_value: the weight of the optimal multi-terminal cut
    """
    for u, v in graph.edges:
        if "capacity" in graph[u][v]:
            continue
        else:
            graph[u][v]["capacity"] = 1.0

    if persistence in {"strong", "weak"}:
        terminals_by_vertex = lp_algorithm(graph, terminals, persistence=persistence)
        branch_and_bound_tree = BranchAndBoundTree(
            graph, terminals=terminals, terminals_by_vertex=terminals_by_vertex
        )
    else:
        terminals_by_vertex = {node: terminals for node in graph.nodes()}
        branch_and_bound_tree = BranchAndBoundTree(
            graph, terminals=terminals, terminals_by_vertex=terminals_by_vertex
        )

    source_sets, cut_value = branch_and_bound_tree.solve(reporting=reporting)

    if reporting:
        print("Nodes Explored:", branch_and_bound_tree.nodes_explored_count)

    return source_sets, cut_value
