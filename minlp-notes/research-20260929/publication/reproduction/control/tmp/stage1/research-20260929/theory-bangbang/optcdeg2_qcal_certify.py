"""optcdeg2: rigorous lower bound from a single quadratic-in-v discrete calibration (no windows).

Calibration (certificate data, any floats are valid):
  S_t(y, v) = py_t * y + pv_t * v + (q_t / 2) * (v - c_t)^2,     t = 1..N,
with (py, pv) the discrete costates of the KKT primal (optcdeg2_refine_primal.py), c_t its
velocities (c_N = 0), and q_t the tangential curvature schedule:
  q = 0 at the two switches and on the u = +0.2 arc; on the u = -0.2 arcs q grows so that the
  v-curvature of every stage residual is 2 * kappa * h (kappa = KH on the head, KT on the tail).

Bound (Lemma: telescoping, valid for every family S):
  f* >= min_u [L_0 + S_1(f_0(x_0, u))] + sum_{t=1}^{N-1} inf_{Omega_t} rho_t + inf_{v=0} [Phi - S_N],
  rho_t(y, v, u) = (h/2) y^2 + S_{t+1}(y + h v, v + h (u - 0.02 y - 0.2 v^2)) - S_t(y, v),
  Omega_t = R x V_t x [-0.2, 0.2], V_t = rigorous state bounds (open-instances/logs/optcdeg2_vbounds.npy).
Per stage: exact minimization over y (convex quadratic), then the residual is a polynomial
  rho~(v, u) = sum c_jk d^j D^k,  d = v - v^h_t, D = u - u^h_t (j <= 4, k <= 2),
whose coefficients are enclosed with outward-rounded interval arithmetic (ivnp); its infimum
over d in V_t - v^h_t, D in U - u^h_t is bounded below on a geometric grid of d-cells with exact
handling of the (quadratic) D-dependence. Cells with a negative lower bound are bisected.
"""
import json
import math
import sys
import time

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
sys.path.insert(0, _REPO + "/research-20260929/open-instances")
import ivnp as I  # noqa: E402

OI = _REPO + "/research-20260929/open-instances/"
N = 50000
hf = 4e-4
H = I.const("0.0004")
AY = I.mul(I.const("0.02"), H)          # 0.02 h
C02H = I.mul(I.const("0.2"), H)         # 0.2 h
C04H = I.mul(I.const("0.4"), H)         # 0.4 h
ULO, UHI = I.dn(np.float64(-0.2)), I.up(np.float64(0.2))   # encloses the decimal box [-.2, .2]


def pt(x):
    return I.point(np.asarray(x, dtype=np.float64))


def lo_(a):
    return a[0]


# ---------------------------------------------------------------- certificate data (float)
def certificate_data(ufile, KH, KT):
    u = np.load(ufile)
    y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
    for t in range(N):
        y[t + 1] = y[t] + hf * v[t]
        v[t + 1] = v[t] + hf * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
    v[N] = 0.0
    k = np.where(np.abs(np.abs(u) - 0.2) > 1e-12)[0]
    s1, s2 = int(k[0]), int(k[1])

    def adj(nu):
        py = np.empty(N + 1); pv = np.empty(N + 1)
        py[N] = hf * y[N]; pv[N] = nu
        for t in range(N - 1, -1, -1):
            py[t] = hf * y[t] + py[t + 1] - 0.02 * hf * pv[t + 1]
            pv[t] = hf * py[t + 1] + (1 - 0.4 * hf * v[t]) * pv[t + 1]
        return py, pv
    a0, a1 = adj(0.0)[1], adj(1.0)[1]
    nu = -a0[s2 + 1] / (a1[s2 + 1] - a0[s2 + 1])
    py, pv = adj(nu)
    q = np.zeros(N + 1)
    for t in range(s1 - 1, -1, -1):
        q[t] = q[t + 1] * (1 - 0.4 * hf * v[t]) ** 2 - 0.4 * hf * pv[t + 1] - 2 * KH * hf
    for t in range(s2 + 1, N):
        q[t + 1] = (q[t] + 0.4 * hf * pv[t + 1] + 2 * KT * hf) / (1 - 0.4 * hf * v[t]) ** 2
    return dict(u=u, y=y, v=v, py=py, pv=pv, q=q, c=v.copy(), s1=s1, s2=s2, nu=nu)


# ---------------------------------------------------------------- bivariate interval polynomials
def padd(P, Q):
    R = dict(P)
    for k, val in Q.items():
        R[k] = I.add(R[k], val) if k in R else val
    return R


def pscale(P, s):
    return {k: I.mul(val, s) for k, val in P.items()}


def pmul(P, Q):
    R = {}
    for (a, b), x in P.items():
        for (c, d), z in Q.items():
            k = (a + c, b + d)
            m = I.mul(x, z)
            R[k] = I.add(R[k], m) if k in R else m
    return R


def stage_poly(t, D):
    """Interval coefficients of rho~_t(v^h_t + d, u^h_t + D), for an array of stages t (1..N-1)."""
    P1y, P1v, Q1, vh1 = pt(D["py"][t + 1]), pt(D["pv"][t + 1]), pt(D["q"][t + 1]), pt(D["c"][t + 1])
    P0y, P0v, Q0, vh0 = pt(D["py"][t]), pt(D["pv"][t]), pt(D["q"][t]), pt(D["c"][t])
    vs, us = pt(D["v"][t]), pt(D["u"][t])
    one = pt(np.ones(len(t)))
    A2 = I.add(I.mul(I.const(0.5), H), I.mul(I.mul(I.const(0.5), Q1), I.sqr(AY)))
    assert np.all(A2[0] > 0)
    B0 = I.sub(I.sub(P1y, P0y), I.mul(AY, P1v))
    K2 = I.div_pos(I.mul(Q1, H), I.mul(I.const(4.0), A2))
    K1 = I.div_pos(I.mul(I.mul(AY, Q1), B0), I.mul(I.const(2.0), A2))
    K0 = I.neg(I.div_pos(I.sqr(B0), I.mul(I.const(4.0), A2)))
    e0 = I.sub(I.sub(I.add(vs, I.mul(H, us)), I.mul(C02H, I.sqr(vs))), vh1)
    e = {(0, 0): e0, (1, 0): I.sub(one, I.mul(C04H, vs)), (2, 0): I.neg(I.mul(C02H, one)),
         (0, 1): I.mul(H, one)}
    rho = pscale(pmul(e, e), K2)
    rho = padd(rho, pscale(e, I.add(K1, P1v)))
    rho = padd(rho, {(0, 0): I.add(K0, I.mul(P1v, vh1))})
    lin = I.sub(I.mul(P1y, H), P0v)
    rho = padd(rho, {(0, 0): I.mul(lin, vs), (1, 0): lin})
    sh = {(0, 0): I.sub(vs, vh0), (1, 0): one}
    rho = padd(rho, pscale(pmul(sh, sh), I.neg(I.mul(I.const(0.5), Q0))))
    # Better-conditioned enclosures of the same two coefficients (identical real numbers,
    # re-associated so that the large costate terms cancel before rounding):
    #   P1v (e0 + vh1) + lin vs = vs (P1v - P0v) + h vs P1y + h P1v us - 0.2 h P1v vs^2,
    #   P1v e_d + lin           = (P1v - P0v) + h P1y - 0.4 h vs P1v.
    dPv = I.sub(P1v, P0v)
    big0 = I.add(I.add(I.mul(vs, dPv), I.mul(I.mul(H, vs), P1y)),
                 I.sub(I.mul(I.mul(H, P1v), us), I.mul(I.mul(C02H, P1v), I.sqr(vs))))
    shq = I.mul(I.neg(I.mul(I.const(0.5), Q0)), I.sqr(I.sub(vs, vh0)))
    c00 = I.add(I.add(I.add(I.mul(K2, I.sqr(e0)), I.mul(K1, e0)), K0), I.add(big0, shq))
    ed = e[(1, 0)]
    big1 = I.add(dPv, I.sub(I.mul(H, P1y), I.mul(I.mul(C04H, vs), P1v)))
    c10 = I.add(I.add(I.mul(I.mul(I.const(2.0), K2), I.mul(e0, ed)), I.mul(K1, ed)),
                I.sub(big1, I.mul(Q0, I.sub(vs, vh0))))
    # keep the intersection of the two enclosures (both are rigorous)
    for key, alt in (((0, 0), c00), ((1, 0), c10)):
        lo = np.maximum(rho[key][0], alt[0]); hi = np.minimum(rho[key][1], alt[1])
        assert np.all(lo <= hi)
        rho[key] = (lo, hi)
    return rho


def dmin_lower(Blo, Bhi, Clo, dl, du):
    """Rigorous lower bound of min_{D in [dl, du]} (B D + C D^2) for B in [Blo, Bhi], C >= Clo."""
    out = np.full(np.broadcast(Blo, dl).shape, np.inf)
    for side in (+1, -1):
        if side > 0:
            a, b = np.maximum(dl, 0.0), du
            B = Blo
        else:
            a, b = dl, np.minimum(du, 0.0)
            B = Bhi
        ok = a <= b
        fa = I.add(I.mul(pt(B), pt(a)), I.mul(pt(Clo), I.sqr(pt(a))))[0]
        fb = I.add(I.mul(pt(B), pt(b)), I.mul(pt(Clo), I.sqr(pt(b))))[0]
        m = np.minimum(fa, fb)
        conv = Clo > 0
        with np.errstate(divide="ignore", invalid="ignore"):
            st = np.where(conv, -B / (2 * np.where(conv, Clo, 1.0)), np.nan)
            st_in = conv & (st >= a - 1e-12 * (1 + np.abs(a))) & (st <= b + 1e-12 * (1 + np.abs(b)))
            den = 4 * np.where(conv, Clo, 1.0)            # exact (power-of-two scaling), > 0 where used
            sv = -I.up(I.up(B * B) / den)                  # lower bound of -B^2 / (4 Clo)
        m = np.where(st_in, np.minimum(m, sv), m)
        out = np.where(ok, np.minimum(out, m), out)
    return out


def cell_lower(P, dlo, dhi, Dl, Du):
    """Lower bound of g(d, D) = rho~ - c00 over the cells [dlo, dhi] x [Dl, Du] (arrays (n, m))."""
    Dc = (dlo, dhi)
    D2 = I.sqr(Dc)
    D3 = I.mul(Dc, D2)
    D4 = I.sqr(D2)
    pw = {1: Dc, 2: D2, 3: D3, 4: D4}

    def col(k):
        return (P[k][0][:, None], P[k][1][:, None])
    a = (np.zeros_like(dlo), np.zeros_like(dlo))
    for j in range(1, 5):
        if (j, 0) in P:
            a = I.add(a, I.mul(col((j, 0)), pw[j]))
    b = col((0, 1))
    if (1, 1) in P:
        b = I.add(b, I.mul(col((1, 1)), Dc))
    if (2, 1) in P:
        b = I.add(b, I.mul(col((2, 1)), D2))
    C = col((0, 2))
    phi = dmin_lower(b[0], b[1], C[0], Dl[:, None], Du[:, None])
    return I.dn(a[0] + phi)


def template(d0=1e-7, r=1.25, dmax=4.0):
    k = int(np.ceil(np.log(dmax / d0) / np.log(r)))
    pos = d0 * r ** np.arange(k + 1)
    return np.concatenate([[-1e300], -pos[::-1], [0.0], pos, [1e300]])


def stage_bounds(D, Vb, ts, refine_rounds=12, tol=1e-16):
    tb = template()
    LB = np.empty(len(ts)); C00 = np.empty(len(ts)); info = dict(refined_cells=0, bad_cells_final=0)
    chunk = 2500
    for c0 in range(0, len(ts), chunk):
        t = ts[c0:c0 + chunk]
        P = stage_poly(t, D)
        vs = D["v"][t]
        dl = I.dn(Vb[0][t] - vs); du = I.up(Vb[1][t] - vs)
        Dl = I.dn(ULO - D["u"][t]); Du = I.up(UHI - D["u"][t])
        cells = np.clip(tb[None, :], dl[:, None], du[:, None])
        lo_c, hi_c = cells[:, :-1], cells[:, 1:]
        L = cell_lower(P, lo_c, hi_c, Dl, Du)
        m = L.min(axis=1)
        # refine stages whose minimum cell bound is negative
        bad = np.where(m < -tol)[0]
        for rnd in range(refine_rounds):
            if len(bad) == 0:
                break
            newm = m.copy()
            for i in bad:
                Pi = {k: (val[0][i:i + 1], val[1][i:i + 1]) for k, val in P.items()}
                sel = L[i] < -tol
                los, his = lo_c[i][sel], hi_c[i][sel]
                ok_part = L[i][~sel].min() if (~sel).any() else np.inf
                for _ in range(rnd + 1):
                    mid = 0.5 * (los + his)
                    los, his = np.concatenate([los, mid]), np.concatenate([mid, his])
                Li = cell_lower(Pi, los[None, :], his[None, :], Dl[i:i + 1], Du[i:i + 1])[0]
                info["refined_cells"] += len(los)
                newm[i] = min(ok_part, Li.min())
            m = newm
            bad = np.where(m < -tol)[0]
        info["bad_cells_final"] += int(len(bad))
        c00 = P[(0, 0)]
        LB[c0:c0 + chunk] = I.dn(c00[0] + m)
        C00[c0:c0 + chunk] = c00[1]
    return LB, C00, info


def stage0(D):
    """min over u in U of L_0 + S_1(f_0(x_0, u)), x_0 = (10, 0): y_1 = 10, v_1 = h (u - 0.2) exactly."""
    P1y, P1v, Q1, c1 = [pt(np.array([D[k][1]])) for k in ("py", "pv", "q", "c")]
    us = D["u"][0]
    ten = I.const(10.0)
    base = I.add(I.mul(I.mul(I.const(0.5), H), I.const(100.0)), I.mul(P1y, ten))
    # v_1 = h (us + D) - 0.02 h 10 = h us - 0.2 h + h D
    v1s = I.sub(I.mul(H, pt(np.array([us]))), I.mul(AY, ten))
    e0 = I.sub(v1s, c1)
    c00 = I.add(base, I.add(I.mul(P1v, v1s), I.mul(I.mul(I.const(0.5), Q1), I.sqr(e0))))
    c01 = I.add(I.mul(P1v, H), I.mul(I.mul(Q1, e0), H))
    c02 = I.mul(I.mul(I.const(0.5), Q1), I.sqr(H))
    Dl = I.dn(ULO - us); Du = I.up(UHI - us)
    phi = dmin_lower(c01[0], c01[1], c02[0], np.array([Dl]), np.array([Du]))
    return float(I.dn(c00[0][0] + phi[0])), float(c00[1][0])


def terminal(D):
    """inf over y of (h/2) y^2 - S_N(y, 0), with c_N = 0: = -py_N^2 / (2h)."""
    assert D["c"][N] == 0.0
    PNy = pt(np.array([D["py"][N]]))
    val = I.neg(I.div_pos(I.sqr(PNy), I.mul(I.const(2.0), H)))
    return float(val[0][0]), float(val[1][0])


def main():
    KH, KT = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0, float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
    ufile = sys.argv[3] if len(sys.argv) > 3 else "logs/optcdeg2_kkt_u.npy"
    t0 = time.time()
    D = certificate_data(ufile, KH, KT)
    np.savez("logs/optcdeg2_qcal_data.npz", py=D["py"], pv=D["pv"], q=D["q"], c=D["c"], u=D["u"], v=D["v"])
    vb = np.load(OI + "logs/optcdeg2_vbounds.npy")
    Vb = (I.dn(vb[:, 0]), I.up(vb[:, 1]))
    ts = np.arange(1, N)
    LB, C00, info = stage_bounds(D, Vb, ts)
    s0_lo, s0_hi = stage0(D)
    te_lo, te_hi = terminal(D)
    # math.fsum returns the correctly rounded exact sum of the float lower ends; one step down
    # gives a rigorous lower bound (sequential rounding would cost about N ulps of 1e3).
    total = I.dn(np.float64(math.fsum(np.concatenate([[s0_lo], LB, [te_lo]]).tolist())))
    upper_at_traj = float(np.sum(C00) + s0_hi + te_hi)     # float value of B at the trajectory (sanity: ~ J)
    loss = C00 - LB
    J = hf / 2 * np.sum(D["y"] ** 2)
    rec = dict(KH=KH, KT=KT, s1=D["s1"], s2=D["s2"], nu=D["nu"], q0=D["q"][0], qN=D["q"][N],
               certified_bound=float(total), sum_at_trajectory=upper_at_traj, J_float=J,
               stage0=[s0_lo, s0_hi], terminal=[te_lo, te_hi],
               loss_total=float(loss.sum()), loss_head=float(loss[ts <= D["s1"]].sum()),
               loss_mid=float(loss[(ts > D["s1"]) & (ts <= D["s2"])].sum()), loss_tail=float(loss[ts > D["s2"]].sum()),
               worst_stage=int(ts[np.argmax(loss)]), worst_loss=float(loss.max()),
               seconds=time.time() - t0, **info)
    print(json.dumps(rec), flush=True)
    np.save("logs/optcdeg2_qcal_stage_lb.npy", LB)
    with open("logs/optcdeg2_qcal_certify.json", "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main()
