"""Exact finite checks for the effort accounting propositions.

Run: python3 research-20261003-adaptive-obbt/theory/check_effort_allocation.py
No solver or third-party packages are needed.
"""
from fractions import Fraction as F
from itertools import product


def check_ledger():
    count = 0
    rejected = 0
    overshoots = 0
    for credit, rate in product((F(0), F(1, 3), F(1)), (F(0), F(1, 4), F(1))):
        # Every optional call costs at most 1/2. Native work releases credit.
        for trace in product(("native", "short", "long"), repeat=7):
            native = extra = F(0)
            for event in trace:
                if event == "native":
                    native += F(1, 3)
                elif extra < credit + rate * native:
                    extra += F(1, 8) if event == "short" else F(1, 2)
                    overshoots += extra > credit + rate * native
                else:
                    rejected += 1
                assert extra <= credit + rate * native + F(1, 2)
                assert native + extra <= (1 + rate) * native + credit + F(1, 2)
            count += 1
    assert rejected and overshoots
    return count


def check_rescue_and_interleaving():
    count = 0
    for ta, th, cap in product(range(1, 41), range(1, 41), range(0, 5)):
        serial = th if th <= cap else cap + ta
        assert serial <= cap + ta
        # One work quantum each, baseline first. Stand-alone work is integral.
        a = h = elapsed = 0
        while a < ta and h < th:
            elapsed += 1
            if elapsed % 2:
                a += 1
            else:
                h += 1
        assert elapsed <= 2 * min(ta, th)
        count += 1
    return count


if __name__ == "__main__":
    print({"ledger_traces": check_ledger(),
           "portfolio_traces": check_rescue_and_interleaving(),
           "result": "passed"})
