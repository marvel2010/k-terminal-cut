"""Solves the IP Formulation of the k-Terminal Cut Problem."""

from ktcut.ip_formulation import IPFormulation


def ip_algorithm(graph, terminals, solver=None):
    """Solves the IP formulation of the Multiterminal Cut Problem.

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k

    Args:
        graph: The networkx graph for which the k-Terminal Cut problem is to be solved.
        terminals: The vertices which are terminals in the k-Terminal Cut problem.
        solver: which solver to use to solve the IP.

    Returns:
        source_sets: dictionary of nodes to terminal.
        cut_value: value of the IP or LP cut.
    """
    ip_formulation = IPFormulation(graph, terminals, solver)
    ip_formulation.solve_ip()

    source_sets = ip_formulation.get_source_sets()
    cut_value = ip_formulation.get_cut_value()

    return source_sets, cut_value
