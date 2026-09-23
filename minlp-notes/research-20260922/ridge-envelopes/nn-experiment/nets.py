"""Benchmark networks: test functions, numpy training (Adam, full batch), I/O.

A network maps x in [-1,1]^d through hidden layers y = sigma(W y_prev + b) to a
linear scalar output w_out . y + b_out that predicts the standardized target.
Run `python nets.py` to train all networks (fixed seeds) into nets/.
"""
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from acts import ACTS, erf, sigmoid

HERE = Path(__file__).resolve().parent
NETDIR = HERE / "nets"


# ---------------------------------------------------------------- test functions
def peaks2(u, v):
    return (3 * (1 - u) ** 2 * np.exp(-u ** 2 - (v + 1) ** 2)
            - 10 * (u / 5 - u ** 3 - v ** 5) * np.exp(-u ** 2 - v ** 2)
            - np.exp(-(u + 1) ** 2 - v ** 2) / 3)


def f_peaks(x):  # peaks on [-3,3]^2, averaged over consecutive coordinate pairs
    u = 3 * x
    return np.mean([peaks2(u[:, i], u[:, i + 1]) for i in range(x.shape[1] - 1)], axis=0)


def f_rosenbrock(x):  # log(1 + Rosenbrock) on [-1.5,1.5]^d
    u = 1.5 * x
    r = np.sum(100 * (u[:, 1:] - u[:, :-1] ** 2) ** 2 + (1 - u[:, :-1]) ** 2, axis=1)
    return np.log1p(r)


def f_ackley(x):  # Ackley on [-2,2]^d
    u = 2 * x
    return (-20 * np.exp(-0.2 * np.sqrt(np.mean(u ** 2, axis=1))) - np.exp(np.mean(np.cos(2 * np.pi * u), axis=1))
            + 20 + math.e)


def f_sines(x):  # sum of sines with a coupling term
    d = x.shape[1]
    return np.sum(np.sin(3 * x + np.arange(d)), axis=1) + 0.5 * np.sin(2 * np.pi * x[:, 0] * x[:, 1])


TARGETS = {"peaks": f_peaks, "ackley": f_ackley, "sines": f_sines, "rosenbrock": f_rosenbrock}
TARGET_ORDER = ["peaks", "ackley", "sines", "rosenbrock"]
ACT_ORDER = ["tanh", "sigmoid", "silu", "gelu", "sin"]
# (input dim, hidden widths); the target rotates with the activation index
ARCHS = [(2, [16]), (2, [16, 16]), (2, [8, 8, 8]), (3, [32]), (3, [16, 16]), (3, [8, 8, 8]), (5, [16, 16]), (5, [32, 32])]
SIREN_OMEGA0 = 5.0


def configs():
    out = []
    for ai, act in enumerate(ACT_ORDER):
        for ci, (d, hid) in enumerate(ARCHS):
            tgt = TARGET_ORDER[(ci + ai) % 4]
            name = "%s_d%d_%s_%s" % (act, d, "x".join(map(str, hid)), tgt)
            out.append(dict(name=name, act=act, d=d, hidden=hid, target=tgt, seed=1000 * ai + ci))
    return out


# ---------------------------------------------------------------- network
class Net:
    def __init__(self, act, Ws, bs, w_out, b_out, lo, hi, meta=None):
        self.act = ACTS[act]
        self.actname = act
        self.Ws, self.bs = [np.asarray(W, float) for W in Ws], [np.asarray(b, float) for b in bs]
        self.w_out, self.b_out = np.asarray(w_out, float), float(b_out)
        self.lo, self.hi = np.asarray(lo, float), np.asarray(hi, float)
        self.meta = meta or {}

    @property
    def d(self):
        return self.Ws[0].shape[1]

    @property
    def widths(self):
        return [W.shape[0] for W in self.Ws]

    def forward(self, X):
        h = np.atleast_2d(X)
        for W, b in zip(self.Ws, self.bs):
            h = self.act.f(h @ W.T + b)
        return h @ self.w_out + self.b_out

    def value_grad(self, X):
        """Output and input gradient for a batch X (N, d)."""
        h = np.atleast_2d(X)
        ders = []
        for W, b in zip(self.Ws, self.bs):
            z = h @ W.T + b
            ders.append(self.act.df(z))
            h = self.act.f(z)
        out = h @ self.w_out + self.b_out
        g = np.repeat(self.w_out[None, :], h.shape[0], axis=0)
        for W, dz in zip(reversed(self.Ws), reversed(ders)):
            g = (g * dz) @ W
        return out, g

    def save(self, path):
        arr = {"W%d" % i: W for i, W in enumerate(self.Ws)}
        arr.update({"b%d" % i: b for i, b in enumerate(self.bs)})
        np.savez(path, w_out=self.w_out, b_out=self.b_out, lo=self.lo, hi=self.hi, act=self.actname,
                 nlayers=len(self.Ws), meta=json.dumps(self.meta), **arr)

    @staticmethod
    def load(path):
        z = np.load(path)
        L = int(z["nlayers"])
        return Net(str(z["act"]), [z["W%d" % i] for i in range(L)], [z["b%d" % i] for i in range(L)],
                   z["w_out"], float(z["b_out"]), z["lo"], z["hi"], json.loads(str(z["meta"])))


def load_all():
    idx = json.loads((NETDIR / "index.json").read_text())
    return [(e, Net.load(NETDIR / (e["name"] + ".npz"))) for e in idx]


# ---------------------------------------------------------------- training
def _act_fd(act, z):
    if act == "tanh":
        f = np.tanh(z)
        return f, 1 - f * f
    if act == "sigmoid":
        s = sigmoid(z)
        return s, s * (1 - s)
    if act == "silu":
        s = sigmoid(z)
        return z * s, s + z * s * (1 - s)
    if act == "gelu":
        Phi = 0.5 * (1 + erf(z / math.sqrt(2)))
        return z * Phi, Phi + z * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    if act == "sin":
        return np.sin(z), np.cos(z)
    raise ValueError(act)


def train(cfg, epochs=4000, ntrain=4096, nval=2048):
    rng = np.random.default_rng(cfg["seed"])
    d, hid, act = cfg["d"], cfg["hidden"], cfg["act"]
    X = rng.uniform(-1, 1, (ntrain, d))
    Xv = rng.uniform(-1, 1, (nval, d))
    f = TARGETS[cfg["target"]]
    Y, Yv = f(X), f(Xv)
    mu, sd = Y.mean(), Y.std()
    Y, Yv = (Y - mu) / sd, (Yv - mu) / sd
    sizes = [d] + hid
    P = []
    for i, (a, b) in enumerate(zip(sizes[:-1], sizes[1:])):
        if act == "sin":  # SIREN initialization with omega_0 folded into the weights
            r = SIREN_OMEGA0 / a if i == 0 else math.sqrt(6.0 / a)
        else:
            r = math.sqrt(6.0 / (a + b))
        P += [rng.uniform(-r, r, (b, a)), np.zeros(b)]
    r = math.sqrt(6.0 / (hid[-1] + 1))
    P += [rng.uniform(-r, r, hid[-1]), np.zeros(1)]
    m = [np.zeros_like(p) for p in P]
    v = [np.zeros_like(p) for p in P]
    b1, b2, eps = 0.9, 0.999, 1e-8
    L = len(hid)
    for ep in range(1, epochs + 1):
        lr = 3e-4 + 0.5 * (3e-3 - 3e-4) * (1 + math.cos(math.pi * ep / epochs))
        hs, ds = [X], []
        for i in range(L):
            fz, dz = _act_fd(act, hs[-1] @ P[2 * i].T + P[2 * i + 1])
            hs.append(fz)
            ds.append(dz)
        out = hs[-1] @ P[2 * L] + P[2 * L + 1][0]
        err = out - Y
        g_out = 2 * err / ntrain
        grads = [None] * len(P)
        grads[2 * L] = hs[-1].T @ g_out
        grads[2 * L + 1] = np.array([g_out.sum()])
        g = np.outer(g_out, P[2 * L])
        for i in reversed(range(L)):
            gz = g * ds[i]
            grads[2 * i] = gz.T @ hs[i]
            grads[2 * i + 1] = gz.sum(0)
            g = gz @ P[2 * i]
        for k in range(len(P)):
            m[k] = b1 * m[k] + (1 - b1) * grads[k]
            v[k] = b2 * v[k] + (1 - b2) * grads[k] ** 2
            P[k] -= lr * (m[k] / (1 - b1 ** ep)) / (np.sqrt(v[k] / (1 - b2 ** ep)) + eps)
    net = Net(act, [P[2 * i] for i in range(L)], [P[2 * i + 1] for i in range(L)], P[2 * L], P[2 * L + 1][0],
              -np.ones(d), np.ones(d))
    rmse = float(np.sqrt(np.mean((net.forward(X) - Y) ** 2)))
    rmse_v = float(np.sqrt(np.mean((net.forward(Xv) - Yv) ** 2)))
    meta = dict(cfg, epochs=epochs, ntrain=ntrain, train_rmse=rmse, val_rmse=rmse_v, target_mean=float(mu),
                target_sd=float(sd), siren_omega0=SIREN_OMEGA0 if act == "sin" else None)
    net.meta = meta
    return net


def _job(cfg):
    t0 = time.time()
    net = train(cfg)
    net.save(NETDIR / (cfg["name"] + ".npz"))
    net.meta["train_seconds"] = time.time() - t0
    return net.meta


if __name__ == "__main__":
    NETDIR.mkdir(exist_ok=True)
    cfgs = configs()
    with Pool(min(len(cfgs), int(sys.argv[1]) if len(sys.argv) > 1 else 20)) as pool:
        metas = pool.map(_job, cfgs)
    (NETDIR / "index.json").write_text(json.dumps(metas, indent=1))
    for mt in metas:
        print("%-40s val_rmse=%.4f train_rmse=%.4f %.0fs" % (mt["name"], mt["val_rmse"], mt["train_rmse"], mt["train_seconds"]))
