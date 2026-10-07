"""Informational only (not a finding): E2, Euler transcription of the w = 0
formulation (gauge F = -k1 x1^2/2 - k2 x1 x2), against the tested k1 = 0
formulation. Reduced Hessian (exactly quadratic problem, float linear algebra)
restricted to the free stages of the box-constrained optimum.
Validation: the k1 = 0 minimum eigenvalues of the note (8.2e-5, 1.0e-5, 1.3e-6
at N = 50, 100, 200)."""
import numpy as np
from scipy.optimize import minimize

k2 = 0.25

def build(N, form):
    h = 3.0 / N
    A = np.array([[1.0, 0.0], [h, 1 - h]])
    bb = np.array([h, 0.0])
    # x_t = A^t x0 + sum_{s<t} A^{t-1-s} b u_s
    x0 = np.array([1.0, 0.0])
    Xc = np.zeros((N + 1, 2)); G = np.zeros((N + 1, 2, N))
    Xc[0] = x0
    for t in range(N):
        Xc[t + 1] = A @ Xc[t]
        G[t + 1] = A @ G[t]
        G[t + 1][:, t] += bb
    # quadratic cost J(u) = 1/2 u^T H u + c^T u + const, assembled exactly
    H = np.zeros((N, N)); c = np.zeros(N)
    def addquad(Qm, t):  # h/2 x_t^T Qm x_t (Qm symmetric), times 2 in the Hessian
        nonlocal H, c
        H += G[t].T @ Qm @ G[t]
        c += G[t].T @ Qm @ Xc[t]
    if form == "k1=0":
        L0 = h * np.eye(2)                     # h (x1^2 + x2^2)/2
        kv = np.array([0.0, k2])               # l1 = k2 x2
        Phi = np.diag([k2, 1 - 2 * k2])
    else:  # w = 0 formulation
        L0 = h * np.array([[1 - 2 * k2, k2], [k2, 1.0]])
        kv = np.zeros(2)
        Phi = np.array([[k2, k2], [k2, 1 - 2 * k2]])
    for t in range(N):
        addquad(L0, t)
        # h (kv . x_t) u_t
        row = h * (kv @ G[t])                  # d/du of (kv.x_t) is kv G[t]; bilinear with e_t
        H[t, :] += row; H[:, t] += row
        c[t] += h * kv @ Xc[t]
    addquad(Phi, N)
    return H, c

for form in ("k1=0", "w=0"):
    for N in (50, 100, 200, 400):
        H, c = build(N, form)
        f = lambda u: 0.5 * u @ H @ u + c @ u
        gr = lambda u: H @ u + c
        r = minimize(f, np.zeros(N), jac=gr, method="L-BFGS-B", bounds=[(-1, 1)] * N,
                     options=dict(maxiter=20000, ftol=1e-15, gtol=1e-13))
        u = r.x
        free = np.where(np.abs(np.abs(u) - 1) > 1e-7)[0]
        ev = np.linalg.eigvalsh(H[np.ix_(free, free)])
        h = 3.0 / N
        print("%-5s N=%4d: J=%.10f, free stages %d (first at t=%.4f), min eig %.3e = %.3f h^3, full-H min eig %.3e"
              % (form, N, r.fun + (0.5 * 0.25 if False else 0), len(free), free[0] * h, ev[0], ev[0] / h**3,
                 np.linalg.eigvalsh(H)[0]))
