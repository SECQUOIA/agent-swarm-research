"""Independent finite-network checks of the capacity perturbation claims.

Run: python research/verification/check_nucleation_bounds.py
Only numpy is needed. Results supplement, rather than replace, the proof.
"""
import json
import numpy as np

rng = np.random.default_rng(20260906)
worst = {"finite_bound_violation": 0.0, "hessian_bound_violation": 0.0,
         "second_difference_error": 0.0, "slope_difference_error": 0.0}

def capacity(B, c):
    L = B.T @ (c[:, None] * B)
    q = np.zeros(B.shape[1])
    q[-1] = 1
    q[1:-1] = np.linalg.solve(L[1:-1, 1:-1], -L[1:-1, -1])
    dq = B @ q
    C = np.sum(c * dq**2)
    return C, q, L, dq

for case in range(200):
    n = int(rng.integers(4, 15))
    edges = {(i, i + 1) for i in range(n - 1)}
    edges.update((i, j) for i in range(n) for j in range(i+1, n)
                 if rng.random() < .3)
    edges = sorted(edges)
    B = np.zeros((len(edges), n))
    for e, (i, j) in enumerate(edges):
        B[e, i], B[e, j] = -1, 1
    c = np.exp(rng.normal(size=len(edges)))
    Q = rng.normal(size=(len(edges), 3))
    C, q, L, dq = capacity(B, c)
    nu = c * dq**2 / C
    mean = nu @ Q
    centered = Q - mean
    V = centered.T @ (nu[:, None] * centered)
    forcing = B.T @ ((c * dq)[:, None] * Q)
    h = np.zeros((n, 3))
    h[1:-1] = np.linalg.solve(L[1:-1, 1:-1], -forcing[1:-1])
    G = h.T @ L @ h / C
    H = V - 2*G
    violation = max(-np.linalg.eigvalsh(V-H).min(),
                    -np.linalg.eigvalsh(V+H).min(), 0)
    worst["hessian_bound_violation"] = max(worst["hessian_bound_violation"], violation)
    v = rng.normal(size=3)
    v /= np.linalg.norm(v)
    score = Q @ v
    for lam in [-2., -.7, .4, 1.6]:
        ratio = capacity(B, c*np.exp(lam*score))[0] / C
        lower = 1/np.sum(nu*np.exp(-lam*score))
        upper = np.sum(nu*np.exp(lam*score))
        violation = max(lower-ratio, ratio-upper, 0)
        worst["finite_bound_violation"] = max(worst["finite_bound_violation"], violation)
    eps = 2e-4
    logm, log0, logp = [np.log(capacity(B,c*np.exp(t*score))[0]) for t in [-eps, 0, eps]]
    worst["second_difference_error"] = max(worst["second_difference_error"], abs((logp-2*log0+logm)/eps**2-v@H@v))
    worst["slope_difference_error"] = max(worst["slope_difference_error"], abs((logp-logm)/(2*eps)-mean@v))

# Series/parallel exact sharpness with precisely the same reference score law.
p = np.array([.2, .3, .5])
Q = np.array([-1., .2, 2.])
Bseries = np.zeros((3,4))
for i in range(3):
    Bseries[i,i], Bseries[i,i+1] = -1,1
Bparallel = np.tile([-1.,1.],(3,1))
sharpness = 0.
for lam in [-2.,-.1,.7,2.]:
    par = capacity(Bparallel, p*np.exp(lam*Q))[0]
    ser = capacity(Bseries, np.exp(lam*Q)/p)[0]
    sharpness = max(sharpness, abs(par-np.sum(p*np.exp(lam*Q))),
                    abs(ser-1/np.sum(p*np.exp(-lam*Q))))
assert worst['finite_bound_violation'] < 1e-10
assert worst['hessian_bound_violation'] < 1e-10
assert worst['second_difference_error'] < 1e-6
assert worst['slope_difference_error'] < 1e-6
assert sharpness < 1e-10
print(json.dumps({'random_networks': 200, 'finite_perturbations': 800,
                  **worst, 'sharpness_absolute_error': sharpness}, indent=2))
