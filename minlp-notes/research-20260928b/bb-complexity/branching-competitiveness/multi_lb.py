"""Theorem N3 check: multisection at the relaxation minimizer on f(x,z) = x^2 over [0,1]^2 (alpha = 1).

Closed forms (m = eps + x^2, independent of z):
  F_x([l,u]) = eps + l*u - (l+u)^2/8  with minimizer (l+u)/4   if u > 3l,
             = eps + l^2              with minimizer l (endpoint) otherwise;
  F_z([c,d]) = -(d-c)^2/4             with minimizer the midpoint.
A box is pruned iff F_x + F_z >= 0.  Rules: multi (split every coordinate whose
minimizer is interior), omega (the more central coordinate), deficit (the more
negative F_i among interior ones), bis (widest side, midpoint).  Exact rationals.
Also builds the explicit guillotine certificate of the proof and checks it.
Usage: python3 multi_lb.py
"""
from fractions import Fraction as Fr
import math


def fx(l, u, eps):
    if u > 3 * l:
        y = (l + u) / 4
        return eps + l * u - (l + u) ** 2 / 8, y
    return eps + l * l, l


def fz(c, d):
    return -(d - c) ** 2 / 4, (c + d) / 2


def run(rule, eps, cap=5_000_000):
    stack = [((Fr(0), Fr(1)), (Fr(0), Fr(1)))]
    nodes = 0
    while stack:
        (l, u), (c, d) = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        vx, yx = fx(l, u, eps)
        vz, yz = fz(c, d)
        if vx + vz >= 0:
            continue
        ax = (yx - l) * (u - yx)
        az = (yz - c) * (d - yz)
        if rule == "multi":
            xs = [(l, yx), (yx, u)] if ax > 0 else [(l, u)]
            stack += [(xi, zi) for xi in xs for zi in ((c, yz), (yz, d))]
            continue
        if rule == "omega":
            i = 0 if ax > az else 1
        elif rule == "deficit":
            i = 0 if (ax > 0 and vx < vz) else 1
        elif rule == "bis":
            i = 0 if u - l > d - c else 1
        if rule == "bis":
            s = (l + u) / 2 if i == 0 else (c + d) / 2
        else:
            s = yx if i == 0 else yz
        if i == 0:
            stack += [((l, s), (c, d)), ((s, u), (c, d))]
        else:
            stack += [((l, u), (c, s)), ((l, u), (s, d))]
    return nodes


def certificate(eps):
    """Explicit guillotine certificate of Theorem N3 (float check); returns its size."""
    h = 2 * math.sqrt(eps)
    strips = [(0.0, h)]
    t = h
    while t < 1:
        strips.append((t, min(2 * t, 1.0)))
        t *= 2
    count = 0
    for (l, u) in strips:
        vx = fx(l, u, eps)[0]
        w = math.sqrt(4 * vx) if vx > 0 else 0
        k = math.ceil(1 / w - 1e-12)
        # check validity of each piece (width 1/k)
        assert vx - (1 / k) ** 2 / 4 >= -1e-15
        count += k
    return count


if __name__ == "__main__":
    print("k-sum lower bound: internal(multi) >= sum_{k=2}^{K} (k-1) 4^k, K = floor(log_16(5/(36 eps)))")
    for p in range(2, 9):
        eps_f = 10.0 ** (-p)
        eps = Fr(1, 10 ** p)
        K = math.floor(math.log(5 / (36 * eps_f), 16))
        lb_internal = sum((k - 1) * 4 ** k for k in range(2, K + 1))
        cert = certificate(eps_f)
        row = {r: (run(r, eps) if p <= 6 or r != "bis" else None) for r in ("multi", "omega", "deficit", "bis")}
        T_opt_ub = 2 * cert - 1
        print(f"eps=1e-{p}: nodes {row}; certificate N={cert} (T_opt <= {T_opt_ub}); "
              f"multi/T_opt >= {row['multi']/T_opt_ub:.2f}; omega/T_opt >= ... {row['omega']/T_opt_ub:.2f}; "
              f"proved internal(multi) >= {lb_internal}", flush=True)
        assert row["multi"] >= 2 * lb_internal + 1
