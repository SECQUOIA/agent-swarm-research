"""pricing050 structure: max -sum_j c_j x_j (c_j >= 0) over x in [0,10]^50 subject to
5 rows  sum_j a_ij x_j exp(g_ij x_j^p_ij) <= r_i  with a_ij < 0, p in {1,2,3}.
The parser asserts every term has exactly this form (exact strings kept)."""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402


def parse():
    I = ev.load("pricing050")
    n = len(I["names"])
    assert n == 50 and all(I["lb"][j] == "0" and I["ub"][j] == "10" and I["vt"][j] == "C" for j in range(n))
    o = I["obj"]
    assert o["sense"] == "max" and o["constant"] == "0" and not o["quad"] and o["nl"] is None
    c = [Fraction(0)] * n
    for j, v in o["lin"].items():
        c[j] = -Fraction(v)
        assert c[j] > 0
    rows = []
    for r in I["cons"]:
        assert r["lb"] == "-INF" and r["constant"] == "0" and not r["lin"] and not r["quad"]
        t = r["nl"]
        assert t[0] == "sum"
        terms = {}
        for term in t[1:]:
            assert term[0] == "product" and len(term) == 3 and term[1][0] == "exp" and term[2][0] == "var"
            j, a = term[2][1], term[2][2]
            assert Fraction(a) < 0
            E = term[1][1]
            if E[0] == "var":
                assert E[1] == j
                p, g = 1, E[2]
            else:
                assert E[0] == "product" and len(E) == 3 and E[2][0] == "num"
                g = E[2][1]
                if E[1][0] == "square":
                    assert E[1][1] == ("var", j, "1")
                    p = 2
                else:
                    assert E[1] == ("power", ("var", j, "1"), ("num", "3"))
                    p = 3
            assert Fraction(g) < 0
            assert j not in terms
            terms[j] = (a, p, g)
        rows.append(dict(r=r["ub"], terms=terms))
    return I, c, rows


if __name__ == "__main__":
    I, c, rows = parse()
    print("c:", [str(v) for v in c])
    for i, R in enumerate(rows):
        print(i, R["r"], len(R["terms"]), sorted({(p, g) for (a, p, g) in R["terms"].values()}))
