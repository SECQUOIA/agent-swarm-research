"""Check of the counting in Proposition 5.8(b) as restated in the third revision:
p = ceil(m log 2/log rho), N = m (p + 1) + 2, beta_0 = log 2/log rho,
beta_1 = sqrt(log 2 log rho), C' = C rho exp(beta_1 sqrt 2).  Verifies, for many
rho and m, that
  (i)   rho^-p <= 2^-m,
  (ii)  p + 1 < beta_0 m + 2  and  N <= beta_0 m^2 + 2 m + 2,
  (iii) m >= sqrt((N - 2)/beta_0) - 1/beta_0,
  (iv)  2^-m <= rho exp(-beta_1 sqrt(N - 2)) <= rho exp(beta_1 sqrt 2) exp(-beta_1 sqrt N).
Also simulates dyadic bisection toward c with the note's kink-cell rule
(the cell containing c; the left one once c is a common endpoint) and checks
that after m steps there are m + 1 cells, the kink cell has width (b-a) 2^-m,
and every other cell lies in one closed piece [a, c] or [c, b].
Exact rationals are used for the bisection; floats for (i)-(iv).
"""
import math
from fractions import Fraction as Fr

out = open("logs/r1_prop58b_count.log", "w")


def log(m):
    print(m)
    out.write(m + "\n")


bad = 0
cases = 0
for rho in [1.01, 1.1, 1.5, 2.0, math.e, 4.0, 8.0, 100.0, 1e6]:
    b0 = math.log(2) / math.log(rho)
    b1 = math.sqrt(math.log(2) * math.log(rho))
    for m in range(0, 200):
        p = math.ceil(m * b0 - 1e-12)
        N = m * (p + 1) + 2
        ok = True
        ok &= rho ** (-p) <= 2.0 ** (-m) * (1 + 1e-12)
        ok &= p + 1 < b0 * m + 2 + 1e-12
        ok &= N <= b0 * m * m + 2 * m + 2 + 1e-9
        ok &= m >= math.sqrt((N - 2) / b0) - 1 / b0 - 1e-9
        lhs = -m * math.log(2)
        mid = math.log(rho) - b1 * math.sqrt(N - 2)
        rhs = math.log(rho) + b1 * math.sqrt(2) - b1 * math.sqrt(N)
        ok &= lhs <= mid + 1e-9 and mid <= rhs + 1e-9
        cases += 1
        if not ok:
            bad += 1
            log(f"  FAIL rho={rho} m={m} p={p} N={N}")
log(f"(i)-(iv): {cases} (rho, m) cases, {bad} failures")

# dyadic bisection with the kink-cell rule
bad = 0
tests = 0
for (a, b, c) in [(Fr(-1), Fr(1), Fr(3, 8)), (Fr(-1), Fr(1), Fr(0)), (Fr(0), Fr(1), Fr(1, 3)),
                  (Fr(-1), Fr(1), Fr(1, 2)), (Fr(-1), Fr(1), Fr(377930, 1000000))]:
    cells = [(a, b)]
    for m in range(1, 25):
        # kink cell: contains c in its interior, else the left one with right endpoint c
        k = [i for i, (x, y) in enumerate(cells) if x < c < y]
        if not k:
            k = [i for i, (x, y) in enumerate(cells) if y == c]
        i = k[0]
        x, y = cells[i]
        mid = (x + y) / 2
        cells[i:i + 1] = [(x, mid), (mid, y)]
        k = [j for j, (x, y) in enumerate(cells) if x < c < y] or [j for j, (x, y) in enumerate(cells) if y == c]
        kc = k[0]
        tests += 1
        ok = len(cells) == m + 1 and (cells[kc][1] - cells[kc][0]) == (b - a) / 2 ** m
        for j, (x, y) in enumerate(cells):
            if j != kc and not (y <= c or x >= c):
                ok = False
        if not ok:
            bad += 1
            log(f"  FAIL bisection a={a} b={b} c={c} m={m}")
log(f"kink-cell bisection: {tests} (c, m) cases, {bad} failures")
