"""R5 consistency check: claims after Prop. tu-misaligned (constraints.tex) and
Example tu-sum, using the graded-grid rule of Definition def:graded (growth.tex).
Exact rational arithmetic."""
from fractions import Fraction as Fr

def graded(lo, hi, c, h, theta):
    nodes = {c}
    t = Fr(0)
    while c + t < hi:
        t = min(t + h + theta * t, hi - c); nodes.add(c + t)
    t = Fr(0)
    while c - t > lo:
        t = min(t + h + theta * t, c - lo); nodes.add(c - t)
    return sorted(nodes)

def corr(G, L):
    d = {}
    for k, v in enumerate(G):
        ws = []
        if k > 0: ws.append(v - G[k-1])
        if k < len(G) - 1: ws.append(G[k+1] - v)
        d[v] = L * max(ws) ** 2 / 8
    return d

L = Fr(1)
h, th = Fr(1, 16), Fr(1, 4)
G1 = graded(Fr(0), Fr(1), Fr(3, 10), h, th)
G2 = graded(Fr(0), Fr(1), Fr(7, 10), h, th)
print("G1 (center 3/10):", len(G1), [str(x) for x in G1])
print("G2 (center 7/10):", len(G2), [str(x) for x in G2])
common = sorted(set(G1) & set(G2))
print("common nodes:", [str(x) for x in common])
d1, d2 = corr(G1, L), corr(G2, L)
m = Fr(1, 2)
for nu in common:
    lhs = L * (nu - m) ** 2; rhs = d1[nu] + d2[nu]
    print(f"nu={nu}: L(nu-m)^2={lhs} > d1+d2={rhs}: {lhs > rhs}")

# Example tu-sum: grid around 0 on [0,3], h=1, theta=1/4
G = graded(Fr(0), Fr(3), Fr(0), Fr(1), Fr(1, 4))
print("tu-sum grid:", [str(x) for x in G], {str(k): str(v) for k, v in corr(G, L).items()})
