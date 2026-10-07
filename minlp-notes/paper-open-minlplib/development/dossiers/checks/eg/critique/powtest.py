import numpy as np
from fractions import Fraction as Fr
rng = np.random.default_rng(7)
x = np.concatenate([rng.uniform(0, 3.2, 200000), rng.uniform(0, 40, 50000), 10.0 ** rng.uniform(-8, 1.5, 50000)])
for k in (3, 4):
    y = x ** k                      # numpy array power -> np.power ufunc (X86_V4 loop)
    yp = x * x * x if k == 3 else (x * x) * (x * x)
    worst = 0.0
    idx = rng.choice(len(x), 20000, replace=False)
    for i in idx:
        ex = Fr(float(x[i])) ** k
        if ex == 0: continue
        worst = max(worst, abs(float((Fr(float(y[i])) - ex) / ex)))
    print(f"x**{k}: differs from repeated products on {np.mean(y != yp)*100:.2f}% ; max rel. error vs exact (20k sample) {worst:.3e} = {worst/2**-53:.2f} u")
# is the stride-0 scalar exponent fast path in play? (exponent 3 is a Python int scalar)
print("np.power(x,3.0) == x**3:", bool(np.all(np.power(x, 3.0) == x ** 3)))
