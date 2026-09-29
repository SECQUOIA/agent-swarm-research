"""(i) Lemma 2.1(b): merged propagation frames.  From a random box B0, run k1
rounds, restart from the forward box of the projected result B1 (as a new run
would), run k2 more rounds, giving Bf.  Split B0 \\ int Bf into the 2n frame
pieces S of the constrained note and check, for each S, that the fixed point
Z*(S, c) projects into Bf (so every y in S \\ Bf has pi_D(S, y) > c).
(ii) Lemma 4.1 / Corollary 4.2 on random polynomials in 2-3 variables in
monomial form (multivariate monomials, single use): pi_D(C) <= F_lo(C) +
max_j width_C(t_j), and no point of U' is removed at c = Phi_full(U').
Run: python3 merge_check.py > logs/merge_check.log
"""
import itertools
import numpy as np
import sympy as sp
import inst as I

rng = np.random.default_rng(23)


def frame_pieces(B0, Bf):
    n = len(B0); out = []
    for i in range(n):
        for side in (0, 1):
            S = []
            for j in range(n):
                if j < i:
                    S.append(Bf[j])
                elif j == i:
                    S.append((B0[i][0], Bf[i][0]) if side == 0 else (Bf[i][1], B0[i][1]))
                else:
                    S.append(B0[j])
            if S[i][1] - S[i][0] > 1e-12:
                out.append(S)
    return out


print('(i) merged frames (boxes around optimal points, cutoff c in [-1e-3, 0.3])')
OPT = {'linediag': lambda: [1.0 + (t := rng.uniform(-0.5, 1.0)), t], 'iso2': lambda: [1.0, 1.0],
       'rot0.1': lambda: [1.0, 0.0], 'nd2': lambda: [0.0, 0.0], 'h1': lambda: [1.0]}
for name, rep in (('linediag', 'exp'), ('iso2', 'exp'), ('rot0.1', 'exp'), ('nd2', 'mono'),
                  ('linediag', 's'), ('h1', 'exp')):
    d = I.make(name); dag = d['reps'][rep]; n = len(d['box'])
    stats = dict(runs=0, pieces=0, bad=0)
    for trial in range(60):
        c = rng.uniform(-1e-3, 0.3)
        y = OPT[name]()
        B0 = []
        for yi, (L, U) in zip(y, d['box']):
            B0.append((max(L, yi - 10 ** rng.uniform(-2, -0.3)), min(U, yi + 10 ** rng.uniform(-2, -0.3))))
        st, Z, _ = dag.propagate(B0, c, max_rounds=int(rng.integers(1, 4)))
        if st == 'empty':
            continue
        B1 = dag.xbox(Z)
        st, Z, _ = dag.propagate(B1, c, max_rounds=int(rng.integers(1, 4)))
        if st == 'empty':
            continue
        Bf = dag.xbox(Z)
        stats['runs'] += 1
        for S in frame_pieces(B0, Bf):
            stats['pieces'] += 1
            st, Zs, _ = dag.propagate(S, c, max_rounds=100000)
            if st == 'empty':
                continue
            xs = dag.xbox(Zs)
            ok = all(Bf[i][0] - 1e-9 <= xs[i][0] and xs[i][1] <= Bf[i][1] + 1e-9 for i in range(n))
            stats['bad'] += not ok
    print(f'  {name}/{rep}: {stats}')

print('(ii) Corollary 4.2 and Lemma 4.1 on random monomial sums')
worst42, viol42, viol41, tot = -np.inf, 0, 0, 0
for trial in range(60):
    n = int(rng.integers(2, 4)); syms = I.X[:n]
    f = 0
    for _ in range(int(rng.integers(3, 7))):
        e = rng.integers(0, 4, size=n)
        f += float(rng.normal()) * sp.prod([s ** int(k) for s, k in zip(syms, e)])
    if not sp.expand(f).free_symbols:
        continue
    dag = I.expanded(f, list(syms))
    poly = sp.Poly(sp.expand(f), *syms)
    tf = [sp.lambdify(syms, float(c) * sp.prod([s ** k for s, k in zip(syms, m)]))
          for m, c in poly.terms() if sum(m) > 0]
    box = [(lo, lo + rng.uniform(0.2, 1.5)) for lo in rng.uniform(-1.2, 0.8, size=n)]
    grid = np.array(list(itertools.product(*[np.linspace(a, b, 9) for a, b in box])))
    vals = np.array([[t(*p) for p in grid] for t in tf])
    width = (vals.max(1) - vals.min(1)).max()   # grid estimate (single-use monomials: extremes at vertices or interior)
    Flo = dag.forward_box(box)[-1][0]
    p = dag.pi(box, hi=Flo + width + 1.0, iters=35, max_rounds=5000)
    tot += 1
    worst42 = max(worst42, p - (Flo + width))
    viol42 += p > Flo + width + 1e-6 * (1 + abs(Flo))
    # Lemma 4.1 with a random sub-box U'
    U = []
    for a, b in box:
        u1, u2 = sorted(rng.uniform(a, b, size=2)); U.append((u1, u2))
    gU = np.array(list(itertools.product(*[np.linspace(a, b, 9) for a, b in U])))
    vU = np.array([[t(*q) for q in gU] for t in tf])
    phif = poly.terms()[-1][1] * 0 + float(poly.as_expr().subs({s: 0 for s in syms}))
    phif += vU.min(1).sum() + (vU.max(1) - vU.min(1)).max()
    # grid min underestimates nothing in the safe direction: grid mins >= true mins,
    # grid widths <= true widths; use exact Phi_full >= grid value - so add slack
    st, Z, _ = dag.propagate(box, phif + 1e-3 * (1 + abs(phif)), max_rounds=20000)
    if st == 'empty':
        viol41 += 1
    else:
        xb = dag.xbox(Z)
        viol41 += not all(xb[i][0] <= U[i][0] + 1e-12 and U[i][1] <= xb[i][1] + 1e-12 for i in range(n))
print(f'  {tot} instances; Cor 4.2 violations {viol42} (max pi_D - (F_lo + max width) = {worst42:.2e}); '
      f'Lemma 4.1 violations {viol41}')
