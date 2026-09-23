"""Deterministic numerical diagnostics; the manuscript proofs are analytic."""
import numpy as np

rng = np.random.default_rng(20260922)
checks = 0

def close(a, b, *, atol=1e-9):
    global checks
    np.testing.assert_allclose(a, b, atol=atol, rtol=1e-8)
    checks += 1

# Singular and indefinite coefficient cores, including a null transformed column.
for singular in [False, True]:
    for _ in range(12):
        c = rng.normal(size=(4, 7))
        c /= np.linalg.norm(c, 2)
        s = c @ c.T
        x, _ = np.linalg.qr(rng.normal(size=(7, 3)))
        _, _, vh = np.linalg.svd(c)
        x[:, 2] = vh[-1] * 1e-12
        x /= max(1, np.linalg.norm(x, 2))
        ell = np.diag([0.6, -0.4, 0 if singular else 0.2])
        n = s + c @ x @ ell @ x.T @ c.T
        k = x.T @ c.T @ np.linalg.solve(s, c @ x)
        j = np.linalg.inv(np.eye(3) + ell @ k)
        close(j, np.eye(3) - ell @ x.T @ c.T @ np.linalg.solve(n, c @ x))
        b = rng.normal(size=4); b /= np.linalg.norm(b)
        h = x.T @ c.T @ np.linalg.solve(s, b)
        z = j @ ell @ h
        close(np.linalg.solve(s, b - c @ x @ z), np.linalg.solve(n, b))

# The exact finite raw-trial law for rectangular, singular transforms.
for _ in range(12):
    t = rng.normal(size=(3, 5)); t[:, -1] = 0
    v = rng.normal(size=5); v /= np.linalg.norm(v)
    bound = np.linalg.norm(t, 2)
    row_count = t.shape[1]
    law = np.zeros(3)
    out = t @ v
    row_sq = (t * t) @ (v * v)
    for col in range(5):
        col_norm = t[:, col] @ t[:, col]
        if col_norm == 0:
            continue
        for row in range(3):
            law[row] += (v[col] ** 2 * col_norm / bound**2
                         * t[row, col]**2 / col_norm
                         * out[row]**2 / (row_count * row_sq[row]))
    close(law, out**2 / (row_count * bound**2))

# Power Hessian, inverse core, physical clipping endpoints, and derivative.
for m in [1, 2, 7]:
    for lam in [1.0, 1.01, 2.0, 10.0]:
        alpha = rng.uniform(0.1, 1, m); alpha /= alpha.sum()
        x = np.exp(rng.normal(size=m))
        p = np.exp(2 * alpha @ np.log(x))
        slack = p / lam
        direction = rng.normal(size=3); direction /= np.linalg.norm(direction)
        z = np.sqrt(p - slack) * direction
        kval = 1 + (2 * lam - 1) * alpha
        c = alpha @ alpha
        a = np.r_[alpha / x, np.zeros(3)]
        zz = np.r_[np.zeros(m), z]
        diag = np.r_[kval / x**2, np.repeat(2 / slack, 3)]
        hess = (np.diag(diag) + 4 * lam * (lam - 1) * np.outer(a, a)
                - 4 * lam / slack * (np.outer(a, zz) + np.outer(zz, a))
                + 4 / slack**2 * np.outer(zz, zz))
        xx = np.zeros((m + 3, 2))
        xx[:m, 0] = alpha / np.sqrt(c * kval)
        xx[m:, 1] = direction
        b = np.array([[4 * lam * (lam - 1) * c, -4 * lam * np.sqrt(c * (lam - 1) / 2)],
                      [-4 * lam * np.sqrt(c * (lam - 1) / 2), 2 * (lam - 1)]])
        norm_h = hess / np.sqrt(np.outer(diag, diag))
        close(norm_h, np.eye(m + 3) + xx @ b @ xx.T)
        t = np.sum(alpha**2 / kval) / c
        lo, hi = 1 / (2 * lam), min(1, 1 / (2 * lam * c))
        assert lo - 1e-12 <= t <= hi + 1e-12
        for test_t in [lo, t, hi]:
            gram = np.diag([test_t, 1])
            core = -np.linalg.solve(np.eye(2) + b @ gram, b)
            close(core, core.T)
            q = np.eye(2) + np.sqrt(gram) @ b @ np.sqrt(gram)
            assert np.linalg.eigvalsh(q).min() >= 1 / (4 * lam) - 1e-10
            assert np.linalg.eigvalsh(q).max() <= 4 * lam + 1e-10
            assert np.linalg.norm(core, 2) <= 10 * lam**2
            if lo + 1e-6 < test_t < hi - 1e-6:
                step = 1e-7
                plus = -np.linalg.solve(np.eye(2) + b @ np.diag([test_t + step, 1]), b)
                minus = -np.linalg.solve(np.eye(2) + b @ np.diag([test_t - step, 1]), b)
                close((plus - minus) / (2 * step), core @ np.diag([1, 0]) @ core, atol=2e-6)
        core = -np.linalg.solve(np.eye(2) + b @ np.diag([t, 1]), b)
        close(np.linalg.inv(norm_h), np.eye(m + 3) + xx @ core @ xx.T)
        # Independent Hessian construction by centered differences of gradient.
        def gradient(point):
            px, pz = point[:m], point[m:]
            pp = np.exp(2 * alpha @ np.log(px))
            ss = pp - pz @ pz
            return np.r_[-(2 * pp / ss * alpha + 1 - alpha) / px, 2 * pz / ss]
        point = np.r_[x, z]
        fd = np.empty_like(hess)
        for jcol in range(m + 3):
            step = 1e-6 * min(1, abs(point[jcol]) + 0.1) / lam
            shift = np.zeros(m + 3); shift[jcol] = step
            fd[:, jcol] = (gradient(point + shift) - gradient(point - shift)) / (2 * step)
        close(fd, hess, atol=1e-5)

# Lorentz inverse and one-hub augmented KKT Schur complement.
for n in [3, 9]:
    for chi in [1, 2, 30]:
        t = (np.sqrt(2 * chi) + np.sqrt(2 / chi)) / 2
        rz = (np.sqrt(2 * chi) - np.sqrt(2 / chi)) / 2
        radial = rng.normal(size=n-1); radial /= np.linalg.norm(radial)
        z = rz * radial
        j0 = np.diag(np.r_[1, -np.ones(n-1)])
        point = np.r_[t, z]; slack = t*t - z@z
        u = j0 @ point
        h = -2 * j0 / slack + 4 * np.outer(u, u) / slack**2
        up = np.r_[1, radial] / np.sqrt(2)
        um = np.r_[1, -radial] / np.sqrt(2)
        inv_h = (slack / 2 * np.eye(n) + rz * (t+rz) * np.outer(up, up)
                 - rz * (t-rz) * np.outer(um, um))
        close(inv_h @ h, np.eye(n))
        a = rng.normal(size=(2, n))
        kkt = np.block([[h, a.T], [a, np.zeros((2, 2))]])
        w = (2*u/slack)[:, None]
        aug = np.block([[-2*j0/slack, w, a.T], [w.T, -np.ones((1, 1)), np.zeros((1, 2))],
                        [a, np.zeros((2, 1)), np.zeros((2, 2))]])
        rhs = rng.normal(size=n+2)
        sol = np.linalg.solve(aug, np.r_[rhs[:n], 0, rhs[n:]])
        close(np.r_[sol[:n], sol[n+1:]], np.linalg.solve(kkt, rhs), atol=1e-7)

print(f"Structured diagnostics passed: {checks} numerical identities and comparison checks.")
