"""Item (2): free-sign 2x2 decompositions (Wei-Atamturk-Gomez-Kucukyavuz, arXiv 2201.00387, Prop. 2)
are below L_2 (Lemma 1.2(d)).

For Q = X'X + lam I pick a decomposition Q = R + sum_T Q_T over all pairs T, with Q_T = g [[d|Q_ab|, Q_ab],
[Q_ab, d|Q_ab|]] (d > 1, so Q_T is PD) and the largest g (times 0.98) keeping R PSD. Then compare
  V_W : min y'y - 2c'beta + beta'R beta + sum_T t_T, with (b_T, z_T, t_T) in Wei et al.'s Prop. 2 hull
        (after the scaling x1 = s b_a, x2 = -sign(Q_ab) s b_b, s = sqrt|Q_ab|, d_i = q_ii/|Q_ab|);
  V_H : the same decomposition with each pair envelope computed from my disjunctive H_T (own B^T per pair);
  L_2 : my disjunctive L_2 model (rc_node.L2);
  OPT : enumeration.
Expected: V_W = V_H (Prop. 2 is the exact free-sign envelope) and V_W <= L_2 <= OPT, at the root and at a
forced-in node. Also prints whether the free-sign optimum has a negative lifted cross moment, i.e. lies
outside every nonnegative (OptPairs-type) lifted hull, which forces B >= 0 entrywise.
usage: python3 rc_decomp.py > rc_decomp.log
"""
import itertools
from rc_common import np, ridge
import cvxpy as cp
from rc_node import L2, node_opt

TOL = dict(tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)


def decomposition(Q, d=1.5):
    p = Q.shape[0]
    pairs = list(itertools.combinations(range(p), 2))

    def parts(g):
        R = Q.copy(); QT = {}
        for a, b in pairs:
            q = Q[a, b]
            M = g * np.array([[d * abs(q), q], [q, d * abs(q)]])
            QT[(a, b)] = M
            R[np.ix_([a, b], [a, b])] -= M
        return R, QT

    lo, hi = 0.0, 1.0
    while np.linalg.eigvalsh(parts(hi)[0]).min() >= 0:
        hi *= 2
    for _ in range(60):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if np.linalg.eigvalsh(parts(mid)[0]).min() >= 0 else (lo, mid)
    return parts(0.98 * lo)


def wei_hull(bt, zt, t, q):
    """Wei et al. Prop. 2 for t >= b'q b (q PD, q12 != 0), via the scaling to d1 x1^2 - 2 x1 x2 + d2 x2^2."""
    q12 = q[0, 1]; s = np.sqrt(abs(q12))
    x1, x2 = s * bt[0], -np.sign(q12) * s * bt[1]
    d1, d2 = q[0, 0] / abs(q12), q[1, 1] / abs(q12)
    Dl = d1 * d2 - 1
    Y = cp.Variable((3, 3), PSD=True)   # [[W11, W12, x1], [W12, W22, x2], [x1, x2, t]]
    W = Y[:2, :2]
    return [Y[0, 2] == x1, Y[1, 2] == x2, Y[2, 2] == t,
            zt >= 0, zt <= 1, d1 * W[0, 0] == W[0, 1] + zt[0], d2 * W[1, 1] == zt[1] + W[0, 1],
            W[0, 1] >= 0, Dl * W[0, 1] >= -1 + zt[0] + zt[1], Dl * W[0, 1] <= zt[0], Dl * W[0, 1] <= zt[1]]


def h_env(bt, zt, q):
    """min <q, B_T> over my disjunctive H_T with first moments (zt, bt); returns (value expr, constraints)."""
    cons, lams, xs, Xs = [], [], [], []
    for s in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        W = cp.Variable((3, 3), PSD=True)
        for t, on in enumerate(s):
            if not on:
                cons += [W[t + 1, :] == 0]
        lams.append((s, W[0, 0])); xs.append(W[1:, 0]); Xs.append(W[1:, 1:])
    BT = sum(Xs)
    cons += [sum(l for _, l in lams) == 1, zt[0] == sum(l for s, l in lams if s[0]),
             zt[1] == sum(l for s, l in lams if s[1]), bt[0] == sum(x[0] for x in xs),
             bt[1] == sum(x[1] for x in xs)]
    return cp.trace(q @ BT), cons


def decomp_value(X, y, lam, k, R, QT, S1=(), mode="wei"):
    p = X.shape[1]
    c = X.T @ y
    z = cp.Variable(p); beta = cp.Variable(p)
    cons = [z >= 0, z <= 1, cp.sum(z) <= k] + [z[i] == 1 for i in S1]
    obj = y @ y - 2 * c @ beta
    Rs = (R + R.T) / 2
    L = np.linalg.cholesky(Rs + 1e-13 * np.eye(p))
    obj = obj + cp.sum_squares(L.T @ beta)
    for (a, b), q in QT.items():
        bt = cp.hstack([beta[a], beta[b]]); zt = cp.hstack([z[a], z[b]])
        if mode == "wei":
            t = cp.Variable()
            cons += wei_hull(bt, zt, t, q); obj = obj + t
        else:
            v, cc = h_env(bt, zt, q); cons += cc; obj = obj + v
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver="CLARABEL", **TOL)
    return prob.value


def main():
    worst_wh, worst_order = 0.0, -np.inf
    for seed in range(5):
        rng = np.random.default_rng(300 + seed)
        n, p, k = 5, 7, 2
        X = rng.standard_normal((n, p))
        beta = np.zeros(p); beta[:k] = np.array([1.0, -1.0]) * (0.4 if seed % 2 else 1.0)
        y = X @ beta + 0.5 * rng.standard_normal(n)
        lam = 1.0
        Q = X.T @ X + lam * np.eye(p)
        R, QT = decomposition(Q)
        j = int(rng.integers(k, p))
        for S1 in [(), (j,)]:
            vW = decomp_value(X, y, lam, k, R, QT, S1, "wei")
            vH = decomp_value(X, y, lam, k, R, QT, S1, "hull")
            vL = L2(X, y, lam, k, S1=S1)
            opt = node_opt(X, y, lam, k, S1=S1)
            worst_wh = max(worst_wh, abs(vW - vH) / opt)
            worst_order = max(worst_order, (vW - vL) / opt, (vL - opt) / opt)
            print(f"seed {seed} S1={S1}: V_W {vW:.9f}  V_H {vH:.9f}  L_2 {vL:.9f}  OPT {opt:.9f}  "
                  f"min eig R {np.linalg.eigvalsh(R).min():.2e}")
        # free-sign optimum: lifted cross moment of the optimal support
        best = min((ridge(X, y, lam, T)[0], T) for s in (1, 2) for T in itertools.combinations(range(p), s))
        bT = ridge(X, y, lam, best[1])[1]
        print(f"   OPT support {best[1]}, beta {np.round(bT, 4)}, negative cross moment: "
              f"{bool(len(bT) == 2 and bT[0] * bT[1] < 0)}")
    print(f"max |V_W - V_H|/OPT = {worst_wh:.1e};  max of (V_W - L_2)/OPT and (L_2 - OPT)/OPT = {worst_order:.1e}")


if __name__ == "__main__":
    main()
