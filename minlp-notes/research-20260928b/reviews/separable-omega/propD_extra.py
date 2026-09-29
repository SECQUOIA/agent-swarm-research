"""Addendum to propD_check.py (review).
(1) Lemma 3.2 on structured instances: m = 0 at M+1 equally spaced knots (caps of width 1/M,
    close to m = 0 at budgets above 1/(4M^2)) and dyadic caps g.
(2) Explicit product certificates for g + g at eps = 1e-4 and 1e-7, verified box by box:
    x-pieces valid at e1, z-pieces valid at eps - e1 (greedy, exact)."""
from fractions import Fraction as Fr
from sepcore import PL, dyadic_caps


def pieces(c, b):
    out, a = [], c.L
    while a < c.U:
        u = c.maxvalid(a, b)
        out.append((a, u))
        a = u
    return out


if __name__ == "__main__":
    M = 400
    saw = PL.from_m([Fr(k, M) for k in range(M + 1)], [0] * (M + 1))
    g = dyadic_caps(60)
    for name, c in (("sawtooth M=400", saw), ("dyadic caps g", g)):
        rs = []
        for k in range(2, 9):
            b = Fr(1, 10 ** k)
            rs.append(f"1e-{k}: {c.ncert(b)}->{c.ncert(b / 2)}")
        print(f"Lemma 3.2, {name}: N(b)->N(b/2): " + ", ".join(rs))
    for k, note in ((3, 27), (4, 50), (5, 81), (6, 102), (7, 145)):
        eps = Fr(1, 10 ** k)
        best = None
        for j in range(1, 64):
            e1 = eps * Fr(j, 64)
            P, Q = pieces(g, e1), pieces(g, eps - e1)
            if best is None or len(P) * len(Q) < best[0]:
                best = (len(P) * len(Q), e1, P, Q)
        n, e1, P, Q = best
        ok = all(g.node(*I)[0] + g.node(*J)[0] + eps >= 0 for I in P for J in Q)
        print(f"g+g eps=1e-{k}: product certificate {len(P)}x{len(Q)} = {n} boxes (e1 = {e1/eps}*eps), "
              f"all boxes valid exactly: {ok}; note's grid optimum {note}")
