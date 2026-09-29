"""Deterministic checks of Sections 1-2 (and Lemmas 3.6, 3.7, (G5)) on small random instances.
Run: python3 identities.py  (single-threaded; about a minute)."""
import numpy as np
from scipy import integrate
from scipy.stats import norm
from common import (make_instance, ridge_on, g_closed, h_val, dual_L, node_primal_cvx,
                    node_dual_cvx, saturated_witness)

rng = np.random.default_rng(12345)
W = {}
def rec(key, v, mode="absmax"):
    if mode == "absmax":
        W[key] = max(W.get(key, 0.0), abs(float(v)))
    elif mode == "max":
        W[key] = max(W.get(key, -np.inf), float(v))
    elif mode == "min":
        W[key] = min(W.get(key, np.inf), float(v))
    elif mode == "count":
        W[key] = W.get(key, 0) + int(v)

for trial in range(40):
    n = int(rng.integers(15, 45)); p = int(rng.integers(20, 60)); k = int(rng.integers(2, 6))
    sigma = float(rng.choice([0.2, 0.5, 1.0])); lam = float(rng.uniform(0.5, 2.0) * np.sqrt(n) * rng.choice([1, 3]))
    X, y, S, beta = make_instance(n, p, k, sigma=sigma, seed=trial)
    fS, bS, r = ridge_on(X, y, lam, S)
    XS = X[:, S]
    # direct p-side ridge
    bdir = np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y)
    rec("ridge: beta^S (n-form vs p-form)", np.max(np.abs(bdir - bS)))
    rec("ridge: f(S)=||r||^2+lam||b||^2 rel", (fS - (r @ r + lam * bS @ bS)) / fS)
    rec("ridge: f(S)=min objective rel", (fS - (np.sum((y - XS @ bdir) ** 2) + lam * bdir @ bdir)) / fS)
    # (F1)-(F3) at random fractional z
    z = rng.uniform(0, 1, p) * (rng.uniform(0, 1, p) < 0.6)
    gz, az = g_closed(X, y, lam, z)
    rec("(F3) g = h(a(z),z) rel", (gz - h_val(X, y, lam, az, z)) / gz)
    rec("(F3) h(a,z) <= g for random a (max excess)", max(h_val(X, y, lam, az + 0.3 * rng.standard_normal(n), z) - gz for _ in range(5)), "max")
    P = np.nonzero(z > 0)[0]
    bP = np.linalg.solve(X[:, P].T @ X[:, P] + lam * np.diag(1 / z[P]), X[:, P].T @ y)
    persp = np.sum((y - X[:, P] @ bP) ** 2) + lam * np.sum(bP ** 2 / z[P])
    rec("(F2) perspective min = g rel", (persp - gz) / gz)
    z1 = np.zeros(p); z1[S] = 1
    rec("(F1) g(1_S) = f(S) rel", (g_closed(X, y, lam, z1)[0] - fS) / fS)
    # Lemma 1.1 strong duality at root and at random single-fixing nodes (independent primal & dual SOCPs)
    if trial < 12:
        nulls = np.setdiff1d(np.arange(p), S)
        nodes = [((), ()), ((int(S[0]),), ()), ((), (int(nulls[0]),)), ((int(nulls[1]),), (int(S[1]),))]
        for S0, S1 in nodes:
            vp, zz, bb, rr = node_primal_cvx(X, y, lam, k, S0, S1)
            vd, ad = node_dual_cvx(X, y, lam, k, S0, S1)
            rec("Lemma 1.1: primal SOCP - dual SOCP (rel)", (vp - vd) / vp)
            rec("Lemma 1.1: L(residual of primal) vs primal (rel)", (vp - dual_L(X, y, lam, k, rr, S0, S1)) / vp)
            rec("Lemma 1.1: g(z*) vs primal SOCP (rel)", (g_closed(X, y, lam, zz)[0] - vp) / vp)
            rec("Lemma 1.1: L(random a) - node value (max, <=0)", dual_L(X, y, lam, k, rr + 0.2 * rng.standard_normal(n), S0, S1) - vp, "max")
    # Lemma 2.1 witness identity for random V, u
    Minv = np.linalg.inv(np.eye(n) + XS @ XS.T / lam)
    nulls = np.setdiff1d(np.arange(p), S)
    V = rng.choice(nulls, int(rng.integers(1, 6)), replace=False)
    XV = X[:, V]; H = XV.T @ Minv @ XV; u = rng.standard_normal(len(V))
    Delta = Minv @ XV @ u; alpha = r - Delta
    rec("Lemma 2.1: h(alpha,1_S) = f(S)-u'Hu (rel)", (h_val(X, y, lam, alpha, z1) - (fS - u @ H @ u)) / fS)
    rec("Lemma 2.1: c_V = a_V - H u", np.max(np.abs(XV.T @ alpha - (XV.T @ r - H @ u))))
    rec("Lemma 2.1: ||Delta||^2 - u'Hu (max, <=0)", Delta @ Delta - u @ H @ u, "max")
    # Proposition 2.3 / Lemma 2.2 on the saturated witness, checked against exact node values
    a = X.T @ r; m0 = np.min(np.abs(a[S]))
    for th in (0.8, 0.95):
        al, Gam, VV, _ = saturated_witness(X, y, lam, S, th * m0)
        if len(VV) and len(VV) > n - k - 1:
            rec("Prop 2.3: skipped (|V| > n-k-1, H_V singular)", 1, "count"); continue
        rec("Prop 2.3: witnesses evaluated", 1, "count")
        c = X.T @ al
        rec("Prop 2.3: |c_V| = kappa", np.max(np.abs(np.abs(c[VV]) - th * m0)) if len(VV) else 0.0)
        rec("Prop 2.3: h(alpha,1_S) = f(S) - Gamma (rel)", (h_val(X, y, lam, al, z1) - (fS - Gam)) / fS)
        m = np.min(np.abs(c[S])); M = np.max(np.abs(c[nulls]))
        if M <= m and trial < 25:
            base = fS - Gam
            # removal nodes
            for i in S[:2]:
                lb = base + (c[i] ** 2 - M ** 2) / lam
                rec("Lemma 2.2: L(alpha) at removal node == formula (rel)", (dual_L(X, y, lam, k, al, (int(i),), ()) - lb) / fS)
                v = node_primal_cvx(X, y, lam, k, (int(i),), ())[0]
                rec("Lemma 2.2: formula - exact removal node (max, <=0)", (lb - v) / fS, "max")
            for j in nulls[np.argsort(-np.abs(c[nulls]))[:2]]:
                lb = base + (m ** 2 - c[j] ** 2) / lam
                rec("Lemma 2.2: L(alpha) at forced-in node == formula (rel)", (dual_L(X, y, lam, k, al, (), (int(j),)) - lb) / fS)
                v = node_primal_cvx(X, y, lam, k, (), (int(j),))[0]
                rec("Lemma 2.2: formula - exact forced-in node (max, <=0)", (lb - v) / fS, "max")
            rec("Lemma 2.2: witnesses with M <= m checked vs exact nodes", 1, "count")
            R = node_primal_cvx(X, y, lam, k)[0]
            rec("Prop 2.3: f(S) - R - Gamma (max, <=0)", (fS - R - Gam) / fS, "max")
    # Corollary 2.4: root exact iff certificate
    if trial < 30:
        R = node_primal_cvx(X, y, lam, k)[0]
        cert = np.max(np.abs(a[nulls])) <= m0
        exact = R >= fS * (1 - 1e-7)
        rec("Cor 2.4: certificate != (R == f(S)) count", cert != exact, "count")
        rec("Cor 2.4: instances with certificate", cert, "count")
    # Lemma 2.5 explicit primal point
    bplus = np.max(np.abs(bS)); kappa = lam * bplus * 1.05
    null_sorted = nulls[np.argsort(-np.abs(a[nulls]))]
    j = int(null_sorted[-1]); Vp = null_sorted[:6]
    e = np.maximum(np.abs(a[Vp]) - kappa, 0); Q = e @ e
    if Q > 0 and k >= 3:
        L = np.linalg.norm(X[:, Vp], 2) ** 2
        s = min(1.0, 0.5)
        w = s * np.sign(a[Vp]) * e / L; tl = lam * np.abs(w) / kappa; T = tl.sum()
        if tl.max() <= 1 and T < k - 1:
            zz = np.zeros(p); zz[S] = 1 - (1 + T) / k; zz[j] = 1; zz[Vp] = tl
            val = g_closed(X, y, lam, zz)[0]
            bound = fS + lam * bplus ** 2 * (1 + (1 + T) ** 2 / (k - 1 - T)) - (2 * s - s * s) * Q / L
            rec("Lemma 2.5: g(z) - bound (max, <=0)", (val - bound) / fS, "max")
            rec("Lemma 2.5: sum z - k (max, <=0)", zz.sum() - k, "max")
            rec("Lemma 2.5: instances checked", 1, "count")
    # Lemma 3.6 leave-one-out formula
    i = 0; Si = np.delete(S, i); Ai = np.linalg.inv(np.eye(n) + X[:, Si] @ X[:, Si].T / lam)
    xi = X[:, S[i]]; yi = y - beta[S[i]] * xi
    q = xi @ Ai @ xi; xii = xi @ Ai @ yi
    rec("Lemma 3.6: beta_i formula", abs(bS[i] - (beta[S[i]] * q + xii) / (lam + q)))
    # Lemma 3.7: v and noise split
    G = XS.T @ XS; v = lam * XS @ np.linalg.solve(lam * np.eye(k) + G, beta[S])
    rec("Lemma 3.7: v = M^-1 X_S beta* (push-through)", np.max(np.abs(v - Minv @ XS @ beta[S])))
    ev = np.linalg.eigvalsh(G); ratio = lam ** 2 * ev / (lam + ev) ** 2
    vv = v @ v; bb2 = beta[S] @ beta[S]
    rec("Lemma 3.7: ||v||^2 outside eigen-bracket (count)", not (bb2 * ratio.min() * (1 - 1e-12) <= vv <= bb2 * ratio.max() * (1 + 1e-12)), "count")

# (G5): m(tau) closed form vs quadrature, and bound 2 phi/tau
for tau in (0.3, 1.0, 2.0, 3.0, 4.5):
    quad = 2 * integrate.quad(lambda zz: np.exp(-zz ** 2 / 2 + (zz - tau) ** 2 / 4) / np.sqrt(2 * np.pi) - norm.pdf(zz), tau, np.inf, limit=200)[0]
    closed = 2 * np.sqrt(2) * np.exp(tau ** 2 / 2) * norm.sf(np.sqrt(2) * tau) - 2 * norm.sf(tau)
    rec("(G5) closed form vs quadrature (rel)", (closed - quad) / quad)
    rec("(G5) m(tau) - 2phi/tau (max, <=0)", closed - 2 * norm.pdf(tau) / tau, "max")
# (G1): 2 Phibar(t) <= exp(-t^2/2)
ts = np.linspace(0, 10, 2001)
rec("(G1) 2Phibar(t) - exp(-t^2/2) (max, <=0)", np.max(2 * norm.sf(ts) - np.exp(-ts ** 2 / 2)), "max")

for key, v in W.items():
    print(f"{key:58s} {v: .3e}" if not isinstance(v, int) else f"{key:58s} {v}")
