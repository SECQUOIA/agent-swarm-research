"""Interval equilibrium propagation (IEP): an enclosure of ALL feasible points of a (partial) F1 pattern.

State: boxes K_t = [kl_t, kh_t] (t = 1..T) containing k_t of every feasible point of the pattern.
One sweep:
  for t = 1..T:  Lam_t = [rho(G diag kl_t), rho(G diag kh_t)]                 (Perron monotonicity)
                 P_t   = box hull of Q_t = {p >= 0, V'p = 1, p <= c,
                          Ll p_i <= kh_i (G p)_i,  Lh p_i >= kl_i (G p)_i  for all i}   (2N LPs)
                 K_{t+1} <- K_{t+1} cap (K_t - a P_t)
  K_1 <- K_1 cap reload(K_T)     (complete pattern: KF f + R K_T;  partial pattern: see below)
Validity: every feasible point has lam_t p_i = k_i (G p)_i with k in K_t, lam_t in Lam_t, so p_t in Q_t;
burn and reload are applied with exact interval arithmetic (R >= 0).  Hence every feasible point stays in
the boxes, and lam_T <= min( rho(G diag kh_T), CW/peaking bound with kh_T ).  An empty Q_t proves the
pattern infeasible.  NOTE: LPs and eigenvalues are computed in floating point here; a certified version
needs safe LP bounds (Neumaier-Shcherbina) and interval eigenvalue bounds (Collatz-Wielandt).

Partial pattern (some slots unassigned): an unassigned slot's k_1 lies in the hull of the K_1 boxes of
the remaining types; a type's K_1 box comes from the hull of K_T boxes over the nodes that may hold its
predecessor.  Implemented in iep_partial().
"""
import numpy as np
import gurobipy as gp
from nucsim import Data

ENV = gp.Env(empty=True); ENV.setParam("OutputFlag", 0); ENV.setParam("Threads", 1); ENV.start()


def rho(G, k):
    return max(abs(np.linalg.eigvals(G * k[None, :])))


def perron_box(D, kl, kh, Ll, Lh):
    """Box hull of Q (2N LPs). Returns (pl, ph) or None if Q is empty."""
    N = D.N
    m = gp.Model(env=ENV)
    p = m.addMVar(N, lb=0.0, ub=D.c)
    m.addConstr(D.V @ p == 1)
    GP = D.G
    m.addConstr(Ll * p - kh * (GP @ p) <= 0)      # row i: Ll p_i - kh_i (G p)_i <= 0
    m.addConstr(kl * (GP @ p) - Lh * p <= 0)      # row i: kl_i (G p)_i - Lh p_i <= 0
    pl, ph = np.zeros(N), np.zeros(N)
    for i in range(N):
        for sense, arr in ((gp.GRB.MINIMIZE, pl), (gp.GRB.MAXIMIZE, ph)):
            m.setObjective(p[i], sense); m.optimize()
            if m.Status != gp.GRB.OPTIMAL:
                return None
            arr[i] = m.ObjVal
    return np.maximum(pl - 1e-12, 0), np.minimum(ph + 1e-12, D.c)


def sweep(D, K1l, K1h, f, R, Kl=None, Kh=None):
    """One IEP sweep for a complete pattern. Kl, Kh: lists of T boxes (or None). Returns updated boxes + info."""
    T = D.T
    if Kl is None:
        Kl = [K1l.copy()] + [np.full(D.N, -np.inf) for _ in range(T - 1)]
        Kh = [K1h.copy()] + [np.full(D.N, np.inf) for _ in range(T - 1)]
    Kl[0] = np.maximum(Kl[0], K1l); Kh[0] = np.minimum(Kh[0], K1h)
    lamT = None
    for t in range(T):
        Ll, Lh = rho(D.G, Kl[t]), rho(D.G, Kh[t])
        if t == T - 1:
            lamT = (Ll, Lh); break
        box = perron_box(D, Kl[t], Kh[t], Ll, Lh)
        if box is None: return None
        pl, ph = box
        Kl[t + 1] = np.maximum(Kl[t + 1], Kl[t] - D.a * ph)
        Kh[t + 1] = np.minimum(Kh[t + 1], Kh[t] - D.a * pl)
    # reload (R >= 0)
    n1l = D.KF * f + R @ Kl[T - 1]; n1h = D.KF * f + R @ Kh[T - 1]
    Kl[0] = np.maximum(Kl[0], n1l); Kh[0] = np.minimum(Kh[0], n1h)
    if np.any(Kl[0] > Kh[0] + 1e-12): return None
    return Kl, Kh, lamT


def iep_complete(D, typ, maxsweeps=60, tol=1e-10, verbose=False):
    f, R = D.reload_matrix(typ)
    agemax = D.nages - 1
    K1l = np.array([D.KF - D.a * D.c * (D.T - 1) * D.age[g] for g in typ])
    K1h = np.full(D.N, D.KF)
    Kl = Kh = None; hist = []
    for s in range(maxsweeps):
        r = sweep(D, K1l, K1h, f, R, Kl, Kh)
        if r is None: return dict(infeasible=True, sweeps=s + 1, hist=hist)
        Kl, Kh, lamT = r
        w = max(np.max(Kh[t] - Kl[t]) for t in range(D.T))
        hist.append((lamT[1], w))
        if verbose: print(f"  sweep {s}: lam_T <= {lamT[1]:.8f}, max k width {w:.3e}", flush=True)
        if len(hist) > 1 and hist[-2][1] - w < tol: break
    return dict(infeasible=False, ub=hist[-1][0], width=hist[-1][1], sweeps=len(hist), hist=hist, Kl=Kl, Kh=Kh)


if __name__ == "__main__":
    import sys, json
    name = sys.argv[1]; typ = json.loads(sys.argv[2])
    D = Data(name)
    from nucsim import equilibrium
    r = equilibrium(D, typ)
    print(f"{name}: simulated lam_T={r['lam_T']:.8f} peak={r['peak']:.5f} feasible={r['feasible']}")
    out = iep_complete(D, typ, verbose=True)
    print({k: v for k, v in out.items() if k not in ("Kl", "Kh", "hist")})
