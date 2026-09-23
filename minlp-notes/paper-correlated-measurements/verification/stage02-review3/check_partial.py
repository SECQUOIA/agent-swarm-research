"""Independent dense-covariance checks; no manuscript or historical outputs changed."""
import itertools
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(90313)
stats = {"models": 0, "schedule_windows": 0, "far_checks": 0,
         "old_checks": 0, "coefficient_checks": 0,
         "max_far_ratio": 0., "max_old_ratio": 0.,
         "max_coefficient_ratio": 0., "max_global_ratio": 0.}

def sym(a):
    return (a + a.T) / 2

def root(a, power):
    w, u = np.linalg.eigh(sym(a))
    assert w.min() > 0
    return (u * w**power) @ u.T

def check_norm(a, bound, key):
    value = np.linalg.norm(a, 2)
    assert value <= bound + 2e-10, (key, value, bound)
    stats[key + "_checks"] += 1
    stats["max_" + key + "_ratio"] = max(stats["max_" + key + "_ratio"], value / bound)

for model in range(6):
    n, latent, d = 7, 4, 2
    gamma = [0.25, 0.65, 0.9][model % 3]
    signal = [0.07, 1.0, 9.0][model % 3]
    kappa = signal / (1 + signal)
    # The support rotates and its rank changes; there is never a latent inverse.
    supports = []
    for t in range(n):
        u, _ = np.linalg.qr(rng.normal(size=(latent, latent)))
        rank = 1 + (t + model) % 3
        supports.append(u[:, :rank] @ np.diag(np.linspace(0.5, 1.5, rank)))
    p = [u @ u.T for u in supports]
    transitions = [None]
    for t in range(1, n):
        c = rng.normal(size=(supports[t].shape[1], supports[t-1].shape[1]))
        c *= gamma / np.linalg.norm(c, 2)
        a = supports[t] @ c @ np.linalg.pinv(supports[t-1])
        transitions.append(a)
        xi = sym(p[t] - a @ p[t-1] @ a.T)
        assert np.linalg.eigvalsh(xi - (1-gamma**2)*p[t]).min() > -2e-12
    v, obs = [], []
    for t in range(n):
        q, _ = np.linalg.qr(rng.normal(size=(d, d)))
        vt = q @ np.diag([0.3 + t/5, 2. + model]) @ q.T
        h = rng.normal(size=(d, latent))
        top = np.linalg.eigvalsh(root(vt, -0.5) @ h @ p[t] @ h.T @ root(vt, -0.5)).max()
        h *= np.sqrt(signal/top)
        v.append(vt)
        obs.append(h)
    r = np.zeros((n*d, n*d))
    sl = [slice(t*d, (t+1)*d) for t in range(n)]
    for t in range(n):
        r[sl[t], sl[t]] = obs[t] @ p[t] @ obs[t].T + v[t]
        phi = np.eye(latent)
        for j in range(t-1, -1, -1):
            phi = phi @ transitions[j+1]
            cross = obs[t] @ phi @ p[j] @ obs[j].T
            r[sl[t], sl[j]] = cross
            r[sl[j], sl[t]] = cross.T
    assert np.linalg.eigvalsh(r).min() > 0
    for bits in itertools.product([0, 1], repeat=n):
        selected = [t for t in range(n) if bits[t]]
        if not selected:
            continue
        inds = np.concatenate([np.arange(t*d, (t+1)*d) for t in selected])
        for window in range(n):
            residual, whiten, coeff, histories = {}, {}, {}, {}
            for t in selected:
                history = [j for j in selected if t-window <= j < t]
                histories[t] = history
                e = np.zeros((d, n*d))
                e[:, sl[t]] = np.eye(d)
                if history:
                    hidx = np.concatenate([np.arange(j*d, (j+1)*d) for j in history])
                    b = np.linalg.solve(r[np.ix_(hidx, hidx)], r[sl[t], :][:, hidx].T).T
                    e[:, hidx] = -b
                    for a, j in enumerate(history):
                        coeff[t, j] = b[:, a*d:(a+1)*d]
                residual[t] = e
                whiten[t] = root(e @ r @ e.T, -0.5)
            w = np.vstack([whiten[t] @ residual[t] for t in selected])
            c = sym(w @ r @ w.T)
            error = np.linalg.norm(c - np.eye(len(inds)), 2)
            tail = gamma**(window+1)/(1-gamma)
            near = sum(gamma**(h+2*dd) for h in range(1, window+1)
                       for dd in range(window+1-h, window+1))
            bound = 0. if window >= n-1 else 2*kappa*(tail + np.sqrt(kappa*signal)*near)
            assert error <= bound + 2e-10
            if bound:
                stats["max_global_ratio"] = max(stats["max_global_ratio"], error/bound)
            # Transfer has the SAME factors, not their reciprocals.
            qr = root(r[np.ix_(inds, inds)], 0.5)
            precision_relative = qr @ (w[:, inds].T @ w[:, inds]) @ qr
            assert abs(np.linalg.norm(precision_relative-np.eye(len(inds)), 2)-error) < 2e-10
            for t in selected:
                for s in selected:
                    if s < t-window:
                        check_norm(whiten[t] @ residual[t] @ r @ residual[s].T @ whiten[s],
                                   kappa*gamma**(t-s), "far")
                for j in range(max(0, t-window)):
                    check_norm(whiten[t] @ residual[t] @ r[:, sl[j]] @ root(v[j], -0.5),
                               np.sqrt(kappa*signal)*gamma**(t-j), "old")
                for j in histories[t]:
                    check_norm(whiten[t] @ coeff[t, j] @ root(v[j], 0.5),
                               kappa*gamma**(t-j), "coefficient")
            stats["schedule_windows"] += 1
    stats["models"] += 1

print(json.dumps(stats, indent=2))
Path(__file__).with_name("results.json").write_text(json.dumps(stats, indent=2) + "\n")
