import numpy as np
# volume of {(x,t2,t3): 1<=x<=2, x^2<=t2<=3x-2, max(x^3, t2^1.5)<=t3<=min(7x-6, 1+7/3 (t2-1))}
for N, M in ((2000, 2000), (4000, 4000)):
    x = 1 + (np.arange(N) + 0.5) / N
    lo2, hi2 = x * x, 3 * x - 2
    u = (np.arange(M) + 0.5) / M
    t2 = lo2[:, None] + u[None, :] * (hi2 - lo2)[:, None]
    a = np.maximum(x[:, None] ** 3, t2 ** 1.5); b = np.minimum((7 * x - 6)[:, None], 1 + 7 / 3 * (t2 - 1))
    vol = (np.clip(b - a, 0, None).mean(axis=1) * (hi2 - lo2)).mean()
    print(N, M, "linked volume %.5f" % vol)
# term-by-term volume in (x,t2,t3): exact 3/20
# volume of the pair relaxation projected to (t2,t3) only (curve-chord region), for reference
t2 = 1 + (np.arange(400000) + 0.5) / 400000 * 3
print("area between chord and curve t3=t2^1.5 on t2 in [1,4]: %.5f" % ((1 + 7 / 3 * (t2 - 1) - t2 ** 1.5).mean() * 3))
