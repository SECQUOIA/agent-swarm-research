"""Independent re-decision of C1 at S* for some cells of Table 6.1 (and the PWE root certificate).
Instances follow the data specification of the note (Section 6 setup and the seeds 1000.. of exp_c1.py):
X iid N(0,1) (n x p), S* uniform, beta*_i = +-b, y = X beta* + sigma w, lam = tau0 sigma sqrt(2 n log p)/b,
drawn with numpy default_rng(seed) in that order.  The decision logic below is my own:
  lower bounds: L(a) of Lemma 1.1 at a = r_S, at saturated witnesses, and at the node's own optimal residual;
  upper bounds: node relaxation value from an independent cvxpy/Clarabel SOC model.
usage: python3 verify_table61.py p alpha [seeds]"""
import sys, json
from common import dual_L, node_primal_cvx, saturated_witness, ridge_on
import numpy as np


def author_instance(n, p, k, b=1.0, sigma=0.5, seed=0, tau0=1.5):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    lam = tau0 * sigma * np.sqrt(2 * n * np.log(p)) / b
    return X, y, float(lam), S


def decide(n, p, k, seed):
    X, y, lam, S = author_instance(n, p, k, seed=seed)
    fS, bS, r = ridge_on(X, y, lam, S)
    a = X.T @ r; nulls = np.setdiff1d(np.arange(p), S); m0 = np.min(np.abs(a[S]))
    pwe = bool(np.max(np.abs(a[nulls])) <= m0)
    duals = [r]
    wit = False
    for th in np.linspace(0.5, 1.0, 26):
        al, Gam, V, _ = saturated_witness(X, y, lam, S, th * m0)
        if len(V) > n - k - 1:
            continue
        c = X.T @ al
        m = np.min(np.abs(c[S])); M = np.max(np.abs(c[nulls]))
        if M <= m and (m * m - M * M) / lam > Gam:
            wit = True
        duals.append(al)
    nodes = [((int(i),), ()) for i in S] + [((), (int(j),)) for j in nulls]
    lb = {nd: max(dual_L(X, y, lam, k, al, *nd) for al in duals) for nd in nodes}
    todo = sorted([nd for nd in nodes if lb[nd] < fS * (1 + 1e-9)], key=lambda nd: lb[nd])
    c1 = True; nsolve = 0; undecided = 0; fail = None
    for nd in todo:
        v, z, bb, res = node_primal_cvx(X, y, lam, k, *nd)
        nsolve += 1
        L = dual_L(X, y, lam, k, res, *nd)
        if v < fS * (1 - 1e-7):
            c1 = False; fail = 'rem' if nd[0] else 'frc'; break
        if L < fS * (1 - 1e-7):
            undecided += 1
    return dict(p=p, n=n, seed=seed, pwe=pwe, wit=wit, c1=c1 if undecided == 0 or c1 is False else None,
                fail=fail, nsolve=nsolve, undecided=undecided, tau2=float((m0 / np.linalg.norm(r)) ** 2))


if __name__ == '__main__':
    p = int(sys.argv[1]); alpha = float(sys.argv[2]); seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    k = 8; n = max(k + 2, int(round(alpha * k * np.log(p))))
    for s in range(seeds):
        print(json.dumps(decide(n, p, k, 1000 + s)), flush=True)
