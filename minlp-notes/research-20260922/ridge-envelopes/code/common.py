"""Shared numerical helpers: Gurobi LP environment and robust 1-D maximization."""
import math

import gurobipy as gp
import numpy as np

_ENV = None


def gurobi_model():
    global _ENV
    if _ENV is None:
        _ENV = gp.Env(empty=True)
        _ENV.setParam("OutputFlag", 0)
        _ENV.start()
    m = gp.Model(env=_ENV)
    m.Params.FeasibilityTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    m.Params.Threads = 1
    return m


_GR = (math.sqrt(5.0) - 1.0) / 2.0


def golden_max(fun, lo, hi, iters=90):
    """Vectorized golden-section maximization of fun on brackets [lo_i, hi_i].

    fun(s, idx) evaluates the i-th objective at points s for bracket indices idx.
    Returns (argmax, max) per bracket, taking the endpoints into account.
    """
    a = np.array(lo, float)
    b = np.array(hi, float)
    idx = np.arange(len(a))
    c = b - _GR * (b - a)
    d = a + _GR * (b - a)
    fc, fd = fun(c, idx), fun(d, idx)
    for _ in range(iters):
        left = fc >= fd  # maximum lies in [a, d]
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        nc = b - _GR * (b - a)
        nd = a + _GR * (b - a)
        # reuse one of the previous evaluations
        new_c = np.where(left, nc, d)
        new_d = np.where(left, c, nd)
        fnew = fun(np.where(left, nc, nd), idx)
        fc, fd = np.where(left, fnew, fd), np.where(left, fc, fnew)
        c, d = new_c, new_d
    cand_s = np.stack([np.array(lo, float), np.array(hi, float), c, d])
    cand_v = np.stack([fun(cand_s[0], idx), fun(cand_s[1], idx), fc, fd])
    j = np.argmax(cand_v, axis=0)
    return cand_s[j, idx], cand_v[j, idx]


def local_maxima_rows(vals):
    """Boolean mask of (weak) local maxima along the last axis, endpoints included."""
    left = np.concatenate([np.full(vals.shape[:-1] + (1,), -np.inf), vals[..., :-1]], axis=-1)
    right = np.concatenate([vals[..., 1:], np.full(vals.shape[:-1] + (1,), -np.inf)], axis=-1)
    return (vals >= left) & (vals >= right)


def maximize_rows(fun, grid, topk=4):
    """Maximize row-wise 1-D functions sampled on per-row grids.

    grid: array (R, G) of increasing points per row. fun(s, rows) evaluates row
    functions at points s for row indices rows (same shape).
    Returns list over rows of arrays [(s, value), ...] of refined local maxima,
    sorted by value (at most topk per row).
    """
    R, G = grid.shape
    rows = np.repeat(np.arange(R)[:, None], G, axis=1)
    vals = fun(grid, rows)
    mask = local_maxima_rows(vals)
    out = []
    lo_list, hi_list, row_list = [], [], []
    for r in range(R):
        idx = np.nonzero(mask[r])[0]
        idx = idx[np.argsort(-vals[r, idx])][:topk]
        for i in idx:
            lo_list.append(grid[r, max(i - 1, 0)])
            hi_list.append(grid[r, min(i + 1, G - 1)])
            row_list.append(r)
    row_arr = np.array(row_list, int)
    s, v = golden_max(lambda s, k: fun(s, row_arr[k]), np.array(lo_list), np.array(hi_list))
    for r in range(R):
        sel = row_arr == r
        o = np.argsort(-v[sel])
        out.append(np.stack([s[sel][o], v[sel][o]], axis=1))
    return out
