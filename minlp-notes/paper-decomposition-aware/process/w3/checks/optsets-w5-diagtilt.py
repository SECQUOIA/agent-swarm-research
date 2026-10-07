"""Exact check of Example ex:diagtilt (Appendix F, W5 optsets).

F = (x - y + t/2)^2 + t(1-t)/8 on [0,1]^3.
Checks: Hessian, indefiniteness via w=(0,1,2), F >= 0 on a grid with zero set
equal to the two segments, KKT signs and multiplier at the minimizers, and
H + Lambda = 2 a a^T.
"""
from fractions import Fraction as Fr
import itertools

a = [Fr(1), Fr(-1), Fr(1, 2)]
def F(x, y, t):
    return (x - y + t / 2) ** 2 + t * (1 - t) / 8
H = [[2 * a[i] * a[j] for j in range(3)] for i in range(3)]
H[2][2] -= Fr(1, 4)
assert [H[i][i] for i in range(3)] == [2, 2, Fr(1, 4)]
w = [0, 1, 2]
assert sum(a[i] * w[i] for i in range(3)) == 0
assert sum(w[i] * H[i][j] * w[j] for i in range(3) for j in range(3)) == -1

def grad(x, y, t):
    r = x - y + t / 2
    return [2 * r, -2 * r, r + (1 - 2 * t) / 8]

N = 16
zeros = set()
for i, j, k in itertools.product(range(N + 1), repeat=3):
    x, y, t = Fr(i, N), Fr(j, N), Fr(k, N)
    v = F(x, y, t)
    assert v >= 0
    if v == 0:
        zeros.add((x, y, t))
seg = {(Fr(i, N), Fr(i, N), Fr(0)) for i in range(N + 1)} | \
      {(Fr(i, N), Fr(i, N) + Fr(1, 2), Fr(1)) for i in range(N // 2 + 1)}
assert zeros == seg, (zeros ^ seg)
for (x, y, t) in seg:
    g = grad(x, y, t)
    assert g[0] == 0 and g[1] == 0
    assert (t == 0 and g[2] == Fr(1, 8)) or (t == 1 and g[2] == Fr(-1, 8))
    lam = [2 * abs(gi) for gi in g]  # widths are 1
    assert lam == [0, 0, Fr(1, 4)]
    HL = [[H[i][j] + (lam[i] if i == j else 0) for j in range(3)] for i in range(3)]
    assert HL == [[2 * a[i] * a[j] for j in range(3)] for i in range(3)]
print('ex:diagtilt verified: zero set = two segments on a 1/16 grid;',
      'H indefinite; Lambda = diag(0,0,1/4); H+Lambda = 2aa^T')
