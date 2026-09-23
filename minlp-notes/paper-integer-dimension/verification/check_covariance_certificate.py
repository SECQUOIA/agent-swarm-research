#!/usr/bin/env python3
"""Check the new determinant certificate against independently known optima.

Exact rational feasibility, complementarity and residual identities are checked;
100-digit evaluation checks the inequality on nonoptimal covariances. This is
finite supporting evidence, not a proof of the general proposition.
"""
import random
import sympy as sp
import mpmath as mp

mp.mp.dps = 100
rng = random.Random(20260905)
def real(q):
    q = sp.Rational(q)
    return mp.mpf(int(q.p)) / int(q.q)

cases = 0
for n in range(1, 6):
    for trial in range(8):
        lam = [sp.Rational(rng.choice([-1, 1]) * rng.randint(1, 7), 2)
               for _ in range(n)]
        threshold = sp.Rational(rng.randint(1, 8), 3)
        pstar = [min(sp.S.One, threshold / abs(v)) for v in lam]
        H = sp.diag(*lam)
        optimum = sp.diag(*pstar)
        budget = sp.trace(H * optimum * H * optimum)
        mu_exact = 1 / (2 * threshold**2)
        S_exact = sp.diag(*[max(sp.S.Zero, 1 - v**2 / threshold**2) for v in lam])
        assert -optimum.inv() + 2 * mu_exact * H * optimum * H + S_exact == sp.zeros(n)
        assert sp.trace(S_exact * (sp.eye(n) - optimum)) == 0
        for perturbed in [False, True]:
            if perturbed:
                B = sp.Matrix(n, n, lambda i, j: rng.randint(-3, 3)) + 4 * sp.eye(n)
                # Adding I makes the covariance positive definite regardless of B.
                T = B * B.T + sp.eye(n)
                P = min(pstar) * T / (2 * sp.trace(T))
                mu = sp.Rational(rng.randint(0, 10), 7)
                C = sp.Matrix(n, n, lambda i, j: rng.randint(-2, 2))
                S = C * C.T / 13
            else:
                P, mu, S = optimum, mu_exact, S_exact
            assert P.det() > 0
            assert (sp.eye(n) - P).is_positive_semidefinite
            energy = sp.trace(H * P * H * P)
            assert energy <= budget
            slack = mu * (budget - energy) + sp.trace(S * (sp.eye(n) - P))
            assert slack >= 0
            R = -P.inv() + 2 * mu * H * P * H + S
            residual_square = sp.trace(P * R * P * R)
            assert residual_square >= 0
            if not perturbed:
                assert slack == residual_square == 0
            gap = mp.log(real(optimum.det())) - mp.log(real(P.det()))
            loss = -mp.log(real(P.det()))
            bound = real(slack) + mp.sqrt(n) * loss * mp.sqrt(real(residual_square))
            assert gap >= -mp.mpf('1e-90')
            assert gap <= bound + mp.mpf('1e-90')
            cases += 1
print(f'Passed {cases} determinant certificates; exact optimal stationarity in 40 signed diagonal cases, and 40 nonoptimal rational covariances.')
