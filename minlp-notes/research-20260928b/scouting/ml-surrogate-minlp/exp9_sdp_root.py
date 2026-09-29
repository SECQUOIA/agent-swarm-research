"""Experiment 9: root bound of the spectrahedral relaxation R_SDP of the hidden layer
(p_e + q_e <= (1 - Y_ij)/2, Y psd, diag(Y) = 1), i.e. the Goemans-Williamson SDP,
on the Petersen graph and on K_n; compare with max cut and with the LP roots."""
import itertools
import numpy as np
import cvxpy as cp

def gw(n, E):
    Y = cp.Variable((n, n), PSD=True)
    obj = cp.Maximize(sum((1 - Y[i, j]) / 2 for i, j in E))
    prob = cp.Problem(obj, [cp.diag(Y) == 1])
    prob.solve(solver=cp.SCS, eps=1e-8) if 'SCS' in cp.installed_solvers() else prob.solve()
    return prob.value

outer = [(i, (i + 1) % 5) for i in range(5)]; spokes = [(i, i + 5) for i in range(5)]
inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
print("solvers:", cp.installed_solvers())
print(f"Petersen: SDP root = {gw(10, outer + spokes + inner):.4f}, max cut = 12, LP roots (triangle / 4-input hulls) = 15")
for n in [5, 6, 7, 8]:
    E = list(itertools.combinations(range(n), 2))
    print(f"K_{n}: SDP root = {gw(n, E):.4f}, max cut = {n*n//4}, triangle LP root = {len(E)}, 3-input LP root = {2*len(E)/3:.3f}")
