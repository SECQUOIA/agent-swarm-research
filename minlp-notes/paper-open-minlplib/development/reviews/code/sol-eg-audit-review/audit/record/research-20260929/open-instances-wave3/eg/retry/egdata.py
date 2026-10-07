"""Shared data for the eg_* retry: exact decoding (via ../eg_model.py, which asserts the
row structure) packed into arrays, plus a float evaluator for exploration.

All four Schoonen instances share one function of y = s * x (s_i in {1, 1/10}):
    row k:  g_k(x) = sum_m a_km exp( sum_i gamma_ki (mu_kmi + s_i x_i)^2 ) + sum_i l_ki x_i,
with gamma_ki common to all 97 terms of a row (asserted here).  Rows 0..23 read
objvar >= c_k + g_k(x); rows 24..27 are side rows  glo_k <= g_k(x) <= ghi_k
(the OSIL rows are lb <= -g_k <= ub).
"""
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import eg_model as em  # noqa: E402

NAMES = ("eg_int_s", "eg_disc_s", "eg_disc2_s", "eg_all_s")


class Data:
    def __init__(self, name):
        M = em.decode(name)
        self.M = M
        self.name = name
        rows = M["rows"]
        self.R = len(rows)
        self.Mt = len(rows[0]["terms"])
        self.d = len(M["dvars"])
        d, R, Mt = self.d, self.R, self.Mt
        assert all(len(r["terms"]) == Mt for r in rows)
        # exact data (Fractions)
        self.qa = [[t[0] for t in r["terms"]] for r in rows]
        self.qmu = [[[t[1][i][1] for i in range(d)] for t in r["terms"]] for r in rows]
        self.qga = []
        for r in rows:
            g = [r["terms"][0][1][i][2] for i in range(d)]
            assert all(t[1][i][2] == g[i] for t in r["terms"] for i in range(d))
            assert all(gi < 0 for gi in g)
            self.qga.append(g)
        self.qs = list(M["scale"])
        self.qlin = [[r["linin"].get(i, Fr(0)) for i in range(d)] for r in rows]
        self.objrows = np.array([r["obj"] for r in rows])
        assert self.objrows[:24].all() and not self.objrows[24:].any() and R == 28
        self.qc = [r["lb"] if r["obj"] else None for r in rows]
        # side rows: lb <= -g <= ub  <=>  -ub <= g <= -lb
        self.qglo = [(-r["ub"] if r["ub"] is not None else None) if not r["obj"] else None for r in rows]
        self.qghi = [(-r["lb"] if r["lb"] is not None else None) if not r["obj"] else None for r in rows]
        self.qlb = list(M["lb"])
        self.qub = list(M["ub"])
        self.isint = np.array(M["isint"])
        # float copies (exploration only)
        self.a = np.array([[float(v) for v in r] for r in self.qa])
        self.mu = np.array([[[float(v) for v in t] for t in r] for r in self.qmu])
        self.ga = np.array([[float(v) for v in r] for r in self.qga])
        self.s = np.array([float(v) for v in self.qs])
        self.lin = np.array([[float(v) for v in r] for r in self.qlin])
        self.c = np.array([float(v) if v is not None else 0.0 for v in self.qc])
        self.glo = np.array([float(v) if v is not None else -np.inf for v in self.qglo])
        self.ghi = np.array([float(v) if v is not None else np.inf for v in self.qghi])
        self.lb = np.array([float(v) for v in self.qlb])
        self.ub = np.array([float(v) for v in self.qub])

    # ---------------- float evaluation (exploration, not rigorous)
    def g(self, x):
        """g_k(x) for x (N, d) -> (N, R); gradient (N, R, d)."""
        x = np.atleast_2d(x)
        t = self.mu[None] + (self.s * x)[:, None, None, :]          # (N, R, M, d)
        E = (self.ga[None, :, None, :] * t * t).sum(-1)              # (N, R, M)
        W = self.a[None] * np.exp(E)
        g = W.sum(-1) + x @ self.lin.T
        dE = 2 * self.ga[None, :, None, :] * t * self.s              # (N, R, M, d)
        G = (W[..., None] * dE).sum(2) + self.lin[None]
        return g, G

    def F(self, x):
        g, _ = self.g(x)
        f = (self.c[None, :24] + g[:, :24]).max(1)
        viol = np.maximum(self.glo[None, 24:] - g[:, 24:], g[:, 24:] - self.ghi[None, 24:]).max(1)
        return f, viol, g
