"""optcdeg2: Lagrangian bound strengthened by branching on the separator v at block
boundaries and dynamic programming over the cells (the program's decomposition scheme).

Same multipliers (mu, lam) and the same separable Lagrangian as optcdeg2_bound.py. The
only change is how the v_t-terms  A_t v_t^2 + B_t v_t  (A_t = 0.2 h lam_t,
B_t = lam_{t-1} - lam_t - h mu_t) are bounded in two segments where lam_t < 0
(the terms are concave there):
  - boundary times T_0 < T_1 < ... < T_K split a segment into blocks of L steps;
  - at each boundary the global interval of v_{T_k} is split into cells;
  - for a cell pair (i at T_{k-1}, j at T_k), interior v_t (T_{k-1} < t < T_k) must lie in
    the forward reachable interval from cell i intersected with the backward reachable
    interval from cell j (interval propagation of the exact dynamics, with the global
    y bounds and u in [-0.2, 0.2]);
  - B_k(i, j) = sum of rigorous lower bounds of the v-terms of the block over these
    intervals (term at T_{k-1} over cell i); an empty interval means no trajectory.
  - DP: D_k(j) = min_i D_{k-1}(i) + B_k(i, j).
Every feasible trajectory selects one cell per boundary, so its Lagrangian value is at
least the DP value plus the other (unchanged) separable terms. All arithmetic is
outward-rounded interval arithmetic (ivnp.py).
"""
import json
import sys
import time

import numpy as np

import ivnp as I
from optcdeg2_common import N, load_minlplib

H = I.const("0.0004")
C02H = I.mul(I.const("0.02"), H)          # 0.02 h
C02h2 = I.mul(I.const("0.2"), H)          # 0.2 h
U = (I.dn(np.float64(-0.2)), I.up(np.float64(0.2)))  # encloses the decimal bounds [-0.2, 0.2]


def load_bounds():
    vb = np.load("logs/optcdeg2_vbounds.npy")
    yb = np.load("logs/optcdeg2_ybounds.npy")
    # the saved floats are nearest roundings of rigorous mpmath endpoints: widen by one ulp
    return (I.dn(vb[:, 0]), I.up(vb[:, 1])), (I.dn(yb[:, 0]), I.up(yb[:, 1]))


def coeffs(mu, lam):
    """Interval coefficients A_t, B_t of the v_t-terms (index t = 0..N-1; t = 0 unused)."""
    Lm = I.point(lam)
    A = I.mul(C02h2, Lm)
    Bv = I.sub(I.sub(I.point(np.concatenate([[0.0], lam[:-1]])), Lm), I.mul(H, I.point(mu)))
    return A, Bv


def g_fwd(vlo, vhi):
    """g(v) = v - 0.2 h v^2 is increasing for v < 6250: image of [vlo, vhi]."""
    assert np.all(vhi < 6000)
    glo = I.sub(I.point(vlo), I.mul(C02h2, I.sqr(I.point(vlo))))[0]
    ghi = I.sub(I.point(vhi), I.mul(C02h2, I.sqr(I.point(vhi))))[1]
    return glo, ghi


def g_inv(z):
    """Enclosure of g^{-1}(z) = (1 - sqrt(1 - 0.8 h z)) / (0.4 h) on the increasing branch."""
    c08h = I.mul(I.const("0.8"), H)
    c04h = I.mul(I.const("0.4"), H)
    s = I.sqrt(I.sub(I.point(np.ones_like(z[0])), I.mul(c08h, z)))
    return I.div_pos(I.sub(I.point(np.ones_like(z[0])), s), c04h)


def block_bound(t0, L, cells_in, cells_out, Vg, Yg, A, Bv):
    """Lower bounds B(i, j) for the block with terms t = t0 .. t0+L-1 and boundary
    v_{t0} in cells_in[i], v_{t0+L} in cells_out[j]. Returns array (ni, nj) (inf = infeasible)."""
    ni, nj = len(cells_in[0]), len(cells_out[0])
    # forward reachable intervals for t = t0 .. t0+L (per start cell)
    flo = np.empty((L + 1, ni)); fhi = np.empty((L + 1, ni))
    flo[0], fhi[0] = np.maximum(cells_in[0], Vg[0][t0]), np.minimum(cells_in[1], Vg[1][t0])
    for s in range(L):
        t = t0 + s
        glo, ghi = g_fwd(flo[s], fhi[s])
        nxt = I.sub(I.add((glo, ghi), I.mul(H, (np.full(ni, U[0]), np.full(ni, U[1])))),
                    I.mul(C02H, (np.full(ni, Yg[0][t]), np.full(ni, Yg[1][t]))))
        flo[s + 1] = np.maximum(nxt[0], Vg[0][t + 1]); fhi[s + 1] = np.minimum(nxt[1], Vg[1][t + 1])
    # backward intervals for t = t0+L down to t0 (per end cell)
    blo = np.empty((L + 1, nj)); bhi = np.empty((L + 1, nj))
    blo[L], bhi[L] = np.maximum(cells_out[0], Vg[0][t0 + L]), np.minimum(cells_out[1], Vg[1][t0 + L])
    for s in range(L - 1, -1, -1):
        t = t0 + s
        # g(v_t) = v_{t+1} - h u_t + 0.02 h y_t
        z = I.add(I.sub((blo[s + 1], bhi[s + 1]), I.mul(H, (np.full(nj, U[0]), np.full(nj, U[1])))),
                  I.mul(C02H, (np.full(nj, Yg[0][t]), np.full(nj, Yg[1][t]))))
        ok = bhi[s + 1] >= blo[s + 1]
        zlo = np.where(ok, z[0], 0.0); zhi = np.where(ok, z[1], 0.0)
        v = g_inv((zlo, zhi))
        blo[s] = np.where(ok, np.maximum(v[0], Vg[0][t]), 1.0)
        bhi[s] = np.where(ok, np.minimum(v[1], Vg[1][t]), 0.0)
    Bsum = np.zeros((ni, nj))
    feas = np.ones((ni, nj), dtype=bool)
    for s in range(L):
        t = t0 + s
        lo = np.maximum(flo[s][:, None], blo[s][None, :])
        hi = np.minimum(fhi[s][:, None], bhi[s][None, :])
        feas &= lo <= hi
        if t == 0:
            continue  # v_0 fixed, no term
        lo2, hi2 = np.where(feas, lo, 0.0), np.where(feas, hi, 0.0)
        term = I.quad_min_lo((np.float64(A[0][t]), np.float64(A[1][t])), (np.float64(Bv[0][t]), np.float64(Bv[1][t])), lo2, hi2)
        Bsum = I.dn(Bsum + term)
    lo = np.maximum(flo[L][:, None], blo[L][None, :]); hi = np.minimum(fhi[L][:, None], bhi[L][None, :])
    feas &= lo <= hi
    return np.where(feas, Bsum, np.inf)


def make_cells(lo, hi, n):
    e = np.linspace(lo, hi, n + 1)
    e[0], e[-1] = lo, hi
    return (e[:-1].copy(), e[1:].copy())


def segment_dp(tstart, tend, L, ncell, start_fixed, end_fixed, Vg, Yg, A, Bv):
    """DP over boundaries tstart, tstart+L, ..., tend. Terms t in [tstart, tend) are included,
    plus the term at tend (over its cell) unless end_fixed."""
    assert (tend - tstart) % L == 0
    bounds = list(range(tstart, tend + 1, L))
    def cells_at(t, fixed):
        if fixed:
            return (np.array([0.0]), np.array([0.0]))
        return make_cells(Vg[0][t], Vg[1][t], ncell)
    cells = [cells_at(t, (t == tstart and start_fixed) or (t == tend and end_fixed)) for t in bounds]
    D = np.zeros(len(cells[0][0]))
    for k in range(1, len(bounds)):
        Bk = block_bound(bounds[k - 1], L, cells[k - 1], cells[k], Vg, Yg, A, Bv)
        D = I.dn(np.min(D[:, None] + Bk, axis=0))
    if not end_fixed:
        t = tend
        term = I.quad_min_lo((np.float64(A[0][t]), np.float64(A[1][t])), (np.float64(Bv[0][t]), np.float64(Bv[1][t])),
                             np.maximum(cells[-1][0], Vg[0][t]), np.minimum(cells[-1][1], Vg[1][t]))
        D = I.dn(D + term)
    return float(np.min(D))


def other_terms(mu, lam, Vg, skip):
    """Rigorous lower bound of all separable terms except the v-terms with t in skip."""
    lo_total = []
    h = H
    M, Lm = I.point(mu), I.point(lam)
    # constants from y_0 = 10: h/2*100 - 10 mu_0 + 0.02 h lam_0 * 10
    c = I.add(I.sub(I.mul(I.mul(h, I.const(50.0)), I.point(np.array([1.0]))), I.mul(I.const(10.0), I.point(mu[:1]))),
              I.mul(I.mul(C02H, I.const(10.0)), I.point(lam[:1])))
    lo_total.append(c[0])
    # y_t, t = 1..N-1: -(b_t)^2/(2h), b_t = mu_{t-1} - mu_t + 0.02 h lam_t
    b = I.add(I.sub(I.point(mu[:-1]), I.point(mu[1:])), I.mul(C02H, I.point(lam[1:])))
    ty = I.neg(I.div_pos(I.sqr(b), I.mul(I.const(2.0), h)))
    lo_total.append(ty[0])
    # y_N: -mu_{N-1}^2/(2h)
    tN = I.neg(I.div_pos(I.sqr(I.point(mu[-1:])), I.mul(I.const(2.0), h)))
    lo_total.append(tN[0])
    # u_t: -0.2 h |lam_t|
    tu = I.neg(I.mul(I.mul(I.const("0.2"), h), I.absval(Lm)))
    lo_total.append(tu[0])
    # v_t with global bounds, t = 1..N-1 not in skip
    A, Bv = coeffs(mu, lam)
    ts = np.array([t for t in range(1, N) if t not in skip])
    tv = I.quad_min_lo((A[0][ts], A[1][ts]), (Bv[0][ts], Bv[1][ts]), Vg[0][ts], Vg[1][ts])
    lo_total.append(tv)
    s = np.float64(0.0)
    for arr in lo_total:
        s = I.dn(s + I.sum_lo(arr))
    return float(s)


def main(L=128, ncell=100, head_end=3200, tail_start=47184):
    t0 = time.time()
    u, y, v = load_minlplib()
    mu, lam = np.load("logs/optcdeg2_mu.npy"), np.load("logs/optcdeg2_lam.npy")
    Vg, Yg = load_bounds()
    A, Bv = coeffs(mu, lam)
    head = segment_dp(0, head_end, L, ncell, True, False, Vg, Yg, A, Bv)
    tail = segment_dp(tail_start, N, L, ncell, False, True, Vg, Yg, A, Bv)
    skip = set(range(1, head_end + 1)) | set(range(tail_start, N))
    rest = other_terms(mu, lam, Vg, skip)
    # plain (no cells) value of the same v-terms for comparison
    ts = np.array(sorted(skip))
    plain = float(I.sum_lo(I.quad_min_lo((A[0][ts], A[1][ts]), (Bv[0][ts], Bv[1][ts]), Vg[0][ts], Vg[1][ts])))
    total = float(I.dn(I.dn(rest + head) + tail))
    rec = dict(L=L, ncell=ncell, head_end=head_end, tail_start=tail_start, head_dp=head, tail_dp=tail,
               head_tail_plain=plain, rest=rest, dual_bound=total, dual_bound_plain=float(I.dn(rest + plain)),
               seconds=time.time() - t0)
    print(json.dumps(rec), flush=True)
    return rec


if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    nc = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rec = main(L, nc)
    with open("logs/optcdeg2_blockdp.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
