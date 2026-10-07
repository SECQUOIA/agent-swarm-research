"""Exact check (sympy) that the period-two class-(a0) split used in c1_wall.py a0 is a split of WALL:
f_n = F_first + sum_{odd interior e} G + sum_{even e} H + F_last for even n, and that its factor minima add up to the
wall value for every even n >= 4 (symbolic in n and in u(-1), u(c), b, c)."""
import sympy as sp
b = sp.Rational(962, 1000)
uc = [0, sp.Rational(1022, 1000), sp.Rational(189, 1000), sp.Rational(1774, 1000), sp.Rational(1086, 1000)]
U = lambda t: sum(cf * t**i for i, cf in enumerate(uc))
for n in (4, 6, 8, 10):
    X = sp.symbols(f"x1:{n+1}")
    f = sum(U(xi) for xi in X) + b * sum(X[i] * X[i + 1] for i in range(n - 1))
    parts = U(X[0]) + b * X[1] * (X[0] + 1) + U(X[n - 1]) + b * X[n - 2] * (X[n - 1] + 1)
    for e in range(2, n - 1):           # bond (e, e+1), 1-based
        x, y = X[e - 1], X[e]
        parts += (b * (x + 1) * (y + 1) - b) if e % 2 == 1 else (U(x) + U(y) + b * x * y - b * (x + y))
    print(f"n={n}: f_n - (sum of split factors) = {sp.expand(f - parts)}")
N, u1, uC, B, C = sp.symbols("n u_m1 u_c b c")
lb = 2 * u1 - (N / 2 - 2) * B + (N / 2 - 1) * (u1 + uC + B - 2 * B * C)
wall = (N / 2 + 1) * u1 + (N / 2 - 1) * uC + B * (1 - (N - 2) * C)
print("sum of factor minima - wall value (symbolic in n) =", sp.simplify(lb - wall))
