"""Machine-checked structural facts and a certified Collatz-Wielandt bound for the nuclear* instances.

Proves (per instance, by checking the rows of the OSiL file):
  (E) lam_T * phi_{i,T} = sum_j G_ij k_{j,T} phi_{j,T} for all nodes i, with G >= 0 (exact decimals);
  (N) sum_i V_i phi_{i,T} k_{i,T} = 1, so phi_T != 0 and lam_T is an eigenvalue of G diag(k_T);
  (B) k_{i,t+1} = k_{i,t} - a phi_{i,t} k_{i,t}, a > 0, and phi, k >= 0 by bounds, so k_{i,T} <= k_{i,1};
  (K) k_{i,1} <= KF (fresh reactivity, 1.2) at every feasible point (family-specific argument, see report);
then  lam_T <= rho(G diag(k_T)) <= KF * max_i (G w)_i / w_i  for any rational w > 0 (exact arithmetic).

The JSON keeps the certified values as exact fractions (`*_exact`); the float fields are nearest-rounded
approximations. The printed bounds are rounded outward from the exact values. `--reuse` re-evaluates the
certificates w and y saved in ../nuclear_cw_bounds.json exactly instead of searching for new ones.
"""
import sys, json, math
from fractions import Fraction as F
import numpy as np
from nuc_struct import structure, NAMES, LISTED

def fr(s): return F(s)

def dec(q, d, up):
    """rational q as a d-decimal string, rounded up (ceiling) if up else down (floor)."""
    n = math.ceil(q * 10 ** d) if up else math.floor(q * 10 ** d)
    return f"{'-' if n < 0 else ''}{abs(n) // 10 ** d}.{abs(n) % 10 ** d:0{d}d}"

def knap_max(a, V, c):
    """exact max a^T p s.t. V^T p = 1, 0 <= p <= c (V > 0): greedy by a_j / V_j. Returns (value, p)."""
    N = len(a); p = [F(0)] * N; rest = F(1)
    for j in sorted(range(N), key=lambda j: a[j] / V[j], reverse=True):
        if rest <= 0: break
        take = min(c[j], rest / V[j]); p[j] = take; rest -= take * V[j]
    assert rest == 0, "P empty"
    return sum(a[j] * p[j] for j in range(N)), p


def dinkelbach(Gx, y, V, c):
    """exact max_{p in P} (y^T G p)/(y^T p) with P = {V^T p = 1, 0 <= p <= c}, y > 0."""
    N = len(y); a = [sum(y[i] * Gx[i][j] for i in range(N)) for j in range(N)]
    _, p = knap_max(a, V, c)
    beta = sum(a[j] * p[j] for j in range(N)) / sum(y[j] * p[j] for j in range(N))
    while True:
        val, p = knap_max([a[j] - beta * y[j] for j in range(N)], V, c)
        if val <= 0: return beta
        beta = sum(a[j] * p[j] for j in range(N)) / sum(y[j] * p[j] for j in range(N))


def peak_y(G, V, c, iters=40):
    """numerically find y > 0 minimizing max_{p in P} y^T G p / y^T p (bisection on beta, LP feasibility
    via the LP dual of the knapsack); the returned y is only a candidate, its value is certified exactly."""
    import gurobipy as gp
    N = len(V); lo, hi = 0.0, float(max(abs(np.linalg.eigvals(G)))) + 1e-6
    best = None
    for _ in range(iters):
        beta = (lo + hi) / 2
        m = gp.Model(); m.Params.OutputFlag = 0
        y = m.addMVar(N, lb=1e-6); mu = m.addVar(lb=-gp.GRB.INFINITY); nu = m.addMVar(N, lb=0)
        m.addConstr(y.sum() == 1)
        m.addConstr(mu + sum(c[j] * nu[j] for j in range(N)) <= 0)
        m.addConstrs(V[j] * mu + nu[j] >= sum(G[i, j] * y[i] for i in range(N) if G[i, j]) - beta * y[j] for j in range(N))
        m.optimize()
        if m.Status == 2: hi = beta; best = y.X.copy()
        else: lo = beta
    if best is None:
        ev, W = np.linalg.eig(G.T); best = np.abs(np.real(W[:, np.argmax(np.real(ev))])) + 1e-9
    return [F(float(v)).limit_denominator(10 ** 9) for v in best]


def analyse(name, cert=None):
    """cert: saved record with rational certificates "w" and "y" to re-evaluate (skips the numerical search)."""
    M, lamT, phiT, kT, G = structure(name)
    N = len(phiT)
    isbin = lambda j: M.vtype[j] == "B"
    rep = {"name": name, "nodes": N}
    # ---- (E) exact G as fractions
    rows = {}
    for r, terms in M.quad.items():
        if r >= 0 and any(lamT in (i, j) for i, j, c in terms): rows[r] = terms
    node = {p: n for n, p in enumerate(phiT)}
    Gx = [[F(0)] * N for _ in range(N)]
    for r, terms in rows.items():
        i = [node[a if b == lamT else b] for a, b, c in terms if lamT in (a, b)][0]
        for a, b, c in terms:
            if lamT in (a, b): continue
            f = a if a in node else b
            Gx[i][node[f]] += fr(c)
    assert all(g >= 0 for row in Gx for g in row); rep["G_nonneg"] = True
    # ---- (B) burnup rows: lin {a:-1, b:+1}, quad {(phi, a, alpha)}
    nxt, alpha, burnphi = {}, set(), {}
    for r in range(M.m):
        L = M.lin[r]; Q = M.quad.get(r, [])
        if len(L) == 2 and len(Q) == 1 and sorted(float(v) for v in L.values()) == [-1, 1] and M.clb[r] == M.cub[r] == "0":
            a = [j for j, v in L.items() if float(v) == -1][0]; b = [j for j, v in L.items() if float(v) == 1][0]
            i, j, c = Q[0]
            if a in (i, j):
                nxt[a] = b; alpha.add(c); burnphi[a] = j if i == a else i
    assert all(float(c) > 0 for c in alpha); rep["alpha"] = sorted(alpha)
    prev = {b: a for a, b in nxt.items()}
    k1, chains = [], []
    for i in range(N):
        ch = [kT[i]]
        while ch[-1] in prev: ch.append(prev[ch[-1]])
        chains.append(ch[::-1]); k1.append(ch[-1])
    T = {len(c) for c in chains}; assert len(T) == 1; rep["T"] = T.pop()
    allk = [v for c in chains for v in c]; allphi = [burnphi[v] for c in chains for v in c[:-1]] + list(phiT)
    assert all(fr(M.vlb[v]) >= 0 for v in allk + allphi); rep["phi_k_lb_nonneg"] = True
    rep["phi_lb_min"] = float(min(fr(M.vlb[v]) for v in allphi)); rep["k_lb_min"] = float(min(fr(M.vlb[v]) for v in allk))
    # ---- (N) normalization at T
    pairs = {frozenset((phiT[i], kT[i])) for i in range(N)}
    normT = [r for r in range(M.m) if M.clb[r] == M.cub[r] == "1" and not M.lin[r] and M.quad.get(r)
             and {frozenset((i, j)) for i, j, c in M.quad[r]} == pairs]
    assert len(normT) == 1 and all(fr(c) > 0 for i, j, c in M.quad[normT[0]]); rep["normalization_T"] = M.cnames[normT[0]]
    # ---- (K) BOC rows: the row where k_{i,1} appears with coefficient +1 and there are fresh terms -KF*b
    copy = {}  # continuous copies x = b
    for r in range(M.m):
        L = M.lin[r]
        if len(L) == 2 and not M.quad.get(r) and M.clb[r] == M.cub[r] == "0":
            (a, ca), (b, cb) = L.items()
            if {float(ca), float(cb)} == {1, -1}:
                if isbin(a) and not isbin(b): copy[b] = a
                if isbin(b) and not isbin(a): copy[a] = b
    asbin = lambda j: j if isbin(j) else copy.get(j)
    eqrows = {}  # frozenset(binaries) -> coefficient dict, for rows sum coef*b = 1 (or <= 1) with binaries only
    for r in range(M.m):
        L = M.lin[r]
        if L and not M.quad.get(r) and all(isbin(j) for j in L) and M.cub[r] == "1":
            eqrows.setdefault(frozenset(L), []).append((r, {j: fr(c) for j, c in L.items()}, M.clb[r]))
    KF, fam, detail = set(), set(), []
    bocrow = {}
    for i in range(N):
        cand = [r for r in range(M.m) if fr(M.lin[r].get(k1[i], "0")) == 1 and not (k1[i] in nxt and r in [])]
        cand = [r for r in cand if any(isbin(j) and fr(c) < 0 for j, c in M.lin[r].items())]
        assert len(cand) == 1, (i, cand); r = cand[0]; bocrow[i] = r
        assert M.clb[r] == M.cub[r] == "0"
        L, Q = M.lin[r], M.quad.get(r, [])
        fresh = [j for j, c in L.items() if isbin(j)]
        KF |= {fr(L[j]) for j in fresh}
        zs = [j for j, c in L.items() if j != k1[i] and not isbin(j)]
        if not Q and zs:  # F3: z <= KF * b rows
            fam.add("F3"); bins = list(fresh)
            for z in zs:
                assert fr(L[z]) == -1 and fr(M.vlb[z]) >= 0
                zr = [rr for rr in range(M.m) if z in M.lin[rr] and len(M.lin[rr]) == 2 and not M.quad.get(rr)
                      and M.clb[rr] == "-INF" and M.cub[rr] == "0" and fr(M.lin[rr][z]) == 1
                      and any(isbin(j) for j in M.lin[rr])]
                ok = False
                for rr in zr:
                    b = [j for j in M.lin[rr] if isbin(j)][0]
                    if 0 <= -fr(M.lin[rr][b]) <= -fr(L[fresh[0]]):  # z <= c*b with c <= KF
                        bins.append(b); ok = True; break
                assert ok, ("no z<=KF*b row", z)
        elif Q and not zs and all((isbin(a) and b in kT) or (isbin(b) and a in kT) for a, b, c in Q):  # F2: k_{j,T} * b
            fam.add("F2"); bins = list(fresh)
            for a, b, c in Q:
                assert fr(c) == -1
                bb, kk = (a, b) if isbin(a) else (b, a)
                assert kk in kT, "reload term is not an EOC k"
                bins.append(bb)
        elif Q and not zs:  # F1: (y, kappa) with y binary or copy of binary
            fam.add("F1"); bins = list(fresh)
            for a, b, c in Q:
                assert fr(c) == -1
                y, kap = (a, b) if asbin(a) is not None else (b, a)
                assert asbin(kap) is None
                bins.append(asbin(y))
        else:
            raise ValueError(("unknown BOC row", name, i))
        key = frozenset(bins)
        assert key in eqrows and any(cl == "1" and all(v == 1 for v in d.values()) for _, d, cl in eqrows[key]), \
            ("node row sum b = 1 missing", i)
    assert len(fam) == 1 and len(KF) == 1; fam = fam.pop(); KF = (-KF.pop())
    rep["family"] = fam; rep["KF"] = float(KF)
    if fam == "F2":
        assert rep["phi_lb_min"] > 0 and rep["k_lb_min"] > 0  # strictly positive burn: no closed reload cycles
    if fam == "F1":
        # kappa rows: kappa - sum_j V_j * kT_j * y_j = 0; y's form a fuel row with the same coefficients V
        kap_of_bin = {}
        for i in range(N):
            for a, b, c in M.quad.get(bocrow[i], []):
                y, kap = (a, b) if asbin(a) is not None else (b, a)
                kap_of_bin[asbin(y)] = kap
        freshbins = {j for i in range(N) for j, c in M.lin[bocrow[i]].items() if isbin(j)}
        fuelrows = {}
        for key, lst in eqrows.items():
            for r, d, cl in lst:
                if cl == "1": fuelrows[key] = d
        pred = {}
        kaps = set(kap_of_bin.values())
        for kap in kaps:
            rr = [r for r in range(M.m) if fr(M.lin[r].get(kap, "0")) == 1 and len(M.lin[r]) == 1 and M.quad.get(r)]
            assert len(rr) == 1; r = rr[0]; assert M.clb[r] == M.cub[r] == "0"
            coef = {}
            for a, b, c in M.quad[r]:
                y, kk = (a, b) if asbin(a) is not None else (b, a)
                assert kk in kT
                coef[asbin(y)] = -fr(c)
            key = frozenset(coef)
            assert key in fuelrows and fuelrows[key] == coef and all(v > 0 for v in coef.values()), "kappa row is not a fuel-row average"
            srcs = {kap_of_bin.get(b, "FRESH" if b in freshbins else None) for b in key}
            assert len(srcs) == 1 and None not in srcs, ("fuel column mixes sources", srcs)
            pred[kap] = srcs.pop()
        # acyclic, every chain reaches FRESH
        depth = {}
        def d(k, seen=()):
            if k == "FRESH": return 0
            assert k not in seen, "cycle in fuel age chain"
            return 1 + d(pred[k], seen + (k,))
        rep["max_age"] = max(d(k) for k in kaps)
    # ---- certified Collatz-Wielandt bound
    Gf = np.array([[float(g) for g in row] for row in Gx])
    if cert:
        w = [F(x) for x in cert["w"]]
    else:
        ev, V = np.linalg.eig(Gf + 1e-9); v = np.abs(np.real(V[:, np.argmax(np.real(ev))]))
        v = v / v.max()
        w = [F(float(max(x, 1e-12))).limit_denominator(10 ** 12) for x in v]
    assert len(w) == N and all(x > 0 for x in w)
    ratios = [sum(Gx[i][j] * w[j] for j in range(N)) / w[i] for i in range(N)]
    rho_bar = max(ratios)
    rep["rho_numpy"] = float(max(abs(np.linalg.eigvals(Gf))))
    rep["rho_bar_certified"] = float(rho_bar)
    rep["bound_lamT"] = float(KF * rho_bar)
    rep["rowsum_bound"] = float(KF * max(sum(r) for r in Gx))
    rep["rho_bar_exact"] = str(rho_bar); rep["bound_lamT_exact"] = str(KF * rho_bar)
    rep["rowsum_bound_exact"] = str(KF * max(sum(r) for r in Gx))
    rep["w"] = [str(x) for x in w]
    # ---- (P) peaking rows at T: phi_{i,T} k_{i,T} <= c ; lam_T >= 0 ; normalization weights V
    assert fr(M.vlb[lamT]) >= 0
    Vn = [None] * N
    for a, b, c in M.quad[normT[0]]:
        Vn[node[a] if a in node else node[b]] = fr(c)
    cpk = [None] * N
    for r in range(M.m):
        Q = M.quad.get(r, [])
        if len(Q) == 1 and not M.lin[r] and M.clb[r] == "-INF" and frozenset(Q[0][:2]) in pairs and fr(Q[0][2]) == 1:
            a, b, _ = Q[0]; i = node[a] if a in node else node[b]
            cpk[i] = fr(M.cub[r]) if cpk[i] is None else min(cpk[i], fr(M.cub[r]))
    assert all(x is not None for x in cpk)
    y = [F(v) for v in cert["y"]] if cert else peak_y(Gf, [float(v) for v in Vn], [float(x) for x in cpk])
    assert len(y) == N and all(v >= 0 for v in y)
    beta = dinkelbach(Gx, y, Vn, cpk)
    rep["peak_c"] = float(max(cpk)); rep["beta_certified"] = float(beta)
    rep["bound_peak"] = float(KF * beta)
    rep["y"] = [str(v) for v in y]
    rep["beta_exact"] = str(beta); rep["bound_peak_exact"] = str(KF * beta)
    best = min(KF * beta, KF * rho_bar)
    rep["best_bound"] = float(best); rep["best_bound_exact"] = str(best)
    p, dual = LISTED[name]
    rep["listed_primal"], rep["listed_dual"] = p, dual
    return rep

if __name__ == "__main__":
    args = sys.argv[1:]
    certs = None
    if "--reuse" in args:
        args.remove("--reuse")
        certs = {r["name"]: r for r in json.load(open("../nuclear_cw_bounds.json"))}
    names = args or NAMES
    out = []
    # printed bounds are rounded outward: upper bounds on lam_T (rho_bar, beta) up, objective bounds down
    up6 = lambda k: dec(F(r[k]), 6, True)
    obj = lambda k, d=6: dec(-F(r[k]), d, False)
    for nm in names:
        r = analyse(nm, certs[nm] if certs else None); out.append(r)
        print(f"{nm:11s} fam={r['family']} N={r['nodes']:3d} T={r['T']:2d} KF={r['KF']} phi_lb={r['phi_lb_min']:.3g} "
              f"k_lb={r['k_lb_min']:.3g} rho={r['rho_numpy']:.6f} rho_bar<= {up6('rho_bar_exact')} "
              f"bound(obj)>= {obj('bound_lamT_exact')} rowsum-bound {obj('rowsum_bound_exact', 4)} listed p/d {r['listed_primal']} / {r['listed_dual']}"
              + (f" max_age={r['max_age']}" if 'max_age' in r else "")
              + f"\n            peak c={r['peak_c']:.4g} beta<= {up6('beta_exact')} peak-bound(obj)>= {obj('bound_peak_exact')}  BEST >= {obj('best_bound_exact')}")
    json.dump(out, open("../nuclear_cw_bounds.json", "w"), indent=1)
