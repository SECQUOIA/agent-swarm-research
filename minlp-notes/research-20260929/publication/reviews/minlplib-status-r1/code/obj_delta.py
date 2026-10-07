"""Verifier: exact objective difference between two OSiL files whose
objectives are polynomials, at a listed point (exact decimals from a .sol;
missing variables are 0). Usage: obj_delta.py A.osil B.osil POINT.sol"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from poly_cmp_lib import read, rowpoly, padd  # noqa: E402
from tri_proof import load_sol  # noqa: E402

A, B = read(sys.argv[1]), read(sys.argv[2])
x = load_sol(sys.argv[3])
pa, _ = rowpoly(A, -1)
pb, _ = rowpoly(B, -1)
d = padd(pa, pb, -1)
print("differing objective coefficients:", len(d))
for k, v in sorted(d.items(), key=lambda kv: -abs(kv[1]))[:4]:
    print("  ", k, "A", pa.get(k), "B", pb.get(k))


def ev(p):
    s = Fraction(0)
    for k, v in p.items():
        t = v
        for n, e in k:
            t *= x.get(n, Fraction(0)) ** e
        s += t
    return s


fa, fb = ev(pa), ev(pb)
print("objective A at point:", float(fa), " B:", float(fb), " B-A exactly:", fb - fa, "=", float(fb - fa))
