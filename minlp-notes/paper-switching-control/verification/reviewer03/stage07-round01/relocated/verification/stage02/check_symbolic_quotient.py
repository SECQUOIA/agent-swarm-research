"""Check direct finite quotients against symbolic coefficients away from 9,10.

This is a regression check of the affine-count reconstruction, not the proof
of all-n topology stabilization; that proof is in the manuscript.
"""
import importlib.util
from pathlib import Path

if not __debug__:
    raise RuntimeError("Run without -O: exact checks require assertions")
checker = Path(__file__).resolve().parents[1] / "reference" / "verify_general_four_block.py"
spec = importlib.util.spec_from_file_location("four_block", checker)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
counts = []
for pair, z in m.CASES:
    V, A, b, B, d, c = m.quotient(9, pair, z)
    counts.append((len(V), len(A), len(B)))
    Vs, As, bs, Bs, ds, cs = m.symbolic_program(pair, z)
    for n in (11, 23, 37):
        Vn, An, bn, Bn, dn, cn = m.quotient(n, pair, z)
        def evaluate(poly):
            return sum(value*n**degree for degree, value in enumerate(poly))
        assert (Vs, As, bs, ds) == (Vn, An, bn, dn)
        assert [[(j, evaluate(v)) for j, v in row.items() if evaluate(v)] for row in Bs] == [list(row) for row in Bn]
        assert list(map(evaluate, cs)) == cn
print("Quotient dimensions (variables, inequalities, equalities):", counts)
print("All ten symbolic quotients agree with direct integer quotients at n=11,23,37.")
