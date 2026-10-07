"""Independent check of Theorem 3 of covering-upper-half.md (rule R3) on
trees WITH BRANCHING and on a path, with my own instance family and code.

Family ("copy trees").  Every non-root node t has variables (s_t, y_t) and
table F_t(s_t, y_t) = kappa (s_t - y_t)^2 + u_t(y_t); the children of t all
have separator s_u = y_t (so a node with two children shares y_t with both).
The root has one variable y_r and table F_r(y_r); its children have
s_u = y_r.  Leaves have y_t private.  All separators are one-dimensional,
s in [-1, 1] on a grid of m = 2^K + 1 points; exact minima over the grid.

Unaries u(y) = A (|y| - v)_+^2 + concave kinks + amp sin(freq y).  Tilts of
opposite signs at the root and at leaves make the near-optimal set nearly
flat along copies.  Semiconcavity constants from Lemma 4.1 of [K]:
  U_e: 2 kappa;  L_e: M(parent table in y) + 2 kappa per sibling.
M_e = max of the two; G_e = 1.02 x the largest grid slope of U_e, L_e.

For rule R3 (tolerance eps/n per edge) we report: cells per edge, the gap
of the explicit graded split with cell-bracket minimizers (direct
evaluation), whether the rule was grid-limited, the Theorem 3 bound, and a
per-level check of the counting step: at each level j with eta_j > 0,
#(interior cells split at level j) <= (8n+2) N_inf({w <= eta_j},
2 sqrt((eps + eta_j)/M_e)), and #(near-boundary cells split) <= 8n with
r_j > rho_e.  Also the bracket-driven rule of Theorem 1 ("bd") and
Proposition B.4 edge by edge ("B4": split while M r^2 - min w > eps/n),
with the gaps of their explicit splits (graded split for bd; for B4 the
LP is not computed, only the graded-split gap, which upper-bounds gap(PA)).
"""
import sys
import numpy as np
from scipy.optimize import minimize_scalar


def valley(s, A, v):
    return A * np.maximum(np.abs(s) - v, 0.0) ** 2


class CopyTree:
    def __init__(self, parent, s, kappa, tables_u, root_table, curv_u, curv_root,
                 chunk=256):
        self.parent = parent
        self.N = len(parent)
        self.ch = [[u for u in range(self.N) if parent[u] == t]
                   for t in range(self.N)]
        self.s, self.k, self.u, self.Fr = s, kappa, tables_u, root_table
        self.curv_u, self.curv_root = curv_u, curv_root
        self.chunk = chunk
        self.n = self.N - 1
        self.E = [0] * self.N
        for t in self.postorder():
            self.E[t] = sum(self.E[u] + 1 for u in self.ch[t])

    def postorder(self):
        out = []

        def rec(t):
            for u in self.ch[t]:
                rec(u)
            out.append(t)
        rec(0)
        return out

    def minconv(self, g):
        """h(x) = min_y [kappa (x - y)^2 + g(y)]."""
        s, m = self.s, len(self.s)
        h = np.empty(m)
        for i0 in range(0, m, self.chunk):
            i1 = min(m, i0 + self.chunk)
            h[i0:i1] = (self.k * (s[i0:i1, None] - s[None, :]) ** 2
                        + g[None, :]).min(axis=1)
        return h

    def value_functions(self):
        U = [None] * self.N
        for t in self.postorder():
            if t == 0:
                continue
            g = self.u[t] + sum((U[c] for c in self.ch[t]), np.zeros_like(self.s))
            U[t] = self.minconv(g)
        fstar = np.min(self.Fr + sum(U[c] for c in self.ch[0]))
        V = [None] * self.N
        order = list(reversed(self.postorder()))   # parents before children
        for t in order:
            for c in self.ch[t]:
                sib = sum((U[c2] for c2 in self.ch[t] if c2 != c),
                          np.zeros_like(self.s))
                if t == 0:
                    V[c] = self.Fr + sib
                else:
                    V[c] = self.minconv(V[t]) + self.u[t] + sib
        return U, V, fstar

    def rho(self, phi):
        s, m = self.s, len(self.s)
        tot = np.min(self.Fr + sum(phi[c] for c in self.ch[0]))
        for t in range(1, self.N):
            g = self.u[t] + sum((phi[c] for c in self.ch[t]), np.zeros_like(s))
            best = np.inf
            for i0 in range(0, m, self.chunk):
                i1 = min(m, i0 + self.chunk)
                D = (self.k * (s[i0:i1, None] - s[None, :]) ** 2 + g[None, :]
                     - phi[t][i0:i1, None])
                best = min(best, D.min())
            tot += best
        return tot

    def M_edge(self, e):
        t = self.parent[e]
        nsib = len(self.ch[t]) - 1
        MA = 2 * self.k
        MB = (self.curv_root if t == 0 else 2 * self.k + self.curv_u[t]) \
            + 2 * self.k * nsib
        return max(MA, MB)


# ----------------------------------------------------------- cell brackets
def bracket(xs, up, lo):
    """g = inf_lam [max(lam x - up) + max(lo - lam x)] (convex in lam);
    returns (g, lam, beta) with the two maxima balanced by beta."""
    if len(xs) == 1:
        return lo[0] - up[0], 0.0, (up[0] + lo[0]) / 2

    def f(lam):
        return np.max(lam * xs - up) + np.max(lo - lam * xs)
    sl = np.max(np.abs(np.concatenate([np.diff(up), np.diff(lo)])
                       / np.diff(xs)[0])) + 1.0
    res = minimize_scalar(f, bounds=(-2 * sl, 2 * sl), method="bounded",
                          options=dict(xatol=1e-13, maxiter=1000))
    lam = res.x
    p = np.max(lam * xs - up)
    q = np.max(lo - lam * xs)
    return p + q, lam, (q - p) / 2


def cover(points, side):
    if len(points) == 0:
        return 0
    pts = np.sort(points)
    cnt, i = 0, 0
    while i < len(pts):
        cnt += 1
        i = np.searchsorted(pts, pts[i] + side * (1 + 1e-12), side="right")
    return cnt


def refine(m, test):
    """Dyadic refinement in index space; returns final cells (i0, i1, lev),
    split log [(i0, i1, lev)], grid_limited flag."""
    todo = [(0, m - 1, 0)]
    final, splits, lim = [], [], False
    while todo:
        i0, i1, lev = todo.pop()
        if test(i0, i1):
            if i1 - i0 == 1:
                lim = True
                final.append((i0, i1, lev))
            else:
                splits.append((i0, i1, lev))
                mid = (i0 + i1) // 2
                todo += [(i0, mid, lev + 1), (mid, i1, lev + 1)]
        else:
            final.append((i0, i1, lev))
    final.sort()
    return final, splits, lim


def split_from_cells(s, cells, up, lo):
    m = len(s)
    phi = np.empty(m)
    gmax = -np.inf
    for k, (i0, i1, lev) in enumerate(cells):
        g, lam, beta = bracket(s[i0:i1 + 1], up[i0:i1 + 1], lo[i0:i1 + 1])
        gmax = max(gmax, g)
        hi = i1 + 1 if k == len(cells) - 1 else i1   # half-open assignment
        phi[i0:hi] = lam * s[i0:hi] + beta
    return phi, gmax


def run_instance(name, T, eps):
    s = T.s
    m, n = len(s), T.n
    ds = s[1] - s[0]
    U, V, fstar = T.value_functions()
    out = {}
    print(f"-- {name}: n = {n} edges, parents {T.parent}, eps = {eps:g}, "
          f"m = {m}, f* = {fstar:.6f}")
    edges = list(range(1, T.N))
    data = {}
    for e in edges:
        L = fstar - V[e]
        w = U[e] - L
        th = (2 * T.E[e] + 1) / (2 * n)
        psi = U[e] - th * w
        M = T.M_edge(e)
        G = 1.02 * max(np.max(np.abs(np.diff(U[e]))),
                       np.max(np.abs(np.diff(L)))) / ds
        emp = max(np.max(np.diff(U[e], 2)), np.max(-np.diff(L, 2))) / ds ** 2
        data[e] = dict(U=U[e], L=L, w=w, psi=psi, M=M, G=G, emp=emp,
                       up=psi + w / (2 * n), lo=psi - w / (2 * n))
    print("   M_e " + str([round(data[e]["M"], 2) for e in edges])
          + ", grid max(U'', -L'') " + str([round(data[e]["emp"], 2) for e in edges])
          + ", G_e " + str([round(data[e]["G"], 2) for e in edges])
          + f", min w_e {[float('%.1e' % data[e]['w'].min()) for e in edges]}")
    for rule in ["R3", "bd", "B4"]:
        phis = [None] * T.N
        counts, lim_any, gm, ok_levels, bnds, Ns = [], False, -np.inf, True, [], []
        for e in edges:
            d = data[e]
            M, G, w = d["M"], d["G"], d["w"]

            if rule == "R3":
                def test(i0, i1, d=d):
                    r = (s[i1] - s[i0]) / 2
                    wmin = d["w"][i0:i1 + 1].min()
                    interior = (s[i0] + 1 >= 8 * n * r) and (1 - s[i1] >= 8 * n * r)
                    if interior:
                        B = (32 * n + 0.5) * d["M"] * r ** 2 - wmin / (2 * n)
                    else:
                        B = 2 * d["G"] * r + 2.5 * d["M"] * r ** 2 - wmin / n
                    return B > eps / n
            elif rule == "bd":
                def test(i0, i1, d=d):
                    g, _, _ = bracket(s[i0:i1 + 1], d["up"][i0:i1 + 1],
                                      d["lo"][i0:i1 + 1])
                    return g > eps / n
            else:
                def test(i0, i1, d=d):
                    r = (s[i1] - s[i0]) / 2
                    return d["M"] * r ** 2 - d["w"][i0:i1 + 1].min() > eps / n
            cells, splits, lim = refine(m, test)
            lim_any = lim_any or lim
            phi, gmax = split_from_cells(s, cells, d["up"], d["lo"])
            phis[e] = phi
            gm = max(gm, gmax)
            counts.append(len(cells))
            if rule == "R3":
                l = 2.0
                J = max(0, int(np.ceil(np.log2(l * np.sqrt((64 * n * n + n) * M
                                                           / (8 * eps))))))
                rho_e = min(eps / (4 * n * G), np.sqrt(eps / (5 * n * M)))
                Jp = max(0, int(np.ceil(np.log2(l / (2 * rho_e)))))
                etas = np.concatenate([[0.0], np.logspace(np.log10(eps / 1e3),
                                                          np.log10(max(w.max(), eps)), 300)])
                # per-level check of the counting step
                levels = {}
                for (i0, i1, lev) in splits:
                    r = (s[i1] - s[i0]) / 2
                    interior = (s[i0] + 1 >= 8 * n * r) and (1 - s[i1] >= 8 * n * r)
                    levels.setdefault(lev, [0, 0, r])
                    levels[lev][0 if interior else 1] += 1
                for lev, (ni, nb, r) in levels.items():
                    eta = (64 * n * n + n) * M * r ** 2 - 2 * eps
                    Nl = cover(s[w <= eta], 2 * np.sqrt((eps + eta) / M)) if eta > 0 else 0
                    if ni > (8 * n + 2) * Nl or nb > 8 * n or (nb > 0 and r <= rho_e) \
                            or (ni > 0 and eta <= 0):
                        ok_levels = False
                    etas = np.append(etas, max(eta, 0.0))
                N = max(cover(s[w <= eta], 2 * np.sqrt((eps + eta) / M)) for eta in etas)
                Ns.append(N)
                bnds.append(1 + (8 * n + 2) * J * N + 8 * n * Jp)
                if len(cells) > bnds[-1]:
                    ok_levels = False
        gap = fstar - T.rho(phis)
        line = (f"   {rule:3s}: cells/edge {counts} (total {sum(counts)}), "
                f"max cell bracket {gm:.2e} (eps/n {eps / n:.2e}), gap(explicit "
                f"split) {gap:.2e}{' [grid-limited]' if lim_any else ''}")
        if rule == "R3":
            line += (f"\n        N_e {Ns}; Theorem 3 bounds {bnds}; per-level "
                     f"counting step {'holds' if ok_levels else 'FAILS'}")
        print(line)
        out[rule] = dict(counts=counts, gap=gap, lim=lim_any, gm=gm,
                         ok=ok_levels, N=Ns)
        sys.stdout.flush()
    return out


def build(kind, m):
    s = np.linspace(-1, 1, m)
    kappa = 8.0
    A, v = 1.0, 0.25
    tilt_amp, tilt_f = 0.2, 2.5
    kink = lambda p, g: np.minimum(0.0, g * (p - s))       # concave kink
    ckink = lambda p, g: np.minimum(0.0, g * (s - p))      # concave kink
    if kind == "branch":
        # root -> 1; 1 -> {2, 3}; 2 -> 4.  Edges 1..4 (n = 4).
        parent = [-1, 0, 1, 1, 2]
        Fr = valley(s, A, v) + tilt_amp * np.sin(tilt_f * s) + kink(0.55, 0.6)
        u = [None,
             valley(s, A, v) + ckink(-0.6, 0.5),
             valley(s, A, v) + kink(0.7, 0.5),
             valley(s, A, v) - 0.5 * tilt_amp * np.sin(tilt_f * s) + ckink(-0.65, 0.4),
             valley(s, A, v) - 0.5 * tilt_amp * np.sin(tilt_f * s) + kink(0.6, 0.5)]
    elif kind == "star":
        # root -> {1, 2, 3}; 3 -> 4.  Edges 1..4.
        parent = [-1, 0, 0, 0, 3]
        Fr = valley(s, A, v) + tilt_amp * np.sin(tilt_f * s) + kink(0.55, 0.6)
        u = [None,
             valley(s, A, v) - (tilt_amp / 3) * np.sin(tilt_f * s) + ckink(-0.6, 0.5),
             valley(s, A, v) - (tilt_amp / 3) * np.sin(tilt_f * s) + kink(0.7, 0.5),
             valley(s, A, v) + ckink(-0.65, 0.4),
             valley(s, A, v) - (tilt_amp / 3) * np.sin(tilt_f * s) + kink(0.6, 0.5)]
    else:
        # path root -> 1 -> 2 -> 3 -> 4 -> 5 (n = 5), two flat valleys
        parent = [-1, 0, 1, 2, 3, 4]
        vv = lambda x: np.minimum(valley(x - 0.45, A, 0.12), valley(x + 0.45, A, 0.12))
        Fr = vv(s) + tilt_amp * np.sin(tilt_f * s)
        u = [None, vv(s) + kink(0.8, 0.5), vv(s) + ckink(-0.8, 0.5), vv(s),
             vv(s) + kink(0.75, 0.5), vv(s) - tilt_amp * np.sin(tilt_f * s)]
    curv = 2 * A + tilt_amp * tilt_f ** 2
    curv_u = [None] + [curv] * (len(parent) - 1)
    return CopyTree(parent, s, kappa, u, Fr, curv_u, curv)


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 8193
    allok = True
    for kind in ["branch", "star", "path"]:
        for eps in [1e-2, 1e-3]:
            T = build(kind, m)
            res = run_instance(kind, T, eps)
            r3 = res["R3"]
            allok = allok and r3["gap"] <= eps and r3["ok"] and not r3["lim"]
    print("R3 overall:", "gap <= eps, counting step and bound hold, never "
          "grid-limited" if allok else "SOME CHECK FAILED")


if __name__ == "__main__":
    main()
