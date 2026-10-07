"""Rigorous Lagrangian lower bound for the power-flow instances.

For multipliers w (free on equality rows, w = m+ - m- with m+/- >= 0 on
inequality rows) and every point of the relaxation R (pf_model):
    obj(y) >= L = const(w) + sum_y (sigma_y y^2 + kappa_y y) + x^T A(w) x.
The bound is evaluated exactly (Fractions) except the psd test of A + eps I,
done by interval Cholesky with outward rounding (success implies every
symmetric matrix in the interval matrix is positive definite).  Then
    x^T A x >= -eps |x|^2 >= -eps * sum_k vmax_k^2
because every point of R satisfies e_k^2 + f_k^2 <= vmax_k^2.
Inner minima over y: closed form over the y box; for y without a box, sigma_y > 0
gives -kappa^2/(4 sigma); if sigma_y = 0 the multiplier of y's defining flow row
is adjusted (exactly) so that kappa_y = 0.

    python3 pf_cert.py <name>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
import time
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
from kan_iv import NI, dn, up, frac_iv  # noqa: E402
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
from ia import isqrt  # noqa: E402

import pf_model as pm  # noqa: E402
import pf_sdp as ps  # noqa: E402


def to_frac(v):
    return Fr(float(v))


def certify(M, raw, eps_list=None, log=print):
    rows = M["rows"]
    # multipliers as exact rationals
    w, const = [], M["obj"]["const"]
    for r, rv in zip(rows, raw):
        if rv[0] == "eq":
            m = to_frac(rv[1])
            w.append(m)
            const -= m * r["lb"]
        else:
            mp_ = to_frac(max(0.0, rv[1])) if rv[1] is not None else Fr(0)
            mm_ = to_frac(max(0.0, rv[2])) if rv[2] is not None else Fr(0)
            w.append(mp_ - mm_)
            if r["ub"] is not None:
                const -= mp_ * r["ub"]
            if r["lb"] is not None:
                const += mm_ * r["lb"]
    ys = M["ys"]
    kappa = {y: M["obj"]["lin"].get(y, Fr(0)) for y in ys}
    sigma = {y: M["obj"]["qy"].get(y, Fr(0)) for y in ys}
    defrow = {}
    for k, r in enumerate(rows):
        for y, c in r["lin"].items():
            kappa[y] += w[k] * c
        for y, c in r["qy"].items():
            sigma[y] += w[k] * c
        if r["kind"] == "flow":
            (y,) = r["lin"]
            assert r["lin"][y] == 1 and r["lb"] == r["ub"] == 0
            defrow[y] = k
    inner = Fr(0)
    nadj = 0
    for y in ys:
        s, kp = sigma[y], kappa[y]
        assert s >= 0
        box = M["ybox"].get(y)
        if box is not None:
            l, u = box
            assert l is not None and u is not None
            if s > 0:
                ystar = min(max(-kp / (2 * s), l), u)
                inner += s * ystar * ystar + kp * ystar
            else:
                inner += min(kp * l, kp * u)
        elif s > 0:
            inner += -kp * kp / (4 * s)
        else:
            k = defrow[y]
            w[k] -= kp            # makes kappa_y exactly 0 (coefficient of y in its row is 1)
            kappa[y] = Fr(0)
            nadj += 1
    # A(w) exact
    n2 = 2 * M["n"]
    A = {}
    for k, r in enumerate(rows):
        if w[k] == 0:
            continue
        for (i, j), c in r["Q"].items():
            A[(i, j)] = A.get((i, j), Fr(0)) + w[k] * c
    Alo = np.zeros((n2, n2)); Ahi = np.zeros((n2, n2))
    for (i, j), c in A.items():
        v = c if i == j else c / 2
        lo, hi = frac_iv(v)
        Alo[i, j] = Alo[j, i] = lo
        Ahi[i, j] = Ahi[j, i] = hi
    vm2 = sum(M["vmax2"])
    # smallest eps from the list with a successful interval Cholesky of A + eps I
    if eps_list is None:
        eps_list = [0.0] + [10.0 ** k for k in range(-14, 1)]
    for eps in eps_list:
        ok = interval_cholesky(Alo + eps * np.eye(n2), Ahi + eps * np.eye(n2))
        if ok:
            break
    else:
        return None
    epsF = Fr(eps)
    bound = const + inner - epsF * vm2
    log(f"  flows with kappa fixed to 0: {nadj}; eps = {eps:g}; const {float(const):.12f} inner {float(inner):.12f}")
    return bound, eps


def interval_cholesky(Alo, Ahi):
    """True if every symmetric matrix in [Alo, Ahi] is positive definite (vectorized rows)."""
    n = Alo.shape[0]
    Llo = np.zeros((n, n)); Lhi = np.zeros((n, n))
    for j in range(n):
        # s = A_jj - sum_k L_jk^2
        if j > 0:
            Ljk = NI(Llo[j, :j], Lhi[j, :j])
            sq = Ljk * Ljk
            sq = NI(np.maximum(sq.lo, 0.0), sq.hi)
            ssum = NI(dn(sq.lo.sum() - j * 1.2e-16 * np.abs(sq.lo).sum()), up(sq.hi.sum() + j * 1.2e-16 * np.abs(sq.hi).sum()))
        else:
            ssum = NI(0.0, 0.0)
        d = NI(Alo[j, j], Ahi[j, j]) - ssum
        if not d.lo > 0:
            return False
        Ljj = isqrt(d)
        Llo[j, j], Lhi[j, j] = float(Ljj.lo), float(Ljj.hi)
        if j + 1 < n:
            # L_ij for i > j:  (A_ij - sum_k L_ik L_jk) / L_jj
            Lik = NI(Llo[j + 1:, :j], Lhi[j + 1:, :j])
            Ljk = NI(Llo[j, :j][None, :], Lhi[j, :j][None, :])
            if j > 0:
                P = Lik * Ljk
                plo = P.lo.sum(axis=1); phi = P.hi.sum(axis=1)
                e_lo = j * 1.2e-16 * np.abs(P.lo).sum(axis=1)
                e_hi = j * 1.2e-16 * np.abs(P.hi).sum(axis=1)
                S = NI(dn(plo - e_lo - 1e-300), up(phi + e_hi + 1e-300))
            else:
                S = NI(np.zeros(n - j - 1), np.zeros(n - j - 1))
            col = (NI(Alo[j + 1:, j], Ahi[j + 1:, j]) - S) / Ljj
            Llo[j + 1:, j], Lhi[j + 1:, j] = col.lo, col.hi
    return True


def best_certificate(M, log=print):
    """solve the dual with all rows and with the angle rows dropped (zero multipliers);
    return the best rigorous bound."""
    import json
    best = None
    variants = [("all rows", M)]
    if any(r["kind"] == "angle" for r in M["rows"]):
        M2 = dict(M)
        M2["rows"] = [r for r in M["rows"] if r["kind"] != "angle"]
        variants.append(("angle rows dropped", M2))
    for label, MM in variants:
        for kw in (dict(chordal_decomposition_enable=False), dict()):
            t = time.time()
            try:
                val, st, raw = ps.solve_dual_vec(MM, **kw)
            except Exception as e:
                log(f"  [{label}; {kw}] solver failed: {e.__class__.__name__}")
                continue
            log(f"  [{label}; {kw}] numerical dual {val!r} ({st}), {time.time()-t:.1f}s")
            res = certify(MM, raw, log=log)
            if res is None:
                log("    certificate failed")
                continue
            b, eps = res
            log(f"    rigorous bound {float(b)!r} (eps {eps:g})")
            if best is None or b > best[0]:
                best = (b, eps, label, kw, val, st, raw)
            break
    return best


if __name__ == "__main__":
    import json, os
    name = sys.argv[1]
    M = pm.decode(name)
    print(f"== {name}")
    best = best_certificate(M)
    b, eps, label, kw, val, st, raw = best
    print(f"  RIGOROUS LOWER BOUND {float(b)!r} ({label}; exact rational, eps = {eps:g})")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", f"{name}.sdpcert.json")
    json.dump(dict(name=name, variant=label, solver_options=kw, sdp_numeric=val, status=st, bound=float(b),
                   bound_exact=str(b), eps=eps, raw=raw), open(out, "w"))
