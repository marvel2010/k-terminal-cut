"""Solves the LP Formulation of the k-Terminal Cut Problem."""

from ktcut.ip_formulation import IPFormulation


def lp_algorithm(graph, terminals, persistence=None, solver=None):
    """Solves the LP formulation of the k-Terminal Cut Problem.

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k

    Args:
        graph: The networkx graph for which the k-Terminal Cut problem is to be solved.
        terminals: The vertices which are terminals in the k-Terminal Cut problem.
        persistence: If `strong', assumes that 0s and 1s are persistent. If
            'weak', assumes only 0s are persistent.
        solver: which solver to use to solve the LP.

    Returns:
        dictionary of possible_terminals_by_node.
        value of the IP or LP cut.
    """
    ip_formulation = IPFormulation(graph, terminals, solver)
    ip_formulation.solve_lp()

    if persistence == "strong":
        return ip_formulation.get_possible_terminals_by_node_strong()
    elif persistence == "weak":
        return ip_formulation.get_possible_terminals_by_node_weak()
    else:
        return ip_formulation.get_cut_value()
