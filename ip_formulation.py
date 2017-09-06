"""Solves the LP and IP Formulations of the Multiterminal Cut Problem using Gurobi."""

from gurobipy import Model
from gurobipy import GRB
from gurobipy import quicksum


def ip_algorithm(graph, terminals, relaxation=False):
    """Solves the IP formulation of the Multiterminal Cut Problem using Gurobi.

    Vertex Variables: x_i^k for each vertex i for each set k
    Edge Variables: z_ij^k for each edge (i, j) for each set k

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k

    Args:
        graph: The networkx graph for which the Multiterminal Cut Problem is to be solved.
        terminals: The nodes which are terminals in the Multiterminal Cut Problem.
        relaxation: Solves the LP relaxation instead of the full IP.

    Returns:
        dictionary of terminal to nodes associated with terminal.
    """

    mdl = Model("MultiTerminalCuts")

    x_variables = {}
    z_variables = {}

    # VARIABLE X: node i, set k
    for i in graph.nodes():
        x_variables[i] = {}
        for k in terminals:
            if relaxation:
                x_variables[i][k] = mdl.addVar(vtype=GRB.CONTINUOUS,
                                               lb=0.0,
                                               ub=1.0,
                                               name="Node %s, Terminal %s" % (i, k))
            else:
                x_variables[i][k] = mdl.addVar(vtype=GRB.BINARY,
                                               name="Node %s, Terminal %s" % (i, k))

    # VARIABLE Z: node i, node j, set k
    for i in graph.nodes():
        z_variables[i] = {}
        for j in graph[i]:
            z_variables[i][j] = {}
            for k in terminals:
                if relaxation:
                    z_variables[i][j][k] = mdl.addVar(vtype=GRB.CONTINUOUS,
                                                      lb=0.0,
                                                      ub=1.0,
                                                      obj=0.5*graph[i][j]['capacity'],
                                                      name="Node %s, Node %s" % (i, j))
                else:
                    z_variables[i][j][k] = mdl.addVar(vtype=GRB.BINARY,
                                                      obj=0.5*graph[i][j]['capacity'],
                                                      name="Node %s, Node %s" % (i, j))

    mdl.modelSense = GRB.MINIMIZE
    mdl.update()

    # CONSTRAINT: one terminal per node
    for i in graph.nodes():
        mdl.addConstr(quicksum(x_variables[i][k] for k in terminals) == 1.0, "CtrNode %s" % str(i))

    # CONSTRAINT: price for cut
    for (i, j) in graph.edges():
        for k in terminals:
            mdl.addConstr(z_variables[i][j][k] >= x_variables[i][k] - x_variables[j][k],
                          name="Z1 %s %s %s" % (i, j, k))
            mdl.addConstr(z_variables[i][j][k] >= x_variables[j][k] - x_variables[i][k],
                          name="Z2 %s %s %s" % (i, j, k))

    # INITIALIZE
    for k in terminals:
        mdl.addConstr(x_variables[k][k] == 1.0, name="Init %s" % k)

    # solve
    mdl.Params.LogToConsole = 0
    mdl.optimize()

    # print solution
    source_sets = {terminal: set() for terminal in terminals}
    for i in graph.nodes():
        for k in terminals:
            if x_variables[i][k].x == 1.0:
                source_sets[k].add(i)
    cut_value = round(mdl.ObjVal, 8)

    return source_sets, cut_value
