"""catmix: own structure check, exact stage polynomials (sympy, exact rationals), exact
nonnegativity checks, and primal checks (reviewer code).

Rows (i = 0..N-1), variables u_0..u_N (idx 0..N), x1_0..x1_N (N+1..2N+1), x2_0..x2_N (2N+2..3N+2):
  x1-row: x1_{i+1} - x1_i + a u_i x1_i - b u_i x2_i + a u_{i+1} x1_{i+1} - b u_{i+1} x2_{i+1} = 0
  x2-row: ep x2_{i+1} - em x2_i - a u_i x1_i + c u_i x2_i - a u_{i+1} x1_{i+1} + c u_{i+1} x2_{i+1} = 0
i.e. P(u_{i+1}) x_{i+1} = Q(u_i) x_i with P = [[1+au, -bu], [-au, ep+cu]], Q = [[1-au, bu], [au, em-cu]].
"""
import os
import sys
from fractions import Fraction as Fr

import sympy as sp

import osilx

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "catmix%d.osil")


def load(N):
    m = osilx.read(OSIL % N)
    assert len(m["names"]) == 3 * N + 3 and len(m["cons"]) == 2 * N and set(m["vt"]) == {"C"}
    U, X1, X2 = (lambda i: i), (lambda i: N + 1 + i), (lambda i: 2 * N + 2 + i)
    for j in range(3 * N + 3):
        b = (m["lb"][j], m["ub"][j])
        exp = ("0", "1") if j <= N else ("1", "1") if j == X1(0) else ("0", "0") if j == X2(0) else ("-INF", "INF")
        assert b == exp, (j, b)
    o = m["obj"]
    assert (o["sense"], o["constant"], o["weight"], o["lin"], o["quad"], o["nl"]) == \
        ("min", "-1", "1", {X1(N): "1", X2(N): "1"}, [], None)
    a = m["cons"][0]["quad"][0][2]
    b = m["cons"][0]["quad"][1][2][1:]
    c = m["cons"][N]["quad"][1][2]
    em = m["cons"][N]["lin"][X2(0)][1:]
    ep = m["cons"][N]["lin"][X2(1)]
    for i in range(N):
        r = m["cons"][i]
        assert (r["lb"], r["ub"], r["constant"], r["nl"]) == ("0", "0", "0", None)
        assert r["lin"] == {X1(i): "-1", X1(i + 1): "1"}
        assert sorted(r["quad"]) == sorted([(U(i), X1(i), a), (U(i), X2(i), "-" + b),
                                            (U(i + 1), X1(i + 1), a), (U(i + 1), X2(i + 1), "-" + b)])
        r = m["cons"][N + i]
        assert (r["lb"], r["ub"], r["constant"], r["nl"]) == ("0", "0", "0", None)
        assert r["lin"] == {X2(i): "-" + em, X2(i + 1): ep}
        assert sorted(r["quad"]) == sorted([(U(i), X1(i), "-" + a), (U(i), X2(i), c),
                                            (U(i + 1), X1(i + 1), "-" + a), (U(i + 1), X2(i + 1), c)])
    K = dict(a=Fr(a), b=Fr(b), c=Fr(c), ep=Fr(ep), em=Fr(em))
    strs = dict(a=a, b=b, c=c, ep=ep, em=em)
    return m, K, strs


def polys(K):
    """exact coefficient lists (low -> high degree, Fractions) derived with sympy."""
    u = sp.symbols("u")
    R = {k: sp.Rational(v.numerator, v.denominator) for k, v in K.items()}
    a, b, c, ep, em = R["a"], R["b"], R["c"], R["ep"], R["em"]
    P = sp.Matrix([[1 + a * u, -b * u], [-a * u, ep + c * u]])
    Q = sp.Matrix([[1 - a * u, b * u], [a * u, em - c * u]])
    D = sp.expand(P.det())
    adj = P.adjugate()
    Nm = (Q * adj).applyfunc(sp.expand)
    T = (sp.Matrix([[1, 1]]) * adj).applyfunc(sp.expand)

    def co(e, deg=2):
        p = sp.Poly(e, u)
        cs = [Fr(int(sp.numer(p.coeff_monomial(u ** k))), int(sp.denom(p.coeff_monomial(u ** k)))) for k in range(deg + 1)]
        assert sp.degree(e, u) <= deg
        return cs
    # sanity: P * adj = det I
    assert sp.simplify(P * adj - D * sp.eye(2)) == sp.zeros(2, 2)
    return dict(N11=co(Nm[0, 0]), N12=co(Nm[0, 1]), N21=co(Nm[1, 0]), N22=co(Nm[1, 1]), D=co(D),
                T1=co(T[0, 0]), T2=co(T[0, 1]), Q11=co(Q[0, 0]), Q21=co(Q[1, 0]))


def qmin01(cs):
    """exact min over [0,1] of a quadratic with Fraction coefficients."""
    c0, c1, c2 = (cs + [Fr(0)] * 3)[:3]
    f = lambda t: c0 + c1 * t + c2 * t * t
    cands = [f(Fr(0)), f(Fr(1))]
    if c2 > 0:
        v = -c1 / (2 * c2)
        if 0 < v < 1:
            cands.append(f(v))
    return min(cands)


def nonneg_checks(Pl):
    out = {}
    for k in ("N11", "N12", "N21", "N22", "T1", "T2", "Q11", "Q21"):
        out[k] = float(qmin01(Pl[k]))
        assert qmin01(Pl[k]) >= 0, k
    out["D"] = float(qmin01(Pl["D"]))
    assert qmin01(Pl["D"]) > 0
    return out


def simulate_exact(K, u):
    """exact rational states for rational controls u_0..u_N; returns x_N and the objective."""
    a, b, c, ep, em = (K[k] for k in ("a", "b", "c", "ep", "em"))
    x1, x2 = Fr(1), Fr(0)
    xs = [(x1, x2)]
    for i in range(len(u) - 1):
        ui, un = u[i], u[i + 1]
        y1 = (1 - a * ui) * x1 + b * ui * x2
        y2 = a * ui * x1 + (em - c * ui) * x2
        p11, p12, p21, p22 = 1 + a * un, -b * un, -a * un, ep + c * un
        det = p11 * p22 - p12 * p21
        x1, x2 = (p22 * y1 - p12 * y2) / det, (p11 * y2 - p21 * y1) / det
        xs.append((x1, x2))
    return xs


def simulate_iv(Kstr, u, dps=60):
    from mpmath import iv
    iv.dps = dps
    a, b, c, ep, em = (iv.mpf(Kstr[k]) for k in ("a", "b", "c", "ep", "em"))
    x1, x2 = iv.mpf(1), iv.mpf(0)
    for i in range(len(u) - 1):
        ui, un = iv.mpf(u[i]), iv.mpf(u[i + 1])
        y1 = (1 - a * ui) * x1 + b * ui * x2
        y2 = a * ui * x1 + (em - c * ui) * x2
        p11, p12, p21, p22 = 1 + a * un, -b * un, -a * un, ep + c * un
        det = p11 * p22 - p12 * p21
        x1, x2 = (p22 * y1 - p12 * y2) / det, (p11 * y2 - p21 * y1) / det
    return x1 + x2 - 1


if __name__ == "__main__":
    import numpy as np
    import mpmath as mp
    base = os.path.join(R29, "open-instances-wave2/cops/logs/")
    for N in [int(v) for v in sys.argv[1:]]:
        m, K, strs = load(N)
        Pl = polys(K)
        print(N, "constants", strs, "ep+em-2 =", K["ep"] + K["em"] - 2, "c-9a =", float(K["c"] - 9 * K["a"]))
        print("  exact min over [0,1]:", nonneg_checks(Pl))
        # author primal: controls and full double vector
        for tag in (["", "_snap"] if N == 800 else [""]):
            try:
                u = np.load(base + "catmix%d_u%s.npy" % (N, tag))
            except FileNotFoundError:
                continue
            assert np.all((u >= 0) & (u <= 1)) and len(u) == N + 1
            J = simulate_iv(strs, [mp.mpf(float(v)) for v in u])
            line = "  controls%s: J enclosure [%s, %s]" % (tag, mp.nstr(J.a, 18), mp.nstr(J.b, 18))
            if N <= 200:
                xs = simulate_exact(K, [Fr(float(v)) for v in u])
                Je = xs[-1][0] + xs[-1][1] - 1
                line += "  exact J = %s" % mp.nstr(mp.mpf(Je.numerator) / Je.denominator, 18)
            print(line, flush=True)
            X = [float(s) for s in open(base + "catmix%d_primal%s.txt" % (N, tag)).read().split()]
            Xf = [Fr(v) for v in X]
            lbv = max(max(Fr(m["lb"][j]) - Xf[j], Xf[j] - Fr(m["ub"][j]), 0) if not osilx.isinf(m["ub"][j]) else 0
                      for j in range(len(X)))
            rv = max(abs(osilx.ev_row(r, Xf, Fr, {})) for r in m["cons"])
            obj = Xf[N + 1 + N] + Xf[2 * N + 2 + N] + Fr(m["obj"]["constant"])
            print("  double vector%s: exact obj %.17g  max row viol %.3g  bound viol %s  controls equal npy: %s" % (
                tag, float(obj), float(rv), float(lbv), bool(np.all(np.array(X[:N + 1]) == u))), flush=True)
