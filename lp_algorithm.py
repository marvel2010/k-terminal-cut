"""Solves the LP Formulation of the Multiterminal Cut Problem using Gurobi."""

from ip_formulation import IPFormulation


def lp_algorithm(graph,
                 terminals,
                 persistence=None):
    """Solves the IP formulation of the Multiterminal Cut Problem using Gurobi.

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k

    Args:
        graph: The networkx graph for which the Multiterminal Cut Problem is to be solved.
        terminals: The nodes which are terminals in the Multiterminal Cut Problem.
        strong_persistence: TODO

    Returns:
        dictionary of possible_terminals_by_node.
        value of the IP or LP cut.
    """

    ip_formulation = IPFormulation(graph, terminals)

    ip_formulation.solve_lp()

    if persistence == 'strong':
        return ip_formulation.get_possible_terminals_by_node_strong()
    elif persistence == 'weak':
        return ip_formulation.get_possible_terminals_by_node_weak()
    else:
        return ip_formulation.get_cut_value()
