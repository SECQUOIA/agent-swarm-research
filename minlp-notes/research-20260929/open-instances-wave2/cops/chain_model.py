"""COPS hanging chain (chain50/100/200/400): exact structure check, z-variables,
and a high-precision KKT point.

OSIL structure (asserted in `extract`):
  variables x_0..x_N (idx 0..N), u_0..u_N (idx N+1..2N+1), all free except
  x_0 = 1, x_N = 3;
  rows i = 0..N-1:  x_{i+1} - x_i - eta*u_i - eta*u_{i+1} = 0;
  row N:            eta * sum_{i<N} (s_i + s_{i+1}) = 4,  s_i = sqrt(u_i^2 + 1);
  objective:        eta * sum_{i<N} (s_i*x_i + s_{i+1}*x_{i+1})   (no constant),
with eta = h/2 = 1/(2N) given as a decimal string.

z-variables: z_i = x_i - eta*u_i (i = 0..N), z_{N+1} = x_N + eta*u_N.
The dynamics rows hold iff x_i = (z_i+z_{i+1})/2 and u_i = (z_{i+1}-z_i)/(2 eta).
With h = 2*eta, d_i = z_{i+1}-z_i, l_i = sqrt(h^2 + d_i^2), rho_0 = rho_N = 1/2,
rho_i = 1 otherwise:  w_i s_i = rho_i l_i, so
  objective = sum_i rho_i l_i (z_i+z_{i+1})/2,   length = sum_i rho_i l_i.
"""
import os
import sys
from fractions import Fraction

import mpmath as mp
import numpy as np

import osilx

OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "chain%d.osil")


def _sq(k):
    return ("sqrt", ("sum", ("square", ("var", k, "1")), ("num", "1")))


def extract(N):
    m = osilx.read(OSIL % N)
    nv = 2 * N + 2
    assert len(m["names"]) == nv and len(m["cons"]) == N + 1
    assert all(t == "C" for t in m["vt"])
    for j in range(nv):
        if j == 0:
            assert (m["lb"][j], m["ub"][j]) == ("1", "1")
        elif j == N:
            assert (m["lb"][j], m["ub"][j]) == ("3", "3")
        else:
            assert (m["lb"][j], m["ub"][j]) == ("-INF", "INF"), j
    eta = m["cons"][0]["lin"][N + 1]
    assert eta.startswith("-")
    eta = eta[1:]
    assert Fraction(eta) == Fraction(1, 2 * N), eta
    for i in range(N):
        c = m["cons"][i]
        assert c["lb"] == "0" and c["ub"] == "0" and c["constant"] == "0"
        assert c["quad"] == [] and c["nl"] is None
        assert c["lin"] == {i: "-1", i + 1: "1", N + 1 + i: "-" + eta, N + 2 + i: "-" + eta}, i
    c = m["cons"][N]
    assert c["lb"] == "4" and c["ub"] == "4" and c["constant"] == "0" and c["lin"] == {} and c["quad"] == []
    terms = []
    for i in range(N):
        terms += [_sq(N + 1 + i), _sq(N + 2 + i)]
    assert c["nl"] == ("product", ("sum",) + tuple(terms), ("num", eta)), "length row"
    o = m["obj"]
    assert o["sense"] == "min" and o["constant"] == "0" and o["weight"] == "1"
    assert o["lin"] == {} and o["quad"] == []
    terms = []
    for i in range(N):
        terms += [("product", _sq(N + 1 + i), ("var", i, "1")),
                  ("product", _sq(N + 2 + i), ("var", i + 1, "1"))]
    assert o["nl"] == ("product", ("sum",) + tuple(terms), ("num", eta)), "objective"
    return m, eta


# ---------------- Lagrangian in z (generic number type) ----------------
def rho(N, i):
    return 0.5 if i in (0, N) else 1.0


def full_z(zin, N):
    """zin = (z_1..z_N) -> z_0..z_{N+1} using x_0 = 1, x_N = 3."""
    return [2 - zin[0]] + list(zin) + [6 - zin[-1]]


def lag_grad_hess(zin, mu, N, h, num=float, sqrt=np.sqrt):
    """Gradient/tridiagonal Hessian of L_mu(z) = sum rho_i l_i (m_i + mu) over z_1..z_N,
    and gradient of G(z) = sum rho_i l_i. Returns (L, G, gL, gG, diag, off)."""
    z = full_z(zin, N)
    L = num(0)
    G = num(0)
    gL = [num(0)] * N
    gG = [num(0)] * N
    dg = [num(0)] * N
    off = [num(0)] * (N - 1)
    for i in range(N + 1):
        r = num(1) / 2 if i in (0, N) else num(1)
        d = z[i + 1] - z[i]
        l = sqrt(h * h + d * d)
        y = (z[i] + z[i + 1]) / 2 + mu
        lp = d / l
        lpp = h * h / (l * l * l)
        L += r * l * y
        G += r * l
        # partials wrt z_i (a) and z_{i+1} (b)
        fa = r * (-lp * y + l / 2)
        fb = r * (lp * y + l / 2)
        faa = r * (lpp * y - lp)
        fbb = r * (lpp * y + lp)
        fab = -r * lpp * y
        ga, gb = -r * lp, r * lp
        gaa = r * lpp
        # chain rule for the ends: z_0 = 2 - z_1, z_{N+1} = 6 - z_N
        if i == 0:
            # f(z1) = phi(2 - z1, z1)
            gL[0] += fb - fa
            gG[0] += gb - ga
            dg[0] += faa - 2 * fab + fbb
        elif i == N:
            gL[N - 1] += fa - fb
            gG[N - 1] += ga - gb
            dg[N - 1] += faa - 2 * fab + fbb
        else:
            a, b = i - 1, i  # positions of z_i, z_{i+1} in zin
            gL[a] += fa
            gL[b] += fb
            gG[a] += ga
            gG[b] += gb
            dg[a] += faa
            dg[b] += fbb
            off[a] += fab
    return L, G, gL, gG, dg, off


def tri_solve(dg, off, rhs):
    n = len(dg)
    c = [None] * n
    d = [None] * n
    b = dg[0]
    c[0] = off[0] / b if n > 1 else None
    d[0] = rhs[0] / b
    for i in range(1, n):
        b = dg[i] - off[i - 1] * c[i - 1]
        if i < n - 1:
            c[i] = off[i] / b
        d[i] = (rhs[i] - off[i - 1] * d[i - 1]) / b
    x = [None] * n
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def newton(zin, mu, N, h, num, sqrt, iters, tol, verbose=False):
    for it in range(iters):
        L, G, gL, gG, dg, off = lag_grad_hess(zin, mu, N, h, num, sqrt)
        # KKT: gL = 0 (gradient of L_mu includes mu*gG), G - 4 = 0
        a = tri_solve(dg, off, [-v for v in gL])
        b = tri_solve(dg, off, gG)
        # G(z+dz) ~ G + gG.dz = 4, dz = a - dmu*b
        ga = sum(gG[k] * a[k] for k in range(N))
        gb = sum(gG[k] * b[k] for k in range(N))
        dmu = (G - 4 + ga) / gb
        dz = [a[k] - dmu * b[k] for k in range(N)]
        zin = [zin[k] + dz[k] for k in range(N)]
        mu = mu + dmu
        step = max(abs(v) for v in dz)
        if verbose:
            print(it, float(step), float(abs(G - 4)), float(max(abs(v) for v in gL)))
        if step < tol:
            break
    return zin, mu


def catenary_start(N):
    from scipy.optimize import fsolve

    def eqs(p):
        C, D, E = p
        return [C * np.cosh(-D / C) + E - 1, C * np.cosh((1 - D) / C) + E - 3,
                C * (np.sinh((1 - D) / C) - np.sinh(-D / C)) - 4]
    C, D, E = fsolve(eqs, [0.3, 0.4, -0.5])
    h = 1.0 / N
    t = (np.arange(1, N + 1) - 0.5) * h
    return list(C * np.cosh((t - D) / C) + E), -E, (C, D, E)


def solve(N, dps=60):
    h = 1.0 / N
    z0, mu0, cat = catenary_start(N)
    z, mu = newton(z0, mu0, N, h, float, np.sqrt, 50, 1e-13)
    mp.mp.dps = dps
    hm = mp.mpf(1) / N
    z = [mp.mpf(v) for v in z]
    mu = mp.mpf(mu)
    z, mu = newton(z, mu, N, hm, mp.mpf, mp.sqrt, 10, mp.mpf(10) ** (-dps + 8))
    return z, mu, cat


def to_xu(zin, N, eta):
    z = full_z(zin, N)
    x = [(z[i] + z[i + 1]) / 2 for i in range(N + 1)]
    u = [(z[i + 1] - z[i]) / (2 * eta) for i in range(N + 1)]
    return x, u


if __name__ == "__main__":
    for N in [int(a) for a in sys.argv[1:]]:
        m, eta = extract(N)
        z, mu, cat = solve(N)
        L, G, gL, gG, dg, off = lag_grad_hess(z, mu, N, mp.mpf(1) / N, mp.mpf, mp.sqrt)
        print(N, "eta", eta, "catenary C,D,E", cat)
        print("  f* =", mp.nstr(L - mu * G, 25), " mu* =", mp.nstr(mu, 25),
              " |G-4| =", mp.nstr(abs(G - 4), 3), " max|grad| =", mp.nstr(max(abs(v) for v in gL), 3))
        print("  z range", mp.nstr(min(z), 10), mp.nstr(max(z), 10))
