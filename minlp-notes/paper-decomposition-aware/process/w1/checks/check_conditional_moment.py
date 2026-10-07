#!/usr/bin/env python3
"""Exact checks for the local-moment obstruction (limits cluster).

Part A re-derives every number of the original four-variable witness.
Part B checks the parity/binomial family that defeats every finite moment
order with bag size three.  Uses sympy with exact rationals and Fraction.
Finite checks support, but do not replace, the proofs in limits-proofs.tex.
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb
import random
import sympy as sp

R = sp.Rational
rng = random.Random(20261003)


def part_a():
    s, u1, u2, v, h = sp.symbols('s u1 u2 v h', positive=True)
    t = s / h
    F = 8 * (t - (u1 + u2) / 2) ** 2 + 8 * (t - R(1, 4) - v / 2) ** 2 \
        + u1 * (1 - u1) + u2 * (1 - u2) + v * (1 - v) + (u1 + u2 + v) / 16
    delta = t - R(1, 8) - (u1 + u2 + v) / 4
    ident = R(1, 4) + 16 * delta ** 2 + 2 * ((1 - v) * u1 * u2 + v * (1 - u1) * (1 - u2)) \
        + (u1 + u2 + v) / 16
    assert sp.expand(F - ident) == 0, "expansion identity"
    # growth: ||x-x*||^2 <= 2 delta^2 + 11/8 ||w||^2 and F-1/4 >= 16 delta^2 + ||w||^2/16
    npts = 0
    for hval in [R(1, 2), R(1, 4), R(1, 64)]:
        for _ in range(400):
            pt = {s: R(rng.randrange(0, 257), 256), u1: R(rng.randrange(0, 65), 64),
                  u2: R(rng.randrange(0, 65), 64), v: R(rng.randrange(0, 65), 64), h: hval}
            gap = F.subs(pt) - R(1, 4)
            dist2 = (pt[s] - hval / 8) ** 2 + pt[u1] ** 2 + pt[u2] ** 2 + pt[v] ** 2
            d = delta.subs(pt)
            w2 = pt[u1] ** 2 + pt[u2] ** 2 + pt[v] ** 2
            assert dist2 <= 2 * d ** 2 + R(11, 8) * w2
            assert gap >= 16 * d ** 2 + w2 / 16
            assert 22 * gap >= dist2
            npts += 1
    # Hessian
    X = [s, u1, u2, v]
    H = sp.hessian(F, X)
    r1 = sp.Matrix([1 / h, -R(1, 2), -R(1, 2), 0])
    r2 = sp.Matrix([1 / h, 0, 0, -R(1, 2)])
    Pc = sp.diag(0, 1, 1, 1)
    assert sp.simplify(H - (16 * r1 * r1.T + 16 * r2 * r2.T - 2 * Pc)) == sp.zeros(4)
    b = sp.Matrix([0, 1, -1, 0])
    assert sp.simplify(H * b + 2 * b) == sp.zeros(4, 1), "eigenvalue -2"
    assert sp.simplify(H[0, 0] - 32 / h ** 2) == 0
    # H + 2I = 16 r1 r1^T + 16 r2 r2^T + 2 e_s e_s^T  => lambda_min = -2 exactly
    assert sp.simplify(H + 2 * sp.eye(4) - (16 * r1 * r1.T + 16 * r2 * r2.T + 2 * sp.diag(1, 0, 0, 0))) == sp.zeros(4)
    # local measures (t, u1, u2) and (t, v)
    left = [(Fr(1, 8), (Fr(0), 0, 0)), (Fr(3, 8), (Fr(1, 2), 1, 0)),
            (Fr(3, 8), (Fr(1, 2), 0, 1)), (Fr(1, 8), (Fr(1), 1, 1))]
    right = [(Fr(1, 2), (Fr(1, 4), 0)), (Fr(1, 2), (Fr(3, 4), 1))]
    mom = lambda meas, k: sum(w * p[0] ** k for w, p in meas)
    assert [mom(left, k) for k in range(4)] == [1, Fr(1, 2), Fr(5, 16), Fr(7, 32)]
    assert [mom(right, k) for k in range(4)] == [1, Fr(1, 2), Fr(5, 16), Fr(7, 32)]
    assert mom(left, 4) == Fr(11, 64) and mom(right, 4) == Fr(41, 256)
    for _, (tt, a, bb) in left:
        assert tt == Fr(a + bb, 2)
    for _, (tt, vv) in right:
        assert tt == Fr(1, 4) + Fr(vv, 2)
    val = Fr(1, 16) * (sum(w * (a + bb) for w, (_, a, bb) in left) + sum(w * vv for w, (_, vv) in right))
    assert val == Fr(3, 32) and Fr(1, 4) - val == Fr(5, 32)
    # PSD completion with mean (h/2, 1/2, 1/2, 1/2)
    for hval in [Fr(1, 2), Fr(1, 8), Fr(1, 2 ** 40)]:
        m = [hval / 2, Fr(1, 2), Fr(1, 2), Fr(1, 2)]
        a = [hval, 1, 1, 2]
        bv = [0, 1, -1, 0]
        Sig = [[Fr(a[i] * a[j], 16) + Fr(3 * bv[i] * bv[j], 16) for j in range(4)] for i in range(4)]
        Y = [[m[i] * m[j] + Sig[i][j] for j in range(4)] for i in range(4)]
        # left-bag second moments in s-coordinates
        L2 = lambda i, j: sum(w * (p[i] * (hval if i == 0 else 1)) * (p[j] * (hval if j == 0 else 1)) for w, p in left)
        for i, j in product(range(3), repeat=2):
            assert Y[i][j] == L2(i, j)
        idx = {0: 0, 1: 3}
        R2 = lambda i, j: sum(w * (p[i] * (hval if i == 0 else 1)) * (p[j] * (hval if j == 0 else 1)) for w, p in right)
        for i, j in product(range(2), repeat=2):
            assert Y[idx[i]][idx[j]] == R2(i, j)
        assert Y[1][3] == Fr(3, 8) and Y[2][3] == Fr(3, 8)
        # McCormick with s in [0,2h], controls in [0,1]
        up = [2 * hval, 1, 1, 1]
        for i, j in product(range(4), repeat=2):
            assert Y[i][j] >= 0
            assert Y[i][j] >= up[i] * m[j] + up[j] * m[i] - up[i] * up[j]
            assert Y[i][j] <= up[i] * m[j] and Y[i][j] <= up[j] * m[i]
        # triangle (Padberg) inequality on (u1,u2,v): E[u1u2 + v - u1 v - u2 v] = -1/8
        assert Y[1][2] + m[3] - Y[1][3] - Y[2][3] == Fr(-1, 8)
        # residual squares have zero pseudo-expectation
        r1v = [1 / hval, Fr(-1, 2), Fr(-1, 2), 0]
        r2v = [1 / hval, 0, 0, Fr(-1, 2)]
        e1 = sum(r1v[i] * r1v[j] * Y[i][j] for i in range(4) for j in range(4)) - 0
        assert e1 == 0
        mean2 = sum(r2v[i] * m[i] for i in range(4)) - Fr(1, 4)
        e2 = sum(r2v[i] * r2v[j] * Y[i][j] for i in range(4) for j in range(4)) \
            - 2 * Fr(1, 4) * sum(r2v[i] * m[i] for i in range(4)) + Fr(1, 16)
        assert mean2 == 0 and e2 == 0
    return npts


def build_family(r, h):
    """Return (F, controls, cont_nodes, symbols) for the parity family."""
    u = sp.symbols(f'u1:{r + 1}')
    v = sp.symbols(f'v1:{r}') if r >= 2 else ()
    p = sp.symbols(f'p1:{r}') if r >= 2 else ()
    q = sp.symbols(f'q1:{r}') if r >= 2 else ()
    s = sp.Symbol('s')
    P = [0] + list(p) + [s]
    Qn = [0] + list(q)
    e = [(P[i] - P[i - 1]) / h - u[i - 1] for i in range(1, r + 1)]
    f = [(Qn[j] - Qn[j - 1]) / h - v[j - 1] for j in range(1, r)]
    f.append((s - Qn[r - 1]) / h - R(1, 2))
    tau = R(1, 8 * r)
    F = 2 * r * (sum(x ** 2 for x in e) + sum(x ** 2 for x in f)) \
        + sum(x * (1 - x) for x in u) + sum(x * (1 - x) for x in v) + tau * (sum(u) + sum(v))
    return F, list(u), list(v), list(p), list(q), s


def part_b(rmax=4):
    out = []
    for r in range(1, rmax + 1):
        h = sp.Symbol('h', positive=True)
        F, u, v, p, q, s = build_family(r, h)
        U, V = sum(u), sum(v)
        E = U - V - R(1, 2)
        # path nodes N_0..N_{2r} (unscaled): 0, P_1..P_{r-1}, A, Q_{r-1}..Q_1, 0
        c = list(u) + [-R(1, 2)] + [-x for x in reversed(v)]
        rho = -E / (2 * r)
        N0 = [0]
        for k in range(2 * r):
            N0.append(N0[-1] + c[k] + rho)
        assert sp.expand(N0[-1]) == 0
        dl = sp.symbols(f'd1:{2 * r}')
        nodes = [N0[k] + dl[k - 1] for k in range(1, 2 * r)]
        sub = {}
        for i, pi in enumerate(p):
            sub[pi] = h * nodes[i]
        sub[s] = h * nodes[r - 1]
        for j, qj in enumerate(q):
            # q_j is node N_{2r-j-1}... q_1 is N_{2r-1}, q_{r-1} is N_{r+1}
            sub[qj] = h * nodes[2 * r - (j + 1) - 1]
        Fs = sp.expand(F.subs(sub, simultaneous=True))
        dd = [0] + list(dl) + [0]
        Psi = E ** 2 + sum(x * (1 - x) for x in u) + sum(x * (1 - x) for x in v) + R(1, 8 * r) * (U + V)
        rhs = sp.expand(Psi + 2 * r * sum((dd[k] - dd[k - 1]) ** 2 for k in range(1, 2 * r + 1)))
        assert sp.expand(Fs - rhs) == 0, f"reduction identity r={r}"
        # Psi - 1/4 = 2 Pi + tau (U+V)
        e2u = sum(u[i] * u[j] for i in range(len(u)) for j in range(i + 1, len(u)))
        e2v = sum(v[i] * v[j] for i in range(len(v)) for j in range(i + 1, len(v)))
        Pi = e2u + e2v - U * V + V
        assert sp.expand(Psi - R(1, 4) - 2 * Pi - R(1, 8 * r) * (U + V)) == 0
        # Pi at vertices
        for bits in product([0, 1], repeat=len(u) + len(v)):
            sb = dict(zip(u + v, bits))
            a_, b_ = sum(bits[:len(u)]), sum(bits[len(u):])
            assert Pi.subs(sb) == R((a_ - b_) * (a_ - b_ - 1), 2) >= 0
        # moments of 2A: even/odd conditioned binomial
        left = {2 * i: Fr(comb(2 * r, 2 * i), 2 ** (2 * r - 1)) for i in range(r + 1)}
        right = {2 * j + 1: Fr(comb(2 * r, 2 * j + 1), 2 ** (2 * r - 1)) for j in range(r)}
        assert sum(left.values()) == 1 and sum(right.values()) == 1
        for m in range(2 * r):
            assert sum(w * k ** m for k, w in left.items()) == sum(w * k ** m for k, w in right.items())
        diff2r = sum(w * k ** (2 * r) for k, w in left.items()) - sum(w * k ** (2 * r) for k, w in right.items())
        assert diff2r != 0
        EU = sum(w * Fr(k, 2) for k, w in left.items())
        EV = sum(w * Fr(k - 1, 2) for k, w in right.items())
        assert EU == Fr(r, 2) and EV == Fr(r - 1, 2)
        relaxed = Fr(1, 8 * r) * (EU + EV)
        gap = Fr(1, 4) - relaxed
        assert gap == Fr(2 * r + 1, 16 * r) and gap >= Fr(1, 8)
        # witness supports: residuals vanish
        hv = R(1, 64 * r)
        for i in range(r + 1):
            uu = [1] * i + [0] * (r - i)
            P = [sum(uu[:k]) for k in range(r + 1)]
            sb = {s: hv * P[r]}
            sb.update({u[k]: uu[k] for k in range(r)})
            sb.update({p[k]: hv * P[k + 1] for k in range(r - 1)})
            # left residuals
            for k in range(1, r + 1):
                assert (hv * P[k] - hv * P[k - 1]) / hv - uu[k - 1] == 0
        for j in range(r):
            vv = [1] * j + [0] * (r - 1 - j)
            Qv = [sum(vv[:k]) for k in range(r)]
            A = j + R(1, 2)
            for k in range(1, r):
                assert Qv[k] - Qv[k - 1] - vv[k - 1] == 0
            assert A - Qv[r - 1] - R(1, 2) == 0
        # growth at random rational points (h = 1/(4r)), with box [-1,1] for continuous vars
        g = R(1, 8 * r * (1 + 8 * (2 * r - 1) ** 2))
        hval = R(1, 4 * r)
        Fh = F.subs(h, hval)
        zstar = {x: 0 for x in u + v}
        Nst = [sp.expand(N0[k]).subs({x: 0 for x in u + v}) for k in range(2 * r + 1)]
        for i, pi in enumerate(p):
            zstar[pi] = hval * Nst[i + 1]
        zstar[s] = hval * Nst[r]
        for j, qj in enumerate(q):
            zstar[qj] = hval * Nst[2 * r - (j + 1)]
        assert Fh.subs(zstar) == R(1, 4)
        assert zstar[s] == hval / 4
        cont = list(p) + [s] + list(q)
        cnt = 0
        for trial in range(150):
            pt = {x: R(rng.randrange(0, 33), 32) for x in u + v}
            for x in cont:
                pt[x] = R(rng.randrange(-64, 65), 64)
            if trial % 3 == 0:  # points near the optimum manifold
                for x in cont:
                    pt[x] = zstar[x] + R(rng.randrange(-8, 9), 256)
            gapv = Fh.subs(pt) - R(1, 4)
            dist2 = sum((pt[x] - zstar[x]) ** 2 for x in pt)
            assert gapv >= g * dist2, (r, trial)
            cnt += 1
        # Hessian + 2 * I_controls is PSD (it is 4r * sum of rank-one Gram terms): check exactly
        X = u + v + cont
        Hm = sp.hessian(F.subs(h, hval), X)
        Pc = sp.diag(*([1] * (len(u) + len(v)) + [0] * len(cont)))
        M = Hm + 2 * Pc
        # exact PSD test via principal-minor-free method: LDL with rational pivots on M + tiny? use eigen-free check:
        assert M.is_positive_semidefinite
        out.append((r, str(gap), str(g), cnt))
    return out


if __name__ == '__main__':
    n = part_a()
    print('Part A passed:', n, 'exact growth points; identity, Hessian, moments, PSD completion, McCormick, triangle')
    res = part_b()
    for r, gap, g, cnt in res:
        print(f'Part B r={r}: moments match to order {2 * r - 1}, gap={gap}, valid g={g}, growth points={cnt}')
    print('ALL PASSED')
