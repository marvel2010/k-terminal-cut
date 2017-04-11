from gurobipy import *


def ip_algorithm(G, terminals):

    m = Model("Scheduling")

    x_variables = {}
    z_variables = {}

    # VARIABLE X:
    # node i, set k
    for i in G.nodes():
        x_variables[i] = {}
        for k in terminals:
            x_variables[i][k] = m.addVar(vtype=GRB.BINARY, name="Node %s, Terminal %s" % (i, k))

    # VARIABLE Z:
    # node i, node j
    for i in G.nodes():
        z_variables[i] = {}
        for j in G.nodes():
            z_variables[i][j] = m.addVar(vtype=GRB.BINARY, obj=1, name="Node %s, Node %s" % (i, j))

    m.modelSense = GRB.MINIMIZE
    m.update()

    # CONSTRAINT
    # one terminal per node
    for i in G.nodes():
        m.addConstr(quicksum(x_variables[i][k] for k in terminals) == 1, "CtrNode %s" % i)

    # CONSTRAINT
    # price for cut
    for (i, j) in G.edges():
        for k in terminals:
            m.addConstr(z_variables[i][j] >= x_variables[i][k] - x_variables[j][k], name="Z1 %s %s %s" % (i, j, k))
            m.addConstr(z_variables[i][j] >= x_variables[j][k] - x_variables[i][k], name="Z2 %s %s %s" % (i, j, k))

    # INITIALIZE
    for k in terminals:
        m.addConstr(x_variables[k][k] == 1.0, name="INIT %s" % k)

    # solve
    m.optimize()

    # print solution
    print("Total Utility: ", m.objVal)
    print("Solution")
    for i in G.nodes():
        for k in terminals:
            if x_variables[i][k].x == 1.0:
                print(i, ' with terminal ', k)

    return 0
