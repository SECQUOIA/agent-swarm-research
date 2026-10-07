"""Independent check of the T1 numbers added in the third revision
(Section 3, Remarks, 'Numbers'; Section 12.3, item 2).

- Best approximant p of |s| on [-1, 1] in P_n (n = 4, 8) by a discrete Remez
  exchange for sqrt(t) on [0, 1] in degree n/2 (t = s^2); own code.
- r = |s| - p.  For the split phi_1 = phi_2 = -p the middle bag is
  r(s1) - r(s2) + K (s1 - s2)^2; its minimum m_B is found by a dense search
  over (s2, d = s1 - s2) followed by a local polish (so -m_B found here is a
  lower bound on the true -m_B, up to rounding, and close to it).
- Compared with the note's 'at least' values and with Lip(r)^2/(4K).
- Also: the finite-K strictness argument's key inequality -rho >= X >=
  max(osc r_1, osc r_2) is tested on random polynomial splits (exact middle
  bag minimum replaced by a fine-grid minimum, which only weakens -rho, so a
  violation would be meaningful; none expected).
Floating point; not certified.
"""
import numpy as np
from scipy.optimize import minimize

out = open("logs/r1_t1_step3.log", "w")


def log(m):
    print(m)
    out.write(m + "\n")
    out.flush()


def remez_sqrt(k, npts=400001, iters=60):
    t = np.unique(np.concatenate([np.linspace(0, 1, npts), np.logspace(-14, 0, npts)]))
    f = np.sqrt(t)
    ref = np.sort(0.5 - 0.5 * np.cos(np.pi * np.arange(k + 2) / (k + 1)))
    ref_idx = np.searchsorted(t, ref).clip(0, len(t) - 1)
    for _ in range(iters):
        x = t[ref_idx]
        A = np.hstack([np.vander(x, k + 1, increasing=True), ((-1.0) ** np.arange(k + 2))[:, None]])
        sol = np.linalg.solve(A, np.sqrt(x))
        a, h = sol[:-1], sol[-1]
        e = f - np.polynomial.polynomial.polyval(t, a)
        # new reference: extrema of alternating sign segments
        sgn = np.sign(e)
        sgn[sgn == 0] = 1
        brk = np.flatnonzero(np.diff(sgn)) + 1
        segs = np.split(np.arange(len(t)), brk)
        cand = [s[np.argmax(np.abs(e[s]))] for s in segs]
        cand = np.array(cand)
        # keep k+2 consecutive candidates with the largest minimum |e|
        if len(cand) > k + 2:
            best, bi = -1, 0
            for i in range(len(cand) - (k + 2) + 1):
                v = np.min(np.abs(e[cand[i:i + k + 2]]))
                if v > best:
                    best, bi = v, i
            cand = cand[bi:bi + k + 2]
        if len(cand) < k + 2:
            break
        new = np.array(cand)
        if np.array_equal(new, ref_idx):
            break
        ref_idx = new
    E = np.max(np.abs(e))
    return a, abs(h), E


def main():
    rng = np.random.default_rng(1)
    for n in [4, 8]:
        a, h, E = remez_sqrt(n // 2)
        p = lambda s: np.polynomial.polynomial.polyval(s * s, a)
        dp = lambda s: np.polynomial.polynomial.polyval(s * s, np.polynomial.polynomial.polyder(a)) * 2 * s
        r = lambda s: np.abs(s) - p(s)
        s = np.linspace(-1, 1, 400001)
        rv = r(s)
        osc = rv.max() - rv.min()
        lip = np.max(np.abs(np.sign(s) - dp(s)))
        log(f"n={n}: Remez levelled error h = {h:.10f}, max error = {E:.10f}, 2E_n = {2 * E:.10f}, osc(r) = {osc:.10f}, Lip(r) = {lip:.6f}")
        for K in [100.0, 1000.0, 10000.0]:
            dmax = 2 * lip / K
            s2 = np.linspace(-1, 1, 20001)
            best, arg = -np.inf, None
            for d in np.linspace(-dmax, dmax, 2001):
                s1 = s2 + d
                ok = np.abs(s1) <= 1
                v = r(s2[ok]) - r(s1[ok]) - K * d * d
                i = np.argmax(v)
                if v[i] > best:
                    best, arg = v[i], (s2[ok][i], s1[ok][i])
            # local polish (bounded)
            obj = lambda z: -(r(np.array([z[0]]))[0] - r(np.array([z[1]]))[0] - K * (z[1] - z[0]) ** 2)
            res = minimize(obj, np.array(arg), method="L-BFGS-B", bounds=[(-1, 1), (-1, 1)])
            pol = max(best, -res.fun)
            ub = lip ** 2 / (4 * K)
            log(f"  K={K:7.0f}: -m_B = {pol:.4e} (grid {best:.4e}) at s2={res.x[0]:.5f}, s1={res.x[1]:.5f}; "
                f"Lip^2/(4K) = {ub:.4e}; gap(-p)/2E_n = {1 + pol / (2 * E):.5f}")
        # random-split test of -rho >= X >= max(osc r_1, osc r_2) at K = 100
        K = 100.0
        sg = np.linspace(-1, 1, 801)
        worst = np.inf
        for trial in range(200):
            q1 = a + rng.normal(scale=10 ** rng.uniform(-4, -1), size=a.shape)
            q2 = a + rng.normal(scale=10 ** rng.uniform(-4, -1), size=a.shape)
            c1, c2 = rng.normal(size=2) * 0.1
            r1 = np.abs(sg) - np.polynomial.polynomial.polyval(sg * sg, q1) - c1
            r2 = np.abs(sg) - np.polynomial.polynomial.polyval(sg * sg, q2) - c2
            mB = np.min(r1[:, None] - r2[None, :] + K * (sg[:, None] - sg[None, :]) ** 2)
            negrho = r1.max() - mB - r2.min()
            X = r1.max() - r2.min() + np.max(r2 - r1)
            o = max(np.ptp(r1), np.ptp(r2))
            worst = min(worst, negrho - X, X - o)
        log(f"  random splits (200, K=100, 801-pt grid): min over trials of min(-rho - X, X - max osc) = {worst:.3e} (>= 0 expected)")


main()
