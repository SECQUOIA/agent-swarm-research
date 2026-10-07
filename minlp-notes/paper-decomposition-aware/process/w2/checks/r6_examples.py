"""R6-writing: exact checks of a few example numbers quoted in rewrites."""
from fractions import Fraction as Fr

def graded(lo, hi, c, h, th):
    nodes = {c}
    for sgn, end in ((1, hi), (-1, lo)):
        t = Fr(0)
        R = abs(end - c)
        while t < R:
            t = min(t + h + th * t, R)
            nodes.add(c + sgn * t)
    return sorted(nodes)

def widths(G):
    w = {}
    for a, b in zip(G, G[1:]):
        w[a] = max(w.get(a, 0), b - a)
        w[b] = max(w.get(b, 0), b - a)
    return w

# constraints.tex: two graded grids around 3/10 and 7/10, h=1/16, theta=1/4
G1 = graded(Fr(0), Fr(1), Fr(3, 10), Fr(1, 16), Fr(1, 4))
G2 = graded(Fr(0), Fr(1), Fr(7, 10), Fr(1, 16), Fr(1, 4))
print("sizes", len(G1), len(G2), "common", sorted(set(G1) & set(G2)))
w1, w2 = widths(G1), widths(G2)
m = Fr(1, 2)
for nu in sorted(set(G1) & set(G2)):
    lhs = (nu - m) ** 2  # times L
    rhs = (w1[nu] ** 2 + w2[nu] ** 2) / 8
    print("nu", nu, "L(nu-m)^2 > d1+d2 ?", lhs > rhs, lhs, rhs)

# Example tu-sum: grid {0,1,9/4,3}, corrections, corrected values (in units of L)
G = [Fr(0), Fr(1), Fr(9, 4), Fr(3)]
w = widths(G)
d = {v: w[v] ** 2 / 8 for v in G}
print("d", d)
target = (Fr(1), Fr(1), Fr(2))
vals = []
for a in G:
    for b in G:
        for c in G:
            if a + b - c == 0:
                F = sum((x - y) ** 2 for x, y in zip((a, b, c), target)) / 2
                vals.append(((a, b, c), F - d[a] - d[b] - d[c]))
for p, v in vals:
    print(p, v)
