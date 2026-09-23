"""Primal heuristic: dense random sampling + multistart projected gradient (Adam)."""
import numpy as np


def local_descent(net, sense, X, lx, ux, iters=400, lr=0.02):
    """Projected Adam on sense * net(x) from the rows of X; returns final points and values."""
    X = np.clip(np.array(X, float), lx, ux)
    w = ux - lx
    m = np.zeros_like(X)
    v = np.zeros_like(X)
    for k in range(1, iters + 1):
        _, g = net.value_grad(X)
        g = sense * g
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        step = lr * (1 - k / (iters + 1)) * w
        X = np.clip(X - step * (m / (1 - 0.9 ** k)) / (np.sqrt(v / (1 - 0.999 ** k)) + 1e-12), lx, ux)
    return X, sense * net.forward(X)


def multistart(net, sense, lx=None, ux=None, nsample=200000, nstart=256, seed=0):
    lx = net.lo if lx is None else lx
    ux = net.hi if ux is None else ux
    rng = np.random.default_rng(seed)
    S = rng.uniform(lx, ux, (nsample, len(lx)))
    fs = sense * net.forward(S)
    best_s = int(np.argmin(fs))
    starts = np.concatenate([S[np.argsort(fs)[:nstart // 2]], rng.uniform(lx, ux, (nstart // 2, len(lx)))])
    X, fx = local_descent(net, sense, starts, lx, ux)
    i = int(np.argmin(fx))
    # polish the best point with small steps
    Xp, fp = local_descent(net, sense, X[i:i + 1], lx, ux, iters=2000, lr=1e-3)
    cands = [(fs[best_s], S[best_s]), (fx[i], X[i]), (fp[0], Xp[0])]
    val, x = min(cands, key=lambda c: c[0])
    return dict(x=x, value=float(val), sample_best=float(fs[best_s]), multistart_best=float(fx[i]),
                distinct_local=int(len(np.unique(np.round(X, 3), axis=0))))
