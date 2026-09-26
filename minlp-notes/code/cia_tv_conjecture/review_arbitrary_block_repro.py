"""Independent reproduction of the reviewer checks for the arbitrary-block CIA bound.

Reproduces "Constructibility and independent recursive tests" in
notes/review-cia-arbitrary-block-one-sided.md (reviewer implementation and
output never archived) for results/cia-arbitrary-block-one-sided-bound.md.
Written 2026-09-25 from the review and the note; it does not reuse the
committed arbitrary_block_certificate.py, which is imported only at the end as
an object under test: its construct() schedules are re-verified here with this
file's own discrepancy evaluator.

The review's inputs were random and not archived, so its counts (360 inputs,
928 recursive reductions, 5 non-base largest-mass shortcuts, 355 one-block
base cases, 241 mass-qualified two-sided checks) cannot be matched exactly.
This file uses 360 new exact-rational inputs with 2..13 modes (30 per mode
count), cycling k through 1..n-1, and reports its own counts.

For every recursive call (reduction, shortcut, or base case) the contract
"negative discrepancy <= C_{n,k} * horizon against that level's (completed,
restricted) control" is checked exactly at every relaxed-grid endpoint and
every switch time of that level (both sides are piecewise linear between
these points).  Each reduction also checks L > 0, E' > 0, C_{n-1,k-1} L <= E',
E >= horizon/n, and that the completed rates lie in the simplex.  Final
schedules must use at most k blocks with pairwise distinct modes; when every
terminal mass is at most C_{n,k} T the positive discrepancy is also checked.
Ties for the maximum-mass mode are broken by the last maximiser here (the
committed checker takes the first); the proof allows either.

Run: /home/sgusev/miniconda3/envs/minlp-notes/bin/python review_arbitrary_block_repro.py
"""
from fractions import Fraction as F
from random import Random

T = F(1)


def coef(n, k):
    return F(n * (n - 1) + (n - k) * (n - k - 1), n * k * (2 * n - k - 1))


def cumulative(rates, cells, pos, t):
    """A_pos(t) for piecewise-constant rates on cells [(start, end), ...]."""
    return sum((r[pos] * max(F(0), min(t, e) - s) for r, (s, e) in zip(rates, cells)), F(0))


def discrepancies(rates, cells, labels, schedule, horizon):
    """Max over [0,horizon] of W_i - A_i (negative error) and A_i - W_i (positive)."""
    times = {s for s, _ in cells if s <= horizon} | {e for _, e in cells if e <= horizon}
    times |= {horizon} | {b for _, b, _ in schedule} | {e for _, _, e in schedule}
    neg = pos = F(0)
    for t in times:
        for p, lab in enumerate(labels):
            w = sum((max(F(0), min(t, e) - b) for m, b, e in schedule if m == lab), F(0))
            delta = w - cumulative(rates, cells, p, t)
            neg, pos = max(neg, delta), max(pos, -delta)
    return neg, pos


class Recursion:
    def __init__(self, tie=max):
        self.tie = tie  # which maximiser to pick among equal masses; any choice is allowed
        self.reductions = self.shortcuts = self.base = self.contracts = 0

    def build(self, rates, cells, labels, k, horizon):
        n = len(labels)
        assert 1 <= k < n
        C = coef(n, k)
        E = C * horizon
        masses = [cumulative(rates, cells, p, horizon) for p in range(n)]
        a = max(masses)
        q = self.tie(p for p in range(n) if masses[p] == a)
        if k == 1:
            self.base += 1
            schedule = [(labels[q], F(0), horizon)]
        elif a >= horizon - E:
            self.shortcuts += 1
            schedule = [(labels[q], F(0), horizon)]
        else:
            self.reductions += 1
            assert E >= horizon / n and coef(n - 1, k - 1) >= F(1, n - 1)
            L = horizon - a - E
            Ep = E - a / (n - 1)
            assert L > 0 and Ep > 0 and coef(n - 1, k - 1) * L <= Ep
            keep = [p for p in range(n) if p != q]
            child = [[r[p] + r[q] / (n - 1) for p in keep] for r in rates]
            assert all(min(r) >= 0 and sum(r) == 1 for r in child)
            ccells = [(s, min(e, L)) for s, e in cells if s < L]
            prefix = self.build(child[:len(ccells)], ccells, [labels[p] for p in keep], k - 1, L)
            schedule = prefix + [(labels[q], L, horizon)]
        neg, _ = discrepancies(rates, cells, labels, schedule, horizon)
        assert neg <= E, (n, k, neg, E)
        self.contracts += 1
        return schedule


def check_schedule(schedule, k, horizon):
    assert len(schedule) <= k
    assert len({m for m, _, _ in schedule}) == len(schedule)
    assert schedule[0][1] == 0 and schedule[-1][2] == horizon
    assert all(schedule[j][2] == schedule[j + 1][1] for j in range(len(schedule) - 1))


def make_inputs(rng):
    inputs = []
    for n in range(2, 14):
        for j in range(30):
            k = 1 + j % (n - 1)
            N = rng.randint(1, 6)
            kind = j % 3
            cols = []
            if kind == 2:  # equal terminal masses: cyclic shifts of one weight vector
                wts = [rng.randint(1, 9) for _ in range(n)]
                N = n
                cols = [[F(wts[(i - c) % n], sum(wts)) for i in range(n)] for c in range(n)]
                rng.shuffle(cols)
            for _ in range(N if kind != 2 else 0):
                wts = [rng.randint(0, 9) for _ in range(n)]
                if kind == 1:  # one dominant mode, to exercise the largest-mass shortcut
                    wts[0] += rng.randint(10, 60)
                wts[rng.randrange(n)] += 1
                cols.append([F(w, sum(wts)) for w in wts])
            inputs.append((n, k, cols))
    return inputs


def main():
    rng = Random(20260925)
    inputs = make_inputs(rng)
    rec = Recursion()
    qualified = 0
    final = []
    for n, k, cols in inputs:
        N = len(cols)
        cells = [(F(c, N), F(c + 1, N)) for c in range(N)]
        schedule = rec.build(cols, cells, list(range(n)), k, T)
        check_schedule(schedule, k, T)
        neg, pos = discrepancies(cols, cells, list(range(n)), schedule, T)
        C = coef(n, k)
        assert neg <= C * T
        if max(cumulative(cols, cells, p, T) for p in range(n)) <= C * T:
            assert pos <= C * T, (n, k, pos)
            qualified += 1
        final.append(schedule)
    assert rec.contracts == rec.reductions + rec.shortcuts + rec.base
    assert rec.shortcuts + rec.base == len(inputs)
    print(f"{len(inputs)} inputs (n=2..13, 30 each): {rec.contracts} recursive contracts "
          f"passed = {rec.reductions} reductions + {rec.shortcuts} non-base largest-mass "
          f"shortcuts + {rec.base} one-block base cases; {qualified} mass-qualified inputs "
          f"passed the two-sided check")
    print("review reports: 360 inputs, 928 reductions, 5 shortcuts, 355 base cases, "
          "241 two-sided")

    # Object under test: the committed author construction, re-verified here.
    from arbitrary_block_certificate import construct
    differ = same_rule = 0
    for (n, k, cols), mine in zip(inputs, final):
        rows = [list(r) for r in zip(*cols)]
        N = len(cols)
        blocks = construct(rows, k)
        check_schedule(blocks, k, T)
        cells = [(F(c, N), F(c + 1, N)) for c in range(N)]
        neg, pos = discrepancies(cols, cells, list(range(n)), blocks, T)
        assert neg <= coef(n, k) * T
        differ += blocks != mine
        first_rule = Recursion(tie=min).build(cols, cells, list(range(n)), k, T)
        same_rule += blocks == first_rule
    assert same_rule == len(inputs)
    print(f"committed arbitrary_block_certificate.construct: all {len(inputs)} schedules pass "
          f"this file's negative-error check; {differ} differ from this file's last-maximiser "
          f"schedules, and all {same_rule} equal this file's schedules under the author's "
          f"first-maximiser tie rule")


if __name__ == "__main__":
    main()
