"""Sign of the Euler Riccati defect F(P(t+h)) - P(t) for the sampled continuous LQ value function.

Scalar LQ: xdot = alpha x + u, l = (u^2 + q x^2)/2, Phi = phiT x^2/2.  The value function
V = P x^2/2 is a (non-strict in x) calibration: r = (u + P x)^2/2.  For the Euler
transcription with the transferred family S^h_t = V(t_t,.) + a_t x, the stage residual,
minimized over u, is a quadratic in x with leading coefficient
    (F(P(t_{t+1})) - P(t_t))/2,   F(P') = h q + (1+h alpha)^2 P' - (h(1+h alpha) P')^2/(h + h^2 P').
If this is negative at some stage, the transferred family is not exact on any compact D
of positive width (the residual is not minimized at the trajectory), for that h.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

rows = []
for alpha, q, phiT in [(0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0),
                       (2.0, 0.0, 1.0), (-2.0, 0.0, 1.0), (0.0, 0.0, 1.0), (1.0, -1.0, 0.5)]:
    T = 1.0
    sol = solve_ivp(lambda t, P: -(q + 2 * alpha * P - P**2), [T, 0.0], [phiT],
                    rtol=1e-12, atol=1e-14, dense_output=True)
    rec = {"alpha": alpha, "q": q, "phiT": phiT}
    for N in (20, 80, 320):
        h = T / N
        tt = h * np.arange(N + 1)
        P = sol.sol(tt)[0]
        F = h * q + (1 + h * alpha) ** 2 * P[1:] - (h * (1 + h * alpha) * P[1:]) ** 2 / (h + h * h * P[1:])
        d = (F - P[:-1]) / h**2
        rec[f"N{N}_min_defect_over_h2"] = float(d.min())
        rec[f"N{N}_max_defect_over_h2"] = float(d.max())
    rows.append(rec)
    print(json.dumps(rec))
json.dump(rows, open("logs/c3_nonstrict_lq_sign.json", "w"), indent=1)
