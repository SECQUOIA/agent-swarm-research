"""Independent brute-force checks of Lemma 0, Theorem 1 and Theorem 1' of
covering-upper-half.md, written without the author's code.

Differences from the author's check_graded_split.py:
  - bags carry private variables (tables are over all bag variables, not
    over separators only);
  - separators of dimension 1 AND 2;
  - up to 3 children per bag;
  - every quantity (U_t, V_t, f*, W_t, the relaxation value) is computed by
    brute-force enumeration of the full variable grid, not by DP;
  - besides random perturbations, an adversarial hill-climb that tries to
    make gap(psi + r) exceed the Theorem 1 bound.

Floating point on finite grids (exact minima over the grid).
"""
import sys
import numpy as np

TOL = 1e-9


# ------------------------------------------------------------------ model
def random_decomposition(rng, n_bags, max_ch, max_sep, q, max_vars=9):
    """Random rooted tree decomposition. Returns (parent, V, S, nv).
    V[t] is a sorted list of variables; S[t] = V[t] & V[parent]."""
    for _ in range(200):
        parent = [-1]
        nch = [0]
        V = []
        nv = 0
        k0 = int(rng.integers(1, 3))
        V.append(list(range(nv, nv + k0)))
        nv += k0
        ok = True
        for t in range(1, n_bags):
            cand = [p for p in range(t) if nch[p] < max_ch]
            p = int(rng.choice(cand))
            nch[p] += 1
            nch.append(0)
            parent.append(p)
            ks = int(rng.integers(1, min(max_sep, len(V[p])) + 1))
            sep = sorted(rng.choice(V[p], size=ks, replace=False).tolist())
            npriv = int(rng.integers(0, 2)) if t < n_bags - 1 else 1
            if ks == len(V[p]) and npriv == 0:
                npriv = 1            # avoid a bag contained in its parent
            priv = list(range(nv, nv + npriv))
            nv += npriv
            V.append(sorted(sep + priv))
        if nv <= max_vars:
            S = [None] + [sorted(set(V[t]) & set(V[parent[t]]))
                          for t in range(1, n_bags)]
            return parent, V, S, nv
    raise RuntimeError("could not build a small decomposition")


def subtree(parent, t):
    out = [t]
    changed = True
    while changed:
        changed = False
        for u in range(len(parent)):
            if u not in out and parent[u] in out and u != 0:
                out.append(u)
                changed = True
    return out


def embed(arr, sub_vars, host_vars, q):
    """Reshape an array over sub_vars (sorted) for broadcasting over the
    sorted host_vars."""
    shape = [q if v in sub_vars else 1 for v in host_vars]
    return arr.reshape(shape)


def reduce_to(arr_full, keep_vars, nv):
    axes = tuple(i for i in range(nv) if i not in keep_vars)
    out = arr_full.min(axis=axes) if axes else arr_full
    return out


class Problem:
    def __init__(self, parent, V, S, nv, q, tables):
        self.parent, self.V, self.S, self.nv, self.q = parent, V, S, nv, q
        self.N = len(V)
        self.F = tables
        self.children = [[u for u in range(self.N) if parent[u] == t]
                         for t in range(self.N)]
        self.allv = list(range(nv))
        self.Ffull = sum(embed(tables[t], V[t], self.allv, q)
                         for t in range(self.N))
        self.Ffull = np.broadcast_to(self.Ffull, (q,) * nv).copy()
        self.fstar = self.Ffull.min()
        self.subs = [subtree(parent, t) for t in range(self.N)]
        self.U, self.Vf, self.w = [None] * self.N, [None] * self.N, [None] * self.N
        for t in range(1, self.N):
            inside = sum(embed(tables[u], V[u], self.allv, q)
                         for u in self.subs[t])
            outside = sum(embed(tables[u], V[u], self.allv, q)
                          for u in range(self.N) if u not in self.subs[t])
            inside = np.broadcast_to(inside, (q,) * nv)
            outside = np.broadcast_to(outside, (q,) * nv)
            self.U[t] = reduce_to(inside, S[t], nv)
            self.Vf[t] = reduce_to(outside, S[t], nv)
            self.w[t] = self.U[t] + self.Vf[t] - self.fstar
        m = self.Ffull - self.fstar
        self.W = [reduce_to(m, V[t], nv) for t in range(self.N)]
        # count of edges in sub(t)
        self.E = [len(self.subs[t]) - 1 for t in range(self.N)]
        self.n = self.N - 1

    def bag_fun(self, t, phi, tables=None):
        T = (self.F if tables is None else tables)[t].copy()
        for u in self.children[t]:
            T = T + embed(phi[u], self.S[u], self.V[t], self.q)
        if t != 0:
            T = T - embed(phi[t], self.S[t], self.V[t], self.q)
        return T

    def rho(self, phi, tables=None):
        return sum(self.bag_fun(t, phi, tables).min() for t in range(self.N))

    def gap(self, phi, tables=None):
        return self.fstar - self.rho(phi, tables)

    def graded(self, D=None, kind="thm1"):
        n = self.n
        psi = [None] * self.N
        for t in range(1, self.N):
            if kind == "thm1":
                th = (2 * self.E[t] + 1) / (2 * n)
            elif kind == "thm1p":
                th = (3 * self.E[t] + 2) / (3 * n + 1)
            elif kind == "rev":
                th = 1 - (2 * self.E[t] + 1) / (2 * n)
            elif kind == "L":
                th = 1.0
            psi[t] = self.U[t] - th * self.w[t]
        return psi

    def bracket(self, r, D):
        return sum(np.max(r[t] - D * self.w[t]) + np.max(-r[t] - D * self.w[t])
                   for t in range(1, self.N))

    def lemma0_rhs(self, phi, err=None):
        """max_x [sum_t err_t + sum_{t != r} delta_t(x_{S_t}) - m(x)] with
        delta from reduced value functions of the (relaxed) tables."""
        tables = self.F if err is None else [self.F[t] - err[t]
                                             for t in range(self.N)]
        # reduced value functions U^phi_t(s) = min_{z in X_Vt, z_St = s}
        #   [F~_t(z) + sum_u phi_u(z_Su)]  (bottom-up is not needed: phi given)
        tot = np.zeros((self.q,) * self.nv)
        for t in range(1, self.N):
            T = tables[t].copy()
            for u in self.children[t]:
                T = T + embed(phi[u], self.S[u], self.V[t], self.q)
            axes = tuple(i for i, v in enumerate(self.V[t])
                         if v not in self.S[t])
            Ured = T.min(axis=axes) if axes else T
            d = Ured - phi[t]
            delta = d - d.min()
            tot = tot + embed(delta, self.S[t], self.allv, self.q)
        if err is not None:
            for t in range(self.N):
                tot = tot + embed(err[t], self.V[t], self.allv, self.q)
        return np.max(tot - (self.Ffull - self.fstar))


def random_problem(rng, max_ch, max_sep, kind):
    n_bags = int(rng.integers(2, 6))
    q = int(rng.integers(3, 5))
    parent, V, S, nv = random_decomposition(rng, n_bags, max_ch, max_sep, q)
    tables = []
    for t in range(len(V)):
        shape = (q,) * len(V[t])
        if kind == "uniform":
            tables.append(rng.uniform(0, 1, size=shape))
        else:
            g = np.meshgrid(*[np.linspace(-1, 1, q)] * len(V[t]),
                            indexing="ij")
            T = sum(rng.normal() * x + rng.normal() * x ** 2 for x in g)
            T = T + 0.2 * rng.uniform(size=shape)
            tables.append(T)
    return Problem(parent, V, S, nv, q, tables)


# ----------------------------------------------------------------- checks
def main():
    rng = np.random.default_rng(314159)
    st = dict(inst=0, sep2=0, branch3=0, priv=0, exact_err=0.0, viol=0,
              checks=0, ratios=[], l0_err=0.0, l0r_err=0.0, t1p_viol=0,
              t1p_checks=0, adv_best=-np.inf, adv_runs=0,
              rev_non=0, rev_tot=0, L_non=0, L_tot=0, t1p_exact=0.0,
              adv_big_fail=0, adv_big_runs=0)
    for trial in range(600):
        max_ch = [1, 2, 3][trial % 3]
        max_sep = 1 if trial % 2 == 0 else 2
        kind = "uniform" if trial % 4 < 2 else "smooth"
        P = random_problem(rng, max_ch, max_sep, kind)
        st["inst"] += 1
        st["sep2"] += any(len(P.S[t]) == 2 for t in range(1, P.N))
        st["branch3"] += any(len(c) >= 3 for c in P.children)
        st["priv"] += any(len(P.V[t]) > len(P.S[t]) + sum(len(P.S[u]) for u in P.children[t]) for t in range(1, P.N))
        n = P.n
        D = 1.0 / (2 * n)
        psi = P.graded()
        st["exact_err"] = max(st["exact_err"], abs(P.gap(psi)))
        # random perturbations
        for scale in [0.02, 0.2, 1.0]:
            for rep in range(4):
                if rep == 0:
                    r = [None] + [scale * rng.normal(size=P.w[t].shape)
                                  for t in range(1, P.N)]
                elif rep == 1:
                    r = [None] + [scale * rng.uniform(-1, 1) * P.w[t]
                                  for t in range(1, P.N)]
                elif rep == 2:   # r_t = +- D w_t (+ small noise): edge of sliver
                    r = [None] + [rng.choice([-1, 1]) * D * P.w[t]
                                  + scale * 0.1 * rng.normal(size=P.w[t].shape)
                                  for t in range(1, P.N)]
                else:            # spikes at single separator values
                    r = [None]
                    for t in range(1, P.N):
                        z = np.zeros(P.w[t].shape)
                        z.flat[rng.integers(z.size)] = scale * rng.normal()
                        r.append(z)
                phi = [None] + [psi[t] + r[t] for t in range(1, P.N)]
                g = P.gap(phi)
                b = P.bracket(r, D)
                st["checks"] += 1
                if g > b + TOL:
                    st["viol"] += 1
                if b > 1e-6:
                    st["ratios"].append(g / b)
        # adversarial hill climb on gap - bound (every 3rd instance)
        if trial % 3 == 0:
            for Dfac, key in [(1.0, "adv"), (1.5, "adv_big")]:
                Dc = Dfac * D
                r = [None] + [0.05 * rng.normal(size=P.w[t].shape)
                              for t in range(1, P.N)]

                def obj(rr):
                    ph = [None] + [psi[t] + rr[t] for t in range(1, P.N)]
                    return P.gap(ph) - P.bracket(rr, Dc)
                cur = obj(r)
                step = 0.2
                for it in range(400):
                    t = int(rng.integers(1, P.N))
                    k = int(rng.integers(r[t].size))
                    old = r[t].flat[k]
                    r[t].flat[k] = old + step * rng.normal()
                    val = obj(r)
                    if val >= cur:
                        cur = val
                    else:
                        r[t].flat[k] = old
                    if it % 100 == 99:
                        step /= 2
                if key == "adv":
                    st["adv_runs"] += 1
                    st["adv_best"] = max(st["adv_best"], cur)
                else:
                    st["adv_big_runs"] += 1
                    if cur > 1e-7:
                        st["adv_big_fail"] += 1
        # Lemma 0 (exact and relaxed) with random phi
        phi = [None] + [rng.normal(size=P.w[t].shape) for t in range(1, P.N)]
        st["l0_err"] = max(st["l0_err"], abs(P.gap(phi) - P.lemma0_rhs(phi)))
        err = [rng.uniform(0, 0.5, size=P.F[t].shape) for t in range(P.N)]
        relaxed = [P.F[t] - err[t] for t in range(P.N)]
        st["l0r_err"] = max(st["l0r_err"],
                            abs(P.gap(phi, relaxed) - P.lemma0_rhs(phi, err)))
        # Theorem 1'
        Dp = 1.0 / (3 * n + 1)
        psip = P.graded(kind="thm1p")
        st["t1p_exact"] = max(st["t1p_exact"], abs(P.gap(psip)))
        for scale in [0.0, 0.1, 0.5]:
            err = [rng.uniform(0, 0.5, size=P.F[t].shape) * (rng.uniform() < 0.7)
                   for t in range(P.N)]
            relaxed = [P.F[t] - err[t] for t in range(P.N)]
            r = [None] + [scale * rng.normal(size=P.w[t].shape)
                          for t in range(1, P.N)]
            ph = [None] + [psip[t] + r[t] for t in range(1, P.N)]
            g = P.gap(ph, relaxed)
            b = P.bracket(r, Dp) + sum(np.max(err[t] - Dp * P.W[t])
                                       for t in range(P.N))
            st["t1p_checks"] += 1
            if g > b + TOL:
                st["t1p_viol"] += 1
        # reversed grading on paths, phi = L on branching trees
        if max_ch == 1 and n >= 2:
            st["rev_tot"] += 1
            if P.gap(P.graded(kind="rev")) > 1e-9:
                st["rev_non"] += 1
        if max(len(c) for c in P.children) >= 2:
            st["L_tot"] += 1
            if P.gap(P.graded(kind="L")) > 1e-9:
                st["L_non"] += 1
    rat = np.array(st["ratios"])
    print("Independent brute-force checks (private variables, 1D/2D "
          "separators, up to 3 children)")
    print(f"instances {st['inst']}: with a 2D separator {st['sep2']}, with a "
          f"bag of >= 3 children {st['branch3']}")
    print(f"Theorem 1(a): max |gap(graded psi)| = {st['exact_err']:.2e}")
    print(f"Theorem 1(b): {st['viol']} violations in {st['checks']} random "
          f"perturbations; gap/bound (bound > 1e-6, {len(rat)} cases): "
          f"max {rat.max():.4f}, median {np.median(rat):.4f}")
    print(f"Theorem 1(b) adversarial hill-climb on gap - bound: best value "
          f"{st['adv_best']:.3e} over {st['adv_runs']} runs (<= 0 expected)")
    print(f"   same with discount 1.5/(2n): gap > bound in "
          f"{st['adv_big_fail']} of {st['adv_big_runs']} runs")
    print(f"Lemma 0 exact bags: max |gap - max_x[sum delta - m]| = "
          f"{st['l0_err']:.2e}")
    print(f"Lemma 0 relaxed bags: max |gap~ - max_x[sum err + sum delta~ - m]|"
          f" = {st['l0r_err']:.2e}")
    print(f"Theorem 1': psi' exact (err = 0): max |gap| = {st['t1p_exact']:.2e};"
          f" {st['t1p_viol']} violations in {st['t1p_checks']} checks")
    print(f"reversed grading on paths: non-exact in {st['rev_non']} of "
          f"{st['rev_tot']}")
    print(f"phi = L on trees with branching: non-exact in {st['L_non']} of "
          f"{st['L_tot']}")
    bad = st["viol"] + st["t1p_viol"] + (st["adv_best"] > 1e-7)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
