"""Exact targeted checks for stage 1 boundary conventions and three-cell proof.

Uses half-integral simplex inputs, including zeros, ties, and masses exactly
at threshold; evaluates errors directly on the union of grid and switch times.
The analytic manuscript proofs, not finite enumeration, establish the theorems.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "one_switch_certificate", ROOT / "code/cia_tv_conjecture/one_switch_certificate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def three_term(a, p, q, tau):
    n, T = len(a), len(a[0])
    m = [sum(row) for row in a]
    return max(max((m[i] for i in range(n) if i not in (p, q)), default=Q(0)),
               tau - module.integrals(a, tau)[p], T - m[q] - tau)


def main():
    count = 0
    for n in (3, 4):
        columns = []
        for i, j in combinations_with_replacement(range(n), 2):
            columns.append(tuple(Q(int(h == i) + int(h == j), 2) for h in range(n)))
        for cols in product(columns, repeat=3):
            a = [list(row) for row in zip(*cols)]
            p, q, tau = module.construct(a)
            direct = module.direct_error(a, p, q, tau)
            assert direct == three_term(a, p, q, tau)
            assert direct <= module.bound(n, 3)
            order = sorted(range(n), key=lambda i: sum(a[i]), reverse=True)
            q, p = order[:2]
            assert module.direct_error(a, p, q, Q(1)) <= 2 - Q(3, n)
            for tau in (Q(0), Q(3)):
                assert module.direct_error(a, p, q, tau) == three_term(a, p, q, tau)
            count += 1
    binary_count = 0
    for first in product((Q(0), Q(1, 2), Q(1)), repeat=3):
        a = [list(first), [1 - x for x in first]]
        for tau in (Q(0), Q(1, 2), Q(1), Q(2), Q(5, 2), Q(3)):
            assert module.direct_error(a, 0, 1, tau) == three_term(a, 0, 1, tau)
            binary_count += 1
    for n in range(3, 31):
        a = [[Q(1, n)] * 3 for _ in range(n)]
        value = min(module.direct_error(a, 0, 1, Q(t)) for t in range(4))
        assert value == 2 - Q(3, n)
    print(f"PASS: {count} half-simplex profiles with zeros/ties/threshold boundaries;")
    print("three-term endpoint identities, one-switch construction, three-cell upper bound;")
    print("28 uniform three-cell sharpness cases, including constant schedules.")
    print(f"{binary_count} binary three-term identities with empty omitted maximum.")


if __name__ == "__main__":
    main()
