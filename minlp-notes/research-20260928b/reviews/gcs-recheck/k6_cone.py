"""Item 6: squared-length perspective formulations.

(a) the note's squared-length examples (Example C', Prop. 5.2 C2/C3) with the explicit rotated cone
    and with cvxpy quad_over_lin, under Clarabel and SCS;
(b) random squared-length DAGs: REL_H under all four (formulation, solver) combinations; counts of
    non-optimal statuses (e.g. false 'infeasible') and value discrepancies; REL_H <= OPT."""
import sys
import numpy as np
from rc import PSet, pt, box, G, relax, opt_exact, simple_paths

COMBOS = [("cone", "CLARABEL"), ("qol", "CLARABEL"), ("cone", "SCS"), ("qol", "SCS")]


def iv(a, b):
    return PSet(V=[[a], [b]])


def show(name, g, **kw):
    vals = []
    for mode, sol in COMBOS:
        v, _, st = relax(g, sq_mode=mode, solver=sol, **kw)
        vals.append(f"{mode}/{sol}={v:.6f}" + ("" if st == "optimal" else f"({st})"))
    print(f"  {name}: " + "  ".join(vals))


print("(a) examples")
# Example C'
sets = {"s": pt(0.0), "A": iv(1, 3), "P": pt(3.5), "Q": pt(4.5), "t": pt(6.0)}
E = [("s", "A"), ("A", "P"), ("A", "Q"), ("P", "t"), ("Q", "t")]
g = G(sets, E, "s", "t", "sq")
print(f"  Example C' OPT(sq)={opt_exact(g)[0]:.6f}")
show("C' REL(sq)", g, hull=False)
show("C' REL_H(sq)", g, hull=True)
ge = G(sets, E, "s", "t", "l2")
print(f"  C' Euclidean: OPT={opt_exact(ge)[0]:.6f} REL={relax(ge, hull=False)[0]:.6f}")

# Prop 5.2: C2 and C3
sets = {"s": pt(-1.0), "1": iv(-0.5, 0.5), "2": pt(0.0), "3": pt(0.0), "t": pt(1.0)}
E = [("s", "1"), ("1", "2"), ("2", "1"), ("1", "t"), ("s", "3"), ("3", "t")]
c2 = G(sets, E, "s", "t", "sq")
print(f"  C2 OPT={opt_exact(c2)[0]:.6f} (simple paths: {[''.join(p) for p in simple_paths(c2)]})")
show("C2 REL_H(deg)", c2, hull=True, degree=True)
show("C2 REL_H(no deg)", c2, hull=True, degree=False)
cut2 = lambda g, y, z, zp, lam, w: [y[("1", "2")] + y[("2", "1")] <= y[("1", "2")]]  # y_12 + y_21 <= y_2 (flow through 2)
show("C2 REL_H(deg)+2-cycle cut", c2, hull=True, degree=True, extra=cut2)
sets3 = dict(sets, **{"4": pt(0.0)})
E3 = [("s", "1"), ("1", "2"), ("2", "4"), ("4", "1"), ("1", "t"), ("s", "3"), ("3", "t")]
c3 = G(sets3, E3, "s", "t", "sq")
print(f"  C3 OPT={opt_exact(c3)[0]:.6f}")
show("C3 REL_H(deg)", c3, hull=True, degree=True)


def flow(g, y, v):
    return sum(y[e] for e in g.inn[v])


def two_cycle_cuts(g, y, z, zp, lam, w):
    cons = []
    for (u, v) in g.E:
        if (v, u) in g.E and u < v:
            for x in (u, v):
                if x not in (g.s, g.t):
                    cons.append(y[(u, v)] + y[(v, u)] <= flow(g, y, x))
    return cons


def gsec(g, y, z, zp, lam, w):
    S = ["1", "2", "4"]
    inner = sum(y[e] for e in g.E if e[0] in S and e[1] in S)
    return [inner <= sum(flow(g, y, v) for v in S if v != k) for k in S]


show("C3 REL_H(deg)+2-cycle cuts", c3, hull=True, degree=True, extra=two_cycle_cuts)
show("C3 REL_H(deg)+GSEC{1,2,4}", c3, hull=True, degree=True, extra=gsec)

# (b) random squared-length DAGs
print("(b) random squared-length layered DAGs (REL_H, no degree constraints)")
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
n_inst = int(sys.argv[2]) if len(sys.argv) > 2 else 60
stat_bad = {c: 0 for c in COMBOS}
maxdev = {c: 0.0 for c in COMBOS}
viol = 0
gaps = 0
for it in range(n_inst):
    dim = int(rng.integers(1, 4))
    layers = [1] + [int(rng.integers(1, 4)) for _ in range(int(rng.integers(2, 4)))] + [1]
    sets, names = {}, []
    for li, k in enumerate(layers):
        row = []
        for j in range(k):
            nm = f"{li}_{j}"
            c = np.r_[3.0 * li, rng.normal(size=dim - 1) * 2] if dim > 1 else np.array([3.0 * li + rng.normal()])
            kind = rng.integers(0, 3) if 0 < li < len(layers) - 1 else 0
            if kind == 0:
                sets[nm] = pt(*c)
            elif kind == 1:
                sets[nm] = box(c - rng.uniform(0.2, 1.5, dim), c + rng.uniform(0.2, 1.5, dim))
            else:
                sets[nm] = PSet(V=c + rng.normal(size=(3, dim)) * 1.2)
            row.append(nm)
        names.append(row)
    E = [(a, b) for li in range(len(layers) - 1) for a in names[li] for b in names[li + 1] if rng.random() < 0.8 or len(names[li + 1]) == 1]
    s, t = names[0][0], names[-1][0]
    g = G(sets, E, s, t, "sq")
    # drop instances without an s-t path through every layer structure
    if not simple_paths(g):
        continue
    ref = None
    vals = {}
    for c in COMBOS:
        v, _, st = relax(g, hull=True, sq_mode=c[0], solver=c[1])
        vals[c] = v
        if st != "optimal":
            stat_bad[c] += 1
    ref = vals[("cone", "CLARABEL")]
    for c in COMBOS:
        if np.isfinite(vals[c]) and np.isfinite(ref):
            maxdev[c] = max(maxdev[c], abs(vals[c] - ref) / max(1.0, abs(ref)))
    o = opt_exact(g)[0]
    viol += ref > o * (1 + 1e-6) + 1e-6
    gaps += o > ref * (1 + 1e-5) + 1e-6
print(f"  instances={n_inst}  non-'optimal' statuses: " + ", ".join(f"{m}/{s}={stat_bad[(m, s)]}" for m, s in COMBOS))
print(f"  max relative deviation from cone/CLARABEL: " + ", ".join(f"{m}/{s}={maxdev[(m, s)]:.1e}" for m, s in COMBOS))
print(f"  REL_H > OPT violations: {viol};  instances with OPT > REL_H: {gaps}")
