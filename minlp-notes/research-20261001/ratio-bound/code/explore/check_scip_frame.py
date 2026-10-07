"""SCIP's set in its balanced normalized frame (Section 4 of the note): with
t^2 = (1 + qbar + ybar^2)/(1 + qbar + xbar^2) the matrix X of C_SCIP = C_X (normalized frame of sbar, parameter t)
is symmetric and proportional to [[1, b], [b, 1]] with
b^2 = (xbar - ybar)^2 qbar / ((wbar + 1)^2 + (xbar - ybar)^2 (1 + qbar)).  Random check on 200 vertices."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import rb

rng = np.random.default_rng(0)
mx = 0.0
for k in range(200):
    xb, yb = rng.normal(size=2) * 3
    qb = np.exp(rng.normal())
    sb = np.array([xb, yb, xb * yb + qb])
    t = np.sqrt((1 + qb + yb * yb) / (1 + qb + xb * xb))
    X = rb.to_normalized_X(rb.scip_F(sb), sb, t)
    S = rb.sym(X) / rb.sym(X)[0, 0]
    d, W = xb - yb, sb[2] + 1
    beta2 = d * d * qb / (W * W + d * d * (1 + qb))
    mx = max(mx, abs(S[1, 1] - 1), abs(S[0, 1] ** 2 - beta2), abs(X[0, 1] - X[1, 0]) / abs(X[0, 0]))
print('vertices 200, max deviation from the formula: %.2e' % mx)
