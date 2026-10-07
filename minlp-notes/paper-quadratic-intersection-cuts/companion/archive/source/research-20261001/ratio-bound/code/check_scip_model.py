"""Check that SCIP's Case-4 set for w <= xy (the scout's reimplementation ms_set of
Chmiela-Munoz-Serrano, used as "SCIP's set" in the sfree note) is the upward closure of
C_F with F^T = R_theta, tan theta = (xbar - ybar)/(wbar + 1), and that its uncompleted
version |yh| <= lambda^T xh is C_F itself.  Compares step lengths on random rays.
Also checks the parabolic-cylinder step formula against a direct membership test."""
import numpy as np
import rb
from scout_sfree import ms_set, step_length

rng = np.random.default_rng(7)
Q, B, C0 = rb.Q, rb.B, rb.C0
maxdiffB = maxdiffA = maxdiffcyl = 0.0
n = 0
for k in range(300):
    sbar = rng.normal(size=3) * rng.choice([0.3, 1, 3])
    sbar[2] = sbar[0] * sbar[1] + np.exp(rng.normal() * 1.5)
    G, case = ms_set(Q, B, C0, sbar)
    assert case == 'case4'
    F = rb.scip_F(sbar)
    X = rb.to_normalized_X(F, sbar)
    xh = lambda s: np.array([(s[0] - s[1]) / 2, (s[2] + 1) / 2])
    yh = lambda s: np.array([(s[0] + s[1]) / 2, (s[2] - 1) / 2])
    lam = xh(sbar) / np.linalg.norm(xh(sbar))
    GA = lambda s: np.linalg.norm(yh(s)) - lam @ xh(s)
    for _ in range(4):
        p = rng.normal(size=3)
        pn = rb.normalize(sbar, p[:, None])
        aB_scout = step_length(G, sbar, p)
        aB_mine = rb.stepB_X(X, pn[:, 0])
        aA_scout = step_length(GA, sbar, p)
        aA_mine = rb.steps_X(X, pn)[0]
        for a1, a2, which in ((aB_scout, aB_mine, 'B'), (aA_scout, aA_mine, 'A')):
            if np.isinf(a1) or np.isinf(a2):
                d = 0.0 if (np.isinf(a1) and np.isinf(a2)) or min(a1, a2) > 1e6 else np.inf
                if d > 0:
                    print('mismatch', which, sbar, p, a1, a2)
            else:
                d = abs(a1 - a2) / max(1.0, abs(a1))
            if which == 'B':
                maxdiffB = max(maxdiffB, d)
            else:
                maxdiffA = max(maxdiffA, d)
        # parabolic cylinder C_t: closed form vs bisection on its definition
        t = np.exp(rng.normal())
        Gc = lambda s: (t * (s[0] - sbar[0]) - (s[1] - sbar[1]) / t) ** 2 / 4 - rb.q(s)
        a_bis = step_length(Gc, sbar, p)
        a_cf = rb.cyl_steps(sbar, p[:, None], t)[0]
        d = 0.0 if (np.isinf(a_bis) and np.isinf(a_cf)) or min(a_bis, a_cf) > 1e6 else abs(a_bis - a_cf) / max(1, a_cf)
        maxdiffcyl = max(maxdiffcyl, d)
        n += 1
print('rays tested', n)
print('max rel diff, SCIP Case-4 set (scout ms_set) vs upward closure of C_{R_theta}:', maxdiffB)
print('max rel diff, plain Munoz-Serrano set |yh| <= lam^T xh vs C_{R_theta}:', maxdiffA)
print('max rel diff, parabolic cylinder closed form vs bisection:', maxdiffcyl)
print('PASS (tolerance 1e-5)' if max(maxdiffA, maxdiffB, maxdiffcyl) < 1e-5 else 'FAIL')
