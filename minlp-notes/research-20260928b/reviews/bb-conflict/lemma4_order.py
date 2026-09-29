"""Lemma 4 needs the incumbent OPT when off-path children are evaluated.
Separable example: phi(z) = sum_i (z_i - 0.1)^2 on [0,1]^p, z in {0,1}^p, so z° = 0,
OPT = 0.01 p, and a single wrong fixing costs 0.8 >= 0.01 (p-1): C1 holds for p <= 81.
Compare depth-first B&B (branch on lowest free index, explore the z_i = 1 child first)
started with incumbent OPT versus with no incumbent."""
import math
p, eps = 10, 1e-9
def bound(fix):            # fix: tuple of fixed values for z_1..z_j
    return sum((v - 0.1) ** 2 for v in fix)          # free coordinates contribute 0
def dfs(UB0):
    UB = [UB0]; nodes = [0]
    def visit(fix):
        nodes[0] += 1
        b = bound(fix)
        if b >= UB[0] - eps:
            return
        if len(fix) == p:          # integral: new incumbent
            UB[0] = min(UB[0], b); return
        for v in (1, 0):
            visit(fix + (v,))
    visit(())
    return nodes[0], UB[0]
OPT = 0.01 * p
print("p=%d, C1 holds: %s" % (p, 0.81 - 0.01 >= 0.01 * (p - 1) - eps))
print("DFS (1-child first) with incumbent OPT: nodes=%d (Lemma 4 bound 2p+1=%d)" % (dfs(OPT)[0], 2 * p + 1))
print("DFS (1-child first) without incumbent:  nodes=%d" % dfs(math.inf)[0])
