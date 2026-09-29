"""Midpoint fallback (split at p if p is in [l+th w, u-th w], else at the midpoint): a deterministic
th-safe rule that ignores where p sits inside the clamp zone. Exact rationals; 1D kink chain.
Counterexample to reading Theorem A as covering every such rule (the theorem itself is about clips)."""
import math
import random
from fractions import Fraction as Fr

def S_mid(a, th, cap=500):
    l, u = Fr(0), Fr(1)
    for k in range(1, cap):
        w = u - l
        s = a if l + th * w <= a <= u - th * w else (l + u) / 2
        if s == a:
            return k
        l, u = (l, s) if a < s else (s, u)
    return None

rng = random.Random(5)
for th in (Fr(1, 5), Fr(1, 4), Fr(1, 3), Fr(2, 5)):
    worst, traps, n = 0, 0, 0
    for _ in range(3000):
        a = Fr(rng.randrange(1, 10 ** 12), 10 ** 12) * Fr(1, 10) ** rng.randrange(0, 10)
        d0 = min(a, 1 - a)
        S = S_mid(a, th)
        n += 1
        if S is None:
            traps += 1
            continue
        pred = (max(0, math.ceil(math.log2(float(th / d0)))) + 1) if d0 < th else 1
        worst = max(worst, S - pred)
    print(f"theta = {th}: {n} kinks, no split on a within 500 steps: {traps}; max S - (ceil(log2(theta/d0)) + 1) = {worst}")
# theta = 2/5 > 1/3: the midpoint child can put the kink into the other zone
print("theta = 2/5, a = 3/10:", S_mid(Fr(3, 10), Fr(2, 5)), "splits")
